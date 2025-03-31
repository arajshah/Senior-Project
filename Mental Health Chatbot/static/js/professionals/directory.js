/**
 * Aurora Professional Help - Directory JavaScript
 * Handles professional directory searching and filtering
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
      AOS.init();
    }
    
    // ----- Professional Search Functionality -----
    const professionalSearch = document.getElementById('professional-search');
    if (professionalSearch) {
      professionalSearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterProfessionals(searchTerm, null);
      });
    }
    
    // ----- Specialty Filter Functionality -----
    const specialtyFilter = document.getElementById('specialty-filter');
    if (specialtyFilter) {
      specialtyFilter.addEventListener('change', function() {
        const filterValue = this.value;
        const searchTerm = professionalSearch ? professionalSearch.value.toLowerCase() : '';
        filterProfessionals(searchTerm, filterValue);
      });
    }
    
    /**
     * Filter professional cards based on search term and/or specialty filter
     */
    function filterProfessionals(searchTerm, filterValue) {
      const professionalCards = document.querySelectorAll('.professional-card');
      
      professionalCards.forEach(card => {
        const name = card.querySelector('h3').textContent.toLowerCase();
        const bio = card.querySelector('.professional-bio').textContent.toLowerCase();
        const specialties = Array.from(card.querySelectorAll('.specialty-tag'))
                              .map(tag => tag.textContent.toLowerCase());
        
        // Check if the card matches the search term
        const matchesSearch = !searchTerm || 
                            name.includes(searchTerm) || 
                            bio.includes(searchTerm) ||
                            specialties.some(specialty => specialty.includes(searchTerm));
        
        // Check if the card matches the filter
        const matchesFilter = !filterValue || 
                            filterValue === 'all' || 
                            specialties.some(specialty => specialty.includes(filterValue.toLowerCase()));
        
        if (matchesSearch && matchesFilter) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
      
      // Check if all cards are hidden
      const visibleCards = Array.from(professionalCards).filter(card => card.style.display !== 'none');
      const emptyState = document.querySelector('.empty-state');
      const professionalContainer = document.getElementById('professionals-container');
      
      if (visibleCards.length === 0 && !emptyState) {
        const newEmptyState = document.createElement('div');
        newEmptyState.className = 'empty-state search-empty';
        newEmptyState.innerHTML = `
          <i class="fas fa-search"></i>
          <p>No professionals match your criteria</p>
          <p class="empty-suggestion">Try different keywords or filters</p>
        `;
        professionalContainer.appendChild(newEmptyState);
      } else if (visibleCards.length > 0 && document.querySelector('.search-empty')) {
        document.querySelector('.search-empty').remove();
      }
    }
    
    // Initialize tooltips or popovers if needed
    const infoIcons = document.querySelectorAll('.info-icon');
    infoIcons.forEach(icon => {
      icon.addEventListener('mouseenter', function() {
        // Show tooltip logic
        const tooltip = this.querySelector('.tooltip');
        if (tooltip) tooltip.style.display = 'block';
      });
      
      icon.addEventListener('mouseleave', function() {
        // Hide tooltip logic
        const tooltip = this.querySelector('.tooltip');
        if (tooltip) tooltip.style.display = 'none';
      });
    });
  });