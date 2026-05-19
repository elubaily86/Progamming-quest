window.PCForgeApp=(function(){
  var Data=window.PCForgeData, Store=window.PCForgeStorage, Render=window.PCForgeRender, U=window.PCForgeUtils;
  var saved=Store.load();
  var state={selected:saved.selected||{},order:saved.order||Data.parts.map(p=>p.id),budget:saved.budget||500000,query:'',category:'all'};
  function persist(){Store.save({selected:state.selected,order:state.order,budget:state.budget})}
  function update(){persist();Render.renderSummary(state);Render.renderParts(state)}
  function toggle(id){var part=Data.parts.find(p=>p.id===id); if(!part)return; if(state.selected[part.cat]===id){delete state.selected[part.cat]; U.toast(part.name+' убран из сборки')}else{state.selected[part.cat]=id; U.toast(part.name+' добавлен')}; update()}
  function setOrder(ids){var hidden=state.order.filter(id=>!ids.includes(id)); state.order=ids.concat(hidden); persist(); U.toast('Порядок карточек сохранён')}
  function reset(){Store.clear(); state.selected={}; state.order=Data.parts.map(p=>p.id); state.budget=500000; state.query=''; state.category='all'; document.getElementById('searchInput').value=''; document.getElementById('budgetRange').value=state.budget; document.getElementById('categoryFilter').value='all'; document.documentElement.setAttribute('data-theme','dark'); update(); U.toast('Настройки сброшены')}
  function exportJson(){var analysis=Render.analyse(state); var payload={project:'PCForge Pro',date:new Date().toISOString(),budget:state.budget,total:analysis.total,estimatedWatts:analysis.watts,compatibility:analysis.score,issues:analysis.issues,parts:analysis.parts.map(p=>({category:p.cat,name:p.name,price:p.price,watts:p.watts>0?p.watts:0}))}; U.download('pcforge-build.json',JSON.stringify(payload,null,2)); U.toast('JSON экспортирован')}
  function auto(){state.selected={CPU:'cpu-7500f',GPU:'gpu-4060',Motherboard:'mb-b650',RAM:'ram-ddr5',Storage:'ssd-1tb',PSU:'psu-650',Case:'case-air',Cooling:'cooler-tower'}; update(); U.toast('Автосборка Balance применена')}
  function bind(){
    Render.fillCategories();
    document.getElementById('budgetRange').value=state.budget;
    document.getElementById('budgetRange').addEventListener('input',U.debounce(function(e){state.budget=Number(e.target.value)||500000; persist(); Render.renderSummary(state)},80));
    document.getElementById('searchInput').addEventListener('input',U.debounce(function(e){state.query=e.target.value.trim(); Render.renderParts(state)},120));
    document.getElementById('categoryFilter').addEventListener('change',function(e){state.category=e.target.value; Render.renderParts(state)});
    document.getElementById('resetAll').addEventListener('click',reset);
    document.getElementById('exportJson').addEventListener('click',exportJson);
    document.getElementById('autoBuild').addEventListener('click',auto);
    document.getElementById('themeToggle').addEventListener('click',function(){var cur=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark'; document.documentElement.setAttribute('data-theme',cur); try{localStorage.setItem('pcforge_pro_theme',cur)}catch(e){} U.toast(cur==='dark'?'Тёмная тема включена':'Светлая тема включена')});
    window.addEventListener('error',function(){U.toast('Ошибка поймана, интерфейс продолжает работу')});
  }
  document.addEventListener('DOMContentLoaded',function(){bind(); Render.renderSummary(state); Render.renderParts(state)});
  return {toggle:toggle,setOrder:setOrder,reset:reset,state:state};
})();
