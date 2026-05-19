window.$ = (q, root=document) => root.querySelector(q);
window.$$ = (q, root=document) => Array.from(root.querySelectorAll(q));
window.debounce = (fn, wait=160) => { let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), wait); }; };
window.throttle = (fn, wait=120) => { let last = 0; return (...args) => { const now = Date.now(); if (now - last >= wait) { last = now; fn(...args); } }; };
window.toast = (text) => { const el = $('#toast'); el.textContent = text; el.classList.add('show'); clearTimeout(window.__toastTimer); window.__toastTimer = setTimeout(()=>el.classList.remove('show'), 2400); };
window.showLoader = (on=true) => { const l = $('#loader'); l.classList.toggle('active', on); l.setAttribute('aria-hidden', String(!on)); };
window.iconSvg = (name) => {
  const common = 'viewBox="0 0 64 64" role="img" aria-hidden="true"';
  const map = {
    calc:`<svg ${common}><rect x="14" y="8" width="36" height="48" rx="8" fill="url(#g)"/><path d="M22 19h20M23 31h4m8 0h4m8 0h4M23 42h4m8 0h4m8 0h4" stroke="#fff" stroke-width="4" stroke-linecap="round"/><defs><linearGradient id="g" x1="10" y1="8" x2="54" y2="56"><stop stop-color="#6ee7ff"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs></svg>`,
    code:`<svg ${common}><rect x="8" y="12" width="48" height="40" rx="10" fill="url(#g)"/><path d="M26 25l-7 7 7 7m12-14l7 7-7 7" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><defs><linearGradient id="g" x1="8" y1="12" x2="56" y2="52"><stop stop-color="#38d996"/><stop offset="1" stop-color="#6ee7ff"/></linearGradient></defs></svg>`,
    shield:`<svg ${common}><path d="M32 6l22 8v17c0 14-9 23-22 28C19 54 10 45 10 31V14z" fill="url(#g)"/><path d="M23 33l6 6 13-16" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><defs><linearGradient id="g" x1="10" y1="6" x2="54" y2="59"><stop stop-color="#ff5470"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs></svg>`,
    people:`<svg ${common}><circle cx="25" cy="24" r="9" fill="#6ee7ff"/><circle cx="42" cy="27" r="7" fill="#8b5cf6"/><path d="M10 53c3-12 11-18 22-18s19 6 22 18" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>`,
    layout:`<svg ${common}><rect x="9" y="10" width="46" height="44" rx="9" fill="url(#g)"/><path d="M18 22h28M18 33h12m8 0h8M18 44h28" stroke="#fff" stroke-width="4" stroke-linecap="round"/><defs><linearGradient id="g" x1="9" y1="10" x2="55" y2="54"><stop stop-color="#ffc857"/><stop offset="1" stop-color="#6ee7ff"/></linearGradient></defs></svg>`,
    book:`<svg ${common}><path d="M14 11h25a8 8 0 018 8v34H21a7 7 0 01-7-7z" fill="url(#g)"/><path d="M22 22h16M22 32h19" stroke="#fff" stroke-width="4" stroke-linecap="round"/><defs><linearGradient id="g" x1="14" y1="11" x2="47" y2="53"><stop stop-color="#8b5cf6"/><stop offset="1" stop-color="#38d996"/></linearGradient></defs></svg>`,
    helmet:`<svg ${common}><path d="M13 37a19 19 0 1138 0v8H13z" fill="url(#g)"/><path d="M9 45h46" stroke="#fff" stroke-width="5" stroke-linecap="round"/><defs><linearGradient id="g" x1="13" y1="18" x2="51" y2="45"><stop stop-color="#ffc857"/><stop offset="1" stop-color="#ff5470"/></linearGradient></defs></svg>`,
    chart:`<svg ${common}><rect x="10" y="10" width="44" height="44" rx="10" fill="url(#g)"/><path d="M21 42V30m11 12V21m11 21V27" stroke="#fff" stroke-width="5" stroke-linecap="round"/><defs><linearGradient id="g" x1="10" y1="10" x2="54" y2="54"><stop stop-color="#38d996"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs></svg>`
  };
  return map[name] || map.layout;
};
