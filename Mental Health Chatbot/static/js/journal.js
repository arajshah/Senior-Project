document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const journalForm = document.getElementById('journal-form');
    const titleInput = document.getElementById('title');
    const contentInput = document.getElementById('content');
    const previewTitle = document.getElementById('preview-title');
    const previewContent = document.getElementById('preview-content');
    const entriesContainer = document.getElementById('entries-container');
    const searchInput = document.getElementById('search-entries');
    const sortSelect = document.getElementById('sort-entries');
    const clearFormButton = document.getElementById('clear-form');
    const toggleFormButton = document.getElementById('toggle-form');
    
    // Modal Elements
    const editModal = document.getElementById('edit-modal');
    const deleteModal = document.getElementById('delete-modal');
    const editForm = document.getElementById('edit-form');
    const editId = document.getElementById('edit-id');
    const editTitle = document.getElementById('edit-title');
    const editContent = document.getElementById('edit-content');
    const deleteId = document.getElementById('delete-id');
    const confirmDeleteBtn = document.getElementById('confirm-delete');
    const closeModalButtons = document.querySelectorAll('.close-modal');
    
    // Entry form live preview
    titleInput.addEventListener('input', updatePreview);
    contentInput.addEventListener('input', updatePreview);
    
    function updatePreview() {
        previewTitle.textContent = titleInput.value || 'Your title will appear here';
        previewContent.textContent = contentInput.value || 'Your content will appear here...';
    }
    
    // Clear form
    clearFormButton.addEventListener('click', function() {
        titleInput.value = '';
        contentInput.value = '';
        updatePreview();
    });
    
    // Toggle form visibility
    toggleFormButton.addEventListener('click', function() {
        const formElements = journalForm.querySelectorAll('.form-group, .form-preview, .submit-button');
        const isVisible = formElements[0].style.display !== 'none';
        
        formElements.forEach(el => {
            if (isVisible) {
                el.style.display = 'none';
                toggleFormButton.querySelector('i').className = 'fas fa-chevron-down';
            } else {
                el.style.display = '';
                toggleFormButton.querySelector('i').className = 'fas fa-chevron-up';
            }
        });
    });
    
    // Submit new journal entry
    journalForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        
        if (!title || !content) {
            showNotification('Please fill in all fields', 'error');
            return;
        }
        
        try {
            const response = await fetch('/user/journal/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, content })
            });
            
            if (response.ok) {
                const result = await response.json();
                showNotification('Journal entry saved successfully!');
                
                // Clear form
                titleInput.value = '';
                contentInput.value = '';
                updatePreview();
                
                // Add new entry to the DOM
                if (result.entry) {
                    addEntryToDOM(result.entry, true);
                } else {
                    // Reload if entry data wasn't returned
                    window.location.reload();
                }
            } else {
                const error = await response.json();
                showNotification(error.message || 'Failed to save journal entry', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred while saving your entry', 'error');
        }
    });
    
    // Toggle entry expansion
    document.addEventListener('click', function(e) {
        if (e.target.closest('.toggle-entry')) {
            const entryCard = e.target.closest('.entry-card');
            entryCard.classList.toggle('expanded');
        }
    });
    
    // Edit entry click handler
    document.addEventListener('click', function(e) {
        if (e.target.closest('.edit-entry')) {
            const entryCard = e.target.closest('.entry-card');
            const entryId = entryCard.dataset.id;
            const title = entryCard.querySelector('.entry-title').textContent;
            const content = entryCard.querySelector('.entry-content-full').textContent;
            
            // Populate edit form
            editId.value = entryId;
            editTitle.value = title;
            editContent.value = content;
            
            // Show modal
            editModal.style.display = 'flex';
        }
    });
    
    // Delete entry click handler
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-entry')) {
            const entryCard = e.target.closest('.entry-card');
            const entryId = entryCard.dataset.id;
            
            // Set delete ID
            deleteId.value = entryId;
            
            // Show modal
            deleteModal.style.display = 'flex';
        }
    });
    
    // Close modals
    closeModalButtons.forEach(button => {
        button.addEventListener('click', function() {
            editModal.style.display = 'none';
            deleteModal.style.display = 'none';
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === editModal) {
            editModal.style.display = 'none';
        }
        if (e.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });
    
    // Submit edit form
    editForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const id = editId.value;
        const title = editTitle.value.trim();
        const content = editContent.value.trim();
        
        if (!title || !content) {
            showNotification('Please fill in all fields', 'error');
            return;
        }
        
        try {
            const response = await fetch(`/user/journal/update/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, content })
            });
            
            if (response.ok) {
                showNotification('Journal entry updated successfully!');
                
                // Update entry in DOM
                const entryCard = document.querySelector(`.entry-card[data-id="${id}"]`);
                entryCard.querySelector('.entry-title').textContent = title;
                entryCard.querySelector('.entry-content-preview').textContent = 
                    content.length > 100 ? content.substring(0, 100) + '...' : content;
                entryCard.querySelector('.entry-content-full').textContent = content;
                
                // Close modal
                editModal.style.display = 'none';
            } else {
                const error = await response.json();
                showNotification(error.message || 'Failed to update journal entry', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred while updating your entry', 'error');
        }
    });
    
    // Confirm delete
    confirmDeleteBtn.addEventListener('click', async function() {
        const id = deleteId.value;
        
        try {
            const response = await fetch(`/user/journal/delete/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showNotification('Journal entry deleted successfully!');
                
                // Remove entry from DOM
                const entryCard = document.querySelector(`.entry-card[data-id="${id}"]`);
                entryCard.remove();
                
                // Check if no entries left
                if (entriesContainer.children.length === 0) {
                    entriesContainer.innerHTML = `
                        <div class="no-entries">
                            <i class="fas fa-book-open"></i>
                            <p>Your journal is empty. Start writing your thoughts!</p>
                        </div>
                    `;
                }
                
                // Close modal
                deleteModal.style.display = 'none';
            } else {
                const error = await response.json();
                showNotification(error.message || 'Failed to delete journal entry', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred while deleting your entry', 'error');
        }
    });
    
    // Search entries
    searchInput.addEventListener('input', filterEntries);
    
    // Sort entries
    sortSelect.addEventListener('change', sortEntries);
    
    function filterEntries() {
        const searchTerm = searchInput.value.toLowerCase();
        const entries = document.querySelectorAll('.entry-card');
        
        entries.forEach(entry => {
            const title = entry.querySelector('.entry-title').textContent.toLowerCase();
            const content = entry.querySelector('.entry-content-full').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || content.includes(searchTerm)) {
                entry.style.display = '';
            } else {
                entry.style.display = 'none';
            }
        });
        
        // Check if no visible entries
        const visibleEntries = Array.from(entries).filter(entry => entry.style.display !== 'none');
        if (visibleEntries.length === 0 && entries.length > 0) {
            let noResultsEl = entriesContainer.querySelector('.no-results');
            if (!noResultsEl) {
                noResultsEl = document.createElement('div');
                noResultsEl.className = 'no-results';
                noResultsEl.innerHTML = '<p>No entries match your search.</p>';
                entriesContainer.appendChild(noResultsEl);
            }
        } else {
            const noResultsEl = entriesContainer.querySelector('.no-results');
            if (noResultsEl) {
                noResultsEl.remove();
            }
        }
    }
    
    function sortEntries() {
        const sortBy = sortSelect.value;
        const entries = Array.from(document.querySelectorAll('.entry-card'));
        
        entries.sort((a, b) => {
            if (sortBy === 'newest') {
                const dateA = new Date(a.querySelector('.entry-date').textContent);
                const dateB = new Date(b.querySelector('.entry-date').textContent);
                return dateB - dateA;
            } else if (sortBy === 'oldest') {
                const dateA = new Date(a.querySelector('.entry-date').textContent);
                const dateB = new Date(b.querySelector('.entry-date').textContent);
                return dateA - dateB;
            } else if (sortBy === 'title') {
                const titleA = a.querySelector('.entry-title').textContent.toLowerCase();
                const titleB = b.querySelector('.entry-title').textContent.toLowerCase();
                return titleA.localeCompare(titleB);
            }
        });
        
        // Reorder entries in the DOM
        entries.forEach(entry => {
            entriesContainer.appendChild(entry);
        });
    }
    
    // Calculate journal streak (placeholder)
    function calculateJournalStreak() {
        const streakEl = document.getElementById('journal-streak');
        if (!streakEl) return;
        
        // In a real app, we might fetch this from the server
        const streak = 3; // Example placeholder
        streakEl.textContent = streak > 0 ? `${streak} days` : 'Start today!';
    }
    
    // Add new entry to DOM
    function addEntryToDOM(entry, prepend = false) {
        // Create container
        const entryCard = document.createElement('div');
        entryCard.className = 'entry-card';
        entryCard.dataset.id = entry.id;
        
        // Format date
        const date = new Date(entry.timestamp);
        const formattedDate = date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        // Build content preview
        const previewText = entry.content.length > 100 
            ? entry.content.substring(0, 100) + '...' 
            : entry.content;
        
        // Fill in the HTML
        entryCard.innerHTML = `
            <div class="entry-header">
                <h3 class="entry-title">${entry.title}</h3>
                <div class="entry-actions">
                    <button class="entry-action edit-entry" title="Edit entry">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="entry-action delete-entry" title="Delete entry">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                    <button class="entry-action toggle-entry" title="Expand/Collapse">
                        <i class="fas fa-chevron-down"></i>
                    </button>
                </div>
            </div>
            <div class="entry-date">${formattedDate}</div>
            <div class="entry-content">
                <p class="entry-content-preview">${previewText}</p>
                <p class="entry-content-full" style="display: none;">${entry.content}</p>
            </div>
        `;
        
        // If there was a "no-entries" message, remove it
        const noEntriesEl = entriesContainer.querySelector('.no-entries');
        if (noEntriesEl) {
            noEntriesEl.remove();
        }
        
        // Insert entry into the DOM
        if (prepend) {
            entriesContainer.insertBefore(entryCard, entriesContainer.firstChild);
        } else {
            entriesContainer.appendChild(entryCard);
        }
        
        // Recalculate streak (optional)
        calculateJournalStreak();
    }
    
    // Optional: Call the streak function on load
    calculateJournalStreak();
});

// Example notification function
function showNotification(message, type = 'success') {
    // Provide your notification logic here,
    // e.g., display a toast or an alert box.
    console.log(`${type.toUpperCase()}: ${message}`);
}
