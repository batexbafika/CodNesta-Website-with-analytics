document.querySelectorAll('.privacy-section').forEach(section => {
  const navItems = section.querySelectorAll('.privacy-nav .nav-item');
  const panels = section.querySelectorAll('.topic-panel');

  navItems.forEach(button => {
    button.addEventListener('click', () => {
      const targetTopic = button.getAttribute('data-topic');

      // Remove active status within this specific section
      navItems.forEach(btn => btn.classList.remove('active'));
      panels.forEach(panel => panel.classList.remove('active'));

      // Activate clicked tab & corresponding article panel
      button.classList.add('active');
      const targetPanel = section.querySelector(`#${targetTopic}`);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });
});