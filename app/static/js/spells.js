// Contents of collapsible-filters.js
var coll = document.getElementsByClassName("collapsible");

coll[0].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });

// Contents of dynamic-filters.js
document.addEventListener('DOMContentLoaded', function() {
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

    window.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            return false;
        }
    });
});
// Contents of multiple-selects.js
document.addEventListener('DOMContentLoaded', function() {
    var selectElements = document.querySelectorAll('.multiple-select');

    selectElements.forEach(function(selectElement) {
        var options = selectElement.querySelectorAll('option');

        options.forEach(function(option) {
            option.addEventListener('mousedown', function(e) {
                e.preventDefault()
                var originalScrollTop = selectElement.scrollTop;
                option.selected = !option.selected;
                selectElement.focus();
                setTimeout(function() {
                    selectElement.scrollTop = originalScrollTop;
                }, 0);
                e.target.dispatchEvent(new Event('input', { bubbles: true }));

                return false;
            });
        });
    });
});
// Contents of add-to-spellbook.js
function send_hybrid_registration(form) {
    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.getAttribute("action"))
    xhr.onload=function(){
        jsonData = JSON.parse(this.responseText);
        var message = document.getElementById('message');
        message.style.display = 'block';
        message.innerText = jsonData.message
        if (jsonData.result == true) {
                document.getElementById('registration-modal').style.display = 'none'                

                document.getElementById('authorization').style.display = 'none'

                document.getElementById('spellbook').style.display = 'block'
                document.getElementById('profile').style.display = 'block'
                document.getElementById('logout').style.display = 'block'

                let flash = document.getElementById('flash-success')
                flash.firstElementChild.innerHTML = 'Успіх! Тепер можна додавати заклинання в Книгу Чарів'
                flash.style.display = 'block'

                makeBooksActive()

                setTimeout(() => {
                    flash.style.display = 'none';
                }, 3950)
            }
        } 
    xhr.send(new FormData(form));
    return false;
}

function uncheckSelectedRows() {
    var checkboxes = document.querySelectorAll('#spells-table .spells-to-add');
    
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    })
}

function CreateSpelllist() {
    let checkboxes = document.querySelectorAll('.spells-table .spells-to-add');
    
    let result = false;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked == true) result = true;  
    });
    return result;
}
// Contents of manage-book.js
function manageBook(img) {
    if (img.src.includes('/static/images/book-inactive.png')) {
        addSpellToSpellbook(img)
    } else {
        deleteSpellFromSpellbook(img)
    }
}

function addSpellToSpellbook(img) {
    let id = getIdFromImage(img)
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "/add-to-spellbook")
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    data = {};
    data['id'] = id;

    xhr.onload = function(){
        if (this.status == 403) {
        document.getElementById('registration-modal').style.display = 'block';
        } else {
            img.src = img.src.replace('inactive', 'active')
        }
    }

    xhr.send(JSON.stringify(data))
} 

function deleteSpellFromSpellbook(img) {
    let id = getIdFromImage(img)
    let formData = new FormData();
    formData.append('spell_id', id)

    let xhr = new XMLHttpRequest()
    xhr.open('POST', "/delete-spellbook-spell")

    xhr.onload = function(){
        if (this.status == 200) {
            img.src = img.src.replace('active', 'inactive')
        }
    }

    xhr.send(formData)
} 


function getIdFromImage(img) {
    tr = img.parentElement.parentElement.parentElement
    return tr.lastElementChild.firstElementChild.value
}

function makeBooksActive() {
    fetch(
        'get-spellbook-spells'
    ).then(response => {
        return response.json()
    }).then(spells => {
        if (spells.length != 0) {
            let spellsRows = document.querySelectorAll('tr');
            for (let i=1; i < spellsRows.length; i++) {
                let spellRow = spellsRows[i] 
                if (spells.includes(parseInt(spellRow.lastElementChild.firstElementChild.value))) {
                    book = spellRow.firstElementChild.firstElementChild.firstElementChild
                    book.src = book.src.replace('inactive', 'active')
                }
            }
        }
    })
}

makeBooksActive()

var modal = document.getElementById('registration-modal');

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}