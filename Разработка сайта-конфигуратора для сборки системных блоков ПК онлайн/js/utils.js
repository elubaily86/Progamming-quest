window.PCForgeUtils=(function(){
  function money(n){return new Intl.NumberFormat('ru-KZ').format(Math.max(0,Math.round(n)))+' ₸'}
  function debounce(fn,wait){var t;return function(){var a=arguments;clearTimeout(t);t=setTimeout(()=>fn.apply(this,a),wait)}}
  function throttle(fn,wait){var ok=true,lastArgs=null;return function(){lastArgs=arguments;if(!ok)return;ok=false;fn.apply(this,lastArgs);setTimeout(()=>{ok=true;if(lastArgs){lastArgs=null}},wait)}}
  function toast(text){var el=document.getElementById('toast'); if(!el)return; el.textContent=text; el.classList.add('show'); clearTimeout(el._t); el._t=setTimeout(()=>el.classList.remove('show'),2600)}
  function escapeReg(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}
  function mark(text,q){if(!q)return text; var r=new RegExp('('+escapeReg(q)+')','ig'); return String(text).replace(r,'<mark class="highlight">$1</mark>')}
  function download(name,content,type){var blob=new Blob([content],{type:type||'application/json'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
  return {money:money,debounce:debounce,throttle:throttle,toast:toast,mark:mark,download:download};
})();
