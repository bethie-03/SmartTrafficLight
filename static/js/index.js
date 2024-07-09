document.addEventListener('DOMContentLoaded', function() {
    var menu = document.querySelector('.menu');
    var menuIcon = document.getElementById('menu_icon');
    var VD_selection = document.getElementById('VD');
    var RA_selection = document.getElementById('RA');
    var Demo_selection = document.getElementById('Demo');
    var click = true

    menuIcon.addEventListener('click', function(event) {
        if (click){
            menu.style.display = 'flex';
            click = false;
        } else{
            menu.style.display = 'none';
            click = true;
        }
        event.stopPropagation();
    });

    document.addEventListener('click', function(event) {
        if (!menu.contains(event.target) && !menuIcon.contains(event.target)) {
            menu.style.display = 'none';
            click = true;
        }
    });

    VD_selection.addEventListener('click', function() {
        window.location.href = '/VD-template';
    })

    RA_selection.addEventListener('click', function() {
        window.location.href = '/RA-template';
    })

    Demo_selection.addEventListener('click', function() {
        window.location.href = '/Pygame-template';
    })
});