window.onload = function() {

    // Load race data
    fetch('/static/data/raceData.txt')
        .then(response => response.text())
        .then(data => {
            const lines = data.split('\n').filter(line => line.trim() !== '');
            const raceData = [];

            for (const line of lines) {
                if (line.startsWith('!')) {
                    raceData.push({
                        name: line.slice(1).trim(),
                        description: lines[lines.indexOf(line) + 1].slice(1).trim()
                    });
                }
            }

            const selectedRace = raceData.find(race => race.name === character.race);
            if (selectedRace) {
                document.getElementById('race-description').textContent = 'Race Description: ' + selectedRace.description;
            }
        });

    // Load class data
    fetch('/static/data/classData.txt')
        .then(response => response.text())
        .then(data => {
            const lines = data.split('\n').filter(line => line.trim() !== '');
            const classData = [];

            for (const line of lines) {
                if (line.startsWith('!')) {
                    classData.push({
                        name: line.slice(1).trim(),
                        description: lines[lines.indexOf(line) + 1].slice(1).trim()
                    });
                }
            }

            const selectedClass = classData.find(class_ => class_.name === character.class);
            if (selectedClass) {
                document.getElementById('class-description').textContent = 'Class Description: ' + selectedClass.description;
            }
        });
}
