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

// Función para agregar un nuevo select de especialidad
function agregarEspecialidad() {
  const especialidadesContainer = document.getElementById('especialidadesContainer');
  const nuevoSelect = document.createElement('select');
  nuevoSelect.name = 'especialidad';

  // Copiar las opciones del primer select
  const opciones = document.querySelector("[name='especialidad']").options;
  for (let i = 0; i < opciones.length; i++) {
    const opcion = document.createElement('option');
    opcion.value = opciones[i].value;
    opcion.text = opciones[i].text;
    nuevoSelect.appendChild(opcion);
  }

  especialidadesContainer.appendChild(nuevoSelect);
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
    // Obtener todas las especialidades seleccionadas
    let especialidades = [];
    nuevoDoctorForm.querySelectorAll("[name='especialidad']").forEach(select => {
      especialidades.push(select.value);
    });

  
    fetch('/doctor/registrar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombres, pApellido, sApellido, fechaNacimiento, sexo, ci, email, direccion, matricula, telefonos, especialidades })
    })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        location.reload();
        closeModal();
        // cargarEgresos();
        // cargarTiposEgreso();
      })
      .catch(error => console.error('Error al registrar doctor:', error));
  }


function openEditModal(doctor_id, nombres, p_apellido, s_apellido, fecha_nacimiento, sexo, ci, email, direccion) {
  let editDoctorForm = document.getElementById("editDoctorForm");

  editDoctorForm.querySelector("[name='doctor_id']").value = doctor_id;
  editDoctorForm.querySelector("[name='nombres']").value = nombres;
  editDoctorForm.querySelector("[name='p_apellido']").value = p_apellido;
  editDoctorForm.querySelector("[name='s_apellido']").value = s_apellido;
  editDoctorForm.querySelector("[name='fecha']").value = fecha_nacimiento;
  editDoctorForm.querySelector("[name='sexo']").value = sexo;
  editDoctorForm.querySelector("[name='ci']").value = ci;
  editDoctorForm.querySelector("[name='email']").value = email;
  editDoctorForm.querySelector("[name='direccion']").value = direccion;
  // editDoctorForm.querySelector("[name='matricula']").value = matricula;

  document.getElementById('editModal').style.display = 'block';
}


// function activar_inactivar(doctor_id, doctor_estado) {
//   let proceder = false;

//   // si se retira un doctor activo, avisar de que se liberarán los consultorios
//   if(doctor_estado == 'A' && confirm("¿Retirar a este doctor hará que todos sus consultorios asignados ahora estén libres. Estás seguro de continuar?")){
//       proceder = true;
//   }
//   if(doctor_estado == 'I'){ proceder = true; }

//   if(proceder){
//     fetch('/doctor/activar_inactivar', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ doctor_id, doctor_estado })
//     })
//       .then(response => response.json())
//       .then(data => {
//         alert(data.message);
//         location.reload();
//         // closeModal();
//         // cargarEgresos();
//         // cargarTiposEgreso();
//       })
//       .catch(error => console.error('Error al registrar egreso:', error));
//   }


  

// }

function editarDoctor() {
  // let descartado = document.getElementById("edit_descartado").checked ? 1 : 0;

  let editDoctorForm = document.getElementById("editDoctorForm");

  let doctorId = editDoctorForm.querySelector("[name='doctor_id']").value;
  let nombres = editDoctorForm.querySelector("[name='nombres']").value;
  let pApellido = editDoctorForm.querySelector("[name='p_apellido']").value;
  let sApellido = editDoctorForm.querySelector("[name='s_apellido']").value;
  let fechaNacimiento = editDoctorForm.querySelector("[name='fecha']").value;
  let sexo = editDoctorForm.querySelector("[name='sexo']").value;
  let ci = editDoctorForm.querySelector("[name='ci']").value;
  let email = editDoctorForm.querySelector("[name='email']").value;
  let direccion = editDoctorForm.querySelector("[name='direccion']").value;
  // let matricula = editDoctorForm.querySelector("[name='matricula']").value;

  fetch('/doctor/editar_doctor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doctorId, nombres, pApellido, sApellido, fechaNacimiento, sexo, ci, email, direccion })
  })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      location.reload();
      closeModal();
      // cargarEgresos();
      // cargarTiposEgreso();
    })
    .catch(error => console.error('Error al editar doctor:', error));
}

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