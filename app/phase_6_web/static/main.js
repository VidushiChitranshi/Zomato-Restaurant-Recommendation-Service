document.addEventListener('DOMContentLoaded', () => {
    const locationSelect = document.getElementById('location');
    const recommendForm = document.getElementById('recommend-form');
    const searchBtn = document.getElementById('search-btn');
    const loader = document.getElementById('loader');
    const aiSection = document.getElementById('ai-section');
    const aiText = document.getElementById('ai-text');
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const resultLimit = document.getElementById('result-limit');
    const limitVal = document.getElementById('limit-val');
    const emptyState = document.getElementById('empty-state');

    // Update limit display
    resultLimit.addEventListener('input', () => {
        limitVal.textContent = resultLimit.value;
    });

    // Fetch locations on load
    async function fetchLocations() {
        try {
            const response = await fetch('/api/locations');
            const data = await response.json();

            data.locations.forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc;
                opt.textContent = loc;
                locationSelect.appendChild(opt);
            });
        } catch (error) {
            console.error('Error fetching locations:', error);
        }
    }

    fetchLocations();

    // 2. Handle form submission
    recommendForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const location = locationSelect.value;
        const maxPrice = document.getElementById('max-price').value;
        const limit = parseInt(resultLimit.value);

        if (!location) {
            alert('Please select a location');
            return;
        }

        // Show loading state
        searchBtn.disabled = true;
        loader.classList.remove('hidden');
        aiSection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        emptyState.classList.add('hidden');

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    location: location,
                    max_price: parseFloat(maxPrice),
                    limit: limit
                })
            });

            const data = await response.json();
            console.log('API Response:', data);

            loader.classList.add('hidden');
            searchBtn.disabled = false;

            if (data.restaurants && data.restaurants.length > 0) {
                console.log(`Rendering ${data.restaurants.length} restaurants`);
                renderResults(data.restaurants);
                renderAI(data.ai_summary);
                resultsSection.classList.remove('hidden');
                aiSection.classList.remove('hidden');
            } else {
                emptyState.classList.remove('hidden');
            }
        } catch (err) {
            console.error('Error fetching recommendations:', err);
            loader.classList.add('hidden');
            searchBtn.disabled = false;
            alert('Something went wrong. Please try again.');
        }
    });

    function renderResults(results) {
        resultsGrid.innerHTML = '';
        results.forEach(res => {
            const card = document.createElement('div');
            card.className = 'resto-card';
            card.innerHTML = `
                <div class="resto-info">
                    <h3 class="resto-name">${res.name}</h3>
                    <div class="resto-rating">${res.rate}</div>
                    <div class="resto-cuisines">${res.cuisines}</div>
                    <div class="resto-meta">
                        <span>${res.location}</span>
                        <span>Cost for 2: <span class="cost-label">₹${res.approx_cost}</span></span>
                    </div>
                </div>
            `;
            resultsGrid.appendChild(card);
        });
    }

    function renderAI(summary) {
        aiText.textContent = summary || "No summary available.";
    }
});
