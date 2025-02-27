function cargarDatos() {
    let inicio = document.getElementById('fechaInicio').value;
    let fin = document.getElementById('fechaFin').value;

    if (!inicio || !fin) {
        alert('Debe seleccionar ambas fechas.');
        return;
    }

    fetch(`/api/reporte_dinero?fecha_inicio=${inicio}&fecha_fin=${fin}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Error: ' + (data.error || 'No se pudieron obtener los datos.'));
                return;
            }

            let tabla = document.getElementById('tablaConsultas');
            tabla.innerHTML = '';

            data.data.forEach(consulta => {
                let fila = `<tr>
                    <td>${consulta.id}</td>
                    <td>${consulta.paciente}</td>
                    <td>${consulta.fecha} ${consulta.hora_ini}</td>
                    <td>$${consulta.importe}</td>
                </tr>`;
                tabla.innerHTML += fila;
            });
        })
        .catch(error => console.error('Error al obtener los datos:', error));
}
