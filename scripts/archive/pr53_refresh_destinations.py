from __future__ import annotations
import json
from pathlib import Path

ROOT = Path('/Users/psyduck/.openclaw/workspace/tabiji')
SOURCE = ROOT / 'find' / 'destinations.json'
FALLBACK_PHOTO = 'https://img.tabiji.ai/owl-logo.png'

ADDITIONS = [
    {'name':'Bangkok','region':'Thailand','continent':'Asia','budget':'$','season':'Nov–Feb','vibes':['City','Nightlife','Cultural'],'travel':['budget','food'],'pitch':'Temple spires, night markets, rooftop bars, and street food that punches way above its price.'},
    {'name':'Phuket','region':'Thailand','continent':'Asia','budget':'$$','season':'Nov–Apr','vibes':['Beach','Relaxation','Nightlife'],'travel':['luxury','family'],'pitch':'Thailand\'s easiest beach escape: island hopping, resort stays, and nightlife without much friction.'},
    {'name':'Kuala Lumpur','region':'Malaysia','continent':'Asia','budget':'$','season':'Dec–Feb, Jun–Aug','vibes':['City','Cultural','Food'],'travel':['budget','solo'],'pitch':'A food-obsessed capital where hawker stalls, mosques, malls, and skyscrapers all share the same block.'},
    {'name':'Taipei','region':'Taiwan','continent':'Asia','budget':'$$','season':'Oct–Apr','vibes':['City','Food','Cultural'],'travel':['solo','food'],'pitch':'Night markets, hot springs, mountain trails, and one of Asia\'s most reliably great food scenes.'},
    {'name':'Guadalajara','region':'Mexico','continent':'North America','budget':'$','season':'Oct–Apr','vibes':['City','Cultural','Nightlife'],'travel':['budget','solo'],'pitch':'Mariachi, tequila country, and a big-city arts scene without Mexico City\'s scale or chaos.'},
    {'name':'Cancun','region':'Mexico','continent':'North America','budget':'$$$','season':'Dec–Apr','vibes':['Beach','Relaxation','Nightlife'],'travel':['luxury','family'],'pitch':'A resort-first Caribbean gateway with easy beaches, day trips, and fast connections to the Riviera Maya.'},
    {'name':'Lima','region':'Peru','continent':'South America','budget':'$','season':'Dec–Apr','vibes':['City','Food','Cultural'],'travel':['food','solo'],'pitch':'Clifftop neighborhoods, world-class restaurants, and a Pacific capital that overdelivers if you eat well.'},
    {'name':'Madrid','region':'Spain','continent':'Europe','budget':'$$','season':'Mar–May, Sep–Nov','vibes':['City','Cultural','Nightlife'],'travel':['solo','food'],'pitch':'Big museums, late dinners, leafy boulevards, and the kind of nightlife that treats 2 a.m. as a warm-up.'},
    {'name':'Florence','region':'Tuscany','continent':'Europe','budget':'$$$','season':'Apr–Jun, Sep–Oct','vibes':['Cultural','Romantic','City'],'travel':['photography','couples'],'pitch':'Renaissance overload in a compact package: art, aperitivo, and a skyline that still feels unreal.'},
    {'name':'Venice','region':'Veneto','continent':'Europe','budget':'$$$','season':'Apr–Jun, Sep–Oct','vibes':['Romantic','Cultural','City'],'travel':['couples','photography'],'pitch':'A city with no roads, just canals, palazzos, and the constant feeling you\'re walking through a fever dream.'},
    {'name':'Vienna','region':'Austria','continent':'Europe','budget':'$$$','season':'Apr–Jun, Sep–Dec','vibes':['Cultural','City','Family'],'travel':['solo','luxury'],'pitch':'Imperial architecture, serious coffeehouse culture, and classical-music energy without trying too hard.'},
    {'name':'Athens','region':'Greece','continent':'Europe','budget':'$$','season':'Apr–Jun, Sep–Oct','vibes':['Cultural','City','Nightlife'],'travel':['budget','solo'],'pitch':'Ancient ruins above a scrappy, creative capital that works as both a city break and island-hopping launchpad.'},
    {'name':'London','region':'England','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['City','Cultural','Family'],'travel':['solo','family'],'pitch':'Museums, markets, pub culture, and enough neighborhoods to feel like several cities stitched together.'},
    {'name':'Istanbul','region':'Turkey','continent':'Europe','budget':'$$','season':'Apr–May, Sep–Oct','vibes':['Cultural','City','Food'],'travel':['solo','food'],'pitch':'Mosques, ferries, bazaars, and a skyline that reminds you this city has been important for a very long time.'},
    {'name':'Cairo','region':'Egypt','continent':'Africa','budget':'$','season':'Oct–Apr','vibes':['Cultural','City','Adventure'],'travel':['budget','history'],'pitch':'Pyramids at the edge of a megacity, Nile sunsets, and enough history to make most capitals feel young.'},
    {'name':'Mykonos','region':'Greece','continent':'Europe','budget':'$$$','season':'Jun–Sep','vibes':['Beach','Nightlife','Luxury'],'travel':['luxury','couples'],'pitch':'Whitewashed lanes, beach clubs, and Cycladic glamour that\'s expensive but rarely subtle.'},
    {'name':'Mallorca','region':'Spain','continent':'Europe','budget':'$$','season':'May–Oct','vibes':['Beach','Relaxation','Family'],'travel':['family','road-trip'],'pitch':'Coves, mountain villages, and enough range to do resort downtime or a much prettier road trip.'},
    {'name':'Ibiza','region':'Spain','continent':'Europe','budget':'$$$','season':'May–Oct','vibes':['Beach','Nightlife','Relaxation'],'travel':['luxury','friends'],'pitch':'Yes, the clubs are famous, but the island also does quiet coves, boutique stays, and slow afternoons well.'},
    {'name':'Canary Islands','region':'Spain','continent':'Europe','budget':'$$','season':'Year-round','vibes':['Beach','Nature','Adventure'],'travel':['family','road-trip'],'pitch':'Europe\'s all-season island cheat code: volcanic landscapes, surf towns, and winter sun without long-haul pain.'},
    {'name':'Interlaken','region':'Switzerland','continent':'Europe','budget':'$$$','season':'Jun–Sep, Dec–Mar','vibes':['Nature','Adventure','Hiking'],'travel':['adventure','photography'],'pitch':'A polished base for lakes, peaks, and adrenaline activities in the part of Switzerland people picture first.'},
    {'name':'Lucerne','region':'Switzerland','continent':'Europe','budget':'$$$','season':'May–Sep, Dec','vibes':['Nature','Romantic','City'],'travel':['couples','photography'],'pitch':'A postcard lake city with easy mountain access and zero interest in pretending it\'s not beautiful.'},
    {'name':'Milan','region':'Lombardy','continent':'Europe','budget':'$$$','season':'Apr–Jun, Sep–Oct','vibes':['City','Luxury','Cultural'],'travel':['luxury','shopping'],'pitch':'Fashion, aperitivo, and a sharper urban edge than the rest of Italy\'s big-name cities.'},
    {'name':'Naples','region':'Campania','continent':'Europe','budget':'$$','season':'Apr–Jun, Sep–Oct','vibes':['City','Food','Cultural'],'travel':['food','budget'],'pitch':'Chaotic, soulful, and probably serving better pizza than wherever you\'re standing right now.'},
    {'name':'Sicily','region':'Italy','continent':'Europe','budget':'$$','season':'Apr–Jun, Sep–Oct','vibes':['Beach','Food','Cultural'],'travel':['road-trip','food'],'pitch':'Ancient ruins, volcanoes, beach towns, and a food culture with no need to impress mainland Italy.'},
    {'name':'Sardinia','region':'Italy','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['Beach','Relaxation','Nature'],'travel':['luxury','family'],'pitch':'Electric-blue water, rugged inland landscapes, and beaches that make the rest of the Mediterranean work harder.'},
    {'name':'Porto','region':'Portugal','continent':'Europe','budget':'$$','season':'May–Oct','vibes':['City','Romantic','Food'],'travel':['couples','food'],'pitch':'Steep lanes, tiled facades, river views, and just enough grit to keep the prettiness from feeling fake.'},
    {'name':'Algarve','region':'Portugal','continent':'Europe','budget':'$$','season':'May–Oct','vibes':['Beach','Relaxation','Family'],'travel':['family','road-trip'],'pitch':'Cliff-backed beaches, resort towns, and reliable sun when the rest of Europe is still negotiating spring.'},
    {'name':'Valencia','region':'Spain','continent':'Europe','budget':'$$','season':'Mar–Jun, Sep–Oct','vibes':['City','Beach','Food'],'travel':['budget','food'],'pitch':'A beach city with great markets, lighter crowds than Barcelona, and a convincing case for staying longer.'},
    {'name':'Seville','region':'Andalusia','continent':'Europe','budget':'$$','season':'Mar–May, Oct–Nov','vibes':['Cultural','Romantic','City'],'travel':['couples','solo'],'pitch':'Orange trees, flamenco, tiled courtyards, and enough heat to force your schedule into proper Spanish hours.'},
    {'name':'Nice','region':'France','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['Beach','City','Relaxation'],'travel':['couples','luxury'],'pitch':'A walkable Riviera base with sea views, old-town charm, and easy access to flashier neighbors.'},
    {'name':'French Riviera','region':'France','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['Beach','Luxury','Romantic'],'travel':['luxury','road-trip'],'pitch':'Sunlit coast, glamorous towns, and the exact version of Mediterranean excess the brochures promised.'},
    {'name':'Edinburgh','region':'Scotland','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['Cultural','City','Romantic'],'travel':['solo','history'],'pitch':'Castle-on-a-hill drama, stone alleys, and enough atmosphere to make rainy weather feel on-brand.'},
    {'name':'Reykjavik','region':'Iceland','continent':'Europe','budget':'$$$','season':'Jun–Aug, Nov–Mar','vibes':['City','Adventure','Nature'],'travel':['photography','road-trip'],'pitch':'A compact capital that mostly functions as a launchpad for waterfalls, geothermal pools, and alien landscapes.'},
    {'name':'Corfu','region':'Greece','continent':'Europe','budget':'$$','season':'May–Sep','vibes':['Beach','Relaxation','Family'],'travel':['family','couples'],'pitch':'Green hills, calm coves, and a softer, easier Greek island vibe than the headline-grabbers.'},
    {'name':'Madeira','region':'Portugal','continent':'Europe','budget':'$$','season':'Year-round','vibes':['Nature','Hiking','Relaxation'],'travel':['adventure','road-trip'],'pitch':'A volcanic Atlantic island built for scenic drives, levada walks, and dramatic coastal views.'},
    {'name':'Hanoi','region':'Vietnam','continent':'Asia','budget':'$','season':'Oct–Apr','vibes':['Cultural','City','Food'],'travel':['budget','food'],'pitch':'Scooters, egg coffee, lakeside walks, and a historic core that somehow works despite the constant motion.'},
    {'name':'Ho Chi Minh','region':'Vietnam','continent':'Asia','budget':'$','season':'Dec–Apr','vibes':['City','Food','Nightlife'],'travel':['budget','solo'],'pitch':'Fast, loud, entrepreneurial, and excellent for food if you don\'t mind crossing the street as a faith exercise.'},
    {'name':'Da Nang','region':'Vietnam','continent':'Asia','budget':'$','season':'Feb–May','vibes':['Beach','City','Relaxation'],'travel':['budget','family'],'pitch':'An easy beach city with modern hotels, good seafood, and quick access to Hoi An and the Hai Van Pass.'},
    {'name':'Sapa','region':'Vietnam','continent':'Asia','budget':'$','season':'Mar–May, Sep–Nov','vibes':['Nature','Hiking','Unfrequented'],'travel':['adventure','photography'],'pitch':'Terraced rice fields, mountain villages, and misty views that look edited even when they\'re not.'},
    {'name':'Ninh Bình','region':'Vietnam','continent':'Asia','budget':'$','season':'Nov–Apr','vibes':['Nature','Relaxation','Cultural'],'travel':['budget','photography'],'pitch':'Limestone karsts, riverboat caves, and the kind of inland scenery people mistake for Ha Long Bay.'},
    {'name':'Krabi','region':'Thailand','continent':'Asia','budget':'$$','season':'Nov–Apr','vibes':['Beach','Adventure','Relaxation'],'travel':['couples','family'],'pitch':'Limestone cliffs, island-hopping boats, and just enough infrastructure to keep paradise fairly convenient.'},
    {'name':'Koh Samui','region':'Thailand','continent':'Asia','budget':'$$','season':'Dec–Aug','vibes':['Beach','Relaxation','Luxury'],'travel':['luxury','couples'],'pitch':'Palm-lined beaches, polished resorts, and a softer, more self-contained island holiday than Phuket.'},
    {'name':'Jakarta','region':'Indonesia','continent':'Asia','budget':'$','season':'Jun–Sep','vibes':['City','Food','Nightlife'],'travel':['budget','business'],'pitch':'A huge, hectic capital that makes more sense if you treat it as an eating city rather than a sightseeing city.'},
    {'name':'Yogyakarta','region':'Indonesia','continent':'Asia','budget':'$','season':'May–Sep','vibes':['Cultural','City','Food'],'travel':['budget','solo'],'pitch':'Java\'s cultural heart: batik, street art, and easy access to Borobudur and Prambanan.'},
    {'name':'Lombok','region':'Indonesia','continent':'Asia','budget':'$$','season':'May–Sep','vibes':['Beach','Nature','Adventure'],'travel':['adventure','couples'],'pitch':'A quieter Bali alternative with surf breaks, waterfalls, and easier access to the Gilis.'},
    {'name':'Komodo','region':'Indonesia','continent':'Asia','budget':'$$$','season':'Apr–Nov','vibes':['Adventure','Nature','Beach'],'travel':['adventure','liveaboard'],'pitch':'Pink beaches, sharp islands, and the rare place where “there are dragons” is not metaphorical.'},
    {'name':'Taiwan','region':'East Asia','continent':'Asia','budget':'$$','season':'Oct–Apr','vibes':['Food','Cultural','Nature'],'travel':['solo','food'],'pitch':'An easy, high-reward island country with great transit, mountain escapes, and absurdly strong food depth.'},
    {'name':'South Korea','region':'East Asia','continent':'Asia','budget':'$$','season':'Apr–May, Sep–Oct','vibes':['City','Cultural','Food'],'travel':['solo','shopping'],'pitch':'Fast trains, mountain temples, beauty retail, and city energy that scales from Seoul to Busan.'},
    {'name':'Japan','region':'East Asia','continent':'Asia','budget':'$$$','season':'Mar–May, Oct–Nov','vibes':['Cultural','Food','City'],'travel':['solo','photography'],'pitch':'The easiest hard sell in travel: extraordinary food, precise logistics, and endless range between cities and countryside.'},
    {'name':'Indonesia','region':'Southeast Asia','continent':'Asia','budget':'$$','season':'May–Sep','vibes':['Beach','Adventure','Nature'],'travel':['budget','island-hopping'],'pitch':'A huge archipelago where the real problem isn\'t finding somewhere good, it\'s narrowing the list down.'},
    {'name':'Cambodia','region':'Southeast Asia','continent':'Asia','budget':'$','season':'Nov–Mar','vibes':['Cultural','Budget','Unfrequented'],'travel':['budget','backpacking'],'pitch':'Anchored by Angkor but stronger than the stereotype, with river towns, islands, and room to slow down.'},
    {'name':'El Nido','region':'Philippines','continent':'Asia','budget':'$$','season':'Nov–May','vibes':['Beach','Adventure','Nature'],'travel':['couples','island-hopping'],'pitch':'Limestone cliffs, clear water, and the sort of island-hopping scenery that makes cameras feel inadequate.'},
    {'name':'Boracay','region':'Philippines','continent':'Asia','budget':'$$','season':'Nov–May','vibes':['Beach','Nightlife','Relaxation'],'travel':['friends','couples'],'pitch':'A small island built around one spectacular beach and a very intentional understanding of vacation mode.'},
    {'name':'Bohol','region':'Philippines','continent':'Asia','budget':'$$','season':'Nov–May','vibes':['Nature','Beach','Family'],'travel':['family','adventure'],'pitch':'Chocolate Hills, tarsiers, reef trips, and enough variety to work beyond just beach time.'},
    {'name':'Siem Reap','region':'Cambodia','continent':'Asia','budget':'$','season':'Nov–Feb','vibes':['Cultural','City','Food'],'travel':['budget','history'],'pitch':'Angkor\'s gateway has grown into a genuinely pleasant base for temples, cafes, and slow recovery days.'},
    {'name':'Puerto Vallarta','region':'Mexico','continent':'North America','budget':'$$','season':'Nov–Apr','vibes':['Beach','Nightlife','Relaxation'],'travel':['couples','family'],'pitch':'A friendly Pacific resort city with a proper old town, good food, and easy beach-and-jungle day trips.'},
    {'name':'Havana','region':'Cuba','continent':'North America','budget':'$','season':'Nov–Apr','vibes':['Cultural','City','Nightlife'],'travel':['history','photography'],'pitch':'Faded grandeur, classic cars, rum, and a city atmosphere strong enough to carry the rough edges.'},
    {'name':'Cusco','region':'Peru','continent':'South America','budget':'$','season':'May–Sep','vibes':['Cultural','City','Adventure'],'travel':['budget','history'],'pitch':'The old Inca capital is more than a stopover: altitude, stonework, and a very good excuse to linger.'},
    {'name':'Machu Picchu','region':'Peru','continent':'South America','budget':'$$$','season':'May–Sep','vibes':['Cultural','Nature','Adventure'],'travel':['history','hiking'],'pitch':'A bucket-list cliché for a reason: dramatic ruins, cloud forest setting, and a payoff that usually survives the hype.'},
    {'name':'Santiago','region':'Chile','continent':'South America','budget':'$$','season':'Sep–Nov, Mar–May','vibes':['City','Food','Adventure'],'travel':['solo','wine'],'pitch':'A modern Andean capital with wine country, ski day trips, and a better quality-of-life feel than it gets credit for.'},
    {'name':'Rio de Janeiro','region':'Brazil','continent':'South America','budget':'$$','season':'May–Oct','vibes':['Beach','City','Nightlife'],'travel':['friends','photography'],'pitch':'One of the few cities dramatic enough to justify its own reputation: mountains, beaches, and nonstop visual flexing.'},
    {'name':'New York City','region':'United States','continent':'North America','budget':'$$$','season':'Apr–Jun, Sep–Dec','vibes':['City','Cultural','Nightlife'],'travel':['solo','food'],'pitch':'The easiest city in the world to build a trip around if your tolerance for stimulation is reasonably high.'},
    {'name':'Miami','region':'United States','continent':'North America','budget':'$$$','season':'Nov–Apr','vibes':['Beach','Nightlife','City'],'travel':['luxury','friends'],'pitch':'Art Deco, Latin energy, flashy hotels, and a beach-city identity that doesn\'t apologize for itself.'},
    {'name':'Las Vegas','region':'United States','continent':'North America','budget':'$$','season':'Mar–May, Oct–Nov','vibes':['Nightlife','City','Luxury'],'travel':['friends','luxury'],'pitch':'A spectacle engine in the desert: casinos, restaurants, shows, and the freedom to behave a little less sensibly.'},
    {'name':'Yellowstone','region':'United States','continent':'North America','budget':'$$','season':'Jun–Sep','vibes':['Nature','Adventure','Family'],'travel':['road-trip','wildlife'],'pitch':'Geysers, bison, and a scale of geothermal weirdness that makes other national parks feel almost normal.'},
    {'name':'Yosemite','region':'United States','continent':'North America','budget':'$$','season':'May–Oct','vibes':['Nature','Hiking','Adventure'],'travel':['hiking','road-trip'],'pitch':'Granite walls, giant waterfalls, and the specific kind of American scenery that looks designed for awe.'},
    {'name':'Oahu','region':'Hawaii','continent':'North America','budget':'$$$','season':'Year-round','vibes':['Beach','City','Family'],'travel':['family','surf'],'pitch':'The easiest Hawaiian island for mixed-interest trips: Waikiki convenience, North Shore surf, and real range beyond both.'},
    {'name':'Banff','region':'Canada','continent':'North America','budget':'$$$','season':'Jun–Sep, Dec–Mar','vibes':['Nature','Adventure','Hiking'],'travel':['road-trip','photography'],'pitch':'Turquoise lakes, mountain lodges, and one of the cleanest easy-mode entries into the Canadian Rockies.'},
    {'name':'Amsterdam','region':'Netherlands','continent':'Europe','budget':'$$$','season':'Apr–Sep','vibes':['City','Cultural','Romantic'],'travel':['solo','couples'],'pitch':'Canals, bikes, brown cafes, and a city center that somehow stays lovely despite the crowds.'},
    {'name':'Bolivia','region':'South America','continent':'South America','budget':'$','season':'May–Oct','vibes':['Adventure','Nature','Unfrequented'],'travel':['budget','backpacking'],'pitch':'Salt flats, high-altitude cities, and wild landscapes that feel bigger than the tourism infrastructure around them.'},
    {'name':'Hawaii','region':'United States','continent':'North America','budget':'$$$','season':'Year-round','vibes':['Beach','Nature','Adventure'],'travel':['family','honeymoon'],'pitch':'Volcanoes, surf, rainforests, and some of the easiest high-payoff tropical travel in the US orbit.'},
    {'name':'Italy','region':'Southern Europe','continent':'Europe','budget':'$$$','season':'Apr–Jun, Sep–Oct','vibes':['Cultural','Food','Romantic'],'travel':['couples','food'],'pitch':'Art cities, dramatic coasts, serious regional food culture, and one of travel\'s deepest benches.'},
    {'name':'Montenegro','region':'Balkans','continent':'Europe','budget':'$$','season':'May–Sep','vibes':['Beach','Nature','Adventure'],'travel':['road-trip','budget'],'pitch':'Bay towns, mountain roads, and Adriatic scenery that still costs less and crowds less than Croatia.'},
    {'name':'Qatar','region':'Middle East','continent':'Asia','budget':'$$$','season':'Nov–Mar','vibes':['Luxury','City','Relaxation'],'travel':['luxury','stopover'],'pitch':'A polished Gulf stopover play with museums, desert excursions, and infrastructure built to feel frictionless.'},
    {'name':'Spain','region':'Southern Europe','continent':'Europe','budget':'$$','season':'Apr–Jun, Sep–Oct','vibes':['Food','Beach','Cultural'],'travel':['food','road-trip'],'pitch':'Tapas cities, island escapes, late-night energy, and enough regional variation to support repeat trips easily.'},
    {'name':'Brussels','region':'Belgium','continent':'Europe','budget':'$$$','season':'Apr–Oct','vibes':['City','Cultural','Food'],'travel':['solo','food'],'pitch':'Grand squares, serious beer culture, and a capital that works best if you treat it as deliciously eccentric rather than polished.'},
    {'name':'Antwerp','region':'Belgium','continent':'Europe','budget':'$$$','season':'Apr–Oct','vibes':['City','Fashion','Cultural'],'travel':['shopping','solo'],'pitch':'A compact Belgian city with fashion-world credibility, good food, and less tourist drag than Bruges or Brussels.'},
    {'name':'Ghent','region':'Belgium','continent':'Europe','budget':'$$','season':'Apr–Oct','vibes':['City','Cultural','Romantic'],'travel':['couples','solo'],'pitch':'Canals, medieval facades, and student-city energy that keeps the prettiness from turning inert.'},
    {'name':'Zurich','region':'Switzerland','continent':'Europe','budget':'$$$$','season':'May–Sep, Dec','vibes':['City','Nature','Luxury'],'travel':['luxury','business'],'pitch':'Lakefront polish, efficient everything, and a Swiss city break that doubles as a transit hub into the Alps.'},
    {'name':'Geneva','region':'Switzerland','continent':'Europe','budget':'$$$$','season':'May–Sep','vibes':['City','Luxury','Relaxation'],'travel':['luxury','business'],'pitch':'Diplomatic calm, lake views, and easy access to both the Alps and French wine country.'},
    {'name':'Zermatt','region':'Switzerland','continent':'Europe','budget':'$$$$','season':'Dec–Mar, Jul–Sep','vibes':['Nature','Adventure','Luxury'],'travel':['ski','honeymoon'],'pitch':'Car-free village, Matterhorn views, and mountain glamour with very little interest in being affordable.'},
    {'name':'Salzburg','region':'Austria','continent':'Europe','budget':'$$$','season':'May–Sep, Dec','vibes':['Cultural','Romantic','City'],'travel':['couples','history'],'pitch':'Baroque old town, hilltop fortress, and music-history density that feels almost unfair for a city this small.'},
    {'name':'Innsbruck','region':'Austria','continent':'Europe','budget':'$$$','season':'Dec–Mar, Jun–Sep','vibes':['Adventure','Nature','City'],'travel':['ski','adventure'],'pitch':'A real city dropped into alpine scenery, useful both for mountain sports and a very scenic urban base.'},
    {'name':'Bratislava','region':'Slovakia','continent':'Europe','budget':'$$','season':'Apr–Oct','vibes':['City','Cultural','Nightlife'],'travel':['budget','weekend'],'pitch':'Compact old town, Danube setting, and easy Central Europe access without the price tag of Vienna or Prague.'},
    {'name':'Split','region':'Croatia','continent':'Europe','budget':'$$','season':'May–Sep','vibes':['Beach','City','Nightlife'],'travel':['friends','island-hopping'],'pitch':'Roman ruins turned living city, ferry hub convenience, and a better balance of nightlife and history than Dubrovnik.'},
    {'name':'Kotor','region':'Montenegro','continent':'Europe','budget':'$$','season':'May–Sep','vibes':['Romantic','Nature','Cultural'],'travel':['couples','cruise'],'pitch':'A fortified bay town with fjord-like scenery and enough visual drama to feel larger than it is.'},
    {'name':'Mostar','region':'Bosnia and Herzegovina','continent':'Europe','budget':'$','season':'Apr–Jun, Sep–Oct','vibes':['Cultural','Romantic','Unfrequented'],'travel':['budget','history'],'pitch':'Bridge-city beauty, Ottoman layers, and one of the Balkans\' clearest high-impact short-stay destinations.'},
    {'name':'Tirana','region':'Albania','continent':'Europe','budget':'$','season':'Apr–Jun, Sep–Oct','vibes':['City','Nightlife','Unfrequented'],'travel':['budget','solo'],'pitch':'Colorful, scrappy, and much more fun than its reputation, with easy launchpad value for the Albanian coast and mountains.'},
    {'name':'Bucharest','region':'Romania','continent':'Europe','budget':'$','season':'Apr–Jun, Sep–Oct','vibes':['City','Nightlife','Cultural'],'travel':['budget','weekend'],'pitch':'Grand old facades, lively bars, and a city that makes more sense once you stop expecting tidy prettiness.'},
    {'name':'Warsaw','region':'Poland','continent':'Europe','budget':'$$','season':'May–Sep','vibes':['City','Cultural','Food'],'travel':['solo','history'],'pitch':'Rebuilt resilience, serious museums, and a modern capital that rewards people willing to look past first impressions.'},
    {'name':'Vilnius','region':'Lithuania','continent':'Europe','budget':'$$','season':'May–Sep','vibes':['City','Cultural','Romantic'],'travel':['budget','weekend'],'pitch':'Baroque old town, cafe culture, and the low-friction charm of a capital not yet crushed by overtourism.'},
    {'name':'Stockholm','region':'Sweden','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['City','Design','Nature'],'travel':['solo','design'],'pitch':'Waterfront light, clean-lined design, and the rare capital that still feels breathable.'},
    {'name':'Oslo','region':'Norway','continent':'Europe','budget':'$$$$','season':'May–Sep','vibes':['City','Nature','Relaxation'],'travel':['solo','outdoors'],'pitch':'A small but expensive capital where fjord access and quality-of-life energy do a lot of the work.'},
    {'name':'Alexandria','region':'Egypt','continent':'Africa','budget':'$','season':'Oct–Apr','vibes':['City','Cultural','Relaxation'],'travel':['history','budget'],'pitch':'Mediterranean light, old intellectual ghosts, and a calmer Egyptian city break than Cairo.'},
    {'name':'Johannesburg','region':'South Africa','continent':'Africa','budget':'$$','season':'May–Sep','vibes':['City','Cultural','Food'],'travel':['solo','history'],'pitch':'Creative, complicated, and worth more than a quick airport-night dismissal if you care about contemporary South Africa.'},
    {'name':'Mombasa','region':'Kenya','continent':'Africa','budget':'$$','season':'Jan–Mar, Jul–Oct','vibes':['Beach','Cultural','Relaxation'],'travel':['family','beach'],'pitch':'Swahili coast character, old-town texture, and a better beach-and-culture mix than many resort-only alternatives.'},
    {'name':'Agadir','region':'Morocco','continent':'Africa','budget':'$$','season':'Year-round','vibes':['Beach','Relaxation','Surf'],'travel':['surf','family'],'pitch':'A practical Atlantic beach base for winter sun, surfing, and easier logistics than Morocco\'s more atmospheric cities.'},
    {'name':'Goa','region':'India','continent':'Asia','budget':'$$','season':'Nov–Feb','vibes':['Beach','Nightlife','Relaxation'],'travel':['friends','beach'],'pitch':'India at its most holiday-coded: beach shacks, party pockets, Portuguese traces, and plenty of easy downtime.'},
    {'name':'Mumbai','region':'India','continent':'Asia','budget':'$$','season':'Nov–Feb','vibes':['City','Food','Nightlife'],'travel':['food','solo'],'pitch':'Dense, ambitious, and exhausting in the best and worst ways, with real cultural weight behind the chaos.'},
    {'name':'Delhi','region':'India','continent':'Asia','budget':'$','season':'Oct–Mar','vibes':['City','Cultural','Food'],'travel':['history','food'],'pitch':'Empire layers, street food intensity, and one of the world\'s clearest examples of a city that refuses simplification.'},
    {'name':'Udaipur','region':'India','continent':'Asia','budget':'$$','season':'Oct–Mar','vibes':['Romantic','Cultural','Relaxation'],'travel':['couples','luxury'],'pitch':'Lake palaces, rooftop dinners, and a very convincing case for Rajasthan as romantic rather than purely frenetic.'},
    {'name':'Varanasi','region':'India','continent':'Asia','budget':'$','season':'Oct–Mar','vibes':['Cultural','Spiritual','City'],'travel':['history','solo'],'pitch':'Intense, sacred, and unforgettable even when it is not comfortable, which is often.'},
    {'name':'Srinagar','region':'India','continent':'Asia','budget':'$$','season':'Apr–Oct','vibes':['Nature','Romantic','Relaxation'],'travel':['couples','photography'],'pitch':'Lake houseboats, mountain views, and a distinctly softer Kashmir aesthetic than much of the rest of India.'},
    {'name':'Manila','region':'Philippines','continent':'Asia','budget':'$','season':'Dec–Feb','vibes':['City','Food','Nightlife'],'travel':['budget','solo'],'pitch':'Messy, traffic-heavy, and worth understanding as a food and neighborhoods city rather than a postcard city.'},
    {'name':'Cebu','region':'Philippines','continent':'Asia','budget':'$','season':'Dec–May','vibes':['Beach','City','Adventure'],'travel':['budget','island-hopping'],'pitch':'A practical gateway with enough beaches, diving, and onward connections to earn real trip-planning value.'},
    {'name':'Coron','region':'Philippines','continent':'Asia','budget':'$$','season':'Nov–May','vibes':['Beach','Adventure','Nature'],'travel':['diving','couples'],'pitch':'Limestone lagoons, wreck dives, and clear-water island days that feel built for screensavers.'},
    {'name':'Jeju','region':'South Korea','continent':'Asia','budget':'$$','season':'Apr–Jun, Sep–Nov','vibes':['Nature','Relaxation','Family'],'travel':['family','road-trip'],'pitch':'South Korea\'s easiest domestic escape: volcanic landscapes, coastal drives, and a softer pace than the mainland.'},
    {'name':'Fukuoka','region':'Japan','continent':'Asia','budget':'$$','season':'Mar–May, Oct–Nov','vibes':['City','Food','Relaxation'],'travel':['food','solo'],'pitch':'A supremely livable Japanese city with great ramen, easier pacing, and excellent gateway value to Kyushu.'},
    {'name':'Hakone','region':'Japan','continent':'Asia','budget':'$$$','season':'Oct–Nov, Mar–May','vibes':['Nature','Relaxation','Romantic'],'travel':['onsen','couples'],'pitch':'Onsen ryokans, lake views, and Fuji cameos in a polished short-trip add-on from Tokyo.'},
    {'name':'Nikko','region':'Japan','continent':'Asia','budget':'$$','season':'Apr–May, Oct–Nov','vibes':['Cultural','Nature','Relaxation'],'travel':['history','day-trip'],'pitch':'Shrines in cedar forest, mountain scenery, and one of Japan\'s cleanest city-plus-nature side trips.'},
    {'name':'Kobe','region':'Japan','continent':'Asia','budget':'$$$','season':'Mar–May, Oct–Nov','vibes':['City','Food','Romantic'],'travel':['food','couples'],'pitch':'Harbor-city ease, good beef if you insist, and a smoother urban feel than Osaka\'s louder energy.'},
    {'name':'Shenzhen','region':'China','continent':'Asia','budget':'$$','season':'Oct–Dec','vibes':['City','Modern','Food'],'travel':['business','shopping'],'pitch':'Fast-built, tech-heavy, and more useful than poetic, but increasingly relevant as a southern China city break.'},
    {'name':'Lijiang','region':'China','continent':'Asia','budget':'$$','season':'Mar–May, Oct–Nov','vibes':['Cultural','Nature','Romantic'],'travel':['photography','couples'],'pitch':'Old-town lanes, mountain backdrops, and a Yunnan entry point that still delivers even with the tourism volume.'},
    {'name':'Zhangjiajie','region':'China','continent':'Asia','budget':'$$','season':'Apr–Oct','vibes':['Nature','Adventure','Photography'],'travel':['hiking','photography'],'pitch':'Pillar-like peaks, glass walkways, and scenery that convinced Hollywood to borrow heavily.'},
    {'name':'Xian','region':'China','continent':'Asia','budget':'$$','season':'Mar–May, Sep–Nov','vibes':['Cultural','City','Food'],'travel':['history','food'],'pitch':'Terracotta Warriors aside, Xian earns its place with Muslim Quarter food and deep dynastic weight.'},
    {'name':'Suzhou','region':'China','continent':'Asia','budget':'$$','season':'Mar–May, Sep–Nov','vibes':['Romantic','Cultural','City'],'travel':['couples','day-trip'],'pitch':'Classical gardens, canals, and a softer old-China image within easy reach of Shanghai.'},
    {'name':'Hangzhou','region':'China','continent':'Asia','budget':'$$','season':'Mar–May, Sep–Nov','vibes':['Nature','City','Relaxation'],'travel':['solo','tea'],'pitch':'West Lake calm, tea culture, and a city that sells poetic China more convincingly than most.'},
    {'name':'Tainan','region':'Taiwan','continent':'Asia','budget':'$','season':'Nov–Mar','vibes':['Food','Cultural','City'],'travel':['food','history'],'pitch':'Taiwan\'s old capital trades Taipei\'s pace for temples, alleyways, and elite snack-game confidence.'},
    {'name':'Kaohsiung','region':'Taiwan','continent':'Asia','budget':'$','season':'Nov–Mar','vibes':['City','Harbor','Relaxation'],'travel':['budget','solo'],'pitch':'A warmer, looser Taiwanese city with waterfront redevelopment and easier pacing than the capital.'},
    {'name':'Marrakesh','region':'Morocco','continent':'Africa','budget':'$$','season':'Mar–May, Oct–Nov','vibes':['Cultural','City','Romantic'],'travel':['couples','food'],'pitch':'Souks, riads, rooftops, and a version of Morocco that knows exactly how to stage an arrival.'},
    {'name':'Chefchaouen','region':'Morocco','continent':'Africa','budget':'$$','season':'Apr–Jun, Sep–Oct','vibes':['Romantic','Cultural','Unfrequented'],'travel':['photography','couples'],'pitch':'The blue city\'s visual gimmick is real, but the mountain setting and slower rhythm give it more staying power than that.'},
    {'name':'Abu Dhabi','region':'United Arab Emirates','continent':'Asia','budget':'$$$','season':'Nov–Mar','vibes':['Luxury','City','Relaxation'],'travel':['luxury','family'],'pitch':'Cleaner, calmer, and more museum-forward than Dubai, with enough polish to work well for upscale short stays.'},
    {'name':'Doha','region':'Qatar','continent':'Asia','budget':'$$$','season':'Nov–Mar','vibes':['Luxury','City','Stopover'],'travel':['luxury','stopover'],'pitch':'A compact Gulf capital built for smooth stopovers, museums, and desert add-ons without much travel friction.'},
    {'name':'Petra','region':'Jordan','continent':'Asia','budget':'$$$','season':'Mar–May, Sep–Nov','vibes':['Cultural','Adventure','Nature'],'travel':['history','hiking'],'pitch':'Rose-colored rock city, canyon approach, and one of the few world icons that still hits in person.'},
    {'name':'Muscat','region':'Oman','continent':'Asia','budget':'$$$','season':'Nov–Mar','vibes':['Relaxation','City','Cultural'],'travel':['road-trip','luxury'],'pitch':'Low-rise, sea-backed, and notably calmer than the flashier Gulf capitals, with Oman trip-building value baked in.'},
    {'name':'Serengeti','region':'Tanzania','continent':'Africa','budget':'$$$$','season':'Jun–Oct, Jan–Mar','vibes':['Nature','Adventure','Luxury'],'travel':['safari','honeymoon'],'pitch':'Big-cat density, migration scale, and the kind of safari shorthand that exists because the place actually delivers.'},
    {'name':'Austin','region':'Texas','continent':'North America','budget':'$$','season':'Mar–May, Oct–Nov','vibes':['City','Nightlife','Food'],'travel':['friends','music'],'pitch':'Live music, tacos, and the easiest US city break to sell if you want energy without full New York intensity.'},
    {'name':'Austria','region':'Central Europe','continent':'Europe','budget':'$$$','season':'May–Sep, Dec','vibes':['Cultural','Nature','Romantic'],'travel':['couples','road-trip'],'pitch':'Imperial cities, alpine scenery, and an unusually strong mix of culture and outdoors in a compact footprint.'},
    {'name':'Berlin','region':'Germany','continent':'Europe','budget':'$$','season':'May–Sep','vibes':['City','Nightlife','Cultural'],'travel':['solo','friends'],'pitch':'Big museums, bigger nightlife, and enough creative sprawl to reward repeat visits.'},
    {'name':'Canggu','region':'Bali','continent':'Asia','budget':'$$','season':'May–Sep','vibes':['Beach','Surf','Nightlife'],'travel':['friends','surf'],'pitch':'Coworking cafes, beach clubs, and a Bali base that optimizes for convenience, social life, and sunsets.'},
    {'name':'Copenhagen','region':'Denmark','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['City','Design','Food'],'travel':['solo','food'],'pitch':'Bike lanes, bakeries, and a polished city break that feels both relaxed and expensive because it is.'},
    {'name':'Dublin','region':'Ireland','continent':'Europe','budget':'$$$','season':'May–Sep','vibes':['City','Nightlife','Cultural'],'travel':['friends','solo'],'pitch':'Pubs, literary history, and an easygoing short-break city with strong music-and-storytelling energy.'},
    {'name':'Kyushu','region':'Japan','continent':'Asia','budget':'$$','season':'Mar–May, Oct–Nov','vibes':['Nature','Food','Relaxation'],'travel':['road-trip','onsen'],'pitch':'Hot springs, volcanic landscapes, and a softer, easier Japan circuit than the Tokyo–Kyoto default.'},
    {'name':'Mexico','region':'North America','continent':'North America','budget':'$$','season':'Nov–Apr','vibes':['Food','Beach','Cultural'],'travel':['food','road-trip'],'pitch':'A broad, repeatable travel giant: food cities, surf coasts, colonial towns, and major range across budgets and styles.'},
    {'name':'Munich','region':'Germany','continent':'Europe','budget':'$$$','season':'May–Sep, Dec','vibes':['City','Cultural','Family'],'travel':['family','beer'],'pitch':'Beer gardens, easy day trips, and a polished Bavarian city break that overdelivers for first-time Germany trips.'},
    {'name':'Nashville','region':'Tennessee','continent':'North America','budget':'$$','season':'Apr–May, Sep–Oct','vibes':['City','Nightlife','Music'],'travel':['friends','weekend'],'pitch':'Honky-tonks, hot chicken, and one of the easiest American weekend cities to understand instantly.'},
    {'name':'Okinawa','region':'Japan','continent':'Asia','budget':'$$','season':'Apr–Jun, Oct–Nov','vibes':['Beach','Relaxation','Family'],'travel':['family','beach'],'pitch':'Japan\'s subtropical escape: island beaches, lower-key pace, and a trip profile that feels very different from the mainland.'},
    {'name':'Switzerland','region':'Central Europe','continent':'Europe','budget':'$$$$','season':'Jun–Sep, Dec–Mar','vibes':['Nature','Adventure','Luxury'],'travel':['photography','rail'],'pitch':'Lakes, peaks, and scenic trains in a country built to make mountain travel feel frictionless if not cheap.'},
]


def unique_list(values):
    seen = set()
    out = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def infer_travel(row: dict):
    vibes = set(row.get('vibes') or [])
    budget = row.get('budget', '')
    inferred = []
    if 'Beach' in vibes:
        inferred.append('beach')
    if {'Adventure', 'Nature', 'Hiking'} & vibes:
        inferred.append('adventure')
    if 'Cultural' in vibes:
        inferred.append('history')
    if 'Romantic' in vibes:
        inferred.append('couples')
    if 'Nightlife' in vibes:
        inferred.append('friends')
    if 'Family' in vibes:
        inferred.append('family')
    if budget == '$':
        inferred.append('budget')
    if budget in ('$$$', '$$$$'):
        inferred.append('luxury')
    return unique_list(inferred)[:3] or ['solo']


def main():
    data = json.loads(SOURCE.read_text())
    by_name = {row.get('name'): row for row in data if isinstance(row, dict)}
    normalized = 0
    added = 0

    for row in data:
        if isinstance(row, dict) and not row.get('travel'):
            row['travel'] = infer_travel(row)
            normalized += 1

    for item in ADDITIONS:
        if item['name'] in by_name:
            row = by_name[item['name']]
            if not row.get('travel'):
                row['travel'] = item['travel']
            continue
        row = {
            'name': item['name'],
            'region': item['region'],
            'continent': item['continent'],
            'photo': FALLBACK_PHOTO,
            'pitch': item['pitch'],
            'budget': item['budget'],
            'season': item['season'],
            'vibes': item['vibes'],
            'travel': item['travel'],
        }
        data.append(row)
        by_name[item['name']] = row
        added += 1

    data.sort(key=lambda r: r.get('name', '').casefold())
    SOURCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(f'normalized={normalized} added={added} total={len(data)}')


if __name__ == '__main__':
    main()
