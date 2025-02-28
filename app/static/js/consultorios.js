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
  
  
  function openEditModal(id, fecha, monto, observacion, tipo, descartado) {
    document.getElementById('edit_id').value = id;
    document.getElementById('edit_fecha').value = fecha;
    document.getElementById('edit_monto').value = monto;
    document.getElementById('edit_observacion').value = observacion;
    document.getElementById('edit_egreso_tipo_id').value = tipo;
    document.getElementById('edit_descartado').checked = descartado;
  
    document.getElementById('editModal').style.display = 'block';
  }