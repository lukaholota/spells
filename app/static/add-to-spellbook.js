function add_to_spellbook() {
    var checkedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');

    if (checkedCheckboxes.length === 0) {
        return false; 
    }

    var formData = new FormData(); 
    checkedCheckboxes.forEach(function(checkbox) {
        formData.append(checkbox.name, checkbox.value);
    });

    var xhr = new XMLHttpRequest();
    xhr.open('POST', "/add-to-spellbook")

    xhr.onload=function(){
            if (this.status == 403) {
            document.getElementById('registration-block').style.display = 'block';
            } else {
                var message = document.getElementById('message');
                message.style.display = 'block';
                message.innerHTML = 'Додано! <a href="/spellbook">Переглянути книгу</a>'
                uncheckSelectedRows()
            }
        }

    xhr.send(formData);
    return false;
}

function send_hybrid_registration(form) {
    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.getAttribute("action"))
    xhr.onload=function(){
        jsonData = JSON.parse(this.responseText);
        var message = document.getElementById('message');
        message.style.display = 'block';
        message.innerText = jsonData.message
        if (jsonData.result == true) {
                document.getElementById('registration-block').style.display = 'none'                

                document.getElementById('sign-up').href = '/spellbook'
                document.getElementById('sign-up').innerText = 'Книга чарів'

                document.getElementById('log-in').href = '/logout'
                document.getElementById('log-in').innerText = 'Вийти'

                setTimeout(function(){
                    message.style.display = 'none'
                }, 5000)
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