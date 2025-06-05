import streamlit as st
import math


# ========================
# CLASES
# ========================

class Jugador:
    def __init__(self, nombre, puntos=0):
        self.nombre = nombre
        self.puntos = puntos

    def ver_jugador(self):
        return f"{self.nombre}: {self.puntos} puntos"

class Parametros:
    def __init__(self, juego, modalidad, puntos):
        self.juego = juego
        self.modalidad = modalidad
        self.puntos = puntos

    def ver_parametros(self):
        texto = f"Juego: {self.juego} \t| Modalidad: {self.modalidad}"
        if self.modalidad != "Libre":
            texto += f" \t| Límite: {self.puntos}"
        return texto

class Cartas:
    cartas = {
        "UNO": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
            "6": 6, "7": 7, "8": 8, "9": 9,
            "+2": 20, "BLOQUEO": 20, "DIRECCION": 20,
            "COLOR": 50, "+4": 50
        },
        "UNO FLIP": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
            "+1": 10, "+5": 20, "DIRECCION": 20,"BLOQUEO": 20, "FLIP": 20, "SALTA A TODOS": 30, "COLOR": 40, "+2": 50, "COMODÍN": 60
        },

        "DOS": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
            "6": 6, "7": 7, "8": 8, "9": 9,
            "#": 40, "COMODIN": 20
        },

        "UNO ALL WILD": {"COLOR": 20, "DIRECCION": 50, "BLOQUEO": 50, "BLOQUEO DOBLE": 50, "+2": 50, "+4": 50, "CAMBIO FORZOSO": 50, "COMODIN +2": 50
        },


        "UNO_TEAMS": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "BLOQUEO": 20, "DIRECCION": 20, "Pase": 20, "+4": 50, "Comodín": 50,
        },
        "UNO_FLEX": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "+2": 20, "BLOQUEO": 20, "DIRECCION": 20, "COLOR": 50, "+4": 50,

            "Carta de Poder": 50,
            "Carta Flex": 20,
            "Acción Flex Saltar Todos": 50,
            "Acción Flex Robar Cartas": 50,
            "Comodín Flex Cambia Color": 50,
            "Comodín Flex Roba Cartas": 50,
        }




    }

    @staticmethod
    def obtener_cartas(juego):
        return Cartas.cartas.get(juego, {})

# ========================
# SESIÓN INICIAL
# ========================

if "jugadores" not in st.session_state:
    st.session_state.jugadores = []

if "fase" not in st.session_state:
    st.session_state.fase = "inicio"

if "parametros" not in st.session_state:
    st.session_state.parametros = None

# ========================
# MENÚ LATERAL
# ========================

st.sidebar.title("Menú")
pagina = st.sidebar.radio("Navegar a:", ["🎮 Juego", "👥 Jugadores", "🔧 Configuración"])

# ========================
# GESTIÓN DE JUGADORES
# ========================

if pagina == "👥 Jugadores":
    st.title("Gestión de Jugadores")
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

    nombre = st.text_input("Nombre del jugador").capitalize()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Añadir Jugador"):
            if nombre and not any(j.nombre == nombre for j in st.session_state.jugadores):
                st.session_state.jugadores.append(Jugador(nombre))
                st.success(f"{nombre} añadido.")
            else:
                st.warning("Nombre vacío o duplicado.")

    with col2:
        if st.button("Eliminar Jugador"):
            if len(st.session_state.jugadores) <= 2:
                st.warning("No se puede eliminar más jugadores. Mínimo 2 jugadores.")
            elif nombre and any(j.nombre == nombre for j in st.session_state.jugadores):
                st.session_state.jugadores = [j for j in st.session_state.jugadores if j.nombre != nombre]
                st.success(f"{nombre} eliminado.")
            else:
                st.warning("Nombre vacío o no existe.")

    with col3:
        nuevo_nombre = st.text_input("Nuevo nombre").capitalize()
        if st.button("Modificar Nombre"):
            if not nombre or not nuevo_nombre:
                st.warning("Ambos campos deben estar llenos.")
            elif not any(j.nombre == nombre for j in st.session_state.jugadores):
                st.warning("El nombre original no existe.")
            elif any(j.nombre == nuevo_nombre for j in st.session_state.jugadores):
                st.warning("El nuevo nombre ya está en uso.")
            else:
                for j in st.session_state.jugadores:
                    if j.nombre == nombre:
                        j.nombre = nuevo_nombre
                        st.success(f"{nombre} cambiado a {nuevo_nombre}.")
                        break


    st.subheader("Jugadores actuales:")
    for j in st.session_state.jugadores:
        st.write(j.ver_jugador())

    if st.button("Resetear Jugadores"):
        st.session_state.jugadores = []
        st.success("Lista de jugadores reiniciada.")

# ========================
# CONFIGURACIÓN DEL JUEGO
# ========================

elif pagina == "🔧 Configuración":
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
    st.title("Configuración del Juego")

    # Opciones con valor por defecto vacío usando "" como primera opción
    juego = st.selectbox("Elige el juego", ["", "UNO", "UNO FLIP", "UNO ALL WILD", "UNO TEAMS", "UNO FLEX", "DOS"])
    modalidad = st.selectbox("Modalidad", ["", "Partidas", "Incremento", "Libre-Partidas", "Libre-Puntos"])
    limite = st.number_input("Límite de puntos / partidas", min_value=3, value=3, placeholder="Introduce un número")

    if st.button("Aplicar configuración"):
        if not juego or not modalidad or not limite:
            st.warning("Por favor, completa todos los campos.")
        else:
            if modalidad == "Partidas":
                if limite % len(st.session_state.jugadores) != 1:
                    st.warning("El límite de partidas no es válido.")
                else:
                    st.session_state.parametros = Parametros(juego, modalidad, limite)
                    st.success("Parámetros configurados correctamente.")
            elif modalidad == "Incremento":
                if limite < 100:
                    st.warning("El límite de puntos debe ser mayor o igual a 100.")
                else:
                    st.session_state.parametros = Parametros(juego, modalidad, limite)
                    st.success("Parámetros configurados correctamente.")
            else:
                st.session_state.parametros = Parametros(juego, modalidad, 0)
                st.success("Parámetros configurados correctamente.")



    if st.session_state.parametros:
        st.info(st.session_state.parametros.ver_parametros())


# ========================
# JUEGO
# ========================

elif pagina == "🎮 Juego":
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

    if not st.session_state.jugadores or len(st.session_state.jugadores) < 2:
        st.warning(f"Añadir al menos 2 jugadores - Actualmente {len(st.session_state.jugadores)} jugador/es.")
    elif not st.session_state.parametros:
        st.warning("Primero configura el juego.")
    else:
        juego = st.session_state.parametros.juego
        cartas = Cartas.obtener_cartas(juego)
        if "cartas_seleccionadas" not in st.session_state:
            st.session_state.cartas_seleccionadas = {}
        if "juego_bloqueado" not in st.session_state:
            st.session_state.juego_bloqueado = False
        if "partida_finalizada" not in st.session_state:
            st.session_state.partida_finalizada = False
        contador_partidas = 0

        st.subheader("Seleccionar GANADOR de la ronda")

        nombres_jugadores = [""] + [j.nombre for j in st.session_state.jugadores]

        nombre_jugador = st.selectbox("Selecciona el nombre del jugador", nombres_jugadores)

        if st.session_state.juego_bloqueado:
            st.warning("🏁 La partida ha finalizado. Reinicia las puntuaciones para comenzar una nueva ronda.")
        else:
            if nombre_jugador == "":
                st.warning("Por favor, selecciona un jugador.")
            else:
                modalidad = st.session_state.parametros.modalidad

                if modalidad == "Partidas":
                    if st.button("Confirmar jugador"):
                        if any(j.nombre == nombre_jugador for j in st.session_state.jugadores):
                            for j in st.session_state.jugadores:
                                if j.nombre == nombre_jugador:
                                    j.puntos += 1
                                    contador_partidas += 1
                            st.success(f"{nombre_jugador} ha ganado 1 punto.")
                        else:
                            st.warning("El nombre no coincide con ningún jugador.")

                elif modalidad in ["Incremento", "Libre-Puntos"]:
                    st.title("Gestión de Jugadores")
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
                    # Mismo bloque para Incremento y Libre-Puntos
                    # Sólo que para Libre-Puntos no bloqueamos partida automáticamente

                    if "cartas_seleccionadas" not in st.session_state:
                        st.session_state.cartas_seleccionadas = {}

                    if "nombre_jugador" not in st.session_state:
                        st.session_state.nombre_jugador = None

                    if "modo_editar_seleccion" not in st.session_state:
                        st.session_state.modo_editar_seleccion = False

                    if st.session_state.nombre_jugador is None:
                        if st.button("Confirmar jugador", key="btn_confirmar_jugador"):
                            if any(j.nombre == nombre_jugador for j in st.session_state.jugadores):
                                st.session_state.nombre_jugador = nombre_jugador
                                st.info(f"Jugador seleccionado: **{nombre_jugador}**")
                            else:
                                st.warning("El nombre no coincide con ningún jugador.")
                    else:
                        st.info(f"Jugador seleccionado: **{nombre_jugador}**")

                        st.subheader("Selecciona las cartas jugadas")
                        cols = st.columns(4)

                        def agregar_carta(carta):
                            if carta in st.session_state.cartas_seleccionadas:
                                st.session_state.cartas_seleccionadas[carta] += 1
                            else:
                                st.session_state.cartas_seleccionadas[carta] = 1

                        # Botones para añadir cartas si no estamos en modo edición
                        if not st.session_state.modo_editar_seleccion:
                            for i, carta in enumerate(cartas.keys()):
                                if cols[i % 4].button(f"{carta}", key=f"carta_{carta}"):
                                    agregar_carta(carta)
                        else:
                            st.warning("Modo edición: modifica las cantidades de cartas seleccionadas")

                        if st.session_state.cartas_seleccionadas:
                            st.markdown("### 🧮 Cartas seleccionadas:")
                            total_puntos = 0

                            if st.session_state.modo_editar_seleccion:
                                nuevas_cantidades = {}
                                for carta, cantidad in st.session_state.cartas_seleccionadas.items():
                                    nuevas_cantidades[carta] = st.number_input(
                                        label=f"{carta}",
                                        min_value=0,
                                        value=cantidad,
                                        step=1,
                                        key=f"editar_{carta}"
                                    )
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("💾 Guardar cambios", key="btn_guardar_cambios"):
                                        st.session_state.cartas_seleccionadas = {c: n for c, n in nuevas_cantidades.items() if n > 0}
                                        st.session_state.modo_editar_seleccion = False
                                        st.success("Cambios guardados.")
                                        st.rerun()

                                with col2:
                                    if st.button("❌ Cancelar edición", key="btn_cancelar_edicion"):
                                        st.session_state.modo_editar_seleccion = False
                                        st.info("Edición cancelada.")
                            else:
                                for carta, cantidad in st.session_state.cartas_seleccionadas.items():
                                    puntos = cartas[carta] * cantidad
                                    total_puntos += puntos
                                    st.write(f"- {carta}: {cantidad} vez/veces ({puntos} puntos)")
                                st.write(f"**Total: {total_puntos} puntos**")

                                col1, col2 = st.columns(2)

                                with col1:
                                    confirmar = st.button("✅ Confirmar elección", key="btn_confirmar_eleccion")
                                    if confirmar:
                                        for j in st.session_state.jugadores:
                                            if j.nombre == nombre_jugador:
                                                j.puntos += total_puntos
                                                st.success(f"{j.nombre} gana {total_puntos} puntos.")
                                        st.session_state.cartas_seleccionadas = {}
                                        st.session_state.nombre_jugador = None
                                        st.rerun()

                                with col2:
                                    modificar = st.button("🔄 Modificar selección", key="btn_modificar_seleccion")
                                    if modificar:
                                        st.session_state.modo_editar_seleccion = True
                                        st.rerun()

                    # Botón para finalizar la partida (solo en Libre-Puntos)
                    if modalidad == "Libre-Puntos":
                        if st.button("Finalizar partida"):
                            st.session_state.partida_finalizada = True
                            st.session_state.juego_bloqueado = True


                elif modalidad == "Libre-Partidas":
                    # Para ambos modos, la mecánica es similar (sumar puntos o partidas)
                    # Pero sin terminar automáticamente
                    st.subheader("Añadir puntos a jugador")

                    if st.button("Confirmar jugador"):
                        if any(j.nombre == nombre_jugador for j in st.session_state.jugadores):
                            puntos_a_sumar = 1 if modalidad == "Libre-Partidas" else 0

                            if modalidad == "Libre-Puntos":
                                # Mostrar input para que usuario ingrese puntos a sumar
                                puntos_a_sumar = st.number_input("Ingresa puntos a sumar", min_value=0, step=1, value=0)

                            for j in st.session_state.jugadores:
                                if j.nombre == nombre_jugador:
                                    j.puntos += puntos_a_sumar
                                    st.success(f"{j.nombre} suma {puntos_a_sumar} puntos.")
                        else:
                            st.warning("El nombre no coincide con ningún jugador.")

                    # Botón para finalizar la partida
                    if st.button("Finalizar partida"):
                        st.session_state.partida_finalizada = True
                        st.session_state.juego_bloqueado = True


        # Mostrar tabla de puntuación actual
        st.subheader("📊 Tabla de puntuación")
        for j in st.session_state.jugadores:
            st.write(j.ver_jugador())

        # Botón para reiniciar puntuaciones (siempre visible)
        if st.button("Reiniciar puntuaciones"):
            for j in st.session_state.jugadores:
                j.puntos = 0
            st.session_state.juego_bloqueado = False
            st.session_state.cartas_seleccionadas = {}
            st.session_state.nombre_jugador = ""
            st.session_state.partida_finalizada = False
            st.success("Puntuaciones reiniciadas.")
            st.rerun()

        # Lógica fin de partida para modos que terminan automático
        if st.session_state.parametros.modalidad == "Incremento":
            ganador = next((j for j in st.session_state.jugadores if j.puntos >= st.session_state.parametros.puntos), None)
            if ganador:
                st.success(f"🏆 ¡{ganador.nombre} ha ganado la partida con {ganador.puntos}/{st.session_state.parametros.puntos} puntos!")
                st.session_state.juego_bloqueado = True

        elif st.session_state.parametros.modalidad == "Partidas":
            max_partidas = st.session_state.parametros.puntos
            partidas_ganadas_necesarias = math.ceil(max_partidas / 2)
            ganador = next((j for j in st.session_state.jugadores if j.puntos >= partidas_ganadas_necesarias), None)
            if ganador:
                st.success(f"🏆 ¡{ganador.nombre} ha ganado con {ganador.puntos}/{st.session_state.parametros.puntos} partidas!")
                st.session_state.juego_bloqueado = True

        # NUEVO: Mostrar ganador para modos Libre-Partidas y Libre-Puntos solo si se finalizó manualmente
        elif st.session_state.parametros.modalidad in ["Libre-Partidas", "Libre-Puntos"]:
            if st.session_state.partida_finalizada:
                max_puntos = max(j.puntos for j in st.session_state.jugadores)
                ganadores = [j for j in st.session_state.jugadores if j.puntos == max_puntos]
                if len(ganadores) == 1:
                    st.success(f"🏆 ¡{ganadores[0].nombre} ha ganado la partida con {ganadores[0].puntos} puntos!")
                else:
                    nombres_ganadores = ", ".join(j.nombre for j in ganadores)
                    st.success(f"🏆 Empate entre: {nombres_ganadores} con {max_puntos} puntos.")




