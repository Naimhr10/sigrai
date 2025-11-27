const mensajes = document.getElementById("messages");
const input = document.getElementById("mensaje");
const btnEnviar = document.getElementById("enviar");
const btnSubir = document.getElementById("subir");
const inputImagen = document.getElementById("imagen");

function agregarMensaje(texto, tipo) {
  const msg = document.createElement("div");
  msg.classList.add("msg", tipo);
  msg.innerText = texto;
  mensajes.appendChild(msg);
  mensajes.scrollTop = mensajes.scrollHeight;
}

btnEnviar.onclick = async () => {
  const texto = input.value.trim();
  if (!texto) return;
  agregarMensaje("🧑‍💻 " + texto, "user");
  input.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mensaje: texto }),
  });
  const data = await res.json();
  agregarMensaje("🤖 " + data.respuesta, "bot");
};

btnSubir.onclick = async () => {
  const file = inputImagen.files[0];
  if (!file) return alert("Selecciona una imagen primero 🩻");
  const formData = new FormData();
  formData.append("imagen", file);

  const res = await fetch("/analizar", { method: "POST", body: formData });
  const data = await res.json();
  agregarMensaje("📊 " + data.respuesta, "bot");
};