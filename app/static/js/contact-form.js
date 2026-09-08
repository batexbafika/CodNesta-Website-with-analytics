// Role-to-Inquiry option selector helper
function switchCtaRole(role) {
  const buttons = document.querySelectorAll('.cta-option-btn');
  buttons.forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-role') === role);
  });

  const select = document.getElementById('inquiryType');
  if (!select) return;

  const roleDefaults = {
    business: 'software_consulting',
    network: 'start_partnership',
    talent: 'predev_academy',
    feedback: 'send_feedback'
  };

  if (roleDefaults[role]) {
    select.value = roleDefaults[role];
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('ctaContactForm');
  if (!form) return;

  const statusMsg = document.getElementById('formStatus');
  const submitBtn = form.querySelector('.cta-submit-btn');

  function showStatus(text, isError = false) {
    if (!statusMsg) return;
    statusMsg.style.display = 'block';
    statusMsg.style.color = isError ? '#ef4444' : '#10b981';
    statusMsg.textContent = text;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (statusMsg) statusMsg.style.display = 'none';

    const name = form.querySelector('#contactName').value.trim();
    const email = form.querySelector('#contactEmail').value.trim();
    const inquiryType = form.querySelector('#inquiryType').value;
    const message = form.querySelector('#contactMessage').value.trim();

    // Client-side Validation
    if (!name || !email || !inquiryType || !message) {
      showStatus('Please fill out all required fields.', true);
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      showStatus('Please enter a valid email address.', true);
      return;
    }

    // Disable button during network request
    submitBtn.disabled = true;
    const btnSpan = submitBtn.querySelector('span');
    const originalText = btnSpan ? btnSpan.textContent : 'Send Message';
    if (btnSpan) btnSpan.textContent = 'Sending...';

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
          name: name,
          email: email,
          inquiry_type: inquiryType,
          message: message
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showStatus(data.message, false);
        form.reset();
      } else {
        showStatus(data.error || 'Failed to send message. Please try again.', true);
      }
    } catch (err) {
      showStatus('Network error. Please check your connection and try again.', true);
    } finally {
      submitBtn.disabled = false;
      if (btnSpan) btnSpan.textContent = originalText;
    }
  });
});