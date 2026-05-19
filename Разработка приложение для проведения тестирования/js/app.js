(() => {
  const data = window.TESTFLOW_DATA;
  let selected = Store.get('testflow.selected', []);
  let questionIndex = 0;
  let answers = Store.get('testflow.answers', {});

  const state = {
    search:'', category:'all',
    order: Store.get('testflow.order', data.tests.map(x=>x.id)),
    builderOrder: Store.get('testflow.builder', data.builder.map(x=>x.id)),
    settings: Store.get('testflow.settings', {duration:45, passScore:70, shuffle:true, antiCheat:true, instantResult:false})
  };

  document.addEventListener('DOMContentLoaded', init);
  function init(){
    bindTopbar(); renderTests(); renderBuilder(); renderQuestion(); bindSettings(); observeCards();
    makeSortable($('#testGrid'), 'testflow.order', ids => state.order = ids);
    makeSortable($('#builderList'), 'testflow.builder', ids => state.builderOrder = ids);
  }
  function bindTopbar(){
    $('#themeToggle').addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next; localStorage.setItem('testflow.theme', next); toast('Тема переключена');
    });
    $('#resetAll').addEventListener('click', () => { Store.clear(); localStorage.removeItem('testflow.answers'); toast('Настройки сброшены'); setTimeout(()=>location.reload(), 450); });
    $('#newTestBtn').addEventListener('click', () => { document.getElementById('constructor').scrollIntoView({behavior:'smooth'}); toast('Открыл конструктор теста'); });
    $('#startDemo').addEventListener('click', () => { document.getElementById('hero').scrollIntoView({behavior:'smooth'}); toast('Демо-тест готов'); });
    $('#exportState').addEventListener('click', exportState);
    $('#searchInput').addEventListener('input', debounce(e => { state.search = e.target.value.trim().toLowerCase(); renderTests(); }, 120));
    $('#categoryFilter').addEventListener('change', e => { state.category = e.target.value; renderTests(); });
    $('#nextQuestion').addEventListener('click', () => { questionIndex = Math.min(data.demoQuestions.length - 1, questionIndex + 1); renderQuestion(); });
    $('#prevQuestion').addEventListener('click', () => { questionIndex = Math.max(0, questionIndex - 1); renderQuestion(); });
  }
  function orderedTests(){
    const map = new Map(data.tests.map(x=>[x.id,x]));
    return state.order.map(id=>map.get(id)).filter(Boolean).concat(data.tests.filter(x=>!state.order.includes(x.id)));
  }
  function renderTests(){
    showLoader(true); setTimeout(()=>{
      const grid = $('#testGrid'); const q = state.search;
      const list = orderedTests().filter(t => (state.category === 'all' || t.category === state.category) && (!q || `${t.title} ${t.desc} ${t.level}`.toLowerCase().includes(q)));
      grid.innerHTML = list.length ? list.map((t,i)=>cardHtml(t,q,i)).join('') : '<div class="empty">Ничего не найдено. Попробуй другой запрос или категорию.</div>';
      $$('.select-test', grid).forEach(btn => btn.addEventListener('click', () => toggleTest(btn.dataset.id)));
      showLoader(false); observeCards();
    }, 180);
  }
  function cardHtml(t,q,i){
    const isSelected = selected.includes(t.id);
    const title = mark(t.title,q); const desc = mark(t.desc,q);
    return `<article class="card drag-item reveal" draggable="true" data-id="${t.id}" style="animation-delay:${i*45}ms" tabindex="0" aria-label="${t.title}">
      <div class="thumb" data-lazy="true">${iconSvg(t.icon)}</div>
      <div class="card-body"><span class="badge">${label(t.category)} • ${t.level}</span><h3>${title}</h3><p>${desc}</p>
      <p><b>${t.questions}</b> вопросов • <b>${t.time}</b> мин • средний балл <b>${t.score}%</b></p>
      <div class="card-actions"><button class="ghost" type="button">Подробнее</button><button class="primary select-test" data-id="${t.id}" type="button">${isSelected?'Выбрано':'Выбрать'}</button></div></div>
    </article>`;
  }
  function mark(text,q){ if(!q) return text; return text.replace(new RegExp(`(${escapeReg(q)})`,'ig'), '<mark class="highlight">$1</mark>'); }
  function escapeReg(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function label(c){ return {school:'Школа',it:'IT',hr:'HR',security:'Безопасность'}[c] || c; }
  function toggleTest(id){ selected = selected.includes(id) ? selected.filter(x=>x!==id) : [...selected,id]; Store.set('testflow.selected', selected); $('#metricTests').textContent = selected.length || data.tests.length; renderTests(); toast(selected.includes(id)?'Тест добавлен':'Тест убран'); }

  function renderBuilder(){
    const map = new Map(data.builder.map(x=>[x.id,x]));
    $('#builderList').innerHTML = state.builderOrder.map(id=>map.get(id)).filter(Boolean).map((b,i)=>`<div class="builder-item drag-item" draggable="true" data-id="${b.id}" tabindex="0"><span class="handle" aria-hidden="true">☷</span><div><strong>${i+1}. ${b.title}</strong><p>${b.desc}</p></div><span>↕</span></div>`).join('');
  }
  function bindSettings(){
    const s = state.settings;
    ['duration','passScore','shuffle','antiCheat','instantResult'].forEach(id => {
      const el = $('#'+id); if (!el) return;
      if (el.type === 'checkbox') el.checked = !!s[id]; else el.value = s[id];
      el.addEventListener('input', () => { updateSettings(); });
    });
    updateSettings(false);
  }
  function updateSettings(save=true){
    state.settings = { duration:+$('#duration').value, passScore:+$('#passScore').value, shuffle:$('#shuffle').checked, antiCheat:$('#antiCheat').checked, instantResult:$('#instantResult').checked };
    $('#durationValue').textContent = state.settings.duration;
    $('#passScoreValue').textContent = state.settings.passScore + '%';
    if (save) { Store.set('testflow.settings', state.settings); toast('Параметры сохранены'); }
  }
  function renderQuestion(){
    const q = data.demoQuestions[questionIndex];
    $('#questionTitle').textContent = q.q;
    $('#progressBar').style.width = `${((questionIndex+1)/data.demoQuestions.length)*100}%`;
    $('#answers').innerHTML = q.a.map((txt,i)=>`<button class="answer" role="radio" aria-checked="${answers[questionIndex]===i}" data-i="${i}" type="button"><span>${String.fromCharCode(65+i)}</span>${txt}</button>`).join('');
    $$('.answer').forEach(btn=>btn.addEventListener('click',()=>{ answers[questionIndex]=+btn.dataset.i; Store.set('testflow.answers',answers); renderQuestion(); }));
  }
  function exportState(){
    const payload = { exportedAt:new Date().toISOString(), selected, settings:state.settings, order:state.order, builderOrder:state.builderOrder, demoAnswers:answers };
    const blob = new Blob([JSON.stringify(payload,null,2)], {type:'application/json'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'testflow-state.json'; a.click(); URL.revokeObjectURL(a.href); toast('JSON экспортирован');
  }
  function observeCards(){
    const obs = new IntersectionObserver(entries=>entries.forEach(e=>{ if(e.isIntersecting){ const thumb=e.target.querySelector('.thumb'); if(thumb) setTimeout(()=>thumb.classList.add('loaded'),180); obs.unobserve(e.target); }}),{rootMargin:'80px'});
    $$('.card').forEach(c=>obs.observe(c));
  }
})();
