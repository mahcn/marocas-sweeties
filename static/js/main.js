document.addEventListener('DOMContentLoaded', () => {
  const btnMenu = document.querySelector('.btn-menu');
  const navMenu = document.querySelector('.nav-menu');

  if (btnMenu && navMenu) {
    btnMenu.addEventListener('click', () => {
      const aberto = navMenu.classList.toggle('ativo');
      btnMenu.classList.toggle('ativo');
      btnMenu.setAttribute('aria-expanded', aberto);
    });
    document.querySelectorAll('.nav-menu a').forEach((link) => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('ativo');
        btnMenu.classList.remove('ativo');
        btnMenu.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const observer = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visivel');
          observer.unobserve(entrada.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  document.querySelectorAll('[data-anim]').forEach((el) => observer.observe(el));

  document.querySelectorAll('[data-whatsapp]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const msg = el.getAttribute('data-whatsapp') || 'Olá, Marocas\'s Sweeties!';
      const number = window.WHATSAPP_NUMBER || '5511999999999';
      window.open(`https://wa.me/${number}?text=${encodeURIComponent(msg)}`, '_blank');
    });
  });

  const form = document.querySelector('.form-contato');
  if (form) {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      const textoOriginal = btn.textContent;
      btn.textContent = 'Enviando...';
      btn.disabled = true;
      setTimeout(() => {
        btn.textContent = textoOriginal;
        btn.disabled = false;
      }, 1200);
    });
  }
});