/**
 * Tabiji — Export to Google Docs
 * 
 * Deployed as a web app at script.google.com.
 * POST { slug, email } → creates a formatted Google Doc, shares as editor.
 */

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var slug = (data.slug || '').replace(/[^a-z0-9\-]/gi, '');
    var email = data.email || '';
    
    if (!slug || !email) {
      return jsonResponse({ error: 'Missing slug or email' }, 400);
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return jsonResponse({ error: 'Invalid email address' }, 400);
    }
    
    // Fetch itinerary HTML
    var url = 'https://tabiji.ai/i/' + slug + '/';
    var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    if (response.getResponseCode() !== 200) {
      return jsonResponse({ error: 'Itinerary not found' }, 404);
    }
    
    var html = response.getContentText();
    var itinerary = parseItinerary(html, url);
    
    // Create & format the Google Doc
    var doc = DocumentApp.create(itinerary.title + ' — tabiji.ai');
    formatDocument(doc.getBody(), itinerary);
    doc.saveAndClose();
    
    // Share with user as editor
    var file = DriveApp.getFileById(doc.getId());
    file.addEditor(email);
    
    // Organize into folder
    var folders = DriveApp.getFoldersByName('Tabiji Exports');
    var folder = folders.hasNext() ? folders.next() : DriveApp.createFolder('Tabiji Exports');
    file.moveTo(folder);
    
    return jsonResponse({
      docUrl: 'https://docs.google.com/document/d/' + doc.getId() + '/edit',
      title: itinerary.title,
      email: email
    });
    
  } catch (err) {
    Logger.log('Error: ' + err.message + '\n' + err.stack);
    return jsonResponse({ error: 'Something went wrong. Please try again.' }, 500);
  }
}

function doGet(e) {
  return jsonResponse({ status: 'ok', service: 'tabiji-export-doc' });
}

function jsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─── Parser ───

function parseItinerary(html, sourceUrl) {
  var result = {
    title: '',
    subtitle: '',
    intro: '',
    sourceUrl: sourceUrl || '',
    quickRef: [],
    days: [],
    tips: []
  };
  
  // Title from <h1> (preferred, shorter) or <title> (fallback, truncated)
  var h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1) {
    // h1 often has "Title: <em>Subtitle</em>" — extract just the main part
    var h1Text = strip(h1[1]);
    result.title = h1Text.split(':')[0].trim() || h1Text;
    if (h1Text.indexOf(':') > -1) result.subtitle = h1Text.split(':').slice(1).join(':').trim();
  } else {
    var titleTag = html.match(/<title>([\s\S]*?)(?:\s*[—|])/i);
    result.title = titleTag ? strip(titleTag[1]).split(':')[0].trim() : 'Itinerary';
  }
  
  // Subtitle / hero tagline
  var sub = html.match(/class="hero-sub"[^>]*>([\s\S]*?)<\/p>/i);
  if (sub) result.subtitle = strip(sub[1]);
  
  // Intro from meta description
  var meta = html.match(/<meta\s+name="description"\s+content="([^"]+)"/i);
  if (meta) result.intro = meta[1];
  
  // Quick reference items (Before You Go)
  var qrSection = html.match(/class="[^"]*quick-ref[^"]*"[\s\S]*?<\/section>/i);
  if (qrSection) {
    var refItems = qrSection[0].match(/<div[^>]*class="[^"]*ref-item[^"]*"[^>]*>[\s\S]*?<\/div>\s*<\/div>/gi) || [];
    refItems.forEach(function(item) {
      var label = (item.match(/<strong>([\s\S]*?)<\/strong>/i) || ['',''])[1];
      var val = (item.match(/<span[^>]*>([\s\S]*?)<\/span>/i) || ['',''])[1];
      if (label) result.quickRef.push({ label: strip(label), value: strip(val) });
    });
  }
  
  // Split by day divs
  var dayParts = html.split(/<div\s+class="day"\s+id="day\d+"/i);
  
  for (var d = 1; d < dayParts.length; d++) {
    var block = dayParts[d];
    var day = { num: '', neighborhoods: '', title: '', image: '', intro: '', timeBlocks: [] };
    
    // Day number + neighborhoods
    day.num = strip((block.match(/class="day-num"[^>]*>([\s\S]*?)<\/span>/i) || ['',''])[1]);
    day.neighborhoods = strip((block.match(/class="day-neighborhoods"[^>]*>([\s\S]*?)<\/span>/i) || ['',''])[1]);
    
    // Day title from <h2>
    day.title = strip((block.match(/<h2[^>]*>([\s\S]*?)<\/h2>/i) || ['',''])[1]);
    
    // Day intro paragraph
    var dayIntro = block.match(/<p\s+style="color:var\(--text-muted\)[^"]*"[^>]*>([\s\S]*?)<\/p>/i);
    if (dayIntro) day.intro = strip(dayIntro[1]);
    
    // Time blocks within this day
    var timeBlocks = block.split(/class="time-block"/i);
    for (var t = 1; t < timeBlocks.length; t++) {
      var tb = timeBlocks[t];
      var timeBlock = { label: '', activities: [] };
      
      // Time label (Morning, Afternoon, Evening)
      timeBlock.label = strip((tb.match(/class="time-label"[^>]*>([\s\S]*?)<\/div>/i) || ['',''])[1]);
      
      // Activities (each <h3>)
      var h3Parts = tb.split(/<h3[^>]*>/i);
      for (var a = 1; a < h3Parts.length; a++) {
        var actBlock = h3Parts[a];
        var activity = { name: '', description: '', details: [], tips: [], meals: [], redditTips: [] };
        
        // Activity name
        activity.name = strip((actBlock.match(/^([\s\S]*?)<\/h3>/i) || ['',''])[1]);
        
        // Main description paragraph
        var descP = actBlock.match(/<p(?:\s[^>]*)?>([\s\S]*?)<\/p>/i);
        if (descP) activity.description = strip(descP[1]);
        
        // Spot details (📍, 🕐, 💰, 💡)
        var details = actBlock.match(/<div\s+class="spot-detail"[^>]*>([\s\S]*?)<\/div>/gi) || [];
        details.forEach(function(det) {
          var text = strip(det.match(/<div[^>]*>([\s\S]*?)<\/div>/i)[1]);
          if (text) activity.details.push(text);
        });
        
        // Insider tips (class="tip")
        var tipDivs = actBlock.match(/<div\s+class="tip"[^>]*>([\s\S]*?)<\/div>/gi) || [];
        tipDivs.forEach(function(tip) {
          var text = strip(tip.match(/<div[^>]*>([\s\S]*?)<\/div>/i)[1]);
          if (text) activity.tips.push(text);
        });
        
        // Meal cards
        var mealCards = actBlock.match(/<div\s+class="meal-card"[\s\S]*?<\/div>\s*<\/div>/gi) || [];
        mealCards.forEach(function(mc) {
          var meal = {
            type: strip((mc.match(/class="meal-type"[^>]*>([\s\S]*?)<\/div>/i) || ['',''])[1]),
            name: strip((mc.match(/class="meal-name"[^>]*>([\s\S]*?)<\/div>/i) || ['',''])[1]),
            desc: strip((mc.match(/class="meal-desc"[^>]*>([\s\S]*?)<\/div>/i) || ['',''])[1]),
            meta: strip((mc.match(/class="meal-meta"[^>]*>([\s\S]*?)<\/div>/i) || ['',''])[1])
          };
          if (meal.name) activity.meals.push(meal);
        });
        
        // Reddit tips
        var rTips = actBlock.match(/<div\s+class="reddit-tip"[\s\S]*?<\/div>/gi) || [];
        rTips.forEach(function(rt) {
          var text = strip(rt.match(/<div[^>]*>([\s\S]*?)<\/div>/i)[1]);
          if (text) activity.redditTips.push(text);
        });
        
        if (activity.name) timeBlock.activities.push(activity);
      }
      
      if (timeBlock.activities.length > 0) day.timeBlocks.push(timeBlock);
    }
    
    if (day.num || day.title) result.days.push(day);
  }
  
  return result;
}

// ─── Formatter ───

function formatDocument(body, itinerary) {
  body.clear();
  
  var C = {
    indigo: '#2D3A5C',
    terracotta: '#C4704B',
    earth: '#8B7355',
    text: '#2C2419',
    muted: '#6B5D4F',
    light: '#AAAAAA'
  };
  
  // ── Title ──
  var title = body.appendParagraph(itinerary.title);
  title.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  title.setForegroundColor(C.indigo);
  title.setSpacingAfter(2);
  
  // Subtitle
  if (itinerary.subtitle) {
    var sub = body.appendParagraph(itinerary.subtitle);
    sub.setForegroundColor(C.muted);
    sub.setItalic(true);
    sub.setFontSize(11);
    sub.setSpacingAfter(4);
  }
  
  // Source link
  if (itinerary.sourceUrl) {
    var srcP = body.appendParagraph('');
    srcP.appendText('🔗 ').setFontSize(9);
    srcP.appendText(itinerary.sourceUrl).setLinkUrl(itinerary.sourceUrl).setForegroundColor(C.terracotta).setFontSize(9);
    srcP.setSpacingAfter(6);
  }
  
  body.appendHorizontalRule();
  
  // Intro
  if (itinerary.intro) {
    var intro = body.appendParagraph(itinerary.intro);
    intro.setForegroundColor(C.muted);
    intro.setFontSize(10);
    intro.setSpacingAfter(12);
  }
  
  // ── Before You Go ──
  if (itinerary.quickRef.length > 0) {
    var qrH = body.appendParagraph('⚡ Before You Go');
    qrH.setHeading(DocumentApp.ParagraphHeading.HEADING2);
    qrH.setForegroundColor(C.indigo);
    
    itinerary.quickRef.forEach(function(ref) {
      var item = body.appendListItem(ref.label + ': ' + ref.value);
      item.setGlyphType(DocumentApp.GlyphType.BULLET);
      item.setForegroundColor(C.text);
      item.editAsText().setBold(0, ref.label.length, true);
    });
    body.appendParagraph('').setSpacingAfter(6);
  }
  
  // ── Days ──
  itinerary.days.forEach(function(day) {
    body.appendHorizontalRule();
    
    // Day header: "Day 1: Arrival & Cowboy Welcome"
    var dayTitle = day.num;
    if (day.title) dayTitle += ': ' + day.title;
    var dh = body.appendParagraph(dayTitle);
    dh.setHeading(DocumentApp.ParagraphHeading.HEADING2);
    dh.setForegroundColor(C.indigo);
    dh.setSpacingAfter(2);
    
    // Neighborhoods
    if (day.neighborhoods) {
      var nh = body.appendParagraph(day.neighborhoods);
      nh.setForegroundColor(C.muted);
      nh.setFontSize(9);
      nh.setItalic(true);
      nh.setSpacingAfter(4);
    }
    
    // Day intro
    if (day.intro) {
      var di = body.appendParagraph(day.intro);
      di.setForegroundColor(C.muted);
      di.setSpacingAfter(8);
    }
    
    // Time blocks
    day.timeBlocks.forEach(function(tb) {
      if (tb.label) {
        var tlP = body.appendParagraph('⏰ ' + tb.label);
        tlP.setBold(true);
        tlP.setForegroundColor(C.earth);
        tlP.setFontSize(10);
        tlP.setSpacingAfter(2);
      }
      
      tb.activities.forEach(function(act) {
        // Activity name
        var actH = body.appendParagraph('→ ' + act.name);
        actH.setHeading(DocumentApp.ParagraphHeading.HEADING3);
        actH.setForegroundColor(C.terracotta);
        
        // Description
        if (act.description) {
          var desc = body.appendParagraph(act.description);
          desc.setForegroundColor(C.text);
          desc.setSpacingAfter(4);
        }
        
        // Details (📍, 🕐, 💰)
        act.details.forEach(function(det) {
          var detP = body.appendParagraph('    ' + det);
          detP.setForegroundColor(C.muted);
          detP.setFontSize(9);
          detP.setSpacingAfter(1);
        });
        
        // Tips
        act.tips.forEach(function(tip) {
          var tipP = body.appendParagraph(tip);
          tipP.setForegroundColor(C.earth);
          tipP.setItalic(true);
          tipP.setFontSize(9);
          tipP.setSpacingAfter(2);
        });
        
        // Meals
        act.meals.forEach(function(meal) {
          var mealH = body.appendParagraph(meal.type + ' ' + meal.name);
          mealH.setBold(true);
          mealH.setForegroundColor(C.text);
          mealH.setFontSize(10);
          
          if (meal.desc) {
            var mealD = body.appendParagraph(meal.desc);
            mealD.setForegroundColor(C.text);
            mealD.setFontSize(9);
          }
          if (meal.meta) {
            var mealM = body.appendParagraph(meal.meta);
            mealM.setForegroundColor(C.muted);
            mealM.setFontSize(8);
            mealM.setSpacingAfter(4);
          }
        });
        
        // Reddit tips
        act.redditTips.forEach(function(rt) {
          var rtP = body.appendParagraph('💬 ' + rt);
          rtP.setForegroundColor(C.earth);
          rtP.setFontSize(9);
          rtP.setItalic(true);
          rtP.setSpacingAfter(4);
        });
        
        body.appendParagraph('').setSpacingAfter(4);
      });
    });
  });
  
  // ── Footer ──
  body.appendHorizontalRule();
  
  // Editable notes section
  var notesH = body.appendParagraph('✏️ Your Notes');
  notesH.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  notesH.setForegroundColor(C.indigo);
  
  var noteHints = [
    '🏨 Accommodation details & confirmation numbers',
    '✈️ Flight info & boarding passes',
    '📋 Packing list',
    '🍽️ Restaurant reservations',
    '📝 Personal notes & ideas'
  ];
  noteHints.forEach(function(hint) {
    var item = body.appendListItem(hint);
    item.setGlyphType(DocumentApp.GlyphType.BULLET);
    item.setForegroundColor(C.light);
    item.setItalic(true);
    item.setFontSize(9);
  });
  
  body.appendParagraph('').setSpacingAfter(16);
  
  // Attribution
  var footer = body.appendParagraph('');
  footer.appendText('Created with ').setForegroundColor(C.muted).setFontSize(8);
  footer.appendText('tabiji.ai').setLinkUrl('https://tabiji.ai').setForegroundColor(C.terracotta).setFontSize(8);
  footer.appendText(' — AI-powered travel planning').setForegroundColor(C.muted).setFontSize(8);
}

// ─── Helpers ───

function strip(html) {
  if (!html) return '';
  return html
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<cite>[\s\S]*?<\/cite>/gi, '')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Test from the script editor */
function testExport() {
  var result = doPost({
    postData: {
      contents: JSON.stringify({ slug: 'dice-earl', email: 'bernard.j.huang@gmail.com' })
    }
  });
  Logger.log(result.getContent());
}
