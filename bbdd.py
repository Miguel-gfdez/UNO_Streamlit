from supabase import create_client
import os
import streamlit as st
from clases import Jugador, Parametros, Cartas
from datetime import datetime
# ========================


def get_client():
    try:
        url = os.getenv("SUPABASE_URL")
        # # url = SUPABASE_URL if url is None else url
        key = os.getenv("SUPABASE_KEY")
        # key = SUPABASE_KEY if key is None else key
    except Exception as e:
        url = " "
        key = " "

    supabase = create_client(url, key)
    return supabase

def borrar_datos_bd():
    client = get_client()
    # Borra todos los jugadores
    client.table("Jugadores").delete().neq("id", 0).execute()
    # Borra todos los parámetros
    client.table("Parametros").delete().neq("id", 0).execute()

def almacenar_jugadores(accion, parametro=None, nombre_original=None, nombre_nuevo=None, jugador_nuevo=None):
    client = get_client()

    jugadores = st.session_state.get("jugadores", [])

    if accion == "eliminar":
        if not jugadores:
            # Borrar todos los registros si no hay jugadores en sesión
            client.table("Jugadores").delete().neq("id", 0).execute()
        elif parametro == "nombre" and nombre_original:
            # Borrar un jugador específico por nombre
            client.table("Jugadores").delete().eq("nombre", nombre_original).execute()
        return

    elif accion == "añadir":
        # Insertar todos los jugadores
        if jugador_nuevo:
            client.table("Jugadores").insert({
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

def almacenar_parametros(accion):
    if st.session_state.parametros is None:
        return
    
    client = get_client()

    if accion == "eliminar":
        # Eliminar todos los parámetros existentes
        client.table("Parametros").delete().neq("id", 0).execute()
        return

    elif accion == "guardar":
        # Primero eliminar cualquier fila anterior
        client.table("Parametros").delete().neq("id", 0).execute()

        # Luego insertar los nuevos parámetros
        parametros = {
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "juego": st.session_state.parametros.juego,
            "modalidad": st.session_state.parametros.modalidad,
            "puntos": st.session_state.parametros.puntos,
            "juego_bloqueado": st.session_state.get("juego_bloqueado", False),
            "partida_finalizada": st.session_state.get("partida_finalizada", False),
            "victoria": st.session_state.get("victoria", False)
        }

        client.table("Parametros").insert(parametros).execute()

def cargar_sesion():
    client = get_client()

    # Obtener todos los jugadores
    res_jugadores = client.table("Jugadores").select("*").execute()
    jugadores = []
    if res_jugadores.data:
        for jugador in res_jugadores.data:
            jugadores.append(Jugador(jugador["nombre"], jugador["puntuacion"]))
        st.session_state.jugadores = jugadores

    # Obtener los últimos parámetros
    res_parametros = client.table("Parametros").select("*").order("id", desc=True).limit(1).execute()
    if res_parametros.data:
        p = res_parametros.data[0]
        st.session_state.parametros = Parametros(p["juego"], p["modalidad"], p["puntos"])
        st.session_state.juego_bloqueado = p.get("juego_bloqueado", False)
        st.session_state.partida_finalizada = p.get("partida_finalizada", False)
        st.session_state.victoria = p.get("victoria", False)
        st.session_state.inicio = True
        st.session_state.cartas = Cartas.obtener_cartas(p["juego"])
