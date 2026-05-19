window.PCForgeDrag=(function(){
  var dragged=null;
  function bind(grid){
    if(!grid || grid._dragBound)return; grid._dragBound=true;
    grid.addEventListener('dragstart',function(e){var card=e.target.closest('.part-card'); if(!card)return; dragged=card; card.classList.add('dragging'); e.dataTransfer.effectAllowed='move'; try{e.dataTransfer.setData('text/plain',card.dataset.id)}catch(_){}});
    grid.addEventListener('dragend',function(){if(dragged)dragged.classList.remove('dragging'); dragged=null; saveOrder(grid)});
    grid.addEventListener('dragover',function(e){e.preventDefault(); var after=getAfterElement(grid,e.clientY,e.clientX); if(!dragged)return; if(after==null)grid.appendChild(dragged); else grid.insertBefore(dragged,after)});
  }
  function getAfterElement(container,y,x){
    var els=[...container.querySelectorAll('.part-card:not(.dragging)')];
    return els.reduce((closest,child)=>{var box=child.getBoundingClientRect(); var offset=(y-box.top-box.height/2)+(x-box.left-box.width/2)*0.15; if(offset<0 && offset>closest.offset)return{offset:offset,element:child}; return closest},{offset:Number.NEGATIVE_INFINITY}).element;
  }
  function saveOrder(grid){var ids=[...grid.querySelectorAll('.part-card')].map(c=>c.dataset.id); if(ids.length && window.PCForgeApp){window.PCForgeApp.setOrder(ids)}}
  return {bind:bind};
})();
