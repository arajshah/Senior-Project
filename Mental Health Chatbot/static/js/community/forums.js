/**
 * Aurora Community - Forums JavaScript
 * Handles forum searching, post creation, replies, and interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
      AOS.init();
    }
    
    // ----- Forum Search Functionality -----
    const forumSearch = document.getElementById('forum-search');
    if (forumSearch) {
      forumSearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const forumCards = document.querySelectorAll('.forum-card');
        
        forumCards.forEach(card => {
          const title = card.querySelector('h3').textContent.toLowerCase();
          const description = card.querySelector('p').textContent.toLowerCase();
          
          if (title.includes(searchTerm) || description.includes(searchTerm)) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
        
        // Check if all cards are hidden
        const visibleCards = Array.from(forumCards).filter(card => card.style.display !== 'none');
        const emptyState = document.querySelector('.empty-state');
        
        if (visibleCards.length === 0 && !emptyState) {
          const container = document.getElementById('forums-container');
          const newEmptyState = document.createElement('div');
          newEmptyState.className = 'empty-state search-empty';
          newEmptyState.innerHTML = `
            <i class="fas fa-search"></i>
            <p>No forums match your search</p>
            <p class="empty-suggestion">Try different keywords</p>
          `;
          container.appendChild(newEmptyState);
        } else if (visibleCards.length > 0) {
          const searchEmpty = document.querySelector('.search-empty');
          if (searchEmpty) {
            searchEmpty.remove();
          }
        }
      });
    }
    
    // ----- Create Post Form Handling -----
    const createPostBtn = document.getElementById('create-post-btn');
    const createPostForm = document.getElementById('create-post-form');
    const cancelPostBtn = document.getElementById('cancel-post');
    const newPostForm = document.getElementById('new-post-form');
    
    if (createPostBtn && createPostForm) {
      createPostBtn.addEventListener('click', function() {
        createPostForm.style.display = 'block';
        createPostBtn.style.display = 'none';
        
        // Scroll to the form
        createPostForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      
      if (cancelPostBtn) {
        cancelPostBtn.addEventListener('click', function() {
          createPostForm.style.display = 'none';
          createPostBtn.style.display = 'block';
        });
      }
      
      if (newPostForm) {
        newPostForm.addEventListener('submit', function(e) {
          e.preventDefault();
          
          const title = document.getElementById('post-title').value;
          const content = document.getElementById('post-content').value;
          
          // In a real app, we would submit this to the server
          // For demo purposes, we'll create a new post element
          
          const forumPosts = document.querySelector('.forum-posts');
          const emptyState = forumPosts.querySelector('.empty-state');
          
          if (emptyState) {
            emptyState.remove();
          }
          
          const now = new Date();
          const formattedDate = now.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            hour12: true
          });
          
          const newPost = document.createElement('div');
          newPost.className = 'post-card';
          newPost.setAttribute('data-aos', 'fade-up');
          newPost.innerHTML = `
            <div class="post-header">
              <div class="post-metadata">
                <span class="post-author">Posted by You</span>
                <span class="post-date">${formattedDate}</span>
              </div>
              <h3 class="post-title">${title}</h3>
            </div>
            <div class="post-content">
              <p>${content}</p>
            </div>
            <div class="post-actions">
              <button class="reply-btn" data-post-id="new-post">
                <i class="fas fa-reply"></i> Reply (0)
              </button>
            </div>
            <div class="replies-container" id="replies-new-post" style="display: none;">
              <div class="reply-form">
                <form class="new-reply-form" data-post-id="new-post">
                  <textarea placeholder="Write a reply..." required></textarea>
                  <button type="submit">Reply</button>
                </form>
              </div>
            </div>
          `;
          
          forumPosts.insertBefore(newPost, forumPosts.firstChild);
          
          // Reset form and hide it
          newPostForm.reset();
          createPostForm.style.display = 'none';
          createPostBtn.style.display = 'block';
          
          // Initialize the reply button for the new post
          initReplyButtons();
        });
      }
    }
    
    // ----- Reply Functionality -----
    function initReplyButtons() {
      const replyButtons = document.querySelectorAll('.reply-btn');
      
      replyButtons.forEach(btn => {
        // Remove any existing event listeners
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
        
        const postId = newBtn.getAttribute('data-post-id');
        const repliesContainer = document.getElementById(`replies-${postId}`);
        
        newBtn.addEventListener('click', function() {
          if (repliesContainer.style.display === 'none') {
            repliesContainer.style.display = 'block';
          } else {
            repliesContainer.style.display = 'none';
          }
        });
      });
      
      // Handle reply form submissions
      const replyForms = document.querySelectorAll('.new-reply-form');
      
      replyForms.forEach(form => {
        // Remove any existing event listeners
        const newForm = form.cloneNode(true);
        form.parentNode.replaceChild(newForm, form);
        
        newForm.addEventListener('submit', function(e) {
          e.preventDefault();
          
          const postId = this.getAttribute('data-post-id');
          const replyContent = this.querySelector('textarea').value;
          const repliesContainer = document.getElementById(`replies-${postId}`);
          
          // Get current number of replies
          const replyBtn = document.querySelector(`.reply-btn[data-post-id="${postId}"]`);
          const currentReplies = parseInt(replyBtn.textContent.match(/\d+/)[0]);
          
          // In a real app, we would submit this to the server
          // For demo purposes, we'll create a new reply element
          
          const now = new Date();
          const formattedDate = now.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            hour12: true
          });
          
          const newReply = document.createElement('div');
          newReply.className = 'reply';
          newReply.innerHTML = `
            <div class="reply-metadata">
              <span class="reply-author">You</span>
              <span class="reply-date">${formattedDate}</span>
            </div>
            <div class="reply-content">
              <p>${replyContent}</p>
            </div>
          `;
          
          // Insert the new reply before the reply form
          const replyForm = repliesContainer.querySelector('.reply-form');
          repliesContainer.insertBefore(newReply, replyForm);
          
          // Update reply count in button
          replyBtn.innerHTML = `<i class="fas fa-reply"></i> Reply (${currentReplies + 1})`;
          
          // Reset the form
          this.querySelector('textarea').value = '';
        });
      });
    }
    
    // Initialize reply buttons on page load
    initReplyButtons();
  });