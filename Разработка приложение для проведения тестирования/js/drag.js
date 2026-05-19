window.makeSortable = (container, storageKey, onUpdate) => {
  let dragged = null;
  const save = () => {
    const ids = $$('.drag-item', container).map(el => el.dataset.id);
    Store.set(storageKey, ids);
    if (onUpdate) onUpdate(ids);
  };
  container.addEventListener('dragstart', e => {
    const item = e.target.closest('.drag-item'); if (!item) return;
    dragged = item; item.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move';
  });
  container.addEventListener('dragend', () => { if (dragged) dragged.classList.remove('dragging'); dragged = null; save(); toast('Порядок сохранён'); });
  container.addEventListener('dragover', throttle(e => {
    e.preventDefault(); if (!dragged) return;
    const after = getAfterElement(container, e.clientY);
    if (after == null) container.appendChild(dragged); else container.insertBefore(dragged, after);
  }, 60));
};
function getAfterElement(container, y){
  const els = [...container.querySelectorAll('.drag-item:not(.dragging)')];
  return els.reduce((closest, child) => {
    const box = child.getBoundingClientRect(); const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) return {offset, element: child};
    return closest;
  }, {offset: Number.NEGATIVE_INFINITY}).element;
}
