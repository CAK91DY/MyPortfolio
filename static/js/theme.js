/* =======================================
   🌙 DataCraft Studio - Theme + Animation
   Gestion du thème et animation DataLines
========================================= */
(function() {
  const root = document.documentElement;
  const key = 'dc-theme';

  // 🌓 Restaure le thème sauvegardé
  const saved = localStorage.getItem(key);
  if (saved) root.setAttribute('data-theme', saved);

  // 🔄 Bouton de bascule (dark / light)
  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('[data-toggle-theme]');
    if(!btn) return;
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem(key, next);
  });

  // 💡 Animation "dataLines"
  document.addEventListener('DOMContentLoaded', ()=>{
    if (!window.gsap) return;
    const lines = document.querySelectorAll("#dataLines .data-line");
    if (!lines.length) return;

    // animation continue d'opacité et largeur (effet de flux)
    gsap.to(lines, {
      opacity: .9,
      scaleX: ()=> gsap.utils.random(0.3, 1),
      duration: .8,
      stagger: .1,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    });
  });
})();




