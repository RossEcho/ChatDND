window.onload = function() {
    fetch('/static/data/raceData.txt')
        .then(response => response.text())
        .then(data => {
            const lines = data.split('\n').filter(line => line.trim() !== '');

            const raceData = [];
            let currentRace = null;

            for (const line of lines) {
                if (line.startsWith('!')) {
                    if (currentRace !== null) {
                        raceData.push(currentRace);
                    }
                    currentRace = {
                        name: line.slice(1).trim(),
                        description: '',
                        traits: []
                    };
                } else if (line.startsWith('$') && currentRace !== null) {
                    currentRace.description = line.slice(1).trim();
                } else if (line.startsWith('#') && currentRace !== null) {
                    currentRace.traits.push(line.slice(1).trim());
                }
            }
            if (currentRace !== null) {
                raceData.push(currentRace);
            }

            const select = document.getElementById('races');
            for (const race of raceData) {
                const option = document.createElement('option');
                option.value = race.name;
                option.textContent = race.name;
                select.appendChild(option);
            }

            window.displayRaceData = function() {
                const selectedRace = raceData.find(race => race.name === select.value);
                const raceInfoDiv = document.getElementById('info');
                raceInfoDiv.innerHTML = `
                    <h2>${selectedRace.name}</h2>
                    <p>${selectedRace.description}</p>
                    <h3>Racial Traits</h3>
                    <ul>
                        ${selectedRace.traits.map(trait => `<li>${trait}</li>`).join('')}
                    </ul>
                `;
            }

            displayRaceData();  // Display data for the initially selected race
        });
}
