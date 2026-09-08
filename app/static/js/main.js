document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menuToggle');
  const navMenu = document.getElementById('navMenu');

  if (menuToggle && navMenu) {
    // Function to close the menu and reset attributes
    const closeMenu = () => {
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.classList.remove('is-open');
      navMenu.classList.remove('is-open');
    };

    // Toggle menu and button animation state
    menuToggle.addEventListener('click', () => {
      const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', !isExpanded);
      menuToggle.classList.toggle('is-open');
      navMenu.classList.toggle('is-open');
    });

    // Close mobile menu when any internal navigation link is clicked
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        closeMenu();
      });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !menuToggle.contains(e.target) && navMenu.classList.contains('is-open')) {
        closeMenu();
      }
    });
  }
});


// Whatsapp button Scripts(Scroll to show/hide)
document.addEventListener('DOMContentLoaded', () => {
  const whatsappBtn = document.getElementById('whatsappFloatBtn');

  if (whatsappBtn) {
    whatsappBtn.style.opacity = '0';
    whatsappBtn.style.visibility = 'hidden';
    whatsappBtn.style.transition += ', opacity 0.4s ease, visibility 0.4s ease';

    window.addEventListener('scroll', () => {
      if (window.scrollY > 150) {
        whatsappBtn.style.opacity = '1';
        whatsappBtn.style.visibility = 'visible';
      } else {
        whatsappBtn.style.opacity = '0';
        whatsappBtn.style.visibility = 'hidden';
      }
    });
  }
});


// Cookie Consent Banner Scripts
document.addEventListener('DOMContentLoaded', () => {
  const cookieBanner = document.getElementById('cookieConsentBanner');
  const acceptBtn = document.getElementById('acceptCookiesBtn');
  const rejectBtn = document.getElementById('rejectCookiesBtn');
  const COOKIE_CONSENT_KEY = 'codnesta_cookie_consent';

  const currentConsent = localStorage.getItem(COOKIE_CONSENT_KEY);

  if (!currentConsent) {
    setTimeout(() => {
      if (cookieBanner) cookieBanner.classList.add('is-visible');
    }, 1000);
  } else if (currentConsent === 'accepted') {
    enableAnalytics();
  }

  if (acceptBtn) {
    acceptBtn.addEventListener('click', () => {
      localStorage.setItem(COOKIE_CONSENT_KEY, 'accepted');
      hideBanner();
      enableAnalytics();
    });
  }

  if (rejectBtn) {
    rejectBtn.addEventListener('click', () => {
      localStorage.setItem(COOKIE_CONSENT_KEY, 'rejected');
      hideBanner();
      disableAnalytics();
    });
  }

  function hideBanner() {
    if (cookieBanner) cookieBanner.classList.remove('is-visible');
  }

  function enableAnalytics() {
  if (window.gaInitialized) return;
  window.gaInitialized = true;

  const MEASUREMENT_ID = 'G-4MWEGGMH2H';

  // 1. Inject GA4 script dynamically
  const gaScript = document.createElement('script');
  gaScript.async = true;
  gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}`;
  document.head.appendChild(gaScript);

  // 2. Initialize Data Layer
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', MEASUREMENT_ID);

  console.log(`[Analytics]: Google Analytics 4 (${MEASUREMENT_ID}) initialized.`);
}

  function disableAnalytics() {
    console.log('[Privacy]: Non-essential scripts disabled.');
  }
});