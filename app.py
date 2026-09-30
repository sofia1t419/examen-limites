import streamlit as st

st.set_page_config(page_title="Examen - Límites Infinitos", page_icon="📐")

st.title("📐 Examen Didáctico: Límites Infinitos")
st.write("Responde el examen interactivo de repaso para Grado 11.")

nombre = st.text_input("Ingresa tu nombre completo para iniciar:")

if nombre:
    st.subheader(f"¡Bienvenido/a, {nombre}!")
    st.write("Selecciona la respuesta correcta en cada caso:")
    st.markdown("---")
    
    # Pregunta 1
    p1 = st.radio(
        "1. Al evaluar un límite, si obtenemos la forma [k/0] con k ≠ 0, ¿cuál es el resultado y su significado gráfico?",
        [
            "Es una indeterminación [0/0] que exige factorizar",
            "Genera un límite infinito (+∞ o -∞) y una asíntota vertical",
            "El límite es siempre igual a cero"
        ]
    )
    
    # Pregunta 2
    p2 = st.radio(
        "2. ¿Cuál es el resultado de lim(x -> 4⁻) [ 2 / (x - 4) ]?",
        [
            "+Infinito (+∞)",
            "-Infinito (-∞)",
            "No existe por ser 0/0"
        ]
    )
    
    # Pregunta 3
    p3 = st.radio(
        "3. Si lim(x -> a⁻) f(x) = -∞ y lim(x -> a⁺) f(x) = +∞, ¿qué se concluye sobre el límite bilateral?",
        [
            "El límite bilateral es +∞",
            "El límite bilateral es -∞",
            "El límite bilateral NO EXISTE (DNE)"
        ]
    )

    # Pregunta 4
    p4 = st.radio(
        "4. Al evaluar lim(x -> 2) [ (x² - 4) / (x - 2) ], ¿qué procedimiento se debe seguir?",
        [
            "Evaluar directamente y concluir que da infinito",
            "Factorizar el numerador para simplificar y obtener 4",
            "Concluir que no tiene solución"
        ]
    )

    st.markdown("---")
    if st.button("📩 Enviar respuestas para calificar"):
        score = 0
        if p1 == "Genera un límite infinito (+∞ o -∞) y una asíntota vertical":
            score += 1
        if p2 == "-Infinito (-∞)":
            score += 1
        if p3 == "El límite bilateral NO EXISTE (DNE)":
            score += 1
        if p4 == "Factorizar el numerador para simplificar y obtener 4":
            score += 1
            
        st.balloons()
        st.success(f"¡Examen completado con éxito, {nombre}! Tu calificación final es: {score} / 4")
