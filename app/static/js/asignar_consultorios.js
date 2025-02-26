document.addEventListener('DOMContentLoaded', function() {
  // Asegúrate de que jQuery esté cargado
  if (typeof $ === 'undefined') {
    console.error("jQuery no está cargado");
    return;
  }

  const openModalBtn = document.getElementById('btnOpenModal');
  const modal = document.getElementById('myModal');
  const closeModalBtn = document.getElementById('closeModal');

  // Abrir modal
  openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block';
  });

  // Cerrar modal con X
  closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // Cerrar modal si se hace clic fuera del contenido
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });

  // Envío del formulario para asignar consultorio
  $("#formAsignacion").submit(function(e){
      e.preventDefault();
      var formData = $(this).serialize();
      $.post("/asignar_consultorios/guardar", formData, function(response){
          $("#mensaje").text(response.message);
          if(response.status === "success"){
              // Recargar la página para actualizar la tabla
              location.reload();
          }
      }, "json").fail(function(error) {
          console.error("Error en guardar asignación:", error);
      });
  });
  
  // Delegación de eventos para el botón de inhabilitar
  $(document).on('click', '.btnDeshabilitar', function(e){
      e.preventDefault();
      var asignacionId = $(this).data("id");
      console.log("Intentando inhabilitar asignación:", asignacionId);
      $.post("/asignar_consultorios/deshabilitar/" + asignacionId, function(response){
          console.log("Respuesta de deshabilitar:", response);
          $("#mensaje").text(response.message);
          if(response.status === "success"){
              // Remover la fila de la tabla con efecto fadeOut
              $("#asignacion-" + asignacionId).fadeOut("slow", function(){
                  $(this).remove();
              });
          }
      }, "json").fail(function(error) {
          console.error("Error en la petición de inhabilitar:", error);
      });
  });
});
