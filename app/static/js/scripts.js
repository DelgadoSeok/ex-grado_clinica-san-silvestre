//aqui incluir login


//menu 
function toggleMenu() {
    var menu = document.querySelector('.menu-container');
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}
/*
function toggleMenu() {
    document.body.classList.toggle('menu-open');
}*/

// Función para abrir y cerrar el menú
function toggleMenu() {
    document.body.classList.toggle('menu-open');
}

// Funciones para abrir y cerrar el modal
function openModal() {
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Escucha el evento de envío del formulario
document.getElementById('duenoForm')?.addEventListener('submit', function (event) {
    event.preventDefault();
    // Aquí puedes manejar el envío del formulario si es necesario
    // Luego, cierra el modal
    closeModal();
});