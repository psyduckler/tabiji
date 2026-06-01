/* ============================================================
   tabiji.ai — China A+ Content · APP (canvas assembly)
   ============================================================ */
const { THEMES } = window.TABIJI;
const TA = THEMES.A;

function Brief() {
  const t = TA;
  const Row = ({ k, name, blurb, c }) => (
    <div style={{ display: 'flex', gap: 12, alignItems: 'baseline', padding: '7px 0', borderTop: `1px solid ${t.lineSoft}` }}>
      <span style={{ width: 22, height: 22, flex: '0 0 auto', background: c, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: t.mono, fontSize: 12, fontWeight: 600 }}>{k}</span>
      <span style={{ fontFamily: t.serif, fontSize: 16, color: t.ink }}>{name}</span>
      <span style={{ fontSize: 12.5, color: t.sub }}>{blurb}</span>
    </div>
  );
  return (
    <div style={{ width: 780, height: 532, background: t.surface, fontFamily: t.sans, color: t.ink, padding: '34px 38px', position: 'relative' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 6 }}>
        <Img src={window.TABIJI.IMG.owl} fallback={window.TABIJI.IMG.owlFly} fit="contain" style={{ width: 50, height: 50 }} />
        <div style={{ fontFamily: t.mono, fontSize: 11, letterSpacing: '.2em', color: t.terra }}>KINDLE A+ CONTENT · CHINA · VOL.7</div>
      </div>
      <div style={{ fontFamily: t.serif, fontSize: 34, lineHeight: 1.05, letterSpacing: '-.015em', color: t.ink, margin: '6px 0 4px' }}>
        Three directions, five modules each.
      </div>
      <div style={{ fontSize: 13.5, color: t.sub, lineHeight: 1.55, maxWidth: 660 }}>
        Comic-forward, sell-this-book-only. Real four-panel art is pulled live from <b style={{ color: t.terra }}>img.tabiji.ai</b> — the same strips that run in the book. Scroll right to compare the full sets.
      </div>
      <div style={{ display: 'flex', gap: 16, margin: '18px 0' }}>
        <div style={{ flex: 1, background: t.surfaceAlt, border: `1px solid ${t.line}`, padding: '12px 14px' }}>
          <div style={{ fontFamily: t.mono, fontSize: 10.5, letterSpacing: '.12em', color: t.terra, marginBottom: 6 }}>HOW A+ WORKS</div>
          <div style={{ fontSize: 12, color: t.sub, lineHeight: 1.5 }}>You upload the <b style={{ color: t.ink }}>images</b>; headings &amp; body are typed as Amazon text. So the design lives in the image assets — built here at true KDP specs: <b style={{ color: t.ink }}>600×180</b>, <b style={{ color: t.ink }}>970×300</b>, <b style={{ color: t.ink }}>300×300</b>.</div>
        </div>
        <div style={{ flex: 1, background: t.surfaceAlt, border: `1px solid ${t.line}`, padding: '12px 14px' }}>
          <div style={{ fontFamily: t.mono, fontSize: 10.5, letterSpacing: '.12em', color: t.terra, marginBottom: 6 }}>NEXT</div>
          <div style={{ fontSize: 12, color: t.sub, lineHeight: 1.5 }}>Pick a direction — or mix modules across them. Then I export every image at exact pixel size, ready to drop into the KDP uploader.</div>
        </div>
      </div>
      <div>
        <Row k="A" name="Field Guide" blurb="Terracotta editorial · authority voice · framed comics" c={THEMES.A.terra} />
        <Row k="B" name="Comic Strip" blurb="Loss-driven · comic-forward · big condensed numerals" c={THEMES.B.terra} />
        <Row k="C" name="Dossier" blurb="Navy case-file · provocative voice · comics as exhibits" c={THEMES.C.terra} />
      </div>
    </div>
  );
}

const SET_H = 2004;

// Warm the CDN cache once so panning never shows a cold image.
function usePreload() {
  React.useEffect(() => {
    const I = window.TABIJI.IMG;
    Object.values(I).forEach((u) => { const im = new Image(); im.src = u; });
  }, []);
}

function App() {
  usePreload();
  return (
    <DesignCanvas>
      <DCSection id="brief" title="China — Kindle A+ Content" subtitle="3 directions · 5 modules each · comic-forward">
        <DCArtboard id="brief" label="Brief · read me" width={780} height={532}><Brief /></DCArtboard>
      </DCSection>
      <DCSection id="sets" title="The three sets" subtitle="Each column is a complete A+ page — logo · header · four-image · multiple-image · description">
        <DCArtboard id="A" label="SET A · Field Guide" width={1026} height={SET_H}><SetPage t={THEMES.A} /></DCArtboard>
        <DCArtboard id="B" label="SET B · Comic Strip" width={1026} height={SET_H}><SetPage t={THEMES.B} /></DCArtboard>
        <DCArtboard id="C" label="SET C · Dossier" width={1026} height={SET_H}><SetPage t={THEMES.C} /></DCArtboard>
      </DCSection>
    </DesignCanvas>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
