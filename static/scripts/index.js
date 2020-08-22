// DOM manipulation

let playlists = document.getElementById('playlists');
let playlistsNames = playlists.getElementsByClassName('playlistName');
let itemsNames = playlists.getElementsByClassName('itemsNames');

// Hide/display items on click of playlist
for (let i = 0; i < playlistsNames.length; i++) {
    playlistsNames[i].addEventListener('click', function () {
        if (itemsNames[i].style.display === 'none') {
            itemsNames[i].style.display = 'block';
        } else {
            itemsNames[i].style.display = 'none'
        }
    })
}