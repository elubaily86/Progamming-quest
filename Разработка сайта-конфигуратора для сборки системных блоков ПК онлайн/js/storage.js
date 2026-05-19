window.PCForgeStorage=(function(){
  var key='pcforge_pro_state_v2';
  function load(){try{return JSON.parse(localStorage.getItem(key)||'{}')}catch(e){return {}}}
  function save(state){try{localStorage.setItem(key,JSON.stringify(state))}catch(e){}}
  function clear(){try{localStorage.removeItem(key);localStorage.removeItem('pcforge_pro_theme')}catch(e){}}
  return {load:load,save:save,clear:clear,key:key};
})();
