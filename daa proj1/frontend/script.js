console.log('Script loaded successfully.');

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('ingredient-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted');
        const form = e.target;
        const button = form.querySelector('button[type="submit"]');
        const ingredients = document.getElementById('ingredients').value.split(',').map(s => s.trim());
        console.log('Ingredients:', ingredients);
        button.classList.add('loading');
        button.disabled = true;
        button.textContent = 'Suggesting...';
        try {
            const response = await fetch('/suggest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ingredients })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const suggestions = await response.json();
            console.log('Suggestions received:', suggestions);
            displayResults(suggestions);
        } catch (error) {
            console.error('Fetch error:', error);
        } finally {
            button.classList.remove('loading');
            button.disabled = false;
            button.textContent = 'Suggest Recipes';
        }
    });
});

function displayResults(suggestions) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    suggestions.forEach((s, index) => {
        const div = document.createElement('div');
        const matchPct = s.match_pct * 100;
        let matchClass = 'low-match';
        if (matchPct > 80) {
            matchClass = 'high-match';
        } else if (matchPct > 50) {
            matchClass = 'medium-match';
        }
        div.className = `recipe ${matchClass}`;
        div.style.animationDelay = `${index * 0.1}s`;
        const icon = '🍛'; // Indian food emoji for appeal
        div.innerHTML = `
            <h3>${icon} ${s.name}</h3>
            <p>Match: ${(s.match_pct * 100).toFixed(1)}%</p>
            <p>Matched: ${s.matched_ings.join(', ')}</p>
            <p>Missing: ${s.missing_ings.join(', ')}</p>
            <p>Substitutions: ${Object.entries(s.substitutions).map(([k,v]) => `${k} -> ${v}`).join(', ')}</p>
        `;
        resultsDiv.appendChild(div);
    });
}
