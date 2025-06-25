import os
import streamlit as st
from datetime import datetime
from supabase import create_client

from clases import Jugador, Parametros, Cartas
# ========================


def get_client():
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
    except Exception as e:
        url = " "
        key = " "

    supabase = create_client(url, key)
    return supabase

def borrar_datos_bd():
    client = get_client()
    # Borra todos los jugadores
    client.table("Jugadores").delete().neq("ID_sesion", 0).execute()
    # Borra todos los parámetros
    client.table("Parametros").delete().neq("ID_sesion", 0).execute()

def borrar_datos_bd_ID(id_sesion):
    client = get_client()
    # Borra todos los jugadores
    client.table("Jugadores").delete().eq("ID_sesion", id_sesion).execute()
    # Borra todos los parámetros
    client.table("Parametros").delete().eq("ID_sesion", id_sesion).execute()

def generar_nuevo_id_sesion():
    client = get_client()

    # Obtener todos los ID_sesion existentes
    res = client.table("Parametros").select("ID_sesion").execute()
    sesiones = [fila["ID_sesion"] for fila in res.data] if res.data else []

    # Calcular nuevo ID_sesion (máximo + 1) o 1 si no hay ninguno
    nuevo_id = max(sesiones) + 1 if sesiones else 1

    # # Insertar una nueva entrada en la tabla Parametros (si quieres registrar algo)
    # client.table("Parametros").insert({
    #     "ID_sesion": nuevo_id
    #     # Puedes añadir más columnas si tu tabla lo requiere
    # }).execute()

    return nuevo_id

def almacenar_jugadores(accion, parametro=None, nombre_original=None, nombre_nuevo=None, jugador_nuevo=None, id=None):
    client = get_client()

    jugadores = st.session_state.get("jugadores", [])

    if accion == "eliminar":
        if id is not None:
            # Eliminar jugadores con ese ID_sesion primero
            client.table("Jugadores").delete().eq("ID_sesion", id).execute()
        else:
            # Eliminar todos los jugadores primero
            client.table("Jugadores").delete().neq("ID_sesion", 0).execute()
            # Luego eliminar todos los parámetros
            client.table("Parametros").delete().neq("ID_sesion", 0).execute()

    elif accion == "añadir":
        # Insertar todos los jugadores
        if jugador_nuevo and st.session_state.id_sesion:
            client.table("Jugadores").insert({
                "ID_sesion": st.session_state.id_sesion,
                "nombre": jugador_nuevo.nombre,
                "puntuacion": jugador_nuevo.puntos
            }).execute()

    elif accion == "modificar":
        if parametro == "valor":
            for jugador in jugadores:
                client.table("Jugadores").update({
                    "puntuacion": jugador.puntos
                }).eq("nombre", jugador.nombre).execute()

        elif parametro == "nombre" and nombre_original and nombre_nuevo:
            client.table("Jugadores").update({
                "nombre": nombre_nuevo
            }).eq("nombre", nombre_original).execute()

def almacenar_parametros(accion, id=None):
    client = get_client()

    parametros = {
        "ID_sesion": st.session_state.id_sesion,
        "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "juego": st.session_state.parametros.juego if st.session_state.parametros else "default",
        "modalidad": st.session_state.parametros.modalidad if st.session_state.parametros else "default",
        "puntos": st.session_state.parametros.puntos if st.session_state.parametros else 0,
        "juego_bloqueado": st.session_state.get("juego_bloqueado", False),
        "partida_finalizada": st.session_state.get("partida_finalizada", False),
        "victoria": st.session_state.get("victoria", False)
    }

    if accion == "inicio":
        # Insertar o actualizar la sesión al inicio (usamos upsert para evitar duplicados)
        client.table("Parametros").upsert(parametros).execute()

    elif accion == "eliminar":
        if id is not None:
            borrar_datos_bd_ID(id)
        else:
            # Eliminar todos (ojo, si quieres mantener algo, evita esto)
            borrar_datos_bd()

    # elif accion == "guardar":
    #     # Insertar nueva fila (si quieres historico)
    #     client.table("Parametros").insert(parametros).execute()

    elif accion == "actualizar" and id is not None:
        # Para actualizar, quitamos 'time' para no modificarlo
        parametros_actualizar = parametros.copy()
        parametros_actualizar.pop("time", None)
        client.table("Parametros").update(parametros_actualizar).eq("ID_sesion", id).execute()
        return

def cargar_sesion(id_sesion):
    client = get_client()

    # Obtener todos los jugadores
    res_jugadores = client.table("Jugadores").select("*").eq("ID_sesion", id_sesion).execute()
    jugadores = []
    if res_jugadores.data:
        for jugador in res_jugadores.data:
            jugadores.append(Jugador(jugador["nombre"], jugador["puntuacion"]))
        st.session_state.jugadores = jugadores

    # Obtener los últimos parámetros
    res_parametros = client.table("Parametros").select("*").eq("ID_sesion", id_sesion).execute()
    if res_parametros.data:
        p = res_parametros.data[0]
        st.session_state.parametros = Parametros(p["juego"], p["modalidad"], p["puntos"])
        st.session_state.juego_bloqueado = p.get("juego_bloqueado", False)
        st.session_state.partida_finalizada = p.get("partida_finalizada", False)
        st.session_state.victoria = p.get("victoria", False)
        st.session_state.inicio = True
        st.session_state.cartas = Cartas.obtener_cartas(p["juego"])



