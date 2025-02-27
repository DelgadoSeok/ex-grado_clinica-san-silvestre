function toggleMenu() {
  document.body.classList.toggle('menu-open');
}
function openModal() {
  document.getElementById('modal').style.display = 'block';
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
}

// registra nuevo consultorio en db
function registrar_consultorio() {
  let f_nuevo_consultorio = document.getElementById("f_nuevo_consultorio");

  let f_nro_consultorio = f_nuevo_consultorio.querySelector("[name='f_nro_consultorio']").value;
  let f_fecha_registro = f_nuevo_consultorio.querySelector("[name='f_fecha_registro']").value;
  let f_estado = f_nuevo_consultorio.querySelector("[name='f_estado']").value;

  fetch('/consultorios/registrar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ f_nro_consultorio, f_fecha_registro, f_estado })
  })
    .then(response => response.json())
    .then(data => {
      alert(data.message); // Muestra el mensaje devuelto por el backend
      if (data.success) {
        location.reload();  // Solo recarga si se registró correctamente
        closeModal();
      }
    })
    .catch(error => console.error('Error al registrar consultorio:', error));
}


function openEditModal(consultorio) {
  document.getElementById("editModal").style.display = "block";

  document.getElementById("edit_id_consultorio").value = consultorio.id;
  document.getElementById("edit_nro_consultorio").value = consultorio.nro_consultorio;
  document.getElementById("edit_estado").value = consultorio.estado;
}


function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

function actualizar_consultorio() {
  const id = document.getElementById("edit_id_consultorio").value;
  const nro_consultorio = document.getElementById("edit_nro_consultorio").value;
  const estado = document.getElementById("edit_estado").value;

  fetch(`/consultorios/actualizar/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id, nro_consultorio, estado })
  })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      if (data.success) {
        location.reload();
      }
    })
    .catch(error => console.error('Error al actualizar consultorio:', error));
}
