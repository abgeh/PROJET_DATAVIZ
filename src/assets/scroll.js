// Utilisation d'Intersection Observer pour révéler les sections
document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.viz-section');
  const options = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15  // déclenchement dès que 15% de la section est visible
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        obs.unobserve(entry.target);  // on n'a besoin que d'une seule révélation
      }
    });
  }, options);

  sections.forEach(sec => observer.observe(sec));
});
