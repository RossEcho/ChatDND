function rollDice() {
    return Math.floor(Math.random() * 6) + 1;
}

function rollAttributes(race) {
    let racialBonuses = {
        "human": { strength: 1, dexterity: 1, constitution: 1, intelligence: 1, wisdom: 1, charisma: 1 },
        "elf": { strength: 0, dexterity: 2, constitution: 0, intelligence: 0, wisdom: 0, charisma: 0 },
        "dwarf": { strength: 0, dexterity: 0, constitution: 2, intelligence: 0, wisdom: 0, charisma: 0 },
        "halfling": { strength: 0, dexterity: 2, constitution: 0, intelligence: 0, wisdom: 0, charisma: 0 }
    };

    let raceBonuses = racialBonuses[race];
    let attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"];
    attributes.forEach((attribute) => {
        let input = document.getElementById(attribute);
        input.value = rollDice() + rollDice() + rollDice() + raceBonuses[attribute];
    });
}

document.getElementById('char_race').addEventListener('change', function () {
    rollAttributes(this.value);
});

document.getElementById('reroll').addEventListener('click', function () {
    let race = document.getElementById('char_race').value;
    rollAttributes(race);
});
