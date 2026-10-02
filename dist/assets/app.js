'use strict';
const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');
function closeMenu(restoreFocus = false) {
  navigation.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  if (restoreFocus) menuButton.focus();
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('open', open);
});
navigation.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation.classList.contains('open')) closeMenu(true);
});
document.addEventListener('click', event => {
  if (!event.target.closest('.header')) closeMenu();
});
window.matchMedia('(min-width: 761px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});
const form = document.querySelector('#quote-form');
if (form) {
  const status = document.querySelector('#form-status');
  function requestText() {
    const name = form.elements.name.value.trim();
    const service = form.elements.service.value;
    const message = form.elements.message.value.trim();
    return `Hola, Reformarvel.\n\nMe gustaría solicitar presupuesto para: ${service}.\n${name ? `Mi nombre es ${name}.\n` : ''}\n${message}\n\nGracias.`;
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const target = `mailto:${form.dataset.email}?subject=${encodeURIComponent('Solicitud de presupuesto · Reformarvel')}&body=${encodeURIComponent(requestText())}`;
    status.textContent = 'Solicitud preparada. Revisa el mensaje en tu aplicación de correo y envíalo cuando quieras. La web no lo ha enviado.';
    window.location.href = target;
  });
  document.querySelector('#copy-message').addEventListener('click', async () => {
    if (!form.reportValidity()) return;
    const text = requestText();
    try {
      await navigator.clipboard.writeText(text);
      status.textContent = 'Solicitud copiada. Puedes pegarla en tu correo o en una conversación de Instagram. La web no la ha enviado.';
    } catch {
      status.textContent = 'No se pudo copiar automáticamente. Selecciona y copia este mensaje:\n\n' + text;
    }
  });
}
