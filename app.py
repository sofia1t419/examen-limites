import streamlit as st
import sqlite3
from datetime import datetime
import time
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. CONFIGURACIÓN ÚNICA DE LA PÁGINA
st.set_page_config(
    page_title="Caja Fuerte: Misión 7 Dígitos", 
    page_icon="🔐", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 2. BASE DE DATOS LOCAL
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

def borrar_todos_los_registros():
    conn = sqlite3.connect("resultados.db")
    c = conn.cursor()
    c.execute("DELETE FROM notas")
    conn.commit()
    conn.close()

# 3. GENERADOR DE PDF
def generar_pdf_reporte(datos):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,
        spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        spaceAfter=20
    )
    
    story.append(Paragraph("<b>REPORTE DE RESULTADOS: CAJA FUERTE</b>", title_style))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    
    tabla_datos = [["#", "Estudiante", "Puntaje", "Tiempo (s)", "Código", "Fecha"]]
    
    for i, row in enumerate(datos, 1):
        tabla_datos.append([
            str(i),
            str(row[0]),
            f"{row[1]} pts",
            f"{row[2]}s",
            str(row[3]),
            str(row[4])
        ])
    
    t = Table(tabla_datos, colWidths=[25, 160, 65, 65, 75, 110])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284C7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer

init_db()

# 4. ESTILOS VISUALES
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

# 5. VARIABLES DE SESIÓN
if "registrado" not in st.session_state:
    st.session_state.registrado = False
    st.session_state.nombre = ""
    st.session_state.puntos = 0
    st.session_state.nivel = 1
    st.session_state.digitos = ["_"] * 7
    st.session_state.inicio_tiempo = 0
    st.session_state.guardado = False

# 6. BANCO DE 7 PROBLEMAS
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

# 7. PANEL DEL PROFESOR
with st.sidebar:
    st.title("🔒 Panel de Control")
    clave = st.text_input("Clave Secreta:", type="password")
    
    if clave == "1128906177":
        st.success("Acceso Autorizado")
        
        datos = obtener_notas()
        
        if datos:
            pdf_bytes = generar_pdf_reporte(datos)
            st.download_button(
                label="📄 Descargar Reporte PDF",
                data=pdf_bytes,
                file_name=f"Reporte_Resultados_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.divider()
        
        if st.button("🗑️ Borrar todos los registros", use_container_width=True):
            borrar_todos_los_registros()
            st.success("¡Registros borrados con éxito!")
            time.sleep(1)
            st.rerun()

        st.subheader("🏆 Registros y Tiempos")
        if datos:
            for row in datos:
                st.write(f"👤 **{row[0]}** — ⭐ {row[1]} pts ({row[2]}s)")
                st.caption(f"🔑 Código Desbloqueado: `{row[3]}`")
                st.caption(f"Fecha: {row[4]}")
                st.divider()
        else:
            st.info("Sin entregas aún.")

# 8. INTERFAZ PRINCIPAL
st.title("🔐 ENCUENTRA LOS DÍGITOS PARA ABRIR LA CAJA FUERTE")
st.caption("Resuelve cada problemática para descubrir los 7 dígitos de la combinación")

if not st.session_state.registrado:
