document.getElementById('name').addEventListener('input', function (event) {
    let searchValue = event.target.value.toLowerCase();
    let spells = document.querySelectorAll('tr');

    for (let i=1; i < spells.length; i++) {
        let spell = spells[i]
        let name = spell.children[1].textContent.toLowerCase();

        if (name.includes(searchValue)) {
            spell.style.display = 'table-row';
        } else {
            spell.style.display = 'none';
        }
    }
});     

$(document).ready(function(){
    let searchValue = $( "#name" )[0].value.toLowerCase();
    let spells = document.querySelectorAll('tr');

    for (let i=1; i < spells.length; i++) {
        let spell = spells[i]
        let name = spell.children[1].textContent.toLowerCase();

        if (name.includes(searchValue)) {
            spell.style.display = 'table-row';
        } else {
            spell.style.display = 'none';
        }
    }
});

$(document).ready(function() {
    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });
  });