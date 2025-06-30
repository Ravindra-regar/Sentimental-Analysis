document.addEventListener('DOMContentLoaded', () => {
    const analyzeButton = document.getElementById('analyze-button');
    const textInput = document.getElementById('text-input');
    const resultsArea = document.getElementById('results-area');
    const sentimentResult = document.getElementById('sentiment-result');
    const emotionList = document.getElementById('emotion-list');
    const graphImage = document.getElementById('graph-image');

    analyzeButton.addEventListener('click', () => {
        const text = textInput.value;

        if (!text.trim()) {
            alert('Please enter some text.');
            return;
        }

        // Show a loading state
        resultsArea.classList.add('hidden');
        analyzeButton.textContent = 'Analyzing...';
        analyzeButton.disabled = true;

        fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`An error occurred: ${data.error}`);
                return;
            }

            // 1. Update Sentiment Result
            sentimentResult.textContent = data.sentiment;

            // 2. Update Emotion List
            emotionList.innerHTML = ''; // Clear previous results
            const emotions = data.emotions;
            if (Object.keys(emotions).length > 0) {
                for (const [emotion, count] of Object.entries(emotions)) {
                    const p = document.createElement('p');
                    p.textContent = `${emotion}: ${count}`;
                    emotionList.appendChild(p);
                }
            } else {
                emotionList.innerHTML = '<p>No specific emotions found.</p>';
            }

            // 3. Update Graph Image
            // Add a timestamp to the URL to force the browser to reload the image
            graphImage.src = `${data.graph_url}?t=${new Date().getTime()}`;

            // Show the results
            resultsArea.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please check the console.');
        })
        .finally(() => {
            // Re-enable the button
            analyzeButton.textContent = 'Analyze Text';
            analyzeButton.disabled = false;
        });
    });
});