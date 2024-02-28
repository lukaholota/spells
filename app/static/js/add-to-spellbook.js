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

                document.getElementById('sign-up').style.display = 'none'
                document.getElementById('log-in').style.display = 'none'

                document.getElementById('spellbook').style.display = 'block'
                document.getElementById('profile').style.display = 'block'
                document.getElementById('logout').style.display = 'block'

                let flash = document.getElementById('flash-success')
                flash.firstElementChild.innerHTML = 'Успіх! Тепер можна додавати заклинання в Книгу Чарів'
                flash.style.display = 'block'

                setTimeout(() => {
                    flash.style.display = 'none';
                }, 4000)
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