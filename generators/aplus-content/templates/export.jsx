/* ============================================================
   Set A — EXACT-SIZE EXPORT TILES (local art → captures cleanly)
   One asset at a time via location.hash: #logo #header #q0..#q3 #ma
   Magenta sentinel bg lets the cropper find exact asset bounds.
   Scales to fit the capture pane; final resize restores true px.
   ============================================================ */
const { IMG, C, THEMES } = window.TABIJI;
const t = THEMES.A;

function XImg({ src, alt, fit = 'cover', pos = 'center' }) {
  return <img src={src} alt={alt || ''} draggable={false}
    style={{ width: '100%', height: '100%', objectFit: fit, objectPosition: pos, display: 'block' }} />;
}

/* ① LOGO 600×180 */
function XLogo() {
  return (
    <div style={{ width: 600, height: 180, background: t.surface, border: `1px solid ${t.line}`, display: 'flex', alignItems: 'center', boxSizing: 'border-box' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 26, padding: '0 46px' }}>
        <div style={{ width: 96, height: 96, flex: '0 0 auto' }}><XImg src={IMG.owl} fit="contain" alt="tabiji owl" /></div>
        <div style={{ width: 1, height: 92, background: t.line }} />
        <div>
          <div style={{ fontFamily: t.serif, fontSize: 46, lineHeight: 1, color: t.ink, letterSpacing: '-.01em' }}>tabiji<span style={{ color: t.terra }}>.ai</span></div>
          <div style={{ width: 188, height: 2, background: t.terra, margin: '12px 0 9px' }} />
          <div style={{ fontFamily: t.sans, fontSize: 12, fontWeight: 600, letterSpacing: '.34em', color: t.sub }}>TRAVEL SAFETY SERIES</div>
        </div>
      </div>
    </div>
  );
}

/* ② HEADER 970×300 */
function XHeader() {
  const h = C.hero.authority;
  return (
    <div style={{ width: 970, height: 300, display: 'flex', background: t.surface, border: `1px solid ${t.line}`, boxSizing: 'border-box' }}>
      <div style={{ flex: 1, padding: '34px 38px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.18em', color: t.terra, marginBottom: 14 }}>{h.kicker}</div>
        <div style={{ fontFamily: t.serif, fontSize: 38, lineHeight: 1.06, color: t.ink, letterSpacing: '-.015em' }}>
          {h.head.map((l, i) => <div key={i}>{l}</div>)}
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 9, margin: '18px 0 9px' }}>
          <span style={{ fontFamily: t.serif, fontSize: 32, color: t.terra, lineHeight: 1 }}>{C.stat.scams}</span>
          <span style={{ fontSize: 13, color: t.sub }}>{C.stat.scamsLabel || 'documented scams'}</span>
          <span style={{ color: t.line }}>·</span>
          <span style={{ fontFamily: t.serif, fontSize: 32, color: t.terra, lineHeight: 1 }}>{C.stat.cities}</span>
          <span style={{ fontSize: 13, color: t.sub }}>{C.stat.unit || 'cities'}</span>
        </div>
        <div style={{ fontFamily: t.mono, fontSize: 9.5, letterSpacing: '.05em', color: t.onPageSub }}>{C.stat.sourcesLine}</div>
      </div>
      <div style={{ flex: '0 0 320px', position: 'relative', borderLeft: `1px solid ${t.line}`, background: t.wash, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ padding: 8, background: t.terraDeep, boxShadow: '0 6px 18px rgba(60,30,15,.18)' }}>
          <div style={{ width: 268, height: 268 }}><XImg src={IMG.beijing2} alt="hero scam comic" /></div>
        </div>
        <div style={{ position: 'absolute', left: 12, top: 12, width: 62, height: 62, borderRadius: '50%', border: `2px solid ${t.terra}`, color: t.terra, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: 'rotate(-9deg)', background: t.wash }}>
          <div style={{ position: 'absolute', inset: 4, borderRadius: '50%', border: `1px solid ${t.terra}`, opacity: .5 }} />
          <div style={{ fontFamily: t.mono, fontSize: 8, letterSpacing: '.06em', lineHeight: 1.3, textAlign: 'center', fontWeight: 600 }}>{C.brand.country}<br />·2026·<br />{C.brand.stamp3}</div>
        </div>
      </div>
    </div>
  );
}

/* ③/④ COMIC TILE 300×300 — full 2×2 comic in a terracotta mat */
function XTile({ src, alt }) {
  return (
    <div style={{ width: 300, height: 300, background: t.terraDeep, padding: 8, boxSizing: 'border-box' }}>
      <div style={{ width: 284, height: 284 }}><XImg src={src} alt={alt} pos="center" /></div>
    </div>
  );
}

/* ④ MULTIPLE IMAGE MODULE A — full designed image at EXACT 970×300 (matches header slot) */
function XInside() {
  const ins = C.inside;
  return (
    <div style={{ width: 970, height: 300, background: t.surface, border: `1px solid ${t.line}`, padding: '16px 26px', display: 'flex', gap: 24, boxSizing: 'border-box', fontFamily: t.sans, alignItems: 'center', overflow: 'hidden' }}>
      <div style={{ flex: '0 0 240px' }}>
        <div style={{ background: t.terraDeep, padding: 6 }}><div style={{ width: 228, height: 228 }}><XImg src={ins.img} alt="inside scam comic" /></div></div>
        <div style={{ fontFamily: t.mono, fontSize: 9, letterSpacing: '.05em', color: t.onPageSub, marginTop: 6 }}>{C.inside.caption}</div>
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.2em', color: t.terra, marginBottom: 7 }}>{`INSIDE THE BOOK — ${C.stat.scams} ENTRIES`}</div>
        <div style={{ fontFamily: t.serif, fontSize: 20, lineHeight: 1.12, color: t.ink, letterSpacing: '-.01em' }}>{ins.head}</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px 20px', marginTop: 11 }}>
          {ins.items.map(([title, sub], i) => (
            <div key={i} style={{ display: 'flex', gap: 8 }}>
              <span style={{ flex: '0 0 auto', marginTop: 1, width: 15, height: 15, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', background: t.terra, fontSize: 10, borderRadius: 3 }}>✓</span>
              <div>
                <div style={{ fontWeight: 600, fontSize: 11.5, color: t.ink, lineHeight: 1.15, whiteSpace: 'nowrap' }}>{title}</div>
                <div style={{ fontSize: 10, color: t.sub, marginTop: 1, lineHeight: 1.3 }}>{sub}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', gap: 7, marginTop: 11 }}>
          {ins.phrases.map((p, i) => (
            <div key={i} style={{ flex: 1, padding: '5px 9px', border: `1px solid ${t.line}`, background: t.surfaceAlt }}>
              <div style={{ fontFamily: t.serif, fontStyle: 'italic', fontSize: 11.5, color: t.ink }}>{p[0]}</div>
              <div style={{ fontSize: 13, color: t.terra, margin: '0 0 1px', letterSpacing: '.04em' }}>{p[1]}</div>
              <div style={{ fontFamily: t.mono, fontSize: 8, letterSpacing: '.05em', color: t.sub, textTransform: 'uppercase' }}>{p[2]}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ⑤ PRODUCT DESCRIPTION — full designed image at EXACT 970×300 (matches header slot) */
function XDesc() {
  const d = C.desc;
  return (
    <div style={{ width: 970, height: 300, background: t.surface, border: `1px solid ${t.line}`, padding: '20px 30px', boxSizing: 'border-box', fontFamily: t.sans, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 11 }}>
        <div style={{ width: 42, height: 42, flex: '0 0 auto' }}><XImg src={IMG.owl} fit="contain" alt="tabiji owl" /></div>
        <div style={{ fontFamily: t.serif, fontSize: 26, color: t.ink, lineHeight: 1, letterSpacing: '-.015em' }}>{d.headline || 'Read it on the flight over.'}</div>
        <div style={{ flex: 1 }} />
        <div style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.08em', color: t.terra, whiteSpace: 'nowrap' }}>{d.price}</div>
      </div>
      <div style={{ height: 1, background: t.line, marginBottom: 12 }} />
      <div style={{ columns: 2, columnGap: 34, fontSize: 11.5, lineHeight: 1.5, color: t.sub, flex: 1 }}>
        {d.body.map((p, i) => <p key={i} style={{ margin: '0 0 9px', breakInside: 'avoid', textWrap: 'pretty' }}>{p}</p>)}
      </div>
      <div style={{ display: 'flex', marginTop: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        {d.badges.map((b, i) => (
          <React.Fragment key={i}>
            {i > 0 && <span style={{ color: t.terra, margin: '0 12px' }}>◆</span>}
            <span style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.12em', color: t.ink, fontWeight: 600 }}>{b}</span>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

/* ===== FIELD-GUIDE layout (comic-less; medical books) ===== */
/* ② hero — title + hook + stat row, with a "safety pause" panel where the comic would be */
function XHeroFG() {
  const h = C.hero;
  return (
    <div style={{ width: 970, height: 300, display: 'flex', background: t.surface, border: `1px solid ${t.line}`, boxSizing: 'border-box' }}>
      <div style={{ flex: 1, padding: '28px 36px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.18em', color: t.terra, marginBottom: 13 }}>{h.eyebrow}</div>
        <div style={{ fontFamily: t.serif, fontSize: 39, lineHeight: 1.05, color: t.ink, letterSpacing: '-.015em' }}>
          {h.title.map((l, i) => <div key={i}>{l}</div>)}
        </div>
        <div style={{ fontFamily: t.sans, fontSize: 14, lineHeight: 1.4, color: t.sub, margin: '13px 0', maxWidth: 540 }}>{h.hook}</div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 9 }}>
          <span style={{ fontFamily: t.serif, fontSize: 30, color: t.terra, lineHeight: 1 }}>{h.statA}</span>
          <span style={{ fontSize: 12.5, color: t.sub }}>{h.statALabel}</span>
          <span style={{ color: t.line }}>·</span>
          <span style={{ fontFamily: t.serif, fontSize: 30, color: t.terra, lineHeight: 1 }}>{h.statB}</span>
          <span style={{ fontSize: 12.5, color: t.sub }}>{h.statBLabel}</span>
        </div>
      </div>
      <div style={{ flex: '0 0 312px', borderLeft: `1px solid ${t.line}`, background: t.wash, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24, boxSizing: 'border-box' }}>
        <div style={{ textAlign: 'center', border: `2px solid ${t.terra}`, borderRadius: 10, padding: '22px 18px', background: t.surface }}>
          <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.2em', color: t.sub }}>{h.pauseTitle}</div>
          <div style={{ fontFamily: t.serif, fontSize: 29, color: t.terra, lineHeight: 1.05, margin: '4px 0 8px' }}>{h.pauseSub}</div>
          <div style={{ width: 36, height: 2, background: t.terra, margin: '0 auto 10px' }} />
          <div style={{ fontFamily: t.sans, fontSize: 11.5, lineHeight: 1.4, color: t.sub, maxWidth: 200 }}>{h.pauseLine}</div>
        </div>
      </div>
    </div>
  );
}
/* ③ tile — a buyer-protection move (number + verb + line) on the deep accent */
function XTileFG({ m }) {
  return (
    <div style={{ width: 300, height: 300, background: t.terraDeep, boxSizing: 'border-box', padding: '26px 24px', display: 'flex', flexDirection: 'column', color: '#fff', fontFamily: t.sans }}>
      <div style={{ fontFamily: t.serif, fontSize: 46, lineHeight: 1, color: t.wash }}>{m.n}</div>
      <div style={{ fontFamily: t.mono, fontSize: 15, letterSpacing: '.18em', marginTop: 14 }}>{m.verb}</div>
      <div style={{ width: 30, height: 2, background: 'rgba(255,255,255,.45)', margin: '12px 0' }} />
      <div style={{ fontSize: 13.5, lineHeight: 1.5, color: 'rgba(255,255,255,.92)' }}>{m.line}</div>
    </div>
  );
}
/* ④ native (300²) — the framework card */
function XFrameworkCard() {
  const ins = C.inside;
  return (
    <div style={{ width: 300, height: 300, background: t.terraDeep, boxSizing: 'border-box', padding: '24px 22px', color: '#fff', fontFamily: t.sans }}>
      <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.2em', color: t.wash }}>{ins.frameworkTitle}</div>
      <div style={{ width: 30, height: 2, background: 'rgba(255,255,255,.45)', margin: '12px 0 14px' }} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
        {ins.framework.map((f, i) => (
          <div key={i} style={{ display: 'flex', gap: 9, alignItems: 'baseline' }}>
            <span style={{ fontFamily: t.serif, fontSize: 15, color: t.wash }}>{i + 1}</span>
            <span style={{ fontSize: 13, lineHeight: 1.25 }}>{f}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
/* ④ full (970×300) — framework panel + value items + green/yellow/red flag chips */
function XInsideFG() {
  const ins = C.inside;
  return (
    <div style={{ width: 970, height: 300, background: t.surface, border: `1px solid ${t.line}`, padding: '18px 26px', display: 'flex', gap: 24, boxSizing: 'border-box', fontFamily: t.sans, overflow: 'hidden' }}>
      <div style={{ flex: '0 0 230px', background: t.terraDeep, color: '#fff', padding: '18px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ fontFamily: t.mono, fontSize: 10.5, letterSpacing: '.18em', color: t.wash }}>{ins.frameworkTitle}</div>
        <div style={{ width: 28, height: 2, background: 'rgba(255,255,255,.45)', margin: '10px 0 12px' }} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {ins.framework.map((f, i) => (
            <div key={i} style={{ display: 'flex', gap: 8, alignItems: 'baseline' }}>
              <span style={{ fontFamily: t.serif, fontSize: 14, color: t.wash }}>{i + 1}</span>
              <span style={{ fontSize: 12, lineHeight: 1.25 }}>{f}</span>
            </div>
          ))}
        </div>
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.2em', color: t.terra, marginBottom: 7 }}>INSIDE THE FIELD GUIDE</div>
        <div style={{ fontFamily: t.serif, fontSize: 20, lineHeight: 1.12, color: t.ink, letterSpacing: '-.01em' }}>{ins.head}</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px 20px', marginTop: 10 }}>
          {ins.items.map(([title, sub], i) => (
            <div key={i} style={{ display: 'flex', gap: 8 }}>
              <span style={{ flex: '0 0 auto', marginTop: 1, width: 15, height: 15, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', background: t.terra, fontSize: 10, borderRadius: 3 }}>✓</span>
              <div>
                <div style={{ fontWeight: 600, fontSize: 11.5, color: t.ink, lineHeight: 1.15, whiteSpace: 'nowrap' }}>{title}</div>
                <div style={{ fontSize: 10, color: t.sub, marginTop: 1, lineHeight: 1.3 }}>{sub}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', gap: 7, marginTop: 11 }}>
          {ins.flags.map((fl, i) => {
            const col = ['#3F7D4E', '#C8902A', '#B23A2E'][i];
            return (
              <div key={i} style={{ flex: 1, padding: '6px 9px', border: `1px solid ${t.line}`, background: t.surfaceAlt, display: 'flex', alignItems: 'center', gap: 7 }}>
                <span style={{ flex: '0 0 auto', width: 9, height: 9, borderRadius: '50%', background: col }} />
                <div>
                  <div style={{ fontFamily: t.mono, fontSize: 9, letterSpacing: '.08em', color: col, fontWeight: 700 }}>{fl[0]}</div>
                  <div style={{ fontSize: 10.5, color: t.sub, lineHeight: 1.2 }}>{fl[1]}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

const FG = C.layout === 'field-guide';
const ASSETS = {
  logo:   { w: 600, h: 180, el: <XLogo /> },
  header: { w: 970, h: 300, el: FG ? <XHeroFG /> : <XHeader /> },
  q0:     { w: 300, h: 300, el: FG ? <XTileFG m={C.moves[0]} /> : <XTile src={C.quad[0].img} alt={C.quad[0].title} /> },
  q1:     { w: 300, h: 300, el: FG ? <XTileFG m={C.moves[1]} /> : <XTile src={C.quad[1].img} alt={C.quad[1].title} /> },
  q2:     { w: 300, h: 300, el: FG ? <XTileFG m={C.moves[2]} /> : <XTile src={C.quad[2].img} alt={C.quad[2].title} /> },
  q3:     { w: 300, h: 300, el: FG ? <XTileFG m={C.moves[3]} /> : <XTile src={C.quad[3].img} alt={C.quad[3].title} /> },
  ma:     { w: 300, h: 300, el: FG ? <XFrameworkCard /> : <XTile src={IMG.shanghai1} alt="inside scam comic" /> },
  inside: { w: 970, h: 300, el: FG ? <XInsideFG /> : <XInside /> },
  desc:   { w: 970, h: 300, el: <XDesc /> },
};

function ExportApp() {
  const q = new URLSearchParams(location.search);
  const key = window.__EXPORT_KEY || q.get('key') || (location.hash || '#logo').slice(1);
  const a = ASSETS[key] || ASSETS.logo;
  const scaleParam = q.get('scale');
  const S = scaleParam ? +scaleParam : Math.min(1, 820 / a.w);  // 820/pane fit; Playwright passes scale=1
  window.__asset = { w: a.w, h: a.h, key, S };
  React.useEffect(() => {
    window.__ready = false; document.title = 'loading';
    let stop = false;
    const iv = setInterval(async () => {
      const imgs = [...document.querySelectorAll('img')];
      if (imgs.every((i) => i.complete && i.naturalWidth > 0)) {  // [].every() === true → zero-image (field-guide) modules pass after fonts
        clearInterval(iv);
        try { await document.fonts.ready; } catch (e) {}
        if (!stop) setTimeout(() => { document.title = 'READY'; window.__ready = true; }, 400);
      }
    }, 100);
    return () => { stop = true; clearInterval(iv); };
  }, [key]);
  return (
    <div id="asset" style={{ position: 'absolute', top: 0, left: 0, transform: `scale(${S})`, transformOrigin: 'top left' }}>
      {a.el}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<ExportApp />);
