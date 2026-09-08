document.addEventListener('DOMContentLoaded', () => {
  const animatedElements = document.querySelectorAll('.animate-on-scroll');

  if (!animatedElements.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -50px 0px', // Triggers 50px before entering viewport
    threshold: 0.05 // Lower threshold so larger elements trigger easily
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target); // Stop observing once animated
      }
    });
  }, observerOptions);

  animatedElements.forEach((el) => {
    // Immediate check if element is already inside the viewport on page load
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom >= 0) {
      el.classList.add('is-visible');
    } else {
      observer.observe(el);
    }
  });
});