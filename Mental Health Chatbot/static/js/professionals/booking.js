/**
 * Aurora Professional Help - Booking JavaScript
 * Handles appointment booking, calendar interactions, and confirmation
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
      AOS.init();
    }
    
    // ----- Variables -----
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();
    
    // ----- Calendar Elements -----
    const calendarGrid = document.getElementById('calendar-grid');
    const currentMonthElement = document.getElementById('current-month');
    const prevMonthButton = document.getElementById('prev-month');
    const nextMonthButton = document.getElementById('next-month');
    const timeSlots = document.getElementById('time-slots');
    const selectedDateInput = document.getElementById('selected-date');
    const selectedTimeInput = document.getElementById('selected-time');
    const bookingForm = document.getElementById('booking-form');
    
    // ----- Simplified Booking on Professional Detail Page -----
    const dateOptions = document.querySelectorAll('.date-option');
    const timeOptions = document.querySelectorAll('.time-option');
    const bookNowBtn = document.getElementById('book-now-btn');
    
    // ----- Modal Elements -----
    const bookingModal = document.getElementById('booking-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const closeModalX = document.querySelector('.close-modal');
    const modalDate = document.getElementById('modal-date');
    const modalTime = document.getElementById('modal-time');
    const modalType = document.getElementById('modal-type');
    
    // ----- Initialize Calendar -----
    if (calendarGrid) {
      generateCalendar(currentMonth, currentYear);
      updateMonthDisplay();
      
      // Month navigation
      prevMonthButton.addEventListener('click', function() {
        currentMonth--;
        if (currentMonth < 0) {
          currentMonth = 11;
          currentYear--;
        }
        generateCalendar(currentMonth, currentYear);
        updateMonthDisplay();
      });
      
      nextMonthButton.addEventListener('click', function() {
        currentMonth++;
        if (currentMonth > 11) {
          currentMonth = 0;
          currentYear++;
        }
        generateCalendar(currentMonth, currentYear);
        updateMonthDisplay();
      });
    }
    
    // ----- Date Options on Detail Page -----
    if (dateOptions.length > 0) {
      dateOptions.forEach(option => {
        option.addEventListener('click', function() {
          // Deselect all date options
          dateOptions.forEach(opt => opt.classList.remove('selected'));
          
          // Select the clicked option
          this.classList.add('selected');
          
          // Update any related UI or data
          const day = this.querySelector('.day-number').textContent;
          const monthName = months[today.getMonth()].substring(0, 3);
          const fullDate = `${monthName} ${day}, ${today.getFullYear()}`;
          
          // If we need to store the selected date
          if (selectedDateInput) {
            selectedDateInput.value = fullDate;
          }
        });
      });
    }
    
    // ----- Time Options on Detail Page -----
    if (timeOptions.length > 0) {
      timeOptions.forEach(option => {
        option.addEventListener('click', function() {
          // Deselect all time options
          timeOptions.forEach(opt => opt.classList.remove('selected'));
          
          // Select the clicked option
          this.classList.add('selected');
          
          // Update any related UI or data
          const timeValue = this.textContent.trim();
          
          // If we need to store the selected time
          if (selectedTimeInput) {
            selectedTimeInput.value = timeValue;
          }
        });
      });
    }
    
    // ----- Book Now Button on Detail Page -----
    if (bookNowBtn) {
      bookNowBtn.addEventListener('click', function() {
        let selectedDate = '';
        let selectedTime = '';
        
        // Get selected date and time
        const dateOption = document.querySelector('.date-option.selected');
        const timeOption = document.querySelector('.time-option.selected');
        
        if (dateOption && timeOption) {
          const dayNum = dateOption.querySelector('.day-number').textContent;
          const dayName = dateOption.querySelector('.day-name').textContent;
          selectedDate = `${dayName}, November ${dayNum}`;
          selectedTime = timeOption.textContent.trim();
          
          // Update modal content
          if (modalDate) modalDate.textContent = selectedDate;
          if (modalTime) modalTime.textContent = selectedTime;
          
          // Show the booking confirmation modal
          if (bookingModal) {
            bookingModal.style.display = 'flex';
            setTimeout(() => {
              bookingModal.classList.add('show');
            }, 10);
          }
        } else {
          // Show error if date or time not selected
          showNotification('Please select both a date and time', 'error');
        }
      });
    }
    
    // ----- Modal Close Button -----
    if (closeModalBtn) {
      closeModalBtn.addEventListener('click', function() {
        closeModal();
      });
    }
    
    // ----- Modal X Button -----
    if (closeModalX) {
      closeModalX.addEventListener('click', function() {
        closeModal();
      });
    }
    
    // ----- Close Modal when clicking outside -----
    if (bookingModal) {
      bookingModal.addEventListener('click', function(e) {
        if (e.target === bookingModal) {
          closeModal();
        }
      });
    }
    
    // ----- Booking Form Submission -----
    if (bookingForm) {
      bookingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate the form
        const selectedDate = selectedDateInput.value;
        const selectedTime = selectedTimeInput.value;
        const sessionType = document.getElementById('session-type').value;
        
        if (!selectedDate || !selectedTime) {
          showNotification('Please select both a date and time', 'error');
          return;
        }
        
        // Update modal content
        if (modalDate) modalDate.textContent = selectedDate;
        if (modalTime) modalTime.textContent = selectedTime;
        if (modalType) modalType.textContent = sessionType;
        
        // Show the booking confirmation modal
        if (bookingModal) {
          bookingModal.style.display = 'flex';
          setTimeout(() => {
            bookingModal.classList.add('show');
          }, 10);
        } else {
          // If no modal, just show a notification
          showNotification('Appointment booked successfully!', 'success');
          
          // Redirect or reset form
          setTimeout(() => {
            window.location.href = '/professionals';
          }, 2000);
        }
      });
    }
    
    /**
     * Generate calendar for the given month and year
     */
    function generateCalendar(month, year) {
      if (!calendarGrid) return;
      
      calendarGrid.innerHTML = '';
      
      // Create header row with day names
      days.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'calendar-day-header';
        dayHeader.textContent = day;
        calendarGrid.appendChild(dayHeader);
      });
      
      // Get first day of month and total days
      const firstDay = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      
      // Create empty cells for days before the first day of the month
      for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day empty';
        calendarGrid.appendChild(emptyDay);
      }
      
      // Create cells for each day of the month
      for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day';
        dayCell.textContent = day;
        
        // Check if this day is in the past
        const currentDate = new Date();
        const cellDate = new Date(year, month, day);
        if (cellDate < new Date(currentDate.setHours(0,0,0,0))) {
          dayCell.classList.add('past');
        } else {
          // Make future days selectable
          dayCell.classList.add('selectable');
          
          // Some days might be unavailable (e.g., weekends or fully booked)
          // This is a simplified example - in a real application, you would check 
          // availability from the server
          if ([0, 6].includes(new Date(year, month, day).getDay())) {
            dayCell.classList.add('unavailable');
            dayCell.title = 'Unavailable';
          } else {
            dayCell.addEventListener('click', function() {
              // Deselect any previously selected day
              document.querySelectorAll('.calendar-day.selected').forEach(el => {
                el.classList.remove('selected');
              });
              
              // Select this day
              this.classList.add('selected');
              
              // Update hidden input
              const selectedDate = `${months[month]} ${day}, ${year}`;
              selectedDateInput.value = selectedDate;
              
              // Show available time slots for this day
              showTimeSlots(year, month, day);
            });
          }
        }
        
        calendarGrid.appendChild(dayCell);
      }
    }
    
    /**
     * Update the month and year display
     */
    function updateMonthDisplay() {
      if (currentMonthElement) {
        currentMonthElement.textContent = `${months[currentMonth]} ${currentYear}`;
      }
    }
    
    /**
     * Show available time slots for a selected date
     */
    function showTimeSlots(year, month, day) {
      if (!timeSlots) return;
      
      // Clear previous time slots
      timeSlots.innerHTML = '';
      
      // Get day of week (0 = Sunday, 6 = Saturday)
      const dayOfWeek = new Date(year, month, day).getDay();
      
      // Sample available times - in a real app, this would come from the server
      const availableTimes = [
        '9:00 AM', '10:00 AM', '11:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM'
      ];
      
      // Different availability based on day of week (just as an example)
      if (dayOfWeek === 5) { // Friday
        availableTimes.pop(); // Remove last time slot
      }
      
      // Create the time slot grid
      const timeGrid = document.createElement('div');
      timeGrid.className = 'time-grid';
      
      availableTimes.forEach(time => {
        const timeSlot = document.createElement('button');
        timeSlot.type = 'button';
        timeSlot.className = 'time-slot';
        timeSlot.textContent = time;
        
        timeSlot.addEventListener('click', function() {
          // Deselect any previously selected time
          document.querySelectorAll('.time-slot.selected').forEach(el => {
            el.classList.remove('selected');
          });
          
          // Select this time
          this.classList.add('selected');
          
          // Update hidden input
          selectedTimeInput.value = time;
        });
        
        timeGrid.appendChild(timeSlot);
      });
      
      timeSlots.appendChild(timeGrid);
    }
    
    /**
     * Close the booking modal
     */
    function closeModal() {
      if (bookingModal) {
        bookingModal.classList.remove('show');
        setTimeout(() => {
          bookingModal.style.display = 'none';
        }, 300);
      }
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