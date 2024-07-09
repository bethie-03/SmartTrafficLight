document.addEventListener('DOMContentLoaded', function() {
    var menu = document.querySelector('.menu');
    var menuIcon = document.getElementById('menu_icon');
    var Home_selection = document.getElementById('Home');
    var VD_selection = document.getElementById('VD');
    var RA_selection = document.getElementById('RA');
    var click = true
    var pygame = document.getElementById('pygame-stream')
    pygame.src = '/stream_pygame'

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
        pygame.src = ''
        window.location.href = '/VD-template';
    })

    RA_selection.addEventListener('click', function() {
        pygame.src = ''
        window.location.href = '/RA-template';
    })

    Home_selection.addEventListener('click', function() {
        pygame.src = ''
        window.location.href = '/';
    })
});

