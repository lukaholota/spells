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