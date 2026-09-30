import streamlit as st
import sqlite3
from datetime import datetime
import time

st.set_page_config(
    page_title="Caja Fuerte: Misión 7 Dígitos", 
    page_icon="🔐", 
    layout="centered",
    initial_sidebar_state="collapsed" # Oculta la barra lateral automáticamente al entrar
)

# --- BASE DE DATOS LOCAL ---
def init_db():
    conn = sqlite3.connect("resultados.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            puntos INTEGER,
            tiempo_segundos INTEGER,
            codigo_final TEXT,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_nota(nombre, puntos, tiempo_seg, codigo):
    conn = sqlite3.connect("resultados.db")
    c = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO notas (nombre, puntos, tiempo_segundos, codigo_final, fecha) VALUES (?, ?, ?, ?, ?)", 
              (nombre, puntos, tiempo_seg, codigo, fecha_actual))
    conn.commit()
    conn.close()

def obtener_notas():
    conn = sqlite3.connect("resultados.db")
    c = conn.cursor()
    c.execute("SELECT nombre, puntos, tiempo_segundos, codigo_final, fecha FROM notas ORDER BY puntos DESC, tiempo_segundos ASC")
    datos = c.fetchall()
    conn.close()
    return datos

init_db()

# --- ESTILOS VISUALES ---
st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .card-mission {
        background-color: #1E293B;
        border: 2px solid #F59E0B;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 15px;
    }
    .code-banner {
        background-color: #0284C7;
        color: #FFFFFF;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 15px;
    }
    .badge-score {
        background-color: #10B981;
        color: #000;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Variables de Sesión
if "registrado" not in st.session_state:
    st.session_state.registrado = False
    st.session_state.nombre = ""
    st.session_state.puntos = 0
    st.session_state.nivel = 1
    st.session_state.digitos = ["_"] * 7
    st.session_state.inicio_tiempo = 0
    st.session_state.guardado = False

# BANCO DE 7 PROBLEMAS CON DÍGITO RESULTADO
problemas = [
    {
        "titulo": "🏎️ Problema 1: El Carro de Carreras y la Asíntota",
        "enunciado": "Un carro deportivo prueba su sistema de frenado. La distancia de frenado de emergencia está dada por la función f(x) = 12 / (x - 5). ¿En qué valor crítico de x el sistema colapsa (asíntota vertical)?",
        "respuesta": 5,
        "pista": "Encuentra en qué valor de x el denominador (x - 5) se convierte en cero."
    },
    {
        "titulo": "🧪 Problema 2: Indeterminación en el Laboratorio",
        "enunciado": "Un químico evalúa la velocidad de reacción dada por lim(x → 3) [(x² - 9) / (x - 3)]. Al simplificar la indeterminación 0/0, ¿cuál es el resultado del límite?",
        "respuesta": 6,
        "pista": "Factoriza la diferencia de cuadrados (x-3)(x+3)/(x-3) y evalúa en x = 3."
    },
    {
        "titulo": "🚀 Problema 3: Propulsión de un Cohete",
        "enunciado": "La aceleración de un prototipo espacial al acercarse a su base sigue la función f(x) = 4 / (x - 2). ¿Para qué valor de x se produce la barrera crítica de aceleración?",
        "respuesta": 2,
        "pista": "Iguala el denominador (x - 2) a cero para hallar la asíntota."
    },
    {
        "titulo": "💰 Problema 4: Economía y Limpieza del Lago",
        "enunciado": "Un municipio evalúa el costo de descontaminación mediante C(x) = (x² - 16) / (x - 4). ¿A qué valor constante equivale el límite cuando x tiende a 4?",
        "respuesta": 8,
        "pista": "Factoriza (x-4)(x+4) / (x-4) y reemplaza x = 4."
    },
    {
        "titulo": "💊 Problema 5: Dosis de Medicamento",
        "enunciado": "La concentración de un fármaco en sangre en un intervalo crítico de tiempo responde al límite simple: lim(x → 4) [x + 3]. ¿Cuál es el resultado obtenido?",
        "respuesta": 7,
        "pista": "Aplica sustitución directa evaluando x = 4."
    },
    {
        "titulo": "⚡ Problema 6: Circuito Eléctrico",
        "enunciado": "La corriente eléctrica en un microchip al regular un voltaje variante responde a lim(x → 2) [ (x² - 4) / (x - 2) ]. ¿Cuál es el valor del límite obtenido?",
        "respuesta": 4,
        "pista": "Factoriza (x-2)(x+2) / (x-2) y evalúa en x = 2."
    },
    {
        "titulo": "🌊 Problema 7: Presión Hidrostática",
        "enunciado": "Un submarino mide el pico de presión en un ducto con la función P(x) = 15 / (x - 9). ¿En qué valor de x la presión alcanza su asíntota vertical?",
        "respuesta": 9,
        "pista": "Determina en qué valor de x el denominador (x - 9) se vuelve cero."
    }
]

# PANEL OCULTO PARA EL PROFESOR
with st.sidebar:
    st.title("🔒 Panel de Control")
    clave = st.text_input("Clave Secreta:", type="password")
    if clave == "1128906177":
        st.success("Acceso Autorizado")
        # Botón para borrar los datos
    if st.button("🗑️ Borrar todos los registros"):
        st.session_state["registros"] = [] # O el nombre de la variable que uses para la lista
        st.success("¡Registros borrados con éxito!")
        st.rerun()
        st.subheader("🏆 Registros y Tiempos")
        datos = obtener_notas()
        if datos:
            for row in datos:
                st.write(f"👤 **{row[0]}** — ⭐ {row[1]} pts ({row[2]}s)")
                st.caption(f"🔑 Código Desbloqueado: `{row[3]}`")
                st.caption(f"Fecha: {row[4]}")
                st.divider()
        else:
            st.info("Sin entregas aún.")

st.title("🔐 ENCUENTRA LOS DÍGITOS PARA ABRIR LA CAJA FUERTE")
st.caption("Resuelve cada problemática para descubrir los 7 dígitos de la combinación")

# --- PASO 1: PANTALLA INICIAL ---
if not st.session_state.registrado:
    st.markdown("""
    <div class='card-mission'>
        <h2>🧰 Misión: Desbloquear la Caja Fuerte</h2>
        <p>Aparecerán 7 problemáticas reales de límites y asíntotas (un carro, un laboratorio, un cohete, etc.).</p>
        <p><b>Cada resultado obtenido corresponderá a un dígito de la clave.</b> ¡Se irán guardando automáticamente arriba para que no los olvides!</p>
    </div>
    """, unsafe_allow_html=True)
    
    nombre_input = st.text_input("Ingresa tu Nombre y Apellido para iniciar:", placeholder="Ej: Mateo Gomez")
    
    if st.button("🚀 Comenzar Misión", use_container_width=True, type="primary"):
        if nombre_input.strip() != "":
            st.session_state.nombre = nombre_input
            st.session_state.registrado = True
            st.session_state.inicio_tiempo = time.time()
            st.rerun()

else:
    # Encabezado del estudiante
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"👤 **Alumno:** {st.session_state.nombre}")
    with col2:
        st.markdown(f"<span class='badge-score'>⭐ {st.session_state.puntos} PTS</span>", unsafe_allow_html=True)
    
    # BANNER QUE GUARDA LOS DÍGITOS AUTOMÁTICAMENTE
    codigo_str = " ".join([f"[{d}]" for d in st.session_state.digitos])
    st.markdown(f"<div class='code-banner'>🔑 DÍGITOS CONSEGUIDOS: {codigo_str}</div>", unsafe_allow_html=True)
    
    idx = st.session_state.nivel - 1

    if idx < 7:
        st.progress((idx + 1) / 7, text=f"Problema {idx + 1} de 7")
        st.divider()

        prob = problemas[idx]
        
        st.markdown(f"""
        <div class='card-mission'>
            <h3>{prob['titulo']}</h3>
            <p style='font-size: 16px;'>{prob['enunciado']}</p>
        </div>
        """, unsafe_allow_html=True)

        resp = st.number_input("Ingresa el resultado obtenido para este dígito:", value=0, step=1, key=f"prob_{idx}")

        if st.button("🔓 CONFIRMAR Y GUARDAR DÍGITO", use_container_width=True, type="primary"):
            if resp == prob["respuesta"]:
                st.balloons()
                st.success(f"¡Correcto! Has descubierto el dígito {idx + 1}: **{resp}**")
                
                st.session_state.digitos[idx] = str(resp)
                st.session_state.puntos += 100
                time.sleep(1.2)
                st.session_state.nivel += 1
                st.rerun()
            else:
                st.error("❌ Dígito incorrecto. Inténtalo de nuevo.")
                st.info(f"💡 Pista: {prob['pista']}")

    # --- PANTALLA FINAL: DESBLOQUEO DE LA CAJA FUERTE ---
    else:
        codigo_final_str = "".join(st.session_state.digitos)
        tiempo_total = int(time.time() - st.session_state.inicio_tiempo)

        if not st.session_state.guardado:
            guardar_nota(st.session_state.nombre, st.session_state.puntos, tiempo_total, codigo_final_str)
            st.session_state.guardado = True

        st.balloons()
        st.markdown(f"""
        <div class='card-mission' style='border-color: #10B981; text-align: center;'>
            <h2>🔓 ¡CAJA FUERTE DESBLOQUEADA!</h2>
            <p>Ingresaste con éxito la combinación de 7 dígitos:</p>
            <h1 style='color: #F59E0B; letter-spacing: 5px;'>{codigo_final_str}</h1>
            <h2 style='color: #10B981;'>{st.session_state.puntos} PTS</h2>
            <p>Tiempo empleado: <b>{tiempo_total} segundos</b>.</p>
            <p style='color: #94A3B8; font-size: 13px;'>¡Felicidades {st.session_state.nombre}! Tu resultado fue guardado.</p>
        </div>
        """, unsafe_allow_html=True)
