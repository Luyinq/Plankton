$(document).ready(function () {
  //VALIDAR CAMPO - SOLO GMAIL
  jQuery.validator.addMethod('gmail', function (value, element) {
    return this.optional(element) || /^[a-z0-9](\.?[a-z0-9]){0,}@gmail\.com$/i.test(value);
  }, "El correo solo puede ser gmail.");
  //VALIDAR CAMPO - SOLO LETRAS
  jQuery.validator.addMethod("sololetras", function (value, element) {
    return this.optional(element) || /^[a-z]+$/i.test(value);
  }, "Solo ingrese letras.");
  //VALIDAR CAMPO - SOLO LETRAS Y ESPACIOS
  jQuery.validator.addMethod("sololetrasyespacios", function (value, element) {
    return this.optional(element) || /^[a-z\s]+$/i.test(value);
  }, "Solo ingrese letras y espacios.");
  //CAMBIAR MENSAJE DE REQUERIDO PARA TODOS LOS CAMPOS
  jQuery.extend(jQuery.validator.messages, {
    required: "Este campo es obligatorio.",
    digits: "Por favor, ingrese solo dígitos."
  });
  //VALIDAR CAMPOS DE FORMULARIO CONTACTO5
  $("#contact-form").validate({
    rules: {
      nombre: {
        required: true,
        minlength: 3,
        sololetrasyespacios: true
      },
      correo: {
        required: true,
        email: true,
        gmail: true
      },
      captcha: {
        required: true,
      },
      asunto: {
        required: true,
        sololetrasyespacios: true,
        minlength: 4
      },
      mensaje: {
        required: true,
        minlength: 20
      },
    },
    messages: {
      nombre: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      correo: {
        email: "El correo debe tener el siguiente formato: correo@dominio.xx"
      },
      asunto: {
        minlength: "El asunto debe tener al menos 4 letras."
      },
      mensaje: {
        minlength: "El mensaje debe tener al menos 20 carácteres."
      }
    }


  });
  //VALIDAR CONTACT-FORM
  $(function () {
    $('#contact-form').submit(function () {
      if ($(this).valid()) {
        var response = grecaptcha.getResponse();
        if (response.length === 0) {
          alert("Necesitas rellenar el captcha");
          return false;
        } else {
          alert('El mensaje se ha enviado con éxito');
          return true;

        }
      }
    });
  });

  //region
  $("#region").ready(function () {
    $.get("https://apis.digital.gob.cl/dpa/regiones",
      function (data) {
        //en data capturo lo que me retorna la API
        $.each(data, function (i, item) {
          //por cada item agrego una nueva fila a mi tabla
          $("#region").append(`<option value="${item.codigo}">${item.nombre}</option>`);
        });
      });
  });

  //provincia
  $("#region").change(function () {
    var select = document.getElementById("provincia");
    var length = select.options.length;
    for (i = 1; i < length;) {
      select.options[i] = null;
      length = select.options.length;
    }

    var select = document.getElementById("comuna");
    var length = select.options.length;
    for (i = 1; i < length;) {
      select.options[i] = null;
      length = select.options.length;
    }
    $.get("https://apis.digital.gob.cl/dpa/provincias",
      function (data) {
        //en data capturo lo que me retorna la API
        $.each(data, function (i, item) {
          if (item.codigo_padre == $("#region").val()) {
            //por cada item agrego una nueva fila a mi tabla
            $("#provincia").append(`<option value="${item.codigo}">
                                     ${item.nombre}
                                </option>`);
          }
        });
      });
  });


  //comuna
  $("#provincia").change(function () {
    var select = document.getElementById("comuna");
    var length = select.options.length;
    for (i = 1; i < length;) {
      select.options[i] = null;
      length = select.options.length;
    }
    $.get("https://apis.digital.gob.cl/dpa/comunas",
      function (data) {
        //en data capturo lo que me retorna la API
        $.each(data, function (i, item) {
          if (item.codigo_padre == $("#provincia").val()) {
            //por cada item agrego una nueva fila a mi tabla
            $("#comuna").append(`<option value="${item.codigo}">
                                     ${item.nombre}
                                </option>`);
          }
        });
      });
  });

  //VALIDAR CAMPOS DE FORMULARIO CONTACTO5
  $("#donation-form").validate({
    rules: {
      nombre: {
        required: true,
        minlength: 3,
        sololetras: true
      },
      apellido: {
        required: true,
        sololetras: true,
        minlength: 3
      },
      correo: {
        required: true,
        email: true
      },
      celular: {
        required: true,
        digits: true,
        min: 900000000,
        max: 999999999
      },
      calle: {
        required: true,
        sololetrasyespacios: true,
        minlength: 5
      },
      region: {
        required: true
      },
      provincia: {
        required: true
      },
      comuna: {
        required: true
      },
      monto: {
        required: true,
        digits: true,
        min: 1000,
        max: 20000
      }
    },
    messages: {
      nombre: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      correo: {
        email: "El correo debe tener el siguiente formato: correo@dominio.xx"
      },
      celular: {
        min: "El número debe tener el siguiente formato 9XXXXXXXX.",
        max: "El número debe tener el siguiente formato 9XXXXXXXX.",
        digits: "Por favor, ingrese un solo dígitos.",
        number: "Por favor, ingrese un solo dígitos."
      },
      calle: {
        minlength: "El mensaje debe tener al menos 5 letras."
      },
      monto: {
        min: "El monto a donar puede ser entre 1.000 a 20.000 CLP",
        max: "El monto a donar puede ser entre 1.000 a 20.000 CLP",
        digits: "Por favor, ingrese un solo dígitos.",
        number: "Por favor, ingrese un solo dígitos."
      }
    }


  });

  //VALIDAR DONATION-FORM
  $(function () {
    $('#donation-form').submit(function () {
      if ($(this).valid()) {
        alert('Será redireccionado a la página de pago');
      }
    });
  });


  //VALIDAR CAMPOS DE FORMULARIO REGISTRO
  $("#registrogeneral").validate({
    rules: {
      nombre: {
        required: true,
        minlength: 3,
      },
      descripcion: {
        required: true,
        minlength: 10,
        maxlength: 200,
      },
      precio: {
        required: true,
        digits: true,
      },
      cantidad: {
        required: true,
        digits: true,
      },
      descuento: {
        required: true,
        digits: true,
        max: 100,
        min: 0
      },
      foto: {
        required: true,
      },
      categoria: {
        required: true,
      },
      apaterno: {
        required: true,
        minlength: 3,
      },
      amaterno: {
        required: true,
        minlength: 3,
      },
      correo: {
        required: true,
        email: true
      },
      run: {
        digits: true,
        required: true,
        min: 90000000,
        max: 999999999,
      },
      celular: {
        required: true,
        digits: true,
        min: 900000000,
        max: 999999999
      }
    },
    messages: {
      nombre: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      descripcion: {
        maxlength: "La descripción no puede pasar los 200 carácteres.",
        minlength: "La descripción debe tener al menos 10 letras."
      },
      descuento: {
        max: "El máximo es de 100.",
        min: "El mínimo es de es 0"
      },
      apaterno: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      amaterno: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      correo: {
        email: "El correo debe tener el siguiente formato: correo@dominio.xx"
      },
      run: {
        min: "El mínimo de números es 8.",
        max: "El máximo de números es 9.",
        digits: "Solo números, si su rut tiene K, cámbielo por un 0."
      },
      celular: {
        min: "El número debe tener el siguiente formato 9XXXXXXXX.",
        max: "El número debe tener el siguiente formato 9XXXXXXXX.",
        digits: "Por favor, ingrese un solo dígitos.",
        number: "Por favor, ingrese un solo dígitos."
      },
      cantidad: {
        digits: "Por favor, ingrese un solo dígitos.",
      }

    }


  });
  //VALIDAR REGISTRO-GENERAL
  $(function () {
    $('#registrogeneral').submit(function () {
      if ($(this).valid()) {
        alert('La solicitud se generó con éxito.');
      }
    });
  });


  //VALIDAR CAMPOS DE FORMULARIO MODIFICAR
  $("#modificar general").validate({
    rules: {
      nombre: {
        required: true,
        minlength: 3,
      },
      descripcion: {
        required: true,
        minlength: 10,
        maxlength: 200,
      },
      precio: {
        required: true,
        digits: true,
      },
      cantidad: {
        required: true,
        digits: true,
      },
      descuento: {
        required: false,
        digits: true,
        max: 100,
        min: 0
      },
      foto: {
        required: false,
      },
      categoria: {
        required: true,
      },
      apaterno: {
        required: true,
        minlength: 3,
      },
      amaterno: {
        required: true,
        minlength: 3,
      },
      correo: {
        required: true,
        email: true
      },
      run: {
        digits: true,
        required: true,
        min: 90000000,
        max: 999999999,
      },
      celular: {
        required: true,
        digits: true,
        min: 900000000,
        max: 999999999
      }
    },
    messages: {
      nombre: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      descripcion: {
        minlength: "La descripción debe tener al menos 10 letras.",
        maxlength: "La descripción no puede pasar los 200 carácteres."
      },
      descuento: {
        max: "El máximo es de 100.",
        min: "El mínimo es de 0"
      },
      apaterno: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      amaterno: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      correo: {
        email: "El correo debe tener el siguiente formato: correo@dominio.xx"
      },
      run: {
        min: "El mínimo de números es 8.",
        max: "El máximo de números es 9.",
        digits: "Solo números, si su rut tiene K, cámbielo por un 0."
      },
      celular: {
        min: "El número debe tener el siguiente formato 9XXXXXXXX.",
        max: "El número debe tener el siguiente formato 9XXXXXXXX.",
        digits: "Por favor, ingrese un solo dígitos.",
        number: "Por favor, ingrese un solo dígitos."
      },
      cantidad: {
        digits: "Por favor, ingrese un solo dígitos.",
      }

    }


  });
  //VALIDAR MODIFICAR-GENERAL
  $(function () {
    $('#modificargeneral').submit(function () {
      if ($(this).valid()) {
        alert('La solicitud se generó con éxito.');
      }
    });
  });

  $('.deleter').off().on('click',function () {
    
    return confirm("¿Desea continuar?");
    
    })


  $("#registro-form").validate({
    rules: {
      nombre: {
        required: true,
        minlength: 3,
        sololetrasyespacios: true
      },
      correo: {
        required: true,
        email: true,
        gmail: true
      },
      captcha: {
        required: true,
      },
      asunto: {
        required: true,
        sololetrasyespacios: true,
        minlength: 4
      },
      mensaje: {
        required: true,
        minlength: 20
      },
    },
    messages: {
      nombre: {
        minlength: "El nombre debe tener al menos 3 letras."
      },
      correo: {
        email: "El correo debe tener el siguiente formato: correo@dominio.xx"
      },
      asunto: {
        minlength: "El asunto debe tener al menos 4 letras."
      },
      mensaje: {
        minlength: "El mensaje debe tener al menos 20 carácteres."
      }
    }


  });
  //VALIDAR CONTACT-FORM
  $(function () {
    $('#registro-form').submit(function () {
      if ($(this).valid()) {
        var response = grecaptcha.getResponse();
        if (response.length === 0) {
          alert("Necesitas rellenar el captcha");
          return false;
        } else {
          alert('Felicidades. Te has registrado.');
          return true;

        }
      }
    });
  });


  $('.comprar').off().on('click',function () {
    
    return confirm("¿Desea continuar?");
    
    })






  });









