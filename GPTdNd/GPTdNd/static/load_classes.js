window.onload = function() {
    fetch('/static/data/classData.txt')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            const classData = data.split('\n!').map(cls => {
                const lines = cls.split('\n');
                if (lines.length < 5) return null;  // Skip invalid data
                const [name, description, hitDie, primaryAbility, savingThrows] = lines;
                return { 
                    name: name.trim(), 
                    description: description.slice(1).trim(), 
                    hitDie: hitDie.slice(1).trim(), 
                    primaryAbility: primaryAbility.slice(1).trim(),
                    savingThrows: savingThrows.slice(1).trim() 
                };
            }).filter(cls => cls);  // Remove null entries

            const select = document.getElementById('classes');
            for (const cls of classData) {
                const option = document.createElement('option');
                option.value = cls.name;
                option.textContent = cls.name;
                select.appendChild(option);
            }

            window.displayClassData = function() {
                const selectedClass = classData.find(cls => cls.name === select.value);
                const classInfoDiv = document.getElementById('info');
                classInfoDiv.innerHTML = `
                    <h2>${selectedClass.name}</h2>
                    <p>${selectedClass.description}</p>
                    <h3>Hit Die</h3>
                    <p>${selectedClass.hitDie}</p>
                    <h3>Primary Ability</h3>
                    <p>${selectedClass.primaryAbility}</p>
                    <h3>Saving Throws</h3>
                    <p>${selectedClass.savingThrows}</p>
                `;
            }

            displayClassData();  // Display data for the initially selected class
        })
        .catch(e => console.log('There was an error: ' + e));
}
