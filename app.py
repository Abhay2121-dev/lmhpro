"""
app.py  –  Gentle Reflection (Manager Demo)
A focused grief journaling prototype: user writes, AI helps them
understand their feelings through gentle reflection and questions.

Run:  streamlit run app.py
Key:  .streamlit/secrets.toml  →  GOOGLE_API_KEY = "..."
"""

import streamlit as st
import streamlit.components.v1 as components
import ai_service as ai
from safety import check as risk_check, Risk, CRISIS_MSG, ELEVATED_MSG

# ── Page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gentle Reflection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

api_config_error = ai.api_key_error()

# ── CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400;1,600&family=Lora:ital,wght@0,400;1,400&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* App background — warm parchment */
.stApp { background: #f4eed9 !important; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

/* Wider main container */
[data-testid="stMainBlockContainer"] {
    max-width: 1400px !important;
    padding: 2rem 2.5rem 3rem !important;
}

/* Remove gap between columns */
[data-testid="stColumns"] {
    gap: 0 !important;
}

/* ── Title ── */
.journal-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 2.2rem;
    color: #2d1500;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: 0.01em;
}
.journal-subtitle {
    font-size: 0.88rem;
    color: #9a7f60;
    text-align: center;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
}
.divider-ornament {
    text-align: center;
    color: #c49a38;
    font-size: 1rem;
    margin: 0.5rem 0 1.8rem;
    letter-spacing: 0.3em;
}

/* ── Column panel labels ── */
.panel-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #b5a080;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #d8c9a8;
}

/* ── Divider between columns ── */
.col-divider {
    width: 1px;
    background: linear-gradient(to bottom, transparent, #d8c9a8 15%, #d8c9a8 85%, transparent);
    margin: 0 1.5rem;
    min-height: 100%;
}

/* ── Prompt selector ── */
.stSelectbox > div > div {
    background: #fdf8ef !important;
    border: 1px solid #d8c9a8 !important;
    border-radius: 8px !important;
    font-family: 'Lora', serif !important;
    font-style: italic !important;
    color: #5a3e2a !important;
}

/* ── Prompt card ── */
.prompt-card {
    background: #fdf8ef;
    border-left: 4px solid #c49a38;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.2rem;
    margin: 0.8rem 0 1rem;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1.05rem;
    color: #3d2c1e;
    line-height: 1.5;
}

/* ── Journal textarea — ruled paper ── */
.stTextArea textarea {
    font-family: 'Lora', serif !important;
    font-size: 1.05rem !important;
    line-height: 2.1 !important;
    color: #1c1208 !important;
    background-color: #fffef8 !important;
    background-image: repeating-linear-gradient(
        transparent, transparent 41px, #dfd0b8 41px, #dfd0b8 42px
    ) !important;
    background-position: 0 8px !important;
    border: 1px solid #d0c0a0 !important;
    border-radius: 10px !important;
    padding: 1rem 1.3rem !important;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.06) !important;
    caret-color: #8b4513 !important;
}
.stTextArea textarea:focus {
    border-color: #c49a38 !important;
    box-shadow: 0 0 0 2px rgba(196,154,56,0.18), inset 0 2px 10px rgba(0,0,0,0.04) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder {
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    color: #c0aa88 !important;
}
.stTextArea label { display: none !important; }

/* ── Word count ── */
.word-count {
    text-align: right;
    font-size: 0.78rem;
    color: #b5a080;
    margin-top: -0.3rem;
    margin-bottom: 0.8rem;
    font-family: 'Inter', sans-serif;
}

/* ── Main CTA button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: #4a2e0a !important;
    color: #f0e0c0 !important;
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    font-size: 1.05rem !important;
    padding: 0.7rem 2rem !important;
    border-radius: 999px !important;
    border: 1px solid rgba(196,154,56,0.4) !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
}
div[data-testid="stButton"] > button:hover {
    background: #6b3e10 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.28) !important;
}

/* ── AI companion placeholder ── */
.ai-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 340px;
    text-align: center;
    color: #c9b898;
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 1rem;
    gap: 1rem;
    padding: 2rem;
    background: rgba(255,254,248,0.5);
    border-radius: 14px;
    border: 1px dashed #d8c9a8;
}
.ai-placeholder-icon {
    font-size: 2.5rem;
    opacity: 0.4;
}
.ai-placeholder-text {
    line-height: 1.7;
    opacity: 0.75;
}

/* ── AI Output cards ── */
.ai-section {
    background: #fffef8;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin: 0 0 0.75rem 0;
    border: 1px solid #e0d0b0;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}
.ai-section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: #c49a38;
    text-transform: uppercase;
    margin-bottom: 0.55rem;
}
.reflection-text {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 1rem;
    color: #3d2c1e;
    line-height: 1.8;
    border-left: 3px solid #c49a38;
    padding-left: 1rem;
}
.question-item {
    font-size: 0.97rem;
    color: #4a3828;
    padding: 0.4rem 0;
    border-bottom: 1px solid #ede0c8;
    line-height: 1.6;
    font-family: 'Lora', serif;
}
.question-item:last-child { border-bottom: none; }
.question-item::before { content: "— "; color: #c49a38; }
.starter-item {
    background: #fdf5e4;
    border: 1px solid #e8d8b0;
    border-radius: 8px;
    padding: 0.45rem 0.85rem;
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 0.93rem;
    color: #5a3e2a;
    margin: 0.2rem 0;
}
.tag-pill {
    display: inline-block;
    background: #e8f0e9;
    color: #3d6b4e;
    border: 1px solid rgba(61,107,78,0.2);
    border-radius: 999px;
    padding: 0.18rem 0.7rem;
    font-size: 0.76rem;
    margin: 0.18rem 0.1rem;
}

/* ── AI companion header ── */
.companion-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #d8c9a8;
}
.companion-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #c49a38, #8b6820);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.companion-name {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #b5a080;
}

/* ── Disclaimer ── */
.disclaimer-footer {
    text-align: center;
    font-size: 0.75rem;
    color: #b5a080;
    margin-top: 2rem;
    line-height: 1.7;
    border-top: 1px solid #d8c9a8;
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ── Ambient sound player (Web Audio API, injected into parent page) ────
components.html("""
<script>
(function () {
  const p = window.parent;
  const pd = p.document;

  /* Only inject once — persists across Streamlit reruns */
  if (pd.getElementById('ambient-player')) return;

  /* ── Styles ── */
  const style = pd.createElement('style');
  style.textContent = `
    #ambient-player {
      position: fixed;
      top: 16px;
      right: 20px;
      z-index: 9999;
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(253,248,239,0.92);
      backdrop-filter: blur(8px);
      border: 1px solid #d8c9a8;
      border-radius: 999px;
      padding: 7px 14px 7px 10px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.12);
      font-family: 'Inter', sans-serif;
      transition: box-shadow 0.2s;
    }
    #ambient-player:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.18); }
    .amb-label {
      font-size: 0.65rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #b5a080;
      margin-right: 4px;
    }
    .amb-btn {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 1.1rem;
      padding: 3px 5px;
      border-radius: 50%;
      transition: background 0.15s, transform 0.1s;
      line-height: 1;
    }
    .amb-btn:hover { background: rgba(196,154,56,0.12); transform: scale(1.15); }
    .amb-btn.active {
      background: rgba(196,154,56,0.22);
      box-shadow: 0 0 0 2px rgba(196,154,56,0.45);
    }
    .amb-vol {
      -webkit-appearance: none;
      appearance: none;
      width: 58px;
      height: 3px;
      border-radius: 2px;
      background: linear-gradient(to right, #c49a38 var(--pct,60%), #d8c9a8 var(--pct,60%));
      outline: none;
      cursor: pointer;
      margin-left: 4px;
    }
    .amb-vol::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 11px; height: 11px;
      border-radius: 50%;
      background: #c49a38;
      cursor: pointer;
    }
  `;
  pd.head.appendChild(style);

  /* ── HTML ── */
  const el = pd.createElement('div');
  el.id = 'ambient-player';
  el.innerHTML = `
    <span class="amb-label">Sound</span>
    <button class="amb-btn" id="amb-rain"   title="Rain">&#127783;</button>
    <button class="amb-btn" id="amb-forest" title="Forest">&#127794;</button>
    <button class="amb-btn" id="amb-ocean"  title="Ocean">&#127754;</button>
    <button class="amb-btn" id="amb-off"    title="Silence">&#128263;</button>
    <input  class="amb-vol" id="amb-vol" type="range" min="0" max="1"
            step="0.01" value="0.55" title="Volume">
  `;
  pd.body.appendChild(el);

  /* ── Web Audio engine ── */
  let actx = null;
  let master = null;
  let activeNodes = [];

  function getCtx() {
    if (!actx) {
      actx = new (p.AudioContext || p.webkitAudioContext)();
      master = actx.createGain();
      master.gain.value = parseFloat(pd.getElementById('amb-vol').value);
      master.connect(actx.destination);
    }
    if (actx.state === 'suspended') actx.resume();
    return actx;
  }

  function stopAll() {
    activeNodes.forEach(n => { try { n.stop(); } catch(e) {} });
    activeNodes = [];
  }

  function whiteNoise(sec) {
    const c = getCtx();
    const buf = c.createBuffer(1, c.sampleRate * sec, c.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    const src = c.createBufferSource(); src.buffer = buf; src.loop = true;
    return src;
  }

  function pinkNoise(sec) {
    const c = getCtx();
    const buf = c.createBuffer(1, c.sampleRate * sec, c.sampleRate);
    const d = buf.getChannelData(0);
    let b0=0,b1=0,b2=0,b3=0,b4=0,b5=0,b6=0;
    for (let i = 0; i < d.length; i++) {
      const w = Math.random()*2-1;
      b0=0.99886*b0+w*0.0555179; b1=0.99332*b1+w*0.0750759;
      b2=0.96900*b2+w*0.1538520; b3=0.86650*b3+w*0.3104856;
      b4=0.55000*b4+w*0.5329522; b5=-0.7616*b5-w*0.0168980;
      d[i]=(b0+b1+b2+b3+b4+b5+b6+w*0.5362)*0.115; b6=w*0.115926;
    }
    const src = c.createBufferSource(); src.buffer = buf; src.loop = true;
    return src;
  }

  function lfo(freq, depth, target) {
    const c = getCtx();
    const osc = c.createOscillator(); const g = c.createGain();
    osc.frequency.value = freq; g.gain.value = depth;
    osc.connect(g); g.connect(target); osc.start();
    return osc;
  }

  function playRain() {
    stopAll();
    const c = getCtx();
    const heavy = whiteNoise(2);
    const f1 = c.createBiquadFilter(); f1.type='lowpass';  f1.frequency.value=1600;
    const f2 = c.createBiquadFilter(); f2.type='highpass'; f2.frequency.value=700;
    const g1 = c.createGain(); g1.gain.value=0.65;
    heavy.connect(f1); f1.connect(f2); f2.connect(g1); g1.connect(master);

    const drip = whiteNoise(2);
    const fd = c.createBiquadFilter(); fd.type='bandpass'; fd.frequency.value=3200; fd.Q.value=0.9;
    const gd = c.createGain(); gd.gain.value=0.07;
    drip.connect(fd); fd.connect(gd); gd.connect(master);

    heavy.start(); drip.start();
    activeNodes.push(heavy, drip);
  }

  function playForest() {
    stopAll();
    const c = getCtx();
    const wind = pinkNoise(2);
    const fw = c.createBiquadFilter(); fw.type='lowpass'; fw.frequency.value=500;
    const l1 = lfo(0.08, 180, fw.frequency);
    const gw = c.createGain(); gw.gain.value=0.45;
    wind.connect(fw); fw.connect(gw); gw.connect(master);

    const leaves = whiteNoise(2);
    const fl = c.createBiquadFilter(); fl.type='bandpass'; fl.frequency.value=2400; fl.Q.value=1.4;
    const gl = c.createGain(); gl.gain.value=0.06;
    leaves.connect(fl); fl.connect(gl); gl.connect(master);

    wind.start(); leaves.start();
    activeNodes.push(wind, leaves, l1);
  }

  function playOcean() {
    stopAll();
    const c = getCtx();
    const noise = pinkNoise(2);
    const filt = c.createBiquadFilter(); filt.type='lowpass'; filt.frequency.value=420;
    const l1 = lfo(0.07, 150, filt.frequency);
    const g = c.createGain(); g.gain.value=0.55;
    const l2 = lfo(0.09, 0.17, g.gain);
    noise.connect(filt); filt.connect(g); g.connect(master);
    noise.start();
    activeNodes.push(noise, l1, l2);
  }

  function setActive(id) {
    ['amb-rain','amb-forest','amb-ocean','amb-off']
      .forEach(k => pd.getElementById(k).classList.remove('active'));
    if (id) pd.getElementById(id).classList.add('active');
  }

  pd.getElementById('amb-rain').onclick   = () => { playRain();   setActive('amb-rain');   };
  pd.getElementById('amb-forest').onclick = () => { playForest(); setActive('amb-forest'); };
  pd.getElementById('amb-ocean').onclick  = () => { playOcean();  setActive('amb-ocean');  };
  pd.getElementById('amb-off').onclick    = () => { stopAll();    setActive('amb-off');    };

  const vol = pd.getElementById('amb-vol');
  vol.oninput = function() {
    if (master) master.gain.setTargetAtTime(+this.value, actx.currentTime, 0.05);
    this.style.setProperty('--pct', (+this.value*100)+'%');
  };
  vol.style.setProperty('--pct', (+vol.value*100)+'%');
})();
</script>
""", height=0)


if "ai_result" not in st.session_state:
    st.session_state.ai_result = None
if "risk_msg" not in st.session_state:
    st.session_state.risk_msg = None
if "last_processed" not in st.session_state:
    st.session_state.last_processed = ""   # text that was last sent to AI
if "ai_loading" not in st.session_state:
    st.session_state.ai_loading = False

# ── Header ────────────────────────────────────────────────────────────
st.markdown('<div class="journal-title">🌿 Gentle Reflection</div>', unsafe_allow_html=True)
st.markdown('<div class="journal-subtitle">A PRIVATE SPACE FOR GRIEF &amp; MEMORY</div>', unsafe_allow_html=True)
st.markdown('<div class="divider-ornament">✦ · ✦ · ✦</div>', unsafe_allow_html=True)

# ── Starter prompts ───────────────────────────────────────────────────
PROMPTS = [
    "Begin anywhere. Write whatever is present for you today…",
    "What I have always wanted to tell you is…",
    "A treasured memory of you is…",
    "Something I never got to say was…",
    "When I miss you, I…",
    "I think of you the most when…",
    "I regret that we never…",
    "One thing I want to keep alive is…",
    "Without you, I feel…",
    "What I now realize is…",
]

selected = st.selectbox(
    "Choose a prompt to start with, or write freely:",
    PROMPTS,
    label_visibility="visible",
)

st.markdown(
    f'<div class="prompt-card">✦ {selected}</div>',
    unsafe_allow_html=True,
)

# ── Two-column layout ─────────────────────────────────────────────────
col_journal, col_divider, col_ai = st.columns([10, 0.3, 9])

with col_journal:
    # Panel label
    st.markdown('<div class="panel-label">📖 &nbsp; Your Journal</div>', unsafe_allow_html=True)

    # Journal textarea
    journal_text = st.text_area(
        "Journal",
        height=380,
        placeholder="Begin writing here… there is no right or wrong way.",
        label_visibility="hidden",
    )

    # ── Debounce JS: fire after 2 s of no typing ──────────────────────
    # Injects into the parent Streamlit page (same-origin iframe).
    # Finds the real textarea DOM node, attaches an 'input' listener,
    # and after DEBOUNCE_MS ms of silence triggers blur so Streamlit
    # picks up the current value and reruns.
    components.html("""
<script>
(function () {
  const DEBOUNCE_MS = 2000;
  let timer = null;
  let attached = null;

  function triggerUpdate(ta) {
    // React ignores synthetic events on the same value, so we must
    // go through the native property setter to mark the value as changed.
    const nativeSetter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype, 'value'
    ).set;
    nativeSetter.call(ta, ta.value);
    ta.dispatchEvent(new Event('input',  { bubbles: true }));
    // Short pause then blur so Streamlit's onBlur handler fires
    setTimeout(() => ta.dispatchEvent(new Event('blur', { bubbles: true })), 80);
  }

  function attach() {
    // Walk up to the parent Streamlit document
    const parentDoc = window.parent.document;
    const ta = parentDoc.querySelector('.stTextArea textarea');
    if (!ta || ta === attached) return;
    attached = ta;

    ta.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(() => triggerUpdate(ta), DEBOUNCE_MS);
    });
  }

  // Attach immediately, then re-attach after each Streamlit rerun
  // (Streamlit replaces DOM nodes on rerun, so we use MutationObserver)
  attach();
  new MutationObserver(attach).observe(
    window.parent.document.body,
    { childList: true, subtree: true }
  );
})();
</script>
""", height=0)

    wc = len(journal_text.split()) if journal_text.strip() else 0
    _trigger_key_hint = journal_text.strip() + "||" + selected
    if wc > 0 and wc < 10:
        _hint = f'<span style="color:#c49a38;font-size:0.75rem"> · {10 - wc} more word{"s" if 10 - wc != 1 else ""} for reflection</span>'
    else:
        _hint = ""
    st.markdown(
        f'<div class="word-count">{wc} word{"s" if wc != 1 else ""}{_hint}</div>',
        unsafe_allow_html=True,
    )

    get_recs_button = st.button("Get AI Recommendations ✦", use_container_width=True)

    if api_config_error:
        st.warning(api_config_error)

    _trigger_key = journal_text.strip() + "||" + selected
    if get_recs_button and journal_text.strip() and not api_config_error:
        st.session_state.risk_msg = None
        risk = risk_check(journal_text)

        if risk == Risk.HIGH:
            st.session_state.risk_msg = "high"
            st.session_state.ai_result = None
        else:
            if risk == Risk.ELEVATED:
                st.session_state.risk_msg = "elevated"

            try:
                ai_risk = ai.classify_risk(journal_text)
                if ai_risk == Risk.HIGH:
                    risk = Risk.HIGH
            except Exception:
                pass

            if risk == Risk.HIGH:
                st.session_state.risk_msg = "high"
                st.session_state.ai_result = None
            else:
                with st.spinner("AI is reflecting on your journal..."):
                    result = ai.reflect(journal_text, selected, "Gentle Reflection")
                if not result.get("error"):
                    st.session_state.ai_result = result
                else:
                    st.session_state.ai_result = None
                    st.error(result.get("error"))

            st.session_state.last_processed = _trigger_key

    # Reset AI result if user clears the text
    if wc == 0 and st.session_state.ai_result is not None:
        st.session_state.ai_result = None
        st.session_state.last_processed = ""

# ── Column divider (visual) ───────────────────────────────────────────
with col_divider:
    st.markdown(
        '<div style="width:1px;background:linear-gradient(to bottom,transparent,#d8c9a8 10%,#d8c9a8 90%,transparent);'
        'min-height:560px;margin:0 auto;"></div>',
        unsafe_allow_html=True,
    )

# ── AI Companion panel ────────────────────────────────────────────────
with col_ai:
    # Companion header
    st.markdown(
        '<div class="companion-header">'
        '<div class="companion-avatar">✦</div>'
        '<span class="companion-name">AI Companion · Reflections</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    r = st.session_state.ai_result
    risk_msg = st.session_state.get("risk_msg")

    if risk_msg == "high":
        st.markdown(CRISIS_MSG, unsafe_allow_html=True)
    elif r is None:
        st.markdown(
            '<div class="ai-placeholder">'
            '<div class="ai-placeholder-icon">🌿</div>'
            '<div class="ai-placeholder-text">'
            'Your reflection will appear here once you write<br>'
            'and ask for support. Take your time.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        if risk_msg == "elevated":
            st.info(ELEVATED_MSG)

        # 1. Main reflection
        reflection = r.get("reflection", "")
        if reflection:
            st.markdown(
                f'<div class="ai-section">'
                f'<div class="reflection-text">{reflection}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # 2. Questions to go deeper
        questions = r.get("follow_up_questions", [])
        if questions:
            qs_html = "".join(
                f'<div class="question-item">{q}</div>' for q in questions
            )
            st.markdown(
                f'<div class="ai-section">'
                f'<div class="ai-section-label">Questions to explore</div>'
                f'{qs_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # 3. Ways to keep writing
        starters = r.get("continuation_starters", [])
        if starters:
            st_html = "".join(
                f'<div class="starter-item">{s}…</div>' for s in starters
            )
            st.markdown(
                f'<div class="ai-section">'
                f'<div class="ai-section-label">Ways to keep writing</div>'
                f'{st_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # 4. Gentle reframe (only if guilt/shame)
        if r.get("reframe"):
            st.markdown(
                f'<div class="ai-section" style="border-left:4px solid #4a7c59">'
                f'<div class="ai-section-label" style="color:#4a7c59">A gentle thought</div>'
                f'<div style="font-family:Lora,serif;font-size:0.97rem;color:#2d4a35;'
                f'line-height:1.75">{r["reframe"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # 5. Feeling tags
        tags = r.get("theme_tags", [])
        if tags:
            pills = "".join(f'<span class="tag-pill">{t}</span>' for t in tags)
            st.markdown(
                f'<div style="margin:0.5rem 0 0.2rem">'
                f'<span style="font-size:0.72rem;color:#b5a080;'
                f'letter-spacing:0.08em;text-transform:uppercase">What you\'re touching on · </span>'
                f'{pills}</div>',
                unsafe_allow_html=True,
            )

# ── Footer disclaimer ─────────────────────────────────────────────────
st.markdown(
    '<div class="disclaimer-footer">'
    'Gentle Reflection is a private journaling tool — not therapy or emergency care.<br>'
    'If you are in crisis, please call or text <strong>988</strong> '
    'or contact your local emergency services.'
    '</div>',
    unsafe_allow_html=True,
)
