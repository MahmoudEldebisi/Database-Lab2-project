// Browser-side checks for the register and login forms.
// The server must repeat every one of these checks.
(function () {
  const form = document.getElementById('auth-form');
  if (!form) return;

  function setError(name, message) {
    const input = form.elements[name];
    const slot = form.querySelector('[data-for="' + name + '"]');
    if (slot) slot.textContent = message || '';
    if (input) input.classList.toggle('invalid', Boolean(message));
  }

  function check() {
    const v = {};
    for (const el of form.elements) if (el.name) v[el.name] = el.value;
    const errors = {};

    if (form.dataset.validate === 'register') {
      if (!v.name.trim()) errors.name = 'Name is required';
      if (!v.email.trim()) errors.email = 'Email is required';
      if (!v.password) errors.password = 'Password is required';
      if (!v.confirm_password) errors.confirm_password = 'Confirm password is required';
      else if (v.password && v.password !== v.confirm_password) errors.confirm_password = 'Passwords do not match';
    } else {
      if (!v.email.trim()) errors.email = 'Email is required';
      if (!v.password) errors.password = 'Password is required';
    }
    return errors;
  }

  form.addEventListener('submit', function (e) {
    const errors = check();
    for (const el of form.elements) if (el.name) setError(el.name, errors[el.name]);
    if (Object.keys(errors).length) e.preventDefault();
  });
})();