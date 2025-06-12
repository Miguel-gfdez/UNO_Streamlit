import streamlit as st
from collections import defaultdict

def aplicar_estilos_botones():
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: cornflowerblue;
            color: white;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: royalblue;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def mostrar_podio(jugadores):

    # Ordenamos jugadores por puntos descendente
    jugadores_ordenados = sorted(jugadores, key=lambda j: j.puntos, reverse=True)

    # Agrupamos jugadores por puntos (clave = puntos)
    grupos_por_puntos = defaultdict(list)
    for jugador in jugadores_ordenados:
        grupos_por_puntos[jugador.puntos].append(jugador)

    # Lista ordenada de puntuaciones descendente
    puntos_ordenados = sorted(grupos_por_puntos.keys(), reverse=True)

    st.markdown("## 🏆 Podio final")

    emojis = ["🥇", "🥈", "🥉"]

    # Sólo mostramos hasta 3 posiciones (podio)
    puestos_mostrados = 0

    # Creamos columnas según el número de grupos para las posiciones mostradas
    # El número de columnas será el mínimo entre 3 y número de grupos
    num_columnas = min(3, len(puntos_ordenados))
    cols = st.columns(num_columnas)

    for idx, puntos in enumerate(puntos_ordenados):
        if puestos_mostrados >= 3:
            break

        grupo = grupos_por_puntos[puntos]

        with cols[puestos_mostrados]:
            st.markdown(f"<h2 style='text-align:center'>{emojis[puestos_mostrados]}</h2>", unsafe_allow_html=True)

            # Mostrar nombres uno debajo de otro, centrados
            for jugador in grupo:
                st.markdown(f"<h3 style='text-align:center; margin: 0'>{jugador.nombre}</h3>", unsafe_allow_html=True)

            # Mostrar puntos solo una vez debajo de todos
            st.markdown(f"<p style='text-align:center; font-weight:bold;'>{puntos} puntos</p>", unsafe_allow_html=True)

        puestos_mostrados += 1

    # Si hay más jugadores fuera del podio, listarlos abajo
    if len(jugadores) > sum(len(grupos_por_puntos[p]) for p in puntos_ordenados[:3]):
        st.markdown("### Otros jugadores:")
        jugadores_fuera_podio = []
        # Sumamos todos los jugadores en los primeros 3 grupos
        jugadores_podio = []
        for p in puntos_ordenados[:3]:
            jugadores_podio.extend(grupos_por_puntos[p])
        # Filtramos los que no están en podio
        for jugador in jugadores_ordenados:
            if jugador not in jugadores_podio:
                jugadores_fuera_podio.append(jugador)

        for jugador in jugadores_fuera_podio:
            st.write(f"- {jugador.nombre}: {jugador.puntos} puntos")




