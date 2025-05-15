let cronometro;
let centesimas = 0;
let segundos = 0;
let minutos = 0;
let corriendo = false;

const display = document.getElementById("cronometro");
const btnIniciar = document.getElementById("iniciar");
const btnDetener = document.getElementById("detener");
const btnReiniciar = document.getElementById("reiniciar");
const btnGuardar = document.getElementById("guardarIntento");
const msgGuardado = document.getElementById("guardadoExito");

function actualizarDisplay() {
    let m = minutos < 10 ? "0" + minutos : minutos;
    let s = segundos < 10 ? "0" + segundos : segundos;
    let c = centesimas < 10 ? "0" + centesimas : centesimas;
    display.textContent = `${m}:${s}.${c}`;
}

function iniciar() {
    if (!corriendo) {
        cronometro = setInterval(() => {
            centesimas++;
            if (centesimas === 100) {
                centesimas = 0;
                segundos++;
            }
            if (segundos === 60) {
                segundos = 0;
                minutos++;
            }
            actualizarDisplay();
        }, 10);
        corriendo = true;
        btnDetener.disabled = false;
        btnGuardar.disabled = true;
    }
}

function detener() {
    clearInterval(cronometro);
    corriendo = false;
    btnGuardar.disabled = false;
}

function reiniciar() {
    clearInterval(cronometro);
    centesimas = 0;
    segundos = 0;
    minutos = 0;
    actualizarDisplay();
    corriendo = false;
    btnGuardar.disabled = true;
    btnDetener.disabled = true;
}

function mostrarMensaje(elemento, duracion = 3000) {
    elemento.style.display = "block";
    setTimeout(() => {
        elemento.style.display = "none";
    }, duracion);
}

async function cargarResultados() {
    try {
        const response = await fetch('/obtener_resultados');
        const html = await response.text();
        document.getElementById("tablaResultados").innerHTML = html;
    } catch (error) {
        console.error('Error al cargar resultados:', error);
    }
}

// Event Listeners
btnIniciar.addEventListener("click", iniciar);
btnDetener.addEventListener("click", detener);
btnReiniciar.addEventListener("click", reiniciar);

btnGuardar.addEventListener("click", async () => {
    const nombre = document.getElementById("nombreRobot").value.trim();
    if (!nombre) {
        alert("Debes ingresar el nombre del robot antes de guardar.");
        return;
    }

    const tiempo = `${minutos}:${segundos}.${centesimas}`;

    try {
        const response = await fetch("/guardar_intento", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ nombre, tiempo })
        });

        const data = await response.json();
        if (data.success) {
            mostrarMensaje(msgGuardado);
            await cargarResultados();
            reiniciar();
        } else {
            alert("Error al guardar intento: " + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Error al guardar el intento");
    }
});

// Registro del robot
const formRobot = document.getElementById("formRobot");
const msgRegistro = document.getElementById("registroExito");

formRobot.addEventListener("submit", async function(e) {
    e.preventDefault();
    const nombre = document.getElementById("nombreRobot").value.trim();

    try {
        const response = await fetch("/registrar_robot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ nombre })
        });

        const data = await response.json();
        if (data.success) {
            mostrarMensaje(msgRegistro);
            document.getElementById("nombreRobot").value = "";
            await cargarResultados();
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Error al registrar el robot");
    }
});

// Template para resultados
document.addEventListener('DOMContentLoaded', () => {
    actualizarDisplay();
    cargarResultados();
});
