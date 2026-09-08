document.addEventListener('DOMContentLoaded', () => {
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -50px 0px', // Triggers 50px before element enters viewport
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target); // Runs animation once per page load
      }
    });
  }, observerOptions);

  // Target all elements set to animate on scroll
  const animatedElements = document.querySelectorAll('.reveal-on-scroll');
  animatedElements.forEach(el => observer.observe(el));
});