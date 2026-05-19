window.Store = {
  get(key, fallback){ try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
  set(key, value){ localStorage.setItem(key, JSON.stringify(value)); },
  remove(key){ localStorage.removeItem(key); },
  clear(){ ['testflow.theme','testflow.order','testflow.builder','testflow.selected','testflow.settings'].forEach(k=>localStorage.removeItem(k)); }
};
