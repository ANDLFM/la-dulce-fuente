document.addEventListener("DOMContentLoaded", function () {
    // Animación de tarjetas en Inicio.
    const elementos = document.querySelectorAll(".producto-card, .promocion-card");

    if ("IntersectionObserver" in window && elementos.length) {
        const observador = new IntersectionObserver(function (entradas) {
            entradas.forEach(function (entrada) {
                if (entrada.isIntersecting) {
                    entrada.target.style.opacity = "1";
                    entrada.target.style.transform = "translateY(0)";
                    observador.unobserve(entrada.target);
                }
            });
        }, { threshold: 0.10 });

        elementos.forEach(function (elemento) {
            elemento.style.opacity = "0";
            elemento.style.transform = "translateY(25px)";
            elemento.style.transition = "opacity .6s ease, transform .6s ease";
            observador.observe(elemento);
        });
    }

    // Cierra el menú móvil después de elegir una opción.
    const enlaces = document.querySelectorAll("#menu .nav-link");
    enlaces.forEach(function (enlace) {
        enlace.addEventListener("click", function () {
            const menu = document.getElementById("menu");
            if (menu && menu.classList.contains("show") && window.bootstrap) {
                const instancia = bootstrap.Collapse.getOrCreateInstance(menu);
                instancia.hide();
            }
        });
    });

    // Validaciones del formulario de pedido.
    const formulario = document.getElementById("formPedido");
    const boton = document.getElementById("botonRegistrar");
    const fecha = document.getElementById("fecha_entrega");

    if (formulario && boton) {
        formulario.addEventListener("submit", function () {
            boton.disabled = true;
            boton.innerHTML = "Registrando pedido... 🍰";
        });
    }

    if (fecha) {
        fecha.addEventListener("change", function () {
            const seleccionada = new Date(this.value + "T00:00:00");
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);

            if (seleccionada < hoy) {
                alert("La fecha de entrega no puede ser anterior a hoy.");
                this.value = "";
            }
        });
    }
});
