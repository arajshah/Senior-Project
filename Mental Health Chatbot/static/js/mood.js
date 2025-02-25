document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const moodSlider = document.getElementById('mood_value');
    const moodValueDisplay = document.querySelector('.mood-value-display');
    const moodForm = document.getElementById('mood-form');
    const weekViewBtn = document.getElementById('week-view');
    const monthViewBtn = document.getElementById('month-view');
    const allViewBtn = document.getElementById('all-view');
    const recentEntriesContainer = document.getElementById('recent-entries');
    const averageMoodElement = document.getElementById('average-mood');
    const entryCountElement = document.getElementById('entry-count');
    const moodTrendElement = document.getElementById('mood-trend');
    
    let moodChart;
    let moodData = [];
    let currentTimeFilter = 'week';
    
    // Update mood value display
    moodSlider.addEventListener('input', function() {
        moodValueDisplay.textContent = this.value;
        
        // Change color based on mood
        let hue = (this.value - 1) * 12; // 1-10 converted to 0-108 hue range
        moodValueDisplay.style.background = `linear-gradient(45deg, hsl(${hue}, 100%, 65%), hsl(${hue + 20}, 100%, 65%))`;
    });
    
    // Submit mood form
    moodForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const moodValue = moodSlider.value;
        const note = document.getElementById('note').value;
        
        try {
            const response = await fetch('/api/mood/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    mood_value: moodValue,
                    note: note
                })
            });
            
            if (response.ok) {
                // Clear form and show confirmation
                document.getElementById('note').value = '';
                showNotification('Mood saved successfully!');
                
                // Refresh data
                loadMoodData();
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to save mood.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        }
    });
    
    // Time filter controls
    weekViewBtn.addEventListener('click', () => updateTimeFilter('week'));
    monthViewBtn.addEventListener('click', () => updateTimeFilter('month'));
    allViewBtn.addEventListener('click', () => updateTimeFilter('all'));
    
    function updateTimeFilter(filter) {
        currentTimeFilter = filter;
        
        // Update active button
        [weekViewBtn, monthViewBtn, allViewBtn].forEach(btn => btn.classList.remove('active'));
        
        if (filter === 'week') weekViewBtn.classList.add('active');
        else if (filter === 'month') monthViewBtn.classList.add('active');
        else allViewBtn.classList.add('active');
        
        // Update chart with filtered data
        updateChart();
    }
    
    // Load mood data from API
    async function loadMoodData() {
        try {
            const response = await fetch('/api/mood/data');
            
            if (response.ok) {
                moodData = await response.json();
                updateChart();
                updateInsights();
                renderRecentEntries();
            } else {
                console.error('Failed to load mood data');
                showNotification('Failed to load mood data.', 'error');
            }
        } catch (error) {
            console.error('Error loading mood data:', error);
        }
    }
    
    // Initialize and update mood chart
    function updateChart() {
        const ctx = document.getElementById('moodChart').getContext('2d');
        
        // Filter data based on time range
        const filteredData = filterDataByTimeRange(moodData, currentTimeFilter);
        
        // Prepare data for chart
        const labels = filteredData.map(entry => new Date(entry.timestamp));
        const data = filteredData.map(entry => entry.mood_value);
        
        // Create or update chart
        if (moodChart) {
            moodChart.data.labels = labels;
            moodChart.data.datasets[0].data = data;
            moodChart.update();
        } else {
            moodChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Mood',
                        data: data,
                        backgroundColor: 'rgba(118, 74, 241, 0.2)',
                        borderColor: 'rgba(118, 74, 241, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(118, 74, 241, 1)',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: currentTimeFilter === 'week' ? 'day' : 'day',
                                displayFormats: {
                                    day: 'MMM d'
                                }
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: 'rgba(255, 255, 255, 0.7)'
                            }
                        },
                        y: {
                            beginAtZero: false,
                            min: 1,
                            max: 10,
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: 'rgba(255, 255, 255, 0.7)',
                                stepSize: 1
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.7)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            callbacks: {
                                label: function(context) {
                                    const entry = filteredData[context.dataIndex];
                                    return `Mood: ${entry.mood_value}${entry.note ? ' | Note: ' + entry.note : ''}`;
                                }
                            }
                        }
                    }
                }
            });
        }
    }
    
    // Filter data based on time range
    function filterDataByTimeRange(data, timeRange) {
        const now = new Date();
        let startDate;
        
        if (timeRange === 'week') {
            startDate = new Date(now);
            startDate.setDate(now.getDate() - 7);
        } else if (timeRange === 'month') {
            startDate = new Date(now);
            startDate.setMonth(now.getMonth() - 1);
        } else {
            // All time
            return data;
        }
        
        return data.filter(entry => new Date(entry.timestamp) >= startDate);
    }
    
    // Update mood insights
    function updateInsights() {
        if (moodData.length === 0) {
            averageMoodElement.textContent = 'No data';
            entryCountElement.textContent = '0 entries';
            moodTrendElement.textContent = 'N/A';
            return;
        }
        
        // Total entries
        entryCountElement.textContent = `${moodData.length} entries`;
        
        // Average mood
        const sum = moodData.reduce((total, entry) => total + parseFloat(entry.mood_value), 0);
        const average = (sum / moodData.length).toFixed(1);
        averageMoodElement.textContent = average;
        
        // Trend (last 5 entries)
        const recentEntries = [...moodData].sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        ).slice(0, 5);
        
        if (recentEntries.length < 2) {
            moodTrendElement.textContent = 'Need more data';
            return;
        }
        
        const firstEntry = recentEntries[recentEntries.length - 1].mood_value;
        const lastEntry = recentEntries[0].mood_value;
        
        if (lastEntry > firstEntry) {
            moodTrendElement.innerHTML = '<span style="color:#7bed9f">↗ Improving</span>';
        } else if (lastEntry < firstEntry) {
            moodTrendElement.innerHTML = '<span style="color:#ff6b6b">↘ Declining</span>';
        } else {
            moodTrendElement.innerHTML = '<span style="color:#ffc371">→ Steady</span>';
        }
    }
    
    // Render recent entries
    function renderRecentEntries() {
        recentEntriesContainer.innerHTML = '';
        
        if (moodData.length === 0) {
            recentEntriesContainer.innerHTML = '<div class="loading-entries">No entries yet. Start tracking your mood!</div>';
            return;
        }
        
        // Sort by timestamp, newest first
        const sortedEntries = [...moodData].sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        ).slice(0, 5); // Show last 5 entries
        
        sortedEntries.forEach(entry => {
            const entryCard = document.createElement('div');
            entryCard.className = 'entry-card';
            
            // Format date
            const date = new Date(entry.timestamp);
            const formattedDate = date.toLocaleDateString('en-US', { 
                weekday: 'short', 
                month: 'short', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            entryCard.innerHTML = `
                <div class="entry-info">
                    <span class="entry-date">${formattedDate}</span>
                    ${entry.note ? `<p class="entry-note">${entry.note}</p>` : ''}
                </div>
                <div class="entry-mood">
                    <div class="mood-badge">${entry.mood_value}</div>
                </div>
            `;
            
            recentEntriesContainer.appendChild(entryCard);
        });
    }
    
    // Show notification
    function showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Add to body
        document.body.appendChild(notification);
        
        // Show with animation
        setTimeout(() => notification.classList.add('show'), 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Initial data load
    loadMoodData();
});