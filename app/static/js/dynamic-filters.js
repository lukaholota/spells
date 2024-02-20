$(document).ready(function(){
    var form = document.getElementById('filter');

    form.addEventListener('input', function(event) {
        var form = new FormData(document.getElementById('filter'));

        fetch('/spells', {
            'method': 'POST',
            'body': form
        })
        .then(response => {
            return response.json()
        })
        .then(spells => {
            var spellNames = [];
            spells.forEach(spell => {
                spellNames.push(spell.name.toLowerCase())
            })

            let spellsRows = document.querySelectorAll('tr');

            for (let i=1; i < spellsRows.length; i++) {
                let spellRow = spellsRows[i]
                if (spellNames.includes(spellRow.children[1].textContent.toLowerCase().trim())) {
                    spellRow.style.display = 'table-row';
                } else {
                    spellRow.style.display = 'none';
                }
            }
        })
    });

    form.onreset = event => {
        let spells = document.querySelectorAll('tr')
        for (let i=1; i < spells.length; i++) {
            let spell = spells[i]
            spell.style.display = 'table-row';
        }
        return true;
    };
});