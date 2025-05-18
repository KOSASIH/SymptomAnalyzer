document.addEventListener('DOMContentLoaded', function() {
    const symptomInput = document.getElementById('symptom-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsContainer = document.getElementById('results-container');
    const symptomsText = document.getElementById('symptoms-text');
    const conditionsList = document.getElementById('conditions-list');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    analyzeBtn.addEventListener('click', analyzeSymptoms);
    
    function analyzeSymptoms() {
        const symptoms = symptomInput.value.trim();
        
        if (!symptoms) {
            alert('Please describe your symptoms before analyzing.');
            return;
        }
        
        // Show loading indicator
        loadingIndicator.style.display = 'flex';
        resultsContainer.style.display = 'none';
        
        // Send symptoms to the API
        fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symptoms })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while analyzing symptoms. Please try again.');
        })
        .finally(() => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
        });
    }
    
    function displayResults(data) {
        // Display the symptoms
        symptomsText.textContent = data.input_symptoms;
        
        // Clear previous conditions
        conditionsList.innerHTML = '';
        
        // Display potential conditions
        if (data.potential_conditions.length === 0) {
            conditionsList.innerHTML = '<p>No specific conditions identified based on the provided symptoms. Please provide more details or consult a healthcare professional.</p>';
        } else {
            data.potential_conditions.forEach(condition => {
                const conditionCard = document.createElement('div');
                conditionCard.className = 'condition-card';
                
                const probabilityPercentage = Math.round(condition.probability * 100);
                
                conditionCard.innerHTML = `
                    <div class="condition-header">
                        <span class="condition-name">${condition.condition}</span>
                        <span class="probability">${probabilityPercentage}% match</span>
                    </div>
                    <div class="recommendation">
                        <div class="recommendation-title">Recommendations:</div>
                        <p>${condition.recommendation}</p>
                    </div>
                `;
                
                conditionsList.appendChild(conditionCard);
            });
        }
        
        // Show results container
        resultsContainer.style.display = 'block';
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
});