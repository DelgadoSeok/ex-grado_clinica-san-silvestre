// Función para cargar la lista de doctores en el select
function cargarDoctores() {
    fetch('/api/doctores')
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById('doctorSelect'); 
            select.innerHTML = '<option value="">Seleccione un doctor</option>';
            
            // Itera sobre data.data
            data.data.forEach(doctor => {
                let nombreCompleto = `${doctor.nombres} ${doctor.p_apellido} ${doctor.s_apellido}`;
                select.innerHTML += `<option value="${doctor.id}">${nombreCompleto}</option>`;
            });
        })
        .catch(error => console.error('Error al cargar doctores:', error));
}

// Ejecutar la función al cargar la página
document.addEventListener('DOMContentLoaded', cargarDoctores);

// Función para cargar el reporte de consultas
function cargarConsultas() {
    let doctorId = document.getElementById('doctorSelect').value;
    let fechaInicio = document.getElementById('fechaInicio').value;
    let fechaFin = document.getElementById('fechaFin').value;

    if (!doctorId || !fechaInicio || !fechaFin) {
        alert('Debe seleccionar un doctor y un rango de fechas.');
        return;
    }

    fetch(`/api/reporte_consultas?doctor_id=${doctorId}&fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Error: ' + (data.error || 'No se pudieron obtener los datos.'));
                return;
            }

            let tabla = document.querySelector('#tablaConsultas tbody');
            tabla.innerHTML = '';

            data.data.forEach(consulta => {
                let fila = `<tr>
                    <td>${consulta.id}</td>
                    <td>${consulta.paciente}</td>
                    <td>${consulta.fecha}</td>
                    <td>${consulta.hora_ini}</td>
                    <td>$${consulta.importe}</td>
                </tr>`;
                tabla.innerHTML += fila;
            });
        })
        .catch(error => console.error('Error al obtener los datos:', error));
}
