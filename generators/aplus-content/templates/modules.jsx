/* ============================================================
   tabiji.ai — China A+ Content · MODULES
   5 Amazon A+ modules, theme-aware, at true pixel specs.
   Directions branch on t.key: A Field Guide · B Comic Strip · C Dossier
   ============================================================ */
const { IMG, C, THEMES } = window.TABIJI;

/* ---------- shared atoms ---------- */
// Robust image: retries the same URL a couple times (cache-bust) before a
// last-resort fallback, then a quiet placeholder. referrerPolicy=no-referrer
// keeps hotlink rules happy; a warm tone sits behind during decode.
function Img({ src, fallback, alt, style, fit = 'cover', pos, label }) {
  const [cur, setCur] = React.useState(src);
  const tries = React.useRef(0);
  const [dead, setDead] = React.useState(false);
  React.useEffect(() => { setCur(src); tries.current = 0; setDead(false); }, [src]);
  const onErr = () => {
    tries.current += 1;
    if (tries.current <= 2) setCur(src + (src.includes('?') ? '&' : '?') + 'rt=' + tries.current);
    else if (fallback && cur.indexOf((fallback.split('?')[0])) < 0) setCur(fallback);
    else setDead(true);
  };
  if (dead) {
    return (
      <div style={{ background: '#e7d8c4', display: 'flex', alignItems: 'center', justifyContent: 'center', ...style }}>
        <span style={{ fontFamily: '"Spline Sans Mono", monospace', fontSize: 10, letterSpacing: '.08em', color: '#9a8a72' }}>{label || 'comic'}</span>
      </div>
    );
  }
  return (
    <div style={{ overflow: 'hidden', background: '#ece0cd', ...style }}>
      <img src={cur} alt={alt || ''} draggable={false} decoding="async"
        onError={onErr}
        style={{ width: '100%', height: '100%', objectFit: fit, objectPosition: pos || 'center', display: 'block' }} />
    </div>
  );
}
function Owl({ size = 70, src = IMG.owl }) {
  return <Img src={src} fallback={IMG.owlFly} alt="tabiji owl"
    fit="contain" style={{ width: size, height: size, flex: '0 0 auto' }} />;
}
function Meta({ t, idx, name, dim }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontFamily: t.mono, fontSize: 11,
      letterSpacing: '.14em', color: t.onPage, padding: '0 1px 10px' }}>
      <span style={{ color: t.terra, fontWeight: 600 }}>{idx}</span>
      <span style={{ textTransform: 'uppercase' }}>{name}</span>
      <span style={{ flex: 1, height: 1, background: t.dark ? t.lineOnPage : t.lineSoft }} />
      <span style={{ color: t.onPageSub }}>{dim}</span>
    </div>
  );
}
// terracotta wax/postmark stamp
function Stamp({ t, label, size = 78, rot = -8, color }) {
  const c = color || t.terra;
  return (
    <div style={{ width: size, height: size, borderRadius: '50%', border: `2px solid ${c}`, color: c,
      display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `rotate(${rot}deg)`,
      textAlign: 'center', position: 'relative', opacity: .9 }}>
      <div style={{ position: 'absolute', inset: 5, borderRadius: '50%', border: `1px solid ${c}`, opacity: .5 }} />
      <div style={{ fontFamily: t.mono, fontSize: 8.5, letterSpacing: '.08em', lineHeight: 1.25, padding: 4, fontWeight: 600 }}>{label}</div>
    </div>
  );
}
function dimTag(t, txt, onDark) {
  return (
    <span style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.1em',
      color: onDark ? 'rgba(255,255,255,.5)' : t.onPageSub }}>{txt}</span>
  );
}
function Phrase({ t, p, dark }) {
  return (
    <div style={{ flex: 1, padding: '8px 11px', border: `1px solid ${dark ? 'rgba(255,255,255,.18)' : t.line}`,
      background: dark ? 'rgba(255,255,255,.05)' : t.surfaceAlt }}>
      <div style={{ fontFamily: t.serif, fontStyle: 'italic', fontSize: 14, color: dark ? '#F2ECDF' : t.ink }}>{p[0]}</div>
      <div style={{ fontSize: 15, color: t.terra, margin: '1px 0 2px', letterSpacing: '.04em' }}>{p[1]}</div>
      <div style={{ fontFamily: t.mono, fontSize: 9.5, letterSpacing: '.06em', color: dark ? 'rgba(242,236,223,.6)' : t.sub, textTransform: 'uppercase' }}>{p[2]}</div>
    </div>
  );
}

/* ===========================================================
   ① COMPANY LOGO — 600 × 180
   =========================================================== */
function ModuleLogo({ t }) {
  let asset;
  if (t.key === 'A') {
    asset = (
      <div style={{ display: 'flex', alignItems: 'center', gap: 26, padding: '0 46px' }}>
        <Owl size={92} />
        <div style={{ width: 1, height: 92, background: t.line }} />
        <div>
          <div style={{ fontFamily: t.serif, fontSize: 46, lineHeight: 1, color: t.ink, letterSpacing: '-.01em' }}>
            tabiji<span style={{ color: t.terra }}>.ai</span>
          </div>
          <div style={{ width: 188, height: 2, background: t.terra, margin: '12px 0 9px' }} />
          <div style={{ fontFamily: t.sans, fontSize: 12, fontWeight: 600, letterSpacing: '.34em', color: t.sub }}>TRAVEL SAFETY SERIES</div>
        </div>
      </div>
    );
  } else if (t.key === 'B') {
    asset = (
      <div style={{ display: 'flex', alignItems: 'center', gap: 24, padding: '0 44px' }}>
        <Owl size={104} />
        <div>
          <div style={{ fontFamily: t.cond, fontWeight: 800, fontSize: 70, lineHeight: .82, letterSpacing: '.01em', color: t.ink }}>TABIJI</div>
          <div style={{ height: 7, background: t.terra, margin: '6px 0 9px', width: '100%' }} />
          <div style={{ fontFamily: t.sans, fontSize: 11, fontWeight: 600, letterSpacing: '.2em', color: t.sub }}>WHAT THE GUIDEBOOKS WON’T TELL YOU</div>
        </div>
      </div>
    );
  } else {
    asset = (
      <div style={{ display: 'flex', alignItems: 'center', gap: 24, padding: '0 42px', height: '100%' }}>
        <Owl size={94} />
        <div style={{ flex: 1 }}>
          <div style={{ fontFamily: t.sans, fontWeight: 800, fontSize: 46, letterSpacing: '.16em', color: '#F3ECDE', lineHeight: 1 }}>TABIJI</div>
          <div style={{ fontFamily: t.mono, fontSize: 12, letterSpacing: '.22em', color: t.terra, marginTop: 11 }}>VOL.7 — CHINA · TRAVEL SAFETY</div>
        </div>
        <div style={{ width: 16, height: 16, background: t.terra }} />
      </div>
    );
  }
  const assetBg = t.key === 'C' ? t.panel : (t.key === 'B' ? '#FFFFFF' : t.surface);
  return (
    <div>
      <Meta t={t} idx="①" name="Standard Company Logo" dim="600 × 180 px" />
      <div style={{ display: 'flex', justifyContent: 'center', padding: t.dark ? 0 : '0' }}>
        <div style={{ width: 600, height: 180, background: assetBg, border: t.key === 'C' ? 'none' : `1px solid ${t.line}`,
          display: 'flex', alignItems: 'center', position: 'relative', boxShadow: t.dark ? '0 2px 0 rgba(0,0,0,.18)' : 'none' }}>
          {asset}
          <span style={{ position: 'absolute', right: 9, bottom: 7 }}>{dimTag(t, '600×180', t.key === 'C')}</span>
        </div>
      </div>
    </div>
  );
}

/* ===========================================================
   ② IMAGE HEADER WITH TEXT — 970 × 300 banner + caption
   =========================================================== */
function ModuleHeader({ t }) {
  const h = t.key === 'A' ? C.hero.authority : t.key === 'B' ? C.hero.loss : C.hero.provocative;
  let banner;

  if (t.key === 'A') {
    banner = (
      <div style={{ width: 970, height: 300, display: 'flex', background: t.surface, border: `1px solid ${t.line}` }}>
        <div style={{ flex: 1, padding: '34px 38px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.18em', color: t.terra, marginBottom: 14 }}>{h.kicker}</div>
          <div style={{ fontFamily: t.serif, fontSize: 38, lineHeight: 1.06, color: t.ink, letterSpacing: '-.015em' }}>
            {h.head.map((l, i) => <div key={i}>{l}</div>)}
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 9, margin: '18px 0 9px' }}>
            <span style={{ fontFamily: t.serif, fontSize: 32, color: t.terra, lineHeight: 1 }}>{C.stat.scams}</span>
            <span style={{ fontSize: 13, color: t.sub }}>documented scams</span>
            <span style={{ color: t.line }}>·</span>
            <span style={{ fontFamily: t.serif, fontSize: 32, color: t.terra, lineHeight: 1 }}>{C.stat.cities}</span>
            <span style={{ fontSize: 13, color: t.sub }}>cities</span>
          </div>
          <div style={{ fontFamily: t.mono, fontSize: 9.5, letterSpacing: '.05em', color: t.onPageSub }}>CHINESE PRESS · REDDIT REPORTS · REAL TRAVELER STORIES · PSB&nbsp;110</div>
        </div>
        <div style={{ flex: '0 0 320px', position: 'relative', borderLeft: `1px solid ${t.line}`, background: t.wash,
          display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {/* square mat so the full 2×2 comic fills the frame, uncropped */}
          <div style={{ padding: 8, background: t.terraDeep, boxShadow: '0 6px 18px rgba(60,30,15,.18)' }}>
            <Img src={IMG.beijing2} fallback={IMG.shanghai1} alt="art-student gallery scam comic"
              fit="cover" style={{ width: 268, height: 268, display: 'block' }} />
          </div>
          <div style={{ position: 'absolute', left: 12, top: 12 }}><Stamp t={t} label={'CHINA\n·2026·\nVOL 7'} size={62} rot={-9} /></div>
        </div>
      </div>
    );
  } else if (t.key === 'B') {
    banner = (
      <div style={{ width: 970, height: 300, position: 'relative', overflow: 'hidden', background: '#1c1712' }}>
        <Img src={IMG.beijing2} fallback={IMG.shanghai1} alt="Wangfujing art-student gallery scam"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} pos="top center" />
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(90deg, rgba(20,15,11,.93) 30%, rgba(20,15,11,.55) 58%, rgba(20,15,11,.08) 100%)' }} />
        <div style={{ position: 'absolute', inset: 0, padding: '34px 40px', display: 'flex', flexDirection: 'column', justifyContent: 'center', maxWidth: 660 }}>
          <div style={{ display: 'inline-flex', alignSelf: 'flex-start', fontFamily: t.mono, fontSize: 10.5, letterSpacing: '.16em', color: '#fff', background: t.terra, padding: '5px 10px', marginBottom: 15 }}>{h.kicker}</div>
          <div style={{ fontFamily: t.cond, fontWeight: 800, fontSize: 50, lineHeight: .94, color: '#fff', letterSpacing: '.005em' }}>
            {h.head.map((l, i) => <div key={i} style={{ color: i === 0 ? '#fff' : (i === 1 ? '#fff' : '#fff') }}>{l.replace('¥2,000', '')}{i === 0 ? <span style={{ color: '#F6B98C' }}>¥2,000</span> : ''}</div>)}
          </div>
          <div style={{ fontSize: 13.5, color: 'rgba(255,255,255,.82)', marginTop: 16, maxWidth: 470, lineHeight: 1.5 }}>{h.sub}</div>
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,.55)', borderTop: `2px solid ${t.terra}`,
          display: 'flex', gap: 26, padding: '8px 40px', fontFamily: t.mono, fontSize: 11, letterSpacing: '.1em', color: 'rgba(255,255,255,.9)' }}>
          <span><b style={{ color: '#F6B98C' }}>98</b> SCAMS</span><span><b style={{ color: '#F6B98C' }}>16</b> CITIES</span><span>CHINESE-PRESS SOURCED</span><span style={{ marginLeft: 'auto' }}>$4.99 · KINDLE</span>
        </div>
      </div>
    );
  } else {
    banner = (
      <div style={{ width: 970, height: 300, display: 'flex', background: t.panel, position: 'relative', overflow: 'hidden' }}>
        <div style={{ flex: '0 0 540px', padding: '38px 42px', display: 'flex', flexDirection: 'column', justifyContent: 'center', position: 'relative', zIndex: 2 }}>
          <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.2em', color: t.terra, marginBottom: 16 }}>{h.kicker}</div>
          <div style={{ fontFamily: t.serif, fontSize: 42, lineHeight: 1.03, color: '#F3ECDE', letterSpacing: '-.015em' }}>
            {h.head.map((l, i) => <div key={i}>{l}</div>)}
          </div>
          <div style={{ width: 64, height: 3, background: t.terra, margin: '20px 0 14px' }} />
          <div style={{ fontFamily: t.mono, fontSize: 10.5, letterSpacing: '.05em', color: '#9AA4BC', lineHeight: 1.6 }}>
            98 SCAMS · 16 CITIES<br />{C.stat.sources.join(' · ')}
          </div>
        </div>
        <div style={{ flex: 1, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ position: 'absolute', inset: 0, backgroundImage: `repeating-linear-gradient(45deg, rgba(255,255,255,.03) 0 10px, transparent 10px 20px)` }} />
          <div style={{ transform: 'rotate(-2deg)', background: t.surface, padding: 10, boxShadow: '0 14px 30px rgba(0,0,0,.4)', position: 'relative' }}>
            <div style={{ position: 'absolute', top: -11, left: '50%', transform: 'translateX(-50%) rotate(2deg)', background: t.terra, color: '#fff', fontFamily: t.mono, fontSize: 10, letterSpacing: '.14em', padding: '3px 12px' }}>EXHIBIT A</div>
            <Img src={IMG.beijing2} fallback={IMG.shanghai1} alt="art-student gallery scam comic"
              style={{ width: 286, height: 214 }} pos="top" />
            <div style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.08em', color: t.sub, padding: '7px 2px 1px' }}>BEIJING · WANGFUJING “ART STUDENT”</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Meta t={t} idx="②" name="Standard Image Header With Text" dim="970 × 300 px + text" />
      {banner}
      {/* the Amazon text portion that sits under the banner image */}
      <div style={{ background: t.dark ? t.panel : t.surface, border: t.dark ? 'none' : `1px solid ${t.line}`, borderTop: 'none',
        padding: '15px 24px', display: 'flex', alignItems: 'baseline', gap: 14 }}>
        <span style={{ fontFamily: t.serif, fontSize: 16, color: t.dark ? '#F3ECDE' : t.ink, flex: '0 0 auto' }}>China: Tourist Scams</span>
        <span style={{ fontSize: 13, color: t.dark ? '#9AA4BC' : t.sub, lineHeight: 1.45 }}>{h.sub}</span>
      </div>
    </div>
  );
}

/* ===========================================================
   ③ FOUR IMAGE & TEXT — 4 × 300×300
   =========================================================== */
function ModuleQuad({ t }) {
  const cards = C.quad;
  let body;
  if (t.key === 'A') {
    body = (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 18 }}>
        {cards.map((c) => (
          <div key={c.n}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 7, marginBottom: 8 }}>
              <span style={{ fontFamily: t.serif, fontSize: 16, color: t.terra }}>{c.n}</span>
              <span style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.12em', color: t.sub, whiteSpace: 'nowrap' }}>{c.tag}</span>
            </div>
            <Img src={c.img} alt={c.title} style={{ width: '100%', height: 192, border: `1px solid ${t.line}` }} pos="top" />
            <div style={{ fontFamily: t.serif, fontSize: 17, color: t.ink, margin: '11px 0 5px', lineHeight: 1.12 }}>{c.title}</div>
            <div style={{ fontSize: 11.5, color: t.sub, lineHeight: 1.5 }}>{c.tl}</div>
          </div>
        ))}
      </div>
    );
  } else if (t.key === 'B') {
    body = (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 14 }}>
        {cards.map((c) => (
          <div key={c.n} style={{ position: 'relative', background: '#15110d' }}>
            <Img src={c.img} alt={c.title} style={{ width: '100%', height: 214 }} pos="top center" />
            <div style={{ padding: '11px 12px 13px', background: '#1c1712' }}>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
                <span style={{ fontFamily: t.cond, fontWeight: 800, fontSize: 30, color: '#F6B98C', lineHeight: .9 }}>{c.loss}</span>
                <span style={{ fontFamily: t.mono, fontSize: 9, letterSpacing: '.1em', color: 'rgba(255,255,255,.55)' }}>{c.city}</span>
              </div>
              <div style={{ fontFamily: t.cond, fontWeight: 700, fontSize: 18, color: '#fff', textTransform: 'uppercase', letterSpacing: '.01em', marginTop: 4, lineHeight: 1 }}>{c.tag}</div>
              <div style={{ fontSize: 11, color: 'rgba(255,255,255,.66)', marginTop: 6, lineHeight: 1.45 }}>{c.title}</div>
            </div>
          </div>
        ))}
      </div>
    );
  } else {
    body = (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 16 }}>
        {cards.map((c, i) => (
          <div key={c.n} style={{ background: t.surface, padding: 9, boxShadow: '0 8px 18px rgba(0,0,0,.28)', transform: `rotate(${i % 2 ? .8 : -.8}deg)` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: t.mono, fontSize: 9.5, letterSpacing: '.08em', color: t.sub, padding: '1px 1px 7px' }}>
              <span>EXHIBIT {c.n}</span><span style={{ color: t.terra }}>{c.tag}</span>
            </div>
            <Img src={c.img} alt={c.title} style={{ width: '100%', height: 178 }} pos="top" />
            <div style={{ fontFamily: t.serif, fontSize: 15.5, color: t.ink, margin: '9px 1px 4px', lineHeight: 1.12 }}>{c.title}</div>
            <div style={{ fontSize: 10.5, color: t.sub, lineHeight: 1.45, padding: '0 1px' }}>{c.tl}</div>
          </div>
        ))}
      </div>
    );
  }

  const wrapBg = t.dark ? t.panel : t.surface;
  return (
    <div>
      <Meta t={t} idx="③" name="Standard Four Image & Text" dim="4 × 300 × 300 px" />
      <div style={{ background: wrapBg, border: t.dark ? 'none' : `1px solid ${t.line}`, padding: '24px 24px 26px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 14, marginBottom: 20 }}>
          <div style={{ fontFamily: t.key === 'B' ? t.cond : t.serif, fontWeight: t.key === 'B' ? 700 : 400,
            fontSize: t.key === 'B' ? 30 : 25, color: t.dark ? '#F3ECDE' : t.ink, lineHeight: 1, letterSpacing: t.key === 'B' ? '.01em' : '-.01em',
            textTransform: t.key === 'B' ? 'uppercase' : 'none' }}>{C.quadHead[t.key]}</div>
          <div style={{ flex: 1, height: 1, background: t.dark ? 'rgba(255,255,255,.16)' : t.line, marginBottom: 6 }} />
        </div>
        {body}
      </div>
    </div>
  );
}

/* ===========================================================
   ④ MULTIPLE IMAGE MODULE A — 300×300 main + value stack
   =========================================================== */
function ModuleInside({ t }) {
  const ins = C.inside;
  const wrapBg = t.dark ? t.panel : t.surface;
  const onWrap = t.dark ? '#F3ECDE' : t.ink;

  const heading = (
    <div style={{ fontFamily: t.key === 'B' ? t.cond : t.serif, fontWeight: t.key === 'B' ? 700 : 400,
      fontSize: t.key === 'B' ? 31 : 25, lineHeight: 1.05, color: onWrap, letterSpacing: t.key === 'B' ? '.005em' : '-.01em',
      textTransform: t.key === 'B' ? 'uppercase' : 'none', maxWidth: 560 }}>
      {t.key === 'B' ? 'What’s inside the book' : ins.head}
    </div>
  );

  const list = (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: t.key === 'B' ? '11px 26px' : '12px 28px', marginTop: 18 }}>
      {ins.items.map(([title, sub], i) => (
        <div key={i} style={{ display: 'flex', gap: 10 }}>
          <span style={{ flex: '0 0 auto', marginTop: 2,
            ...(t.key === 'C'
              ? { fontFamily: t.mono, fontSize: 12, color: t.terra, fontWeight: 600 }
              : { width: 16, height: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', background: t.terra, fontSize: 11, borderRadius: t.key === 'B' ? 0 : 3 }) }}>
            {t.key === 'C' ? '0' + (i + 1) : '✓'}
          </span>
          <div>
            <div style={{ fontFamily: t.key === 'B' ? t.cond : t.sans, fontWeight: t.key === 'B' ? 700 : 600,
              fontSize: t.key === 'B' ? 17 : 14, color: t.dark ? '#EDE6D8' : t.ink, lineHeight: 1.12,
              textTransform: t.key === 'B' ? 'uppercase' : 'none', letterSpacing: t.key === 'B' ? '.01em' : 0 }}>{title}</div>
            <div style={{ fontSize: 11.5, color: t.dark ? '#9AA4BC' : t.sub, marginTop: 2, lineHeight: 1.4 }}>{sub}</div>
          </div>
        </div>
      ))}
    </div>
  );

  // left image — exhibit-framed for C, plain mat for A, full for B
  const image = t.key === 'C' ? (
    <div style={{ flex: '0 0 300px', background: t.surface, padding: 10, transform: 'rotate(-1.5deg)', boxShadow: '0 12px 26px rgba(0,0,0,.3)', alignSelf: 'flex-start' }}>
      <Img src={ins.img} alt="Nanjing Road tea-house scam comic" style={{ width: 280, height: 280 }} pos="top" />
      <div style={{ fontFamily: t.mono, fontSize: 9.5, letterSpacing: '.08em', color: t.sub, padding: '7px 2px 1px' }}>SHANGHAI · NANJING-RD TEA HOUSE</div>
    </div>
  ) : (
    <div style={{ flex: '0 0 300px', alignSelf: 'flex-start' }}>
      <Img src={ins.img} alt="Nanjing Road tea-house scam comic"
        style={{ width: 300, height: 300, border: t.key === 'A' ? `7px solid ${t.terraDeep}` : `1px solid ${t.line}` }} pos="top" />
      <div style={{ fontFamily: t.mono, fontSize: 10, letterSpacing: '.06em', color: t.onPageSub, marginTop: 7 }}>SHANGHAI · NANJING-RD TEA HOUSE</div>
    </div>
  );

  return (
    <div>
      <Meta t={t} idx="④" name="Standard Multiple Image Module A" dim="300 × 300 px + text" />
      <div style={{ background: wrapBg, border: t.dark ? 'none' : `1px solid ${t.line}`, padding: '26px 26px 24px', display: 'flex', gap: 34 }}>
        {image}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          {t.key === 'C' && <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.2em', color: t.terra, marginBottom: 12 }}>FILE CONTENTS — 98 ENTRIES</div>}
          {heading}
          {list}
          <div style={{ display: 'flex', gap: 9, marginTop: 20 }}>
            {ins.phrases.map((p, i) => <Phrase key={i} t={t} p={p} dark={t.dark} />)}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ===========================================================
   ⑤ PRODUCT DESCRIPTION TEXT — closing trust block
   =========================================================== */
function ModuleDesc({ t }) {
  const d = C.desc;
  const wrapBg = t.dark ? t.panel : t.surface;
  const onWrap = t.dark ? '#F3ECDE' : t.ink;
  const subC = t.dark ? '#9AA4BC' : t.sub;

  return (
    <div>
      <Meta t={t} idx="⑤" name="Standard Product Description Text" dim="text only" />
      <div style={{ background: wrapBg, border: t.dark ? 'none' : `1px solid ${t.line}`, padding: '30px 34px 28px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 16, marginBottom: 18 }}>
          {t.key !== 'B' && <Owl size={46} src={t.dark ? IMG.owlFly : IMG.owl} />}
          <div style={{ fontFamily: t.key === 'B' ? t.cond : t.serif, fontWeight: t.key === 'B' ? 800 : 400,
            fontSize: t.key === 'B' ? 38 : 30, color: onWrap, lineHeight: 1, letterSpacing: t.key === 'B' ? '.005em' : '-.015em',
            textTransform: t.key === 'B' ? 'uppercase' : 'none' }}>{d.head[t.key]}</div>
          <div style={{ flex: 1 }} />
          <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.08em', color: t.terra, whiteSpace: 'nowrap' }}>{d.price}</div>
        </div>
        <div style={{ width: '100%', height: 1, background: t.dark ? 'rgba(255,255,255,.16)' : t.line, marginBottom: 18 }} />
        <div style={{ columns: 2, columnGap: 40, fontSize: 13, lineHeight: 1.62, color: subC }}>
          {d.body.map((p, i) => (
            <p key={i} style={{ margin: i === 0 ? '0 0 12px' : '0 0 12px', breakInside: 'avoid', textWrap: 'pretty' }}>{p}</p>
          ))}
        </div>
        <div style={{ display: 'flex', gap: 0, marginTop: 22, flexWrap: 'wrap', alignItems: 'center' }}>
          {d.badges.map((b, i) => (
            <React.Fragment key={i}>
              {i > 0 && <span style={{ color: t.terra, margin: '0 14px' }}>◆</span>}
              <span style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.13em', color: t.dark ? '#C9D0DF' : t.ink, fontWeight: 600 }}>{b}</span>
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ===========================================================
   SET PAGE — stacks all five modules on the page bg
   =========================================================== */
function SetPage({ t }) {
  return (
    <div style={{ width: 1026, background: t.pageBg, fontFamily: t.sans, color: t.ink,
      padding: '30px 28px 34px', display: 'flex', flexDirection: 'column', gap: 30,
      backgroundImage: t.dark ? 'none' : `radial-gradient(circle at 1px 1px, ${t.lineSoft} 1px, transparent 0)`,
      backgroundSize: '22px 22px' }}>
      <ModuleLogo t={t} />
      <ModuleHeader t={t} />
      <ModuleQuad t={t} />
      <ModuleInside t={t} />
      <ModuleDesc t={t} />
    </div>
  );
}

Object.assign(window, { SetPage, ModuleLogo, ModuleHeader, ModuleQuad, ModuleInside, ModuleDesc });
