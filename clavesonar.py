import streamlit as st
import numpy as np
import io
import wave
import matplotlib.pyplot as plt

# ---------------------------
# Configuración general de la página
# ---------------------------
st.set_page_config(page_title="SonarClave", layout="wide", page_icon="🎵")

# ---------------------------
# Definiciones musicales
# ---------------------------
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_INDEX = {n: i for i, n in enumerate(NOTE_NAMES)}

CHORD_FORMULAS = {
    "mayor": [0, 4, 7],
    "menor": [0, 3, 7],
}

# ---------------------------
# Funciones y bloques de comando para acordes
# ---------------------------
def pitch_class_to_freq(pc_name: str, octave=4):
    idx = NOTE_INDEX[pc_name]
    midi = idx + (octave + 1) * 12
    return 440.0 * (2 ** ((midi - 69) / 12.0))

def build_chord(root: str, chord_type: str):
    root_idx = NOTE_INDEX[root]
    formula = CHORD_FORMULAS.get(chord_type, CHORD_FORMULAS["mayor"])
    notes = [NOTE_NAMES[(root_idx + interval) % 12] for interval in formula]
    return notes

def draw_chord_diagram(chord_notes):
    """Dibuja un diagrama visual tipo teclado para un acorde"""
    fig, ax = plt.subplots(figsize=(6, 1.5))
    all_keys = NOTE_NAMES

    # Dibujar teclas blancas y negras
    for i, n in enumerate(all_keys):
        color = 'black' if '#' in n else 'white'
        x = i
        if color == 'white':
            ax.add_patch(plt.Rectangle((x, 0), 1, 1, facecolor='white', edgecolor='black'))
        else:
            ax.add_patch(plt.Rectangle((x - 0.25, 0.5), 0.5, 0.5, facecolor='black', edgecolor='black'))

    # Resaltar notas del acorde
    for n in chord_notes:
        i = NOTE_INDEX[n]
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor='gold', alpha=0.6, edgecolor='red', linewidth=2))
        ax.text(i + 0.5, 0.5, n, ha='center', va='center', color='black', fontsize=12, weight='bold')

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

def synthesize_chord(note_names, base_octave=4, duration_s=2.0, sr=44100):
    """Genera un audio WAV de un acorde"""
    t = np.linspace(0, duration_s, int(sr * duration_s), False)
    chord_signal = np.zeros_like(t)
    for i, n in enumerate(note_names):
        octave = base_octave
        if i > 1:
            octave = base_octave - 1
        freq = pitch_class_to_freq(n, octave=octave)
        wave_i = np.sin(2 * np.pi * freq * t) * np.exp(-2.0 * t)
        chord_signal += wave_i
    chord_signal = chord_signal / (np.max(np.abs(chord_signal)) + 1e-9) * 0.9
    pcm_data = (chord_signal * 32767).astype(np.int16)
    bio = io.BytesIO()
    with wave.open(bio, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm_data.tobytes())
    bio.seek(0)
    return bio

# ---------------------------
# Navegación entre páginas
# ---------------------------
page = st.sidebar.radio("Navegar a:", ["Inicio", "Generador de Piano", "Contacto"])

# ---------------------------
# Inicio
# ---------------------------
if page == "Inicio":
    st.title("🎵 Bienvenido a SonarClave")
    st.header("Para que sirvo")
    st.write("""
    SonarClave es una herramienta innovadora diseñada para músicos y entusiastas del piano que desean explorar la armonía y la teoría musical de manera interactiva. Esta plataforma permite generar acordes de piano de forma sencilla, escuchar su sonido y visualizar un diagrama claro de las notas correspondientes. Gracias a esta combinación de funciones auditivas y visuales, los usuarios pueden comprender de manera práctica cómo se construyen los acordes y cómo se relacionan entre sí dentro de diferentes tonalidades. SonarClave resulta especialmente útil para quienes no tienen acceso a un piano físico, ya que ofrece una experiencia de aprendizaje completa y accesible desde cualquier dispositivo. Además, su enfoque interactivo fomenta la experimentación y la práctica constante, acelerando el proceso de aprendizaje y haciendo que la teoría musical sea mucho más intuitiva y divertida.
    """)

    st.header("Usuario objetivo")
    st.write("""
    - Edad: 12 hasta la muerte  
    - Ubicación: cualquier lugar con acceso a internet  
    - Estilo de vida: estudiantes, músicos principiantes, autodidactas  
    - Necesidad: aprender acordes de piano de forma visual y auditiva
    """)

    st.header("Cómo ayuda esta aplicación")
    st.write("""
    SonarClave permite generar acordes de piano, escuchar su sonido y ver un diagrama visual de las notas.
    Esto facilita el aprendizaje práctico y rápido, especialmente para quienes no pueden acceder a un piano físico.
    """)


    st.image("https://tse1.mm.bing.net/th/id/OIP.Zh8QWlme8zVd-Rny9Pc8oAHaHa?rs=1&pid=ImgDetMain&o=7&rm=3")

# ---------------------------
# Generador de Piano
# ---------------------------
elif page == "Generador de Piano":
    st.title("SonarClave: Generador de Acordes de Piano")
    st.write("Genera acordes de piano y escucha su sonido de manera inmediata.")

    # Sidebar para opciones
    st.sidebar.header("Configuración del acorde")
    root = st.sidebar.selectbox("Nota raíz", NOTE_NAMES)
    chord_type = st.sidebar.selectbox("Tipo de acorde", list(CHORD_FORMULAS.keys()))
    audio_octave = st.sidebar.slider("Octava base (nota raíz)", 2, 5, 4)
    duration = st.sidebar.slider("Duración del audio (segundos)", 1.0, 5.0, 2.0, step=0.5)
    generate = st.sidebar.button("Generar acorde")

    if generate:
        chord_notes = build_chord(root, chord_type)
        st.subheader(f"Acorde: {root} {chord_type}")
        st.markdown(f"**Notas:** {' — '.join(chord_notes)}")

        # Diagrama visual
        img_buf = draw_chord_diagram(chord_notes)
        st.image(img_buf, caption=f"Representación del acorde {root} {chord_type}")

        # Audio del acorde
        audio_bytes = synthesize_chord(chord_notes, base_octave=audio_octave, duration_s=duration)
        st.audio(audio_bytes, format='audio/wav')

# ---------------------------
# Contacto de la pagina
# ---------------------------
elif page == "Contacto":
    st.title("📞 Contacto")
    st.header("Integrantes del equipo")
    st.write("""
    - Juan Pérez  
    - María López  
    - Carlos Sánchez  
   
   
    Correo de contacto: Sonarclaveymusicologistica@gmail.com
    """)
