//menu 
// Función para abrir y cerrar el menú
function toggleMenu() {
    document.body.classList.toggle('menu-open');
}

function setActiveLink() {
    const links = document.querySelectorAll('.menu-container ul li a');
    const currentPath = window.location.pathname; // Obtiene la ruta actual

    links.forEach(link => {
        const linkPath = link.getAttribute('href'); // Obtiene la ruta del enlace (ej: "/consultas")

        // Normaliza las rutas para eliminar barras finales y hacer la comparación más flexible
        const normalizedCurrentPath = currentPath.replace(/\/+$/, ''); // Elimina barras finales
        const normalizedLinkPath = linkPath.replace(/\/+$/, ''); // Elimina barras finales

        // Compara las rutas normalizadas
        if (normalizedCurrentPath === normalizedLinkPath) {
            link.parentElement.classList.add('active'); // Marca el <li> como activo
        }

        // Opcional: Agrega un evento para marcar el enlace activo al hacer clic
        link.addEventListener('click', function () {
            // Remueve la clase 'active' de todos los elementos <li>
            links.forEach(link => link.parentElement.classList.remove('active'));
            // Agrega la clase 'active' al <li> padre del enlace clickeado
            this.parentElement.classList.add('active');
        });
    });
}

// Ejecuta la función para marcar el enlace activo cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', setActiveLink);