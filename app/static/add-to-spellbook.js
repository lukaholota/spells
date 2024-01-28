function add_to_spellbook(form) {
    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.getAttribute("action"))

    xml.onreadystatechange=function(){
        if(this.readyState==4) {
            if (this.status == 0) {
                document.getElementById('')
            }
        }
        }

    xhr.send(new FormData(form));
    return false;
}