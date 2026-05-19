window.PCForgeRender=(function(){
  var D=window.PCForgeData, U=window.PCForgeUtils;
  function getSelectedParts(state){return Object.values(state.selected).map(id=>D.parts.find(p=>p.id===id)).filter(Boolean)}
  function card(part,state,index){
    var selected=state.selected[part.cat]===part.id;
    var q=state.query||'';
    var el=document.createElement('article');
    el.className='part-card'; el.draggable=true; el.tabIndex=0; el.dataset.id=part.id; el.style.setProperty('--i',index);
    el.setAttribute('aria-label',part.name+'. '+part.desc);
    el.innerHTML='<div class="part-media"><img loading="lazy" decoding="async" alt="'+part.name.replace(/"/g,'&quot;')+'" data-src="'+part.img+'"></div><div class="part-body"><div class="part-top"><span class="badge">'+part.cat+' · '+part.tag+'</span><button class="icon-button select-btn '+(selected?'is-selected':'')+'" type="button" aria-label="'+(selected?'Убрать':'Выбрать')+' '+part.name+'">'+(selected?'✓':'+')+'</button></div><h3>'+U.mark(part.name,q)+'</h3><p>'+U.mark(part.desc,q)+'</p><dl class="specs">'+Object.entries(part.specs).map(([k,v])=>'<div><dt>'+k+'</dt><dd>'+v+'</dd></div>').join('')+'</dl><div class="part-footer"><strong class="price">'+U.money(part.price)+'</strong><small class="watts">'+(part.watts<0?part.capacity+'W запас':part.watts+'W')+'</small></div></div>';
    el.querySelector('.select-btn').addEventListener('click',function(e){e.stopPropagation();window.PCForgeApp.toggle(part.id)});
    el.addEventListener('dblclick',()=>window.PCForgeApp.toggle(part.id));
    el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();window.PCForgeApp.toggle(part.id)}});
    var img=el.querySelector('img'); img.addEventListener('load',()=>img.parentElement.classList.add('loaded')); img.addEventListener('error',()=>{img.parentElement.classList.add('loaded'); img.alt='Изображение недоступно';}); img.src=img.dataset.src;
    return el;
  }
  function renderParts(state){
    var grid=document.getElementById('partsGrid'); var loading=document.getElementById('loading');
    if(!grid)return; loading&&loading.classList.add('is-visible');
    setTimeout(function(){
      var q=(state.query||'').toLowerCase(); var cat=state.category||'all';
      var ordered=(state.order&&state.order.length?state.order:D.parts.map(p=>p.id)).map(id=>D.parts.find(p=>p.id===id)).filter(Boolean);
      D.parts.forEach(p=>{if(!ordered.find(x=>x.id===p.id)) ordered.push(p)});
      var filtered=ordered.filter(p=>(cat==='all'||p.cat===cat)&&(!q||(p.name+p.desc+p.cat+p.tag+JSON.stringify(p.specs)).toLowerCase().includes(q)));
      grid.innerHTML=''; filtered.forEach((p,i)=>grid.appendChild(card(p,state,i)));
      if(!filtered.length){grid.innerHTML='<div class="stat-card" style="grid-column:1/-1"><strong>Ничего не найдено</strong><p style="color:var(--muted)">Попробуй RTX, Ryzen, DDR5, SSD или сбрось фильтр.</p></div>'}
      window.PCForgeDrag && window.PCForgeDrag.bind(grid);
      loading&&loading.classList.remove('is-visible');
    },180);
  }
  function analyse(state){
    var parts=getSelectedParts(state), total=parts.reduce((s,p)=>s+p.price,0), watts=parts.reduce((s,p)=>s+(p.watts>0?p.watts:0),0);
    var psu=parts.find(p=>p.cat==='PSU'), cpu=parts.find(p=>p.cat==='CPU'), mb=parts.find(p=>p.cat==='Motherboard'), ram=parts.find(p=>p.cat==='RAM'), gpu=parts.find(p=>p.cat==='GPU');
    var issues=[]; var score=45;
    if(parts.length) score+=Math.min(25,parts.length*3);
    if(cpu&&mb){ if(cpu.socket===mb.socket){score+=18}else{issues.push('Сокет CPU и материнской платы не совпадает.');score-=25} }
    if(ram&&mb){ if(mb.ram.includes(ram.ram)){score+=10}else{issues.push('Тип памяти '+ram.ram+' не подходит к плате '+mb.ram+'.');score-=22} }
    if(psu){ var need=Math.ceil((watts*1.45+80)/50)*50; if(psu.capacity>=need){score+=12}else{issues.push('БП слабоват: желательно минимум '+need+'W.');score-=18} }
    if(gpu&&cpu){ var ratio=gpu.score/cpu.score; if(ratio>1.22) issues.push('Видеокарта заметно сильнее CPU: возможен CPU bottleneck в некоторых играх.'); }
    score=Math.max(0,Math.min(100,Math.round(score)));
    var balance=parts.length?Math.round(parts.reduce((s,p)=>s+p.score,0)/parts.length):0;
    return {parts,total,watts,psu,cpu,mb,ram,gpu,issues,score,balance};
  }
  function renderSummary(state){
    var a=analyse(state), U=window.PCForgeUtils;
    document.getElementById('totalPrice').textContent=U.money(a.total);
    document.getElementById('totalWatts').textContent=a.watts+' W';
    document.getElementById('compatScore').textContent=a.score+'%';
    document.getElementById('balanceScore').textContent=a.balance? a.balance+'/100':'—';
    document.getElementById('budgetHint').textContent=a.total===0?'Пока ничего не выбрано':(a.total<=state.budget?'В бюджете: запас '+U.money(state.budget-a.total):'Превышение: '+U.money(a.total-state.budget));
    var recommended=Math.ceil((a.watts*1.45+80)/50)*50; document.getElementById('psuHint').textContent=a.watts?('Рекомендованный БП: '+recommended+'W'):'БП будет рассчитан автоматически';
    document.getElementById('compatHint').textContent=a.issues[0]|| (a.parts.length?'Критических проблем не найдено':'Выбери комплектующие');
    document.getElementById('compatText').textContent=a.issues.length?a.issues.join(' '): (a.parts.length?'Сборка выглядит согласованной. Проверь реальные габариты корпуса и длину видеокарты перед покупкой.':'Добавь процессор, видеокарту, плату и блок питания — появится детальная проверка.');
    document.getElementById('compatMeter').style.width=a.score+'%';
    document.getElementById('riskBadge').textContent=a.issues.length?'есть риски':(a.parts.length?'OK':'ожидание');
    document.getElementById('riskBadge').style.color=a.issues.length?'var(--warn)':'var(--ok)';
    document.getElementById('heroCpu').textContent=a.cpu?a.cpu.name.replace('AMD ','').replace('Intel ',''):'—';
    document.getElementById('heroPsu').textContent=a.psu?a.psu.capacity+' W':'— W';
    var list=document.getElementById('chosenList'); list.innerHTML='';
    a.parts.forEach(p=>{var li=document.createElement('li');li.innerHTML='<div><b>'+p.cat+'</b><span>'+p.name+'</span></div><strong>'+U.money(p.price)+'</strong>';list.appendChild(li)});
    if(!a.parts.length){list.innerHTML='<li><div><b>Сборка пустая</b><span>Нажми + на карточках комплектующих</span></div></li>'}
    document.getElementById('chosenCount').textContent=a.parts.length+'/8';
    document.getElementById('budgetOut').textContent=U.money(state.budget);
    return a;
  }
  function fillCategories(){var s=document.getElementById('categoryFilter'); if(!s)return; D.categories.forEach(c=>{var o=document.createElement('option');o.value=c;o.textContent=c;s.appendChild(o)})}
  return {renderParts:renderParts,renderSummary:renderSummary,analyse:analyse,fillCategories:fillCategories};
})();
