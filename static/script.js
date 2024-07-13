// Methods - Page: Registrar paseo

function cargarImagen(elemento){
    let imagenSeleccionada = elemento.value;
    let numeroImagen = elemento.id.split('imagen')[1];

    if (imagenSeleccionada !== "") { //Imagen cargada
        let archivo = elemento.files[0]
        let img = new Image();

        img.onload =  function(){
            if (this.width.toFixed(0) > 500 && this.height.toFixed(0) > 400){
                alert('Intenta subir otra imagen con las dimensiones permitidas. Ancho máximo: 500px, Alto máximo: 400px.');
                elemento.value = "";
            }else{
                cargarCarrusel(img.src, numeroImagen);
            }
        }
        img.src = URL.createObjectURL(archivo);

    } else { //Cancela carga
        document.getElementById('papelera'+numeroImagen).setAttribute('hidden', true);
        this.cambiarVistaP(numeroImagen);
    }
}

function cargarCarrusel(url, numeroImagen){
    let carrusel = document.getElementById('carrusel');
    let divSinImagen = document.getElementById('noImagen');
    let divs = carrusel.getElementsByTagName('div'); //Divs de las imagenes

    // Habilitar papelera
    document.getElementById('papelera'+numeroImagen).removeAttribute('hidden');

    //Cargar vista previa de las imágenes
    divSinImagen.setAttribute('hidden', true); //ocultar el div sin imagenes
    
    //Carrusel
    carrusel.removeAttribute('hidden'); //Habilitar

    //Quitar el activo de otra imagen
    let imagenActiva = document.getElementsByClassName('carousel-item active ms-5 me-5');
    if (imagenActiva.length > 0){ imagenActiva[0].setAttribute('class','carousel-item ms-5 me-5')};

    //Verificar si ya se habia cargado imagen en el mismo input 
    let divPrevio = document.getElementById('prev'+numeroImagen);
    if (divPrevio === null){ 
        //Crear el div y la imagen nueva
        let div = document.createElement('div');
        div.setAttribute('class', "carousel-item active ms-5 me-5");
        div.setAttribute('style', 'width: 80%');
        let img = document.createElement('img');
        img.setAttribute('class', 'd-block w-100 img-thumbnail');
        img.setAttribute('style', 'border: 2px solid #000000');
        img.setAttribute('src', url);
        div.setAttribute('id', 'prev'+numeroImagen);
        div.appendChild(img);
        carrusel.appendChild(div);

    } else {
        //Reemplazar foto
        divPrevio.getElementsByTagName('img')[0].setAttribute('src', url);
        divPrevio.setAttribute('class', 'carousel-item active ms-5 me-5');
    }
    
    //Botones carrusel
    if (divs.length > 1){
        document.getElementById('botonPrev').removeAttribute('hidden');
        document.getElementById('botonNext').removeAttribute('hidden');
    }
        
}

function eliminarImagen(elemento) {
    let numeroImagen = elemento.id.split('papelera')[1];
    let nombreArchivo = document.getElementById('imagen'+numeroImagen);
    
    //Deshabilitar papelera y eliminar imagen
    nombreArchivo.value = "";
    elemento.setAttribute('hidden',true);

    //Cambiar vista previa
    this.cambiarVistaP(numeroImagen);
}

function cambiarVistaP(numeroImagen){

    let carrusel = document.getElementById('carrusel');
    let divSinImagen = document.getElementById('noImagen');
    let divEliminado = document.getElementById('prev'+numeroImagen);
    let estadoDiv = divEliminado.className;
    carrusel.removeChild(divEliminado);
    let divs = carrusel.getElementsByTagName('div'); //Divs de las imagenes

    //Verificar si quedan imagenes
    if (divs.length > 0){
        if(estadoDiv === 'carousel-item active ms-5 me-5'){ //Eliminando imagen activa
            divs[0].setAttribute("class", 'carousel-item active ms-5 me-5'); //Dar el focus a otra imagen
        } 

        if(divs.length === 1){ //Ocultar botones - Solo queda una imagen
            document.getElementById('botonPrev').setAttribute('hidden', true);
            document.getElementById('botonNext').setAttribute('hidden', true);
        }

    }else{
        //Ocultar carrusel
        carrusel.setAttribute('hidden', true);
        //Habilitar div sin imagen
        divSinImagen.removeAttribute('hidden');
        //Ocultar botones
        document.getElementById('botonPrev').setAttribute('hidden', true);
        document.getElementById('botonNext').setAttribute('hidden', true);
    }

}

function seleccionarEsquema(elemento){
    let opcionSeleccionada = elemento.value;
    let texto1 = document.getElementById('esquema');
    let input1 = document.getElementById('esquema1');
    let texto2 = document.getElementById('esquema2');
    let input2 = document.getElementById('esquema3');

    //Configurar las opciones según el esquema
    if (opcionSeleccionada === 'Volumen'){

        texto1.removeAttribute('hidden');
        texto1.textContent = 'Punto Equilibrio';
        
        input1.removeAttribute('hidden');
        input1.setAttribute('type', 'number'); 
        input1.setAttribute('name', 'equilibrio');
        input1.setAttribute('min','0');
        input1.setAttribute('required', '');
        input1.value = null;

        texto2.removeAttribute('hidden');
        texto2.textContent = 'Descuento';

        input2.removeAttribute('hidden');
        input2.setAttribute('name','descuento');
        input2.setAttribute('required', '');
        input2.value = null;

    } else if (opcionSeleccionada === 'Aerolínea'){

        texto1.removeAttribute('hidden');
        texto1.textContent = 'Fecha Aumento';

        input1.removeAttribute('hidden');
        input1.removeAttribute('min');
        input1.setAttribute('type', 'date'); 
        input1.setAttribute('name', 'fechaAumento');
        input1.setAttribute('required', '');
        input1.value = null;

        texto2.removeAttribute('hidden');
        texto2.textContent = 'Valor Aumento';

        input2.removeAttribute('hidden');
        input2.setAttribute('name','aumento');
        input2.setAttribute('required', '');
        input2.value = null;

    } else {
        document.getElementById('esquema').setAttribute('hidden', 'true');
        document.getElementById('esquema1').setAttribute('hidden', 'true');
        document.getElementById('esquema2').setAttribute('hidden', 'true');
        document.getElementById('esquema3').setAttribute('hidden', 'true');
        document.getElementById('valor').value = null;
    }
}

function confirmarDesembolso(elemento){
    if (elemento.checked){ // Chequea la columna de completado

        // Confirmacion del desembolso
        var myModal = new bootstrap.Modal(document.getElementById('confirmacion'+elemento.getAttribute('data-python-variable')));
        myModal.show();
    }
}

function completarDesembolso(elemento){

    // ID del desembolso
    let id = elemento.getAttribute('data-python-variable');

    if (elemento.value === 'confirmar'){
        //Obtenemos el token CSRF
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                    break;
                }
            }
        }

        // Obtenemos el comprobante
        let comprobante = document.getElementsByName('comprobante' + id)[0].files[0]
        const formData = new FormData();
        formData.append('comprobante', comprobante);
        formData.append('desembolsoID', id);
        
        //Lanzamos una solicitud POST
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': cookieValue
            },
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            document.open();
            document.write(html);
            document.close();
        })
        .catch(error => console.error('Error:', error));

    } else if (elemento.value === 'cancelar'){
        document.getElementsByName(id)[0].checked = false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const reservaModal = new bootstrap.Modal(document.getElementById('reservaModal'));
    const reservaForm = document.getElementById('reserva-form');
    const paseoIdInput = document.getElementById('paseo-id');

    document.querySelectorAll('.reservar-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            paseoIdInput.value = event.target.dataset.id;
            reservaModal.show();
        });
    });

    reservaForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(reservaForm);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('{% url "crearReserva" %}', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                reservaModal.hide();
                alert('Reserva creada con éxito');
            } else {
                alert('Error al crear la reserva');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});