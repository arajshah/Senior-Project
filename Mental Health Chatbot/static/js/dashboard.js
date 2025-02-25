document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true
    });
    
    // Mood Chart Rendering
    const ctx = document.getElementById('moodChart').getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(124, 58, 237, 0.5)');
    gradient.addColorStop(1, 'rgba(124, 58, 237, 0)');
    
    // Example data - in a real app, this would come from the backend
    const moodChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['7 days ago', '6 days ago', '5 days ago', '4 days ago', '3 days ago', '2 days ago', 'Today'],
            datasets: [{
                label: 'Mood Rating',
                data: [6, 7, 5, 8, 4, 7, 8],
                backgroundColor: gradient,
                borderColor: '#7c3aed',
                borderWidth: 2,
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#ffffff',
                pointRadius: 5,
                pointHoverRadius: 7,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `Mood Rating: ${context.raw}/10`;
                        }
                    }
                }
            }
        }
    });
    
    // Add hover effects to support cards
    const supportCards = document.querySelectorAll('.support-card');
    supportCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
});