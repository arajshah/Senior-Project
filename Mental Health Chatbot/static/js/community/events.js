/**
 * Aurora Community - Events JavaScript
 * Handles event searching, filtering, registration, and calendar functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
      AOS.init();
    }
    
    // ----- Event Search Functionality -----
    const eventSearch = document.getElementById('event-search');
    if (eventSearch) {
      eventSearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterEvents(searchTerm, null);
      });
    }
    
    // ----- Event Filter Functionality -----
    const eventFilter = document.getElementById('event-filter');
    if (eventFilter) {
      eventFilter.addEventListener('change', function() {
        const filterValue = this.value;
        const searchTerm = eventSearch ? eventSearch.value.toLowerCase() : '';
        filterEvents(searchTerm, filterValue);
      });
    }
    
    /**
     * Filter event cards based on search term and/or filter
     */
    function filterEvents(searchTerm, filterValue) {
      // Apply to both upcoming and past events
      filterEventSection('upcoming-events-container', searchTerm, filterValue);
      filterEventSection('past-events-container', searchTerm, filterValue);
    }
    
    function filterEventSection(containerId, searchTerm, filterValue) {
      const container = document.getElementById(containerId);
      if (!container) return;
      
      const eventCards = container.querySelectorAll('.event-card');
      
      eventCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('.event-description') ? 
                          card.querySelector('.event-description').textContent.toLowerCase() : '';
        
        // Check if the card matches the search term
        const matchesSearch = !searchTerm || 
                            title.includes(searchTerm) || 
                            description.includes(searchTerm);
        
        // Check if the card matches the filter
        // In a real app, we'd have category data for each event
        // For demo purposes, we'll just check if title/description contains the filter value
        const matchesFilter = !filterValue || 
                            filterValue === 'all' || 
                            title.includes(filterValue.toLowerCase()) ||
                            description.includes(filterValue.toLowerCase());
        
        if (matchesSearch && matchesFilter) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
      
      // Check if all cards are hidden
      const visibleCards = Array.from(eventCards).filter(card => card.style.display !== 'none');
      let emptyState = container.querySelector('.empty-state');
      
      if (visibleCards.length === 0) {
        // Remove existing search-empty if it exists
        const existingEmpty = container.querySelector('.search-empty');
        if (existingEmpty) {
          existingEmpty.remove();
        }
        
        // If there's a natural empty state (no events at all), don't add a search empty
        if (!emptyState) {
          const newEmptyState = document.createElement('div');
          newEmptyState.className = 'empty-state search-empty';
          newEmptyState.innerHTML = `
            <i class="fas fa-search"></i>
            <p>No events match your criteria</p>
            <p class="empty-suggestion">Try different keywords or filters</p>
          `;
          container.appendChild(newEmptyState);
        }
      } else {
        const searchEmpty = container.querySelector('.search-empty');
        if (searchEmpty) {
          searchEmpty.remove();
        }
      }
    }
    
    // ----- Register for Event Functionality -----
    const registerBtn = document.getElementById('register-event-btn');
    const unregisterBtn = document.getElementById('unregister-event-btn');
    
    if (registerBtn) {
      registerBtn.addEventListener('click', function() {
        // In a real app, this would send a request to the server
        // For demo purposes, we'll just toggle the button visibility
        
        const eventId = this.getAttribute('data-event-id');
        const attendeesCount = document.querySelector('.attendees-count');
        
        if (attendeesCount) {
          const currentAttendees = parseInt(attendeesCount.textContent.split('(')[1]);
          attendeesCount.textContent = `Attendees (${currentAttendees + 1})`;
        }
        
        // Hide register button, show unregister button
        registerBtn.style.display = 'none';
        unregisterBtn.style.display = 'inline-flex';
        
        // Show success message
        showNotification('You have registered for this event!', 'success');
        
        // In a real app, we would also add the user to the attendees list
        const attendeesList = document.querySelector('.attendees-list');
        if (attendeesList) {
          const newAttendee = document.createElement('div');
          newAttendee.className = 'attendee-item';
          newAttendee.innerHTML = `
            <div class="attendee-avatar">
              Y
            </div>
            <div class="attendee-name">
              You
            </div>
          `;
          attendeesList.appendChild(newAttendee);
        }
      });
    }
    
    if (unregisterBtn) {
      unregisterBtn.addEventListener('click', function() {
        // In a real app, this would send a request to the server
        // For demo purposes, we'll just toggle the button visibility
        
        const eventId = this.getAttribute('data-event-id');
        const attendeesCount = document.querySelector('.attendees-count');
        
        if (attendeesCount) {
          const currentAttendees = parseInt(attendeesCount.textContent.split('(')[1]);
          attendeesCount.textContent = `Attendees (${currentAttendees - 1})`;
        }
        
        // Hide unregister button, show register button
        unregisterBtn.style.display = 'none';
        registerBtn.style.display = 'inline-flex';
        
        // Show message
        showNotification('You have unregistered from this event', 'info');
        
        // In a real app, we would also remove the user from the attendees list
        const attendeeItem = document.querySelector('.attendee-name:contains("You")');
        if (attendeeItem) {
          attendeeItem.closest('.attendee-item').remove();
        }
      });
    }
    
    // ----- Add to Calendar Functionality -----
    const addToCalendarBtn = document.getElementById('add-to-calendar-btn');
    
    if (addToCalendarBtn) {
      addToCalendarBtn.addEventListener('click', function() {
        // In a real app, this would generate calendar files or links
        // For demo purposes, we'll just show a notification
        
        showNotification('Event added to your calendar!', 'success');
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