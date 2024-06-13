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
                URL.revokeObjectURL(img.src);
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
    let imagenActiva = document.getElementsByClassName('carousel-item active ms-5');
    if (imagenActiva.length > 0){ imagenActiva[0].setAttribute('class','carousel-item ms-5')};

    //Verificar si ya se habia cargado imagen en el mismo input 
    let divPrevio = document.getElementById('prev'+numeroImagen);
    if (divPrevio === null){ 
        //Crear el div y la imagen nueva
        let div = document.createElement('div');
        div.setAttribute('class', "carousel-item active ms-5");
        div.setAttribute('style', 'width: 70%');
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
        divPrevio.setAttribute('class', 'carousel-item active ms-5');
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
    let url = divEliminado.getElementsByTagName('img')[0].src;
    // URL.revokeObjectURL(url); //Eliminar imagen del almacenamiento local
    carrusel.removeChild(divEliminado);
    let divs = carrusel.getElementsByTagName('div'); //Divs de las imagenes

    //Verificar si quedan imagenes
    if (divs.length > 0){
        if(estadoDiv === 'carousel-item active'){ //Eliminando imagen activa
            divs[0].setAttribute("class", 'carousel-item active') //Dar el focus a otra imagen
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

function seleccionarChiva(elemento, disponibilidad) {
    let opcionSeleccionada = elemento.value;
    // let placa = opcionSeleccionada.split(' - ');
    // Hacer consulta a bd para obtener la capacidad de la chiva

    // Habilitar/Deshabilitar el campo de cupos
    if (opcionSeleccionada !== 'Seleccionar'){
        // document.getElementById('cupos').removeAttribute('hidden');
        // //Debemos conectarnos a la bd para conocer la capacidad de la chiva seleccionada
        // const sqlite3 = require('sqlite3').verbose();
        // // Conectarse a la base de datos
        // const db = new sqlite3.Database('/db.sqlite3', sqlite3.OPEN_READWRITE, (err) => {
        // if (err) {    
        //     console.error(err.message);
        // }
        // console.log('Conectado a la base de datos SQLite.');                            
        // });

        // // Realizar consulta
        // const sql = 'SELECT * FROM paseos_chiva WHERE placa = ? ';

        // db.all(sql, [placa], (err, rows) => {
        // if (err) {
        //     throw err;
        // }
        // rows.forEach((row) => {
        //     console.log(row);
        // });
        // });

        // // Cerrar la conexión con la base de datos
        // db.close((err) => {
        // if (err) {
        //     console.error(err.message);
        // }
        // console.log('Conexión a la base de datos cerrada.');
        // });

        document.getElementById('valorCupos').value = disponibilidad;
        document.getElementById('valorCupos').removeAttribute('hidden');

    } else {
        document.getElementById('cupos').setAttribute('hidden', 'true');
        document.getElementById('valorCupos').setAttribute('hidden', 'true');
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

        texto2.removeAttribute('hidden');
        texto2.textContent = 'Descuento';

        input2.removeAttribute('hidden');
        input2.setAttribute('name','descuento');

    } else if (opcionSeleccionada === 'Aerolínea'){

        texto1.removeAttribute('hidden');
        texto1.textContent = 'Fecha Aumento';

        input1.removeAttribute('hidden');
        input1.setAttribute('type', 'date'); 
        input1.setAttribute('name', 'fechaAumento');

        texto2.removeAttribute('hidden');
        texto2.textContent = 'Valor Aumento';

        input2.removeAttribute('hidden');
        input2.setAttribute('name','aumento');

    } else {
        document.getElementById('esquema').setAttribute('hidden', 'true');
        document.getElementById('esquema1').setAttribute('hidden', 'true');
        document.getElementById('esquema2').setAttribute('hidden', 'true');
        document.getElementById('esquema3').setAttribute('hidden', 'true');
    }
}