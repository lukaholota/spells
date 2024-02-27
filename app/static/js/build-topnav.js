function buildTopnav() {
    fetch(
        '/get-user-info'
    ).then(response => {
        return response.json()
    }).then(info => {
        if (info.is_authenticated == true) {
            document.getElementById('spellbook').style.display = 'block'
            document.getElementById('profile').style.display = 'block'
            document.getElementById('logout').style.display = 'block'
        } else {
            document.getElementById('sign-up').style.display = 'block'
            document.getElementById('log-in').style.display = 'block'
        }
    })
}

buildTopnav()