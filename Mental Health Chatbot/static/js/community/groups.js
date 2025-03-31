/**
 * Aurora Community - Groups JavaScript
 * Handles group searching, filtering, joining/leaving groups
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
      AOS.init();
    }
    
    // ----- Group Search Functionality -----
    const groupSearch = document.getElementById('group-search');
    if (groupSearch) {
      groupSearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterGroups(searchTerm, null);
      });
    }
    
    // ----- Group Filter Functionality -----
    const groupFilter = document.getElementById('group-filter');
    if (groupFilter) {
      groupFilter.addEventListener('change', function() {
        const filterValue = this.value;
        const searchTerm = groupSearch ? groupSearch.value.toLowerCase() : '';
        filterGroups(searchTerm, filterValue);
      });
    }
    
    /**
     * Filter group cards based on search term and/or filter
     */
    function filterGroups(searchTerm, filterValue) {
      const groupCards = document.querySelectorAll('.group-card');
      
      groupCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        
        // Check if the card matches the search term
        const matchesSearch = !searchTerm || 
                            title.includes(searchTerm) || 
                            description.includes(searchTerm);
        
        // Check if the card matches the filter
        // In a real app, we'd have category data for each group
        // For demo purposes, we'll just check if description contains the filter value
        const matchesFilter = !filterValue || 
                            filterValue === 'all' || 
                            description.toLowerCase().includes(filterValue.toLowerCase());
        
        if (matchesSearch && matchesFilter) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
      
      // Check if all cards are hidden
      const visibleCards = Array.from(groupCards).filter(card => card.style.display !== 'none');
      const emptyState = document.querySelector('.empty-state');
      
      if (visibleCards.length === 0 && !emptyState) {
        const container = document.getElementById('groups-container');
        const newEmptyState = document.createElement('div');
        newEmptyState.className = 'empty-state search-empty';
        newEmptyState.innerHTML = `
          <i class="fas fa-search"></i>
          <p>No groups match your criteria</p>
          <p class="empty-suggestion">Try different keywords or filters</p>
        `;
        container.appendChild(newEmptyState);
      } else if (visibleCards.length > 0) {
        const searchEmpty = document.querySelector('.search-empty');
        if (searchEmpty) {
          searchEmpty.remove();
        }
      }
    }
    
    // ----- Join/Leave Group Functionality -----
    const joinGroupBtn = document.getElementById('join-group-btn');
    const leaveGroupBtn = document.getElementById('leave-group-btn');
    
    if (joinGroupBtn) {
      joinGroupBtn.addEventListener('click', function() {
        // In a real app, this would send a request to the server
        // For demo purposes, we'll just toggle the button visibility
        
        const groupId = this.getAttribute('data-group-id');
        const membersCount = document.querySelector('.member-count');
        const currentMembers = parseInt(membersCount.textContent.split('/')[0]);
        const maxMembers = parseInt(membersCount.textContent.split('/')[1]);
        
        if (currentMembers < maxMembers) {
          // Update members count
          membersCount.textContent = `${currentMembers + 1}/${maxMembers}`;
          
          // Hide join button, show leave button
          joinGroupBtn.style.display = 'none';
          leaveGroupBtn.style.display = 'block';
          
          // Show success message
          showNotification('You have joined this group!', 'success');
          
          // In a real app, we would also add the user to the members list
          const membersList = document.querySelector('.members-list');
          if (membersList) {
            const newMember = document.createElement('div');
            newMember.className = 'member-item';
            newMember.innerHTML = `
              <div class="member-avatar">
                Y
              </div>
              <div class="member-name">
                You
              </div>
            `;
            membersList.appendChild(newMember);
          }
        } else {
          showNotification('This group is full', 'error');
        }
      });
    }
    
    if (leaveGroupBtn) {
      leaveGroupBtn.addEventListener('click', function() {
        // In a real app, this would send a request to the server
        // For demo purposes, we'll just toggle the button visibility
        
        const groupId = this.getAttribute('data-group-id');
        const membersCount = document.querySelector('.member-count');
        const currentMembers = parseInt(membersCount.textContent.split('/')[0]);
        const maxMembers = parseInt(membersCount.textContent.split('/')[1]);
        
        // Update members count
        membersCount.textContent = `${currentMembers - 1}/${maxMembers}`;
        
        // Hide leave button, show join button
        leaveGroupBtn.style.display = 'none';
        joinGroupBtn.style.display = 'block';
        
        // Show success message
        showNotification('You have left this group', 'info');
        
        // In a real app, we would also remove the user from the members list
        const memberItem = document.querySelector('.member-name:contains("You")').closest('.member-item');
        if (memberItem) {
          memberItem.remove();
        }
      });
    }
    
    /**
     * Display a notification message
     */
    function showNotification(message, type) {
      const notification = document.createElement('div');
      notification.className = `notification ${type}`;
      notification.innerHTML = `
        <div class="notification-content">
          <i class="fas ${type === 'success' ? 'fa-check-circle' : 
                         type === 'error' ? 'fa-exclamation-circle' : 
                         'fa-info-circle'}"></i>
          <span>${message}</span>
        </div>
      `;
      
      document.body.appendChild(notification);
      
      // Show the notification
      setTimeout(() => {
        notification.classList.add('show');
      }, 10);
      
      // Hide and remove the notification after 3 seconds
      setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
          notification.remove();
        }, 300);
      }, 3000);
    }
  });