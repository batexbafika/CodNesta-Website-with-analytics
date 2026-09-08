document.addEventListener('DOMContentLoaded', function () {
  fetchRecentBlogPosts();
});

async function fetchRecentBlogPosts() {
  const apiEndpoint = 'https://blog.codnesta.com/api/v1/recent-posts';
  const gridContainer = document.getElementById('blogPostsGrid');

  try {
    const response = await fetch(apiEndpoint);
    if (!response.ok) throw new Error('API Unavailable');

    const posts = await response.json(); // Expected array of 3 posts

    if (posts && posts.length > 0) {
      // Remove preview style state
      gridContainer.classList.remove('blog-grid-preview');
      gridContainer.innerHTML = ''; // Clear placeholder cards

      posts.slice(0, 3).forEach(post => {
        const postCardHTML = `
          <article class="blog-card">
            <div class="blog-card-media">
              <span class="blog-category-badge">${post.category_name || 'General'}</span>
              <img src="${post.featured_image || 'static/images/blog-default.jpg'}" alt="${post.title}" class="blog-card-img" />
            </div>
            <div class="blog-card-content">
              <div class="blog-meta">
                <span class="blog-date">${post.published_at_formatted}</span>
                <span class="blog-read-time">${post.read_time || '3 min'} read</span>
              </div>
              <h4 class="blog-card-title">${post.title}</h4>
              <p class="blog-card-excerpt">${post.excerpt}</p>
              <div class="blog-card-footer">
                <a href="${post.url}" target="_blank" class="blog-read-more">
                  Read Article <i class="fa-solid fa-arrow-right"></i>
                </a>
              </div>
            </div>
          </article>
        `;
        gridContainer.innerHTML += postCardHTML;
      });
    }
  } catch (error) {
    // Gracefully fallback to showing the "Coming Soon" static layout if API fails or is not ready
    console.log('Blog API currently offline or launching soon.');
  }
}