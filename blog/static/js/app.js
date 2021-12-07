const list = document.getElementById('list');
const moreButton = document.getElementById('show-more');
moreButton.addEventListener('click', function () {
  list.classList.toggle('full');
});