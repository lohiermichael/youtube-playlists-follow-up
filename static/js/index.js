// DOM manipulation

// Hide display last update data on click
let playlists = document.getElementById('playlists');
let displayDataButton = document.getElementById('displayData');

displayDataButton.addEventListener('click', function () {
    if (this.className === 'hidden') {
        playlists.style.display = 'block';
        this.className = 'visible';
        this.textContent = 'Hide your data';
    } else {
        playlists.style.display = 'none';
        this.className = 'hidden';
        this.textContent = 'See your data';
    }
});


// Hide/display items on click of playlist

let playlistsNames = playlists.getElementsByClassName('playlistName');
let itemsNames = playlists.getElementsByClassName('itemsNames');

for (let i = 0; i < playlistsNames.length; i++) {
    playlistsNames[i].addEventListener('click', function () {
        if (itemsNames[i].style.display === 'none') {
            itemsNames[i].style.display = 'block';
        } else {
            itemsNames[i].style.display = 'none'
        }
    })
};