function toggleMenu() {
  document.body.classList.toggle('menu-open');
}
function openModal() {
  document.getElementById('modal').style.display = 'block';
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

// Función para agregar un nuevo campo de número de teléfono
function agregarTelefono() {
    const telefonosContainer = document.getElementById('telefonosContainer');
    const nuevoTelefono = document.createElement('input');
    nuevoTelefono.type = 'text';
    nuevoTelefono.name = 'telefono';
    telefonosContainer.appendChild(nuevoTelefono);
  }

// registra nuevo doctor en db
function registrarDoctor() {
    let nuevoDoctorForm = document.getElementById("nuevoDoctorForm");

    let nombres = nuevoDoctorForm.querySelector("[name='nombres']").value;
    let pApellido = nuevoDoctorForm.querySelector("[name='p_apellido']").value;
    let sApellido = nuevoDoctorForm.querySelector("[name='s_apellido']").value;
    let fechaNacimiento = nuevoDoctorForm.querySelector("[name='fecha']").value;
    let sexo = nuevoDoctorForm.querySelector("[name='sexo']").value;
    let ci = nuevoDoctorForm.querySelector("[name='ci']").value;
    let email = nuevoDoctorForm.querySelector("[name='email']").value;
    let direccion = nuevoDoctorForm.querySelector("[name='direccion']").value;
    let matricula = nuevoDoctorForm.querySelector("[name='matricula']").value;

    // Obtener todos los números de teléfono
    let telefonos = [];
    nuevoDoctorForm.querySelectorAll("[name='telefono']").forEach(input => {
        telefonos.push(input.value);
    });

  
    fetch('/doctor/registrar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombres, pApellido, sApellido, fechaNacimiento, sexo, ci, email, direccion, matricula, telefonos })
    })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        location.reload();
        closeModal();
        // cargarEgresos();
        // cargarTiposEgreso();
      })
      .catch(error => console.error('Error al registrar egreso:', error));
  }


function openEditModal(id, fecha, monto, observacion, tipo, descartado) {
  document.getElementById('edit_id').value = id;
  document.getElementById('edit_fecha').value = fecha;
  document.getElementById('edit_monto').value = monto;
  document.getElementById('edit_observacion').value = observacion;
  document.getElementById('edit_egreso_tipo_id').value = tipo;
  document.getElementById('edit_descartado').checked = descartado;

  document.getElementById('editModal').style.display = 'block';
}

// function editarEgreso() {
//   let id = document.getElementById("edit_id").value;
//   let fecha = document.getElementById("edit_fecha").value;
//   let monto = document.getElementById("edit_monto").value;
//   let observacion = document.getElementById("edit_observacion").value;
//   let tipo = document.getElementById("edit_egreso_tipo_id").value;
//   let descartado = document.getElementById("edit_descartado").checked ? 1 : 0;

//   let dataToSend = {};

//   if (observacion) dataToSend.observacion = observacion;
//   if (monto) dataToSend.monto = monto;
//   if (fecha) dataToSend.fecha = fecha;
//   if (tipo) dataToSend.tipo = tipo;
//   if (descartado) dataToSend.descartado = descartado;
//   console.log("Enviando datos para editar:", dataToSend);

//   fetch(`/egresos/editar/${id}`, {
//     method: 'PUT',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(dataToSend)
//   })
//     .then(response => response.json())
//     .then(data => {
//       console.log("Respuesta del servidor:", data);
//       alert(data.mensaje);
//       closeEditModal();
//       location.reload();
//       cargarEgresos();
//       cargarTiposEgreso();

//     })
//     .catch(error => console.error('Error al editar egreso:', error));
// }

// function cargarEgresos() {
//   fetch('/egresos/')
//     .then(response => response.json())
//     .then(data => {
//       let tbody = document.querySelector('tbody');
//       tbody.innerHTML = '';

//       if (data && Array.isArray(data)) {
//         data.forEach(egreso => {
//           let row = document.createElement('tr');
//           row.innerHTML = `
//         <td>${egreso.fecha}</td>
//         <td>${egreso.monto}</td>
//         <td>${egreso.observacion}</td>
//         <td>${egreso.egreso_tipo_id}</td>
//         <td>${egreso.descartado ? 'Sí' : 'No'}</td>
//         <td>
//           <button class="btn btn-edit" onclick="openEditModal(
//             '${egreso.id}',
//             '${egreso.fecha}',
//             '${egreso.monto}',
//             '${egreso.observacion}',
//             '${egreso.egreso_tipo_id}',
//             ${egreso.descartado}
//           )">Editar</button>
//           <button class="btn btn-danger" onclick="descartarEgreso('${egreso.id}')">Descartar</button>
//         </td>
//       `;
//           tbody.appendChild(row);
//         });
//       } else {
//         let row = document.createElement('tr');
//         row.innerHTML = `<td colspan="6" style="text-align: center;">No hay egresos registrados.</td>`;
//         tbody.appendChild(row);
//       }
//     })
//     .catch(error => console.error('Error al cargar egresos:', error));
// }

// function cargarTiposEgreso() {
//   fetch('/egresos/tipos')
//     .then(response => response.json())
//     .then(data => {
//       let select = document.getElementById("egreso_tipo_id");
//       let editSelect = document.getElementById("edit_egreso_tipo_id");
//       select.innerHTML = '';
//       editSelect.innerHTML = '';

//       data.forEach(egreso_tipo_id => {
//         let option = document.createElement('option');
//         option.value = egreso_tipo_id.id;
//         option.textContent = egreso_tipo_id.descripcion;
//         select.appendChild(option);

//         let editOption = document.createElement('option');
//         editOption.value = egreso_tipo_id.id;
//         editOption.textContent = egreso_tipo_id.descripcion;
//         editSelect.appendChild(editOption);
//       });
//     })
//     .catch(error => console.error('Error al cargar tipos de egreso:', error));
// }

// document.addEventListener("DOMContentLoaded", function () {
//   cargarEgresos();
//   cargarTiposEgreso();
//   document.getElementById('egresoForm').addEventListener('submit', event => {
//     event.preventDefault();
//     registrarEgreso();
//   });

// });