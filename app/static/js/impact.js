document.addEventListener('DOMContentLoaded', () => {
  const animationDuration = 2000; // Animation duration in milliseconds

  const animateCountDown = (element) => {
    const target = parseInt(element.getAttribute('data-target'), 10);
    // Use data-start if specified, otherwise start from target + 50 (or target * 2)
    const startValue = element.hasAttribute('data-start') 
      ? parseInt(element.getAttribute('data-start'), 10) 
      : target + 50;

    let startTime = null;

    const step = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / animationDuration, 1);
      
      // Quadratic ease-out formula for smooth deceleration
      const easeOutProgress = 1 - Math.pow(1 - progress, 2);
      
      // Calculate current count counting DOWN
      const currentCount = Math.floor(startValue - (easeOutProgress * (startValue - target)));

      element.textContent = currentCount;

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        element.textContent = target; // Ensure exact target number at the end
      }
    };

    requestAnimationFrame(step);
  };

  // IntersectionObserver to trigger animation when scrolled into view
  const observerOptions = {
    threshold: 0.3
  };

  const observer = new IntersectionObserver((entries, observerInstance) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const numberElement = entry.target.querySelector('.stat-number');
        if (numberElement && !numberElement.classList.contains('has-animated')) {
          numberElement.classList.add('has-animated');
          animateCountDown(numberElement);
        }
        observerInstance.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.impact-stat-item').forEach(item => {
    observer.observe(item);
  });
});