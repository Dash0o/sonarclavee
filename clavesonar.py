import streamlit como st
import numpy como np
import io
import wave
import matplotlib.pyplot como plt

# ---------------------------
# Configuración general de la página
# ---------------------------
st.set_page_config(page_title="SonarClave", layout="ancho", page_icon="🎵")

# ---------------------------
# Definiciones musicales
# ---------------------------
NOTAS_NOMBRES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
ÍNDICE_DE_NOTA = {n: i para i, n en enumerar(NOMBRES_DE_NOTA)}

FÓRMULAS DE ACORDES = {
"alcalde": [0, 4, 7],
"menor": [0, 3, 7],
}

# ---------------------------
# Funciones y bloques de comando para acordes
# ---------------------------
def pitch_class_to_freq(nombre_pc: str, octava=4):
idx = ÍNDICE_DE_NOTA[nombre_de_pc]
midi = idx + (octava + 1) * 12
devuelve 440.0 * (2 ** ((midi - 69) / 12.0))

def build_chord(raíz: str, tipo_de_acorde: str):
root_idx = ÍNDICE_DE_NOTA[raíz]
fórmula = FÓRMULAS_DE_ACORDES.get(tipo_de_acorde, FÓRMULAS_DE_ACORDES["mayor"])
notas = [NOMBRES_DE_NOTAS[(id_raíz + intervalo) % 12] para el intervalo en la fórmula]
notas de devolución

def dibujar_diagrama_de_acordes(notas_de_acordes):
"""Dibuja un diagrama visual tipo teclado para un acorde"""
fig, ax = plt.subplots(figsize=(6, 1.5))
all_keys = NOMBRES_DE_NOTAS

# Dibujar teclas blancas y negras
para i, n en enumerate(all_keys):
color = 'negro' si '#' en n de lo contrario 'blanco'
x = yo
si color == 'blanco':
ax.add_patch(plt.Rectangle((x, 0), 1, 1, color de la cara='blanco', color del borde='negro'))
demás:
ax.add_patch(plt.Rectangle((x - 0.25, 0.5), 0.5, 0.5, color de la cara='negro', color del borde='negro'))

# Resaltar notas del acorde
para n en notas de acorde:
i = ÍNDICE_NOTA[n]
ax.add_patch(plt.Rectangle((i, 0), 1, 1, color de la cara='dorado', alfa=0.6, color del borde='rojo', ancho de línea=2))
ax.text(i + 0.5, 0.5, n, ha='centro', va='centro', color='negro', tamaño de fuente=12, peso='negrita')

ax.set_xlim(0, 12)
ax.set_ylim(0, 1)
ax.axis('off')
buf = io.BytesIO()
plt.tight_layout()
plt.savefig(buf, formato='png')
buf.seek(0)
plt.close(fig)
devolver buf

def sintetizar_acorde(nombres_de_nota, octava_base=4, duración_s=2.0, sr=44100):
"""Genera un audio WAV de un acorde"""
t = np.linspace(0, duración_s, int(sr * duración_s), Falso)
señal_de_acorde = np.zeros_like(t)
para i, n en enumerate(nombres_de_nota):
octava = octava_base
si i > 1:
octava = octava base - 1
frecuencia = clase_de_tono_a_frecuencia(n, octava=octava)
onda_i = np.sin(2 * np.pi * frecuencia * t) * np.exp(-2.0 * t)
señal_de_cuerda += onda_i
señal_de_acorde = señal_de_acorde / (np.max(np.abs(señal_de_acorde)) + 1e-9) * 0.9
pcm_data = (señal_de_acorde * 32767).astype(np.int16)
biografía = io.BytesIO()
con wave.open(bio, 'wb') como wf:
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(sr)
wf.writeframes(pcm_data.tobytes())
bio.seek(0)
volver biografía

# ---------------------------
# Navegación entre páginas
# ---------------------------
page = st.sidebar.radio("Navegar a:", ["Inicio", "Generador de Piano", "Contacto"])

# ---------------------------
# Inicio
# ---------------------------
si página == "Inicio":
st.title("🎵 Bienvenido a SonarClave")
st.header("Para que sirva")
st.write("""
SonarClave es una herramienta innovadora diseñada para músicos y entusiastas del piano que desean explorar la armonía y la teoría musical de manera interactiva. Esta plataforma permite generar acordes de piano de forma sencilla, escuchar su sonido y visualizar un diagrama claro de las notas correspondientes. Gracias a esta combinación de funciones auditivas y visuales, los usuarios pueden comprender de manera práctica cómo se construyen los acordes y cómo se relacionan entre sí dentro de diferentes tonalidades. SonarClave resulta especialmente útil para quienes no tienen acceso a un piano físico, ya que ofrece una experiencia de aprendizaje completa y accesible desde cualquier dispositivo. Además, su enfoque interactivo fomenta la experimentación y la práctica constante, acelerando el proceso de aprendizaje y haciendo que la teoría musical sea mucho más intuitiva y divertida.
""")

st.header("Usuario objetivo")
st.write("""
- Edad: 12 hasta la muerte
- Ubicación: cualquier lugar con acceso a internet.
- Estilo de vida: estudiantes, músicos principiantes, autodidactas.
- Necesidad: aprender acordes de piano de forma visual y auditiva
""")

st.header("Cómo ayuda esta aplicación")
st.write("""
SonarClave permite generar acordes de piano, escuchar su sonido y ver un diagrama visual de las notas.
Esto facilita el aprendizaje práctico y rápido, especialmente para quienes no pueden acceder a un piano físico.
""")


st.image(" https://tse1.mm.bing.net/th/id/OIP.Zh8QWlme8zVd-Rny9Pc8oAHaHa?rs=1&pid=ImgDetMain&o=7&rm=3 ")

# ---------------------------
# Generador de piano
# ---------------------------
página elif == "Generador de Piano":
st.title("SonarClave: Generador de Acordes de Piano")
st.write("Genera acordes de piano y escucha su sonido de manera inmediata.")

# Barra lateral para opciones
st.sidebar.header("Configuración del acorde")
root = st.sidebar.selectbox("Nota raíz", NOTE_NAMES)
chord_type = st.sidebar.selectbox("Tipo de acorde", list(CHORD_FORMULAS.keys()))
audio_octave = st.sidebar.slider("Octava base (nota raíz)", 2, 5, 4)
duracion = st.sidebar.slider("Duración del audio (segundos)", 1.0, 5.0, 2.0, step=0.5)
generar = st.sidebar.button("Generar acorde")

si generar:
notas_de_acorde = construir_acorde(raíz, tipo_de_acorde)
st.subheader(f"Acorde: {raíz} {tipo_de_acorde}")
st.markdown(f"**Notas:** {' — '.join(chord_notes)}")

# Diagrama visual
img_buf = dibujar_diagrama_de_acordes(notas_de_acordes)
st.image(img_buf, caption=f"Representación del acorde {root} {chord_type}")

# Audio del acorde
audio_bytes = sintetizar_acorde(notas_del_acorde, octava_base=octava_de_audio, duración_s=duración)
st.audio(audio_bytes, formato='audio/wav')

# ---------------------------
# Contacto de la página
# ---------------------------
página elif == "Contacto":
st.title("📞 Contacto")
st.header("Integrantes del equipo")
st.write("""
- Juan Pérez
- María López
- Carlos Sánchez


Correo de contacto: Sonarclaveymusicologistica@gmail.com
""")