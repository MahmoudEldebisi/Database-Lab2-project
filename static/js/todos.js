
(function () {
  document.querySelectorAll('form[data-validate="title"]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      const input = form.elements.title;
      const slot = form.querySelector('[data-for="title"]');
      const title = input.value.trim();
      let message = '';
      if (!title) message = 'Title is required';
      else if (title.length > 200) message = 'Title is too long (200 characters at most)';
      if (slot) slot.textContent = message;
      input.classList.toggle('invalid', Boolean(message));
      if (message) e.preventDefault();
    });
  });

  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.confirm(form.dataset.confirm)) e.preventDefault();
    });
  });
})();
