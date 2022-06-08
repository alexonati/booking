link.addEventListener('click', function (event) {
  if (this.parentElement.classList.contains('readonly')) {
    event.preventDefault();
  }
});