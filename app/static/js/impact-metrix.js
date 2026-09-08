document.addEventListener('DOMContentLoaded', () => {
  const animationDuration = 1800; // Animation duration in milliseconds

  const animateCounter = (element) => {
    const target = parseInt(element.getAttribute('data-target'), 10);
    let startTime = null;

    const step = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / animationDuration, 1);
      
      // Smooth quadratic ease-out slowing down at the finish
      const easeOutProgress = 1 - Math.pow(1 - progress, 2);
      const currentCount = Math.floor(easeOutProgress * target);

      element.textContent = currentCount;

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        element.textContent = target; // Guarantees exact target end-value
      }
    };

    requestAnimationFrame(step);
  };

  // IntersectionObserver to trigger animation when scrolled into view
  const observerOptions = {
    threshold: 0.2
  };

  const observer = new IntersectionObserver((entries, observerInstance) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const numberElement = entry.target.querySelector('.metric-number');
        if (numberElement && !numberElement.classList.contains('has-animated')) {
          numberElement.classList.add('has-animated');
          animateCounter(numberElement);
        }
        observerInstance.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.metric-card').forEach(card => {
    observer.observe(card);
  });
});