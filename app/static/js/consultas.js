document.addEventListener("DOMContentLoaded", function () {
  // Cargar pacientes y doctores al cargar la página
  cargarPacientes();
  cargarDoctores();
  cargarConsultorios();

  // Evento para cargar horarios disponibles cuando se selecciona una fecha
  document.getElementById("fecha").addEventListener("change", function () {
    // Obtener la fecha seleccionada desde el campo de fecha
    const fecha = this.value;

    // Verificar si la fecha es válida
    if (fecha) {
      // Realizar la solicitud GET a la ruta con la fecha como parámetro
      fetch(`/consultas/hora_ini?fecha=${fecha}`)
        .then((response) => response.json()) // Asumiendo que la respuesta es en formato JSON
        .then((data) => {
          console.log("Horas disponibles:", data);

          // Aquí podrías actualizar el HTML con las horas disponibles si es necesario
          const horaIni = data.hora_ini;
          const horaSelect = document.getElementById("hora_ini");

          // Limpiar las opciones existentes en el select
          horaSelect.innerHTML =
            '<option value="">Seleccione una hora</option>';

          // Si hay horas disponibles, agregar las opciones al select
          if (horaIni.length > 0) {
            horaIni.forEach((hora) => {
              const option = document.createElement("option");
              option.value = hora;
              option.textContent = hora;
              horaSelect.appendChild(option);
            });
          } else {
            // Si no hay horas disponibles, agregar una opción para informar al usuario
            const option = document.createElement("option");
            option.value = "";
            option.textContent = "No hay horas disponibles";
            horaSelect.appendChild(option);
          }
        })
        .catch((error) => {
          console.error("Error al obtener las horas:", error);
        });
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
  fetch("/consultas/nueva_consulta")
    .then((response) => response.json())
    .then((data) => {
      console.log("Pacientes recibidos:", data.pacientes);
      const select = document.getElementById("paciente_id");
      select.innerHTML = '<option value="">Seleccione un paciente</option>';
      data.pacientes.forEach((paciente) => {
        const option = document.createElement("option");
        option.value = paciente.id;
        option.textContent = paciente.nombre_completo;
        select.appendChild(option);
      });
    })
    .catch((error) => console.error("Error:", error));
}

function cargarDoctores() {
  fetch("/consultas/nueva_consulta")
    .then((response) => response.json())
    .then((data) => {
      console.log("Doctores recibidos:", data.doctores);
      const select = document.getElementById("doctor_id");
      select.innerHTML = '<option value="">Seleccione un doctor</option>';
      data.doctores.forEach((doctor) => {
        const option = document.createElement("option");
        option.value = doctor.id;
        option.textContent = doctor.nombre_completo;
        select.appendChild(option);
      });
    })
    .catch((error) => console.error("Error:", error));
}

function cargarConsultorios() {
  fetch(`/consultas/nueva_consulta`)
    .then((response) => response.json())
    .then((data) => {
      console.log("Consultorios recibidos:", data.consultorios);
      const select = document.getElementById("consultorio_id");
      select.innerHTML = '<option value="">Seleccione un consultorio</option>';
      data.consultorios.forEach((consultorio) => {
        const option = document.createElement("option");
        option.value = consultorio.id;
        option.textContent = consultorio.nro_consultorio;
        select.appendChild(option);
      });
    })
    .catch((error) => console.error("Error:", error));
}

function crearConsulta() {
  const pacienteId = document.getElementById("paciente_id").value;
  const doctorId = document.getElementById("doctor_id").value;
  const consultorioId = document.getElementById("consultorio_id").value;
  const fecha = document.getElementById("fecha").value;
  const horaIni = document.getElementById("hora_ini").value;
  const tipo = document.getElementById("tipo").value;

  const horaIniDate = new Date(`1970-01-01T${horaIni}`); 
  horaIniDate.setMinutes(horaIniDate.getMinutes() + 20);
  const horaFin = horaIniDate.toTimeString().slice(0, 5);

  fetch("/consultas/crear_consulta", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      paciente_id: pacienteId,
      doctor_id: doctorId,
      consultorio_id: consultorioId,
      fecha: fecha,
      hora_ini: horaIni,
      hora_fin: horaFin, 
      tipo: tipo,
      estado: 'A'
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Consulta creada exitosamente");
        window.open(`/consultas/reporte/${data.consulta_id}`, "_blank");
        location.reload();
      } else {
        alert("Error al crear la consulta: " + data.error);
      }
    })
    .catch((error) => console.error("Error:", error));
}

function generarPDF(consultaId) {
  // Redirigir a la ruta que genera el PDF
  window.open(`/consultas/reporte/${consultaId}`, "_blank");
}
