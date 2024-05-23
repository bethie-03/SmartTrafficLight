document.addEventListener('DOMContentLoaded', function() {
    var menu = document.querySelector('.menu');
    var menuIcon = document.getElementById('menu_icon');

    menuIcon.addEventListener('click', function(event) {
        menu.style.display = 'flex';
        event.stopPropagation(); 
    });

    document.addEventListener('click', function(event) {
        if (!menu.contains(event.target) && !menuIcon.contains(event.target)) {
            menu.style.display = 'none';
        }
    });
});