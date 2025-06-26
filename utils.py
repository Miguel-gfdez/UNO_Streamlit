import streamlit as st
from collections import defaultdict
from bbdd import get_client


# ========================
# FUNCIONES AUXILIARES
# ========================
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

def progreso_incremento(progreso, texto=""):
    porcentaje = min(max(progreso * 100, 0), 100)
    css = """
    <style>
    .small-bar-container {
      width: 280px;  /* más pequeña que la barra principal */
      height: 20px;
      background-color: #e0e0e0;
      border-radius: 50px;
      margin-left: 10px;
      margin-top: 5px;
      overflow: hidden;
      position: relative;
      font-size: 12px;
      color: black;
      font-weight: bold;
      text-align: center;
      line-height: 15px;
      user-select: none;
    }
    .small-bar {
      height: 100%;
      background-color: crimson;
      width: 0%;
      transition: width 0.5s ease-in-out;
      border-radius: 50px;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
    }
    .small-bar-text {
      position: relative;
      z-index: 2;
    }
    </style>
    """
    barra_html = f"""
    {css}
    <div class="small-bar-container">
        <div class="small-bar" style="width: {porcentaje}%;"></div>
        <div class="small-bar-text">{texto}</div>
    </div>
    """
    return barra_html

def progreso_partidas(progreso, clase_css, x, y):
    porcentaje = min(max(progreso * 100, 0), 100)
    texto = f"{x}/{y}"

    barra_html = f"""
    <style>
    .bar-container {{
      width: 100%;
      background-color: #e0e0e0;
      border-radius: 8px;
      margin-bottom: 5px;
      height: 20px;
      overflow: hidden;
      position: relative;
      font-size: 12px;
      color: black; /* color del texto interno de la barra*/
      text-align: center;
      line-height: 20px;
      font-weight: bold;
    }}
    .bar-azul {{
      height: 100%;
      background-color: cornflowerblue;
      width: 0%;
      transition: width 0.5s ease-in-out;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
    }}
    .bar-roja {{
      height: 100%;
      background-color: crimson;
      width: 0%;
      transition: width 0.5s ease-in-out;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
    }}
    .bar-texto {{
      position: relative;
      z-index: 2;
    }}
    </style>
    <div class="bar-container">
        <div class="{clase_css}" style="width: {porcentaje}%;"></div>
        <div class="bar-texto">{texto}</div>
    </div>
    """
    st.markdown(barra_html, unsafe_allow_html=True)

def borrar_session_state():
    st.session_state.victoria = False
    st.session_state.jugadores = []
    st.session_state.inicio = False
    st.session_state.parametros = None
    st.session_state.inicio_confirmado = False
    st.session_state.juego_bloqueado = False
    st.session_state.id_sesion = None
    st.session_state.cartas_seleccionadas = {}  # Mejor dict vacío, no None
    st.session_state.partida_finalizada = False
    st.session_state.nombre_jugador = None  # Si usas esta variable, resetea también

def reenumerar_ids_historial():
    client = get_client()
    # Obtener todos los registros ordenados por id ascendente
    response = client.table("Historial").select("id").order("id", desc=False).execute()

    if response.data:
        registros = response.data
        for nuevo_id, registro in enumerate(registros, start=1):
            id_actual = registro["id"]
            if id_actual != nuevo_id:
                # Actualizar id para que sea secuencial
                update_resp = client.table("Historial").update({"id": nuevo_id}).eq("id", id_actual).execute()

                if hasattr(update_resp, "error") and update_resp.error is not None:
                    # st.error(f"Error actualizando id {id_actual} a {nuevo_id}: {update_resp.error.message}")
                    pass
    else:
        pass


# def reenumerar_ids_sesion():
#     client = get_client()

#     sesiones_resp = client.table("Parametros").select("*").order("ID_sesion", desc=False).execute()
#     if not sesiones_resp.data:
#         st.info("No hay sesiones para reenumerar.")
#         return

#     sesiones = sesiones_resp.data
#     mapa_ids = {}
#     for nuevo_id, sesion in enumerate(sesiones, start=1):
#         id_actual = sesion["ID_sesion"]
#         if id_actual != nuevo_id:
#             mapa_ids[id_actual] = nuevo_id

#     # Paso 1: Insertar filas temporales en Parametros con IDs negativos
#     for id_viejo in mapa_ids.keys():
#         temp_id = -id_viejo
#         sesion = next(s for s in sesiones if s["ID_sesion"] == id_viejo)
#         temp_sesion = sesion.copy()
#         temp_sesion["ID_sesion"] = temp_id
#         insert_resp = client.table("Parametros").insert(temp_sesion).execute()
#         if hasattr(insert_resp, "error") and insert_resp.error:
#             st.error(f"Error insertando sesión temporal {temp_id}: {insert_resp.error.message}")

#     # Paso 2: Actualizar Jugadores a IDs temporales
#     for id_viejo in mapa_ids.keys():
#         temp_id = -id_viejo
#         update_jug_temp = client.table("Jugadores").update({"ID_sesion": temp_id}).eq("ID_sesion", id_viejo).execute()
#         if hasattr(update_jug_temp, "error") and update_jug_temp.error:
#             st.error(f"Error actualizando ID_sesion {id_viejo} a temporal {temp_id} en Jugadores: {update_jug_temp.error.message}")

#     # Paso 3: Actualizar Parametros a IDs temporales (no hace falta si ya insertaste copias temporales)

#     # Paso 4: Actualizar Parametros a IDs nuevos
#     for id_viejo, id_nuevo in mapa_ids.items():
#         temp_id = -id_viejo
#         update_param_final = client.table("Parametros").update({"ID_sesion": id_nuevo}).eq("ID_sesion", temp_id).execute()
#         if hasattr(update_param_final, "error") and update_param_final.error:
#             st.error(f"Error actualizando ID_sesion temporal {temp_id} a final {id_nuevo} en Parametros: {update_param_final.error.message}")

#     # Paso 5: Actualizar Jugadores a IDs nuevos
#     for id_viejo, id_nuevo in mapa_ids.items():
#         temp_id = -id_viejo
#         update_jug_final = client.table("Jugadores").update({"ID_sesion": id_nuevo}).eq("ID_sesion", temp_id).execute()
#         if hasattr(update_jug_final, "error") and update_jug_final.error:
#             st.error(f"Error actualizando ID_sesion temporal {temp_id} a final {id_nuevo} en Jugadores: {update_jug_final.error.message}")

#     # Paso 6 (opcional): borrar sesiones temporales
#     for id_viejo in mapa_ids.keys():
#         temp_id = -id_viejo
#         delete_resp = client.table("Parametros").delete().eq("ID_sesion", temp_id).execute()
#         if hasattr(delete_resp, "error") and delete_resp.error:
#             st.error(f"Error borrando sesión temporal {temp_id}: {delete_resp.error.message}")

#     st.success("Reenumeración de ID_sesion completada con éxito.")
