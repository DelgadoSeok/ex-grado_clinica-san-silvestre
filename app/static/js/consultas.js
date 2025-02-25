// document.addEventListener('DOMContentLoaded', function () {
//     const doctorSelect = document.getElementById('doctor_id');
//     const consultorioSelect = document.getElementById('consultorio_id');
//     const fechaInput = document.getElementById('fecha');
//     const horaIniInput = document.getElementById('hora_ini');

//     // Cargar consultorios al seleccionar un doctor
//     doctorSelect.addEventListener('change', function () {
//         const doctorId = this.value;
//         fetch(`/consultas/consultorios/${doctorId}`)
//             .then(response => response.json())
//             .then(data => {
//                 consultorioSelect.innerHTML = '';
//                 data.forEach(consultorio => {
//                     const option = document.createElement('option');
//                     option.value = consultorio.id;
//                     option.textContent = consultorio.nombre;
//                     consultorioSelect.appendChild(option);
//                 });
//             });
//     });

//     // Verificar disponibilidad de hora
//     horaIniInput.addEventListener('change', function () {
//         const doctorId = doctorSelect.value;
//         const fecha = fechaInput.value;
//         const horaIni = horaIniInput.value;

//         fetch('/consultas/verificar_disponibilidad', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ doctor_id: doctorId, fecha: fecha, hora_ini: horaIni })
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (!data.disponible) {
//                 alert('La hora seleccionada no está disponible.');
//             }
//         });
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
  // Cargar pacientes y doctores al cargar la página
  cargarPacientes();
  cargarDoctores();

  // Evento para cargar consultorios cuando se selecciona un doctor
  document.getElementById("doctor_id").addEventListener("change", function () {
    const doctorId = this.value;
    cargarConsultorios(doctorId);
  });

  // Evento para cargar horarios disponibles cuando se selecciona una fecha
  document.getElementById("fecha").addEventListener("change", function () {
    const consultorioId = document.getElementById("consultorio_id").value;
    const fecha = this.value;
    if (consultorioId && fecha) {
      cargarHorariosDisponibles(consultorioId, fecha);
    }
  });

  // Evento para crear una nueva consulta
  document
    .getElementById("consultaForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      crearConsulta();
    });
});

function cargarPacientes() {
  fetch('/consultas/nueva_consulta')
      .then(response => response.json())
      .then(data => {
          const select = document.getElementById('paciente_id');
          select.innerHTML = '<option value="">Seleccione un paciente</option>';
          data.pacientes.forEach(paciente => {
              const option = document.createElement('option');
              option.value = paciente.id;
              option.textContent = paciente.nombre;
              select.appendChild(option);
          });
      })
      .catch(error => console.error('Error:', error));
}

function cargarDoctores() {
  fetch('/consultas/nueva_consulta')
      .then(response => response.json())
      .then(data => {
          const select = document.getElementById('doctor_id');
          select.innerHTML = '<option value="">Seleccione un doctor</option>';
          data.doctores.forEach(doctor => {
              const option = document.createElement('option');
              option.value = doctor.id;
              option.textContent = doctor.nombre;
              select.appendChild(option);
          });
      })
      .catch(error => console.error('Error:', error));
}

function cargarConsultorios(doctorId) {
  fetch(`/consultas/obtener_consultorios/${doctorId}`)
      .then(response => response.json())
      .then(data => {
          const select = document.getElementById('consultorio_id');
          select.innerHTML = '<option value="">Seleccione un consultorio</option>';
          data.forEach(consultorio => {
              const option = document.createElement('option');
              option.value = consultorio.id;
              option.textContent = consultorio.nro;
              select.appendChild(option);
          });
      })
      .catch(error => console.error('Error:', error));
}

function cargarHorariosDisponibles(consultorioId, fecha) {
  fetch('/consultas/obtener_horarios_disponibles', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ consultorio_id: consultorioId, fecha: fecha })
  })
      .then(response => response.json())
      .then(data => {
          const select = document.getElementById('hora_ini');
          select.innerHTML = '<option value="">Seleccione una hora</option>';
          data.horarios_disponibles.forEach(hora => {
              const option = document.createElement('option');
              option.value = hora;
              option.textContent = hora;
              select.appendChild(option);
          });
      })
      .catch(error => console.error('Error:', error));
}

function crearConsulta() {
  const pacienteId = document.getElementById('paciente_id').value;
  const doctorId = document.getElementById('doctor_id').value;
  const consultorioId = document.getElementById('consultorio_id').value;
  const fecha = document.getElementById('fecha').value;
  const horaIni = document.getElementById('hora_ini').value;
  const tipo = document.getElementById('tipo').value;

  fetch('/consultas/crear_consulta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
          paciente_id: pacienteId,
          doctor_id: doctorId,
          consultorio_id: consultorioId,
          fecha: fecha,
          hora_ini: horaIni,
          tipo: tipo
      })
  })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Consulta creada exitosamente');
              window.open(`/consultas/reporte/${data.consulta_id}`, '_blank');
              location.reload();
          } else {
              alert('Error al crear la consulta: ' + data.error);
          }
      })
      .catch(error => console.error('Error:', error));
}

function generarPDF(consultaId) {
  // Redirigir a la ruta que genera el PDF
  window.open(`/consultas/reporte/${consultaId}`, '_blank');
}