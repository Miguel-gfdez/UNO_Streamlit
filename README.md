# Sistema de Puntuación de Cartas para Juegos con Streamlit

## Descripción general

Este proyecto es una aplicación web interactiva desarrollada con [Streamlit](https://streamlit.io/) que permite gestionar y contabilizar la puntuación de jugadores en juegos de cartas con modalidades variables, específicamente modalidades tipo **“Incremento”** y **“Libre-Puntos”**. 

La aplicación facilita la selección dinámica de cartas jugadas por cada jugador y calcula automáticamente los puntos obtenidos, permitiendo también la adición manual de puntos extra. Está diseñada para usarse tanto en dispositivos de escritorio como en móviles, con una interfaz intuitiva y adaptada para diferentes tamaños de pantalla.

---

## Objetivos del proyecto

- **Gestionar partidas de juegos de cartas** con reglas personalizables, donde los jugadores acumulan puntos según cartas jugadas.
- **Permitir la selección y contabilización rápida y visual** de cartas jugadas mediante botones que reflejan la cantidad de cartas seleccionadas.
- **Adaptabilidad para uso en móviles y escritorio**, con botones distribuidos en columnas para mejor experiencia en pantallas pequeñas.
- **Modos de edición y confirmación**, que permiten modificar cantidades de cartas seleccionadas antes de finalizar el conteo.
- **Registro y almacenamiento automático de los puntos acumulados** para cada jugador, permitiendo llevar un historial durante la partida.
- **Flexibilidad para añadir puntos manualmente**, que no dependen de cartas, para contemplar situaciones especiales o reglas adicionales.

---

## Funcionalidades principales

- **Selección dinámica de cartas:** Los usuarios pueden seleccionar cartas jugadas mediante botones agrupados en columnas (2 columnas para móviles, 3 para escritorio).
- **Visualización en tiempo real:** Se muestra un resumen de cartas seleccionadas, su cantidad y los puntos acumulados.
- **Modo edición:** Permite modificar las cantidades antes de confirmar la suma final.
- **Confirmación de puntajes:** Al confirmar, los puntos se suman al total del jugador seleccionado y se almacena el resultado.
- **Finalización de partida:** En la modalidad “Libre-Puntos” se puede finalizar la partida bloqueando más modificaciones.
- **Interfaz estilizada con CSS:** Botones con estilos personalizados para una mejor experiencia visual.

---

## Tecnologías usadas

- **Python 3.x**
- **Streamlit:** Framework para construir la interfaz web reactiva.
- **Manejo de estado con `st.session_state`:** para almacenar información temporal como cartas seleccionadas, jugadores, y modos de edición.
- **CSS embebido:** para personalizar estilos de botones y mejorar la usabilidad en distintos dispositivos.

---

## Estructura del proyecto

- **Funciones clave:**
  - `agregar_carta(carta)`: Añade o incrementa la cantidad de una carta seleccionada.
  - `mostrar_cartas(cartas)`: Muestra botones para seleccionar cartas en columnas adaptables.
- **Estado de la sesión:**
  - `cartas_seleccionadas`: Diccionario con cartas y sus cantidades.
  - `nombre_jugador`: Jugador activo.
  - `modo_editar_seleccion`: Indica si se está modificando la selección.
- **Interacción del usuario:**
  - Selección y edición de cartas.
  - Añadir puntos manuales.
  - Confirmar selección y actualizar puntajes.
  - Finalizar partida en modo “Libre-Puntos”.

---

## Uso esperado

1. Seleccionar un jugador activo.
2. Pulsar los botones correspondientes a las cartas jugadas, acumulando puntos.
3. Revisar y editar la selección de cartas si es necesario.
4. Añadir puntos manuales adicionales si se desea.
5. Confirmar la selección para actualizar el puntaje total del jugador.
6. Repetir para otros jugadores y continuar la partida.
7. Finalizar la partida cuando corresponda.

---

## Consideraciones y mejoras futuras

- Mejorar la detección automática del dispositivo para ajustar columnas (desktop vs móvil).
- Incorporar historial visual y exportación de resultados.
- Añadir soporte para más modalidades de juego y reglas personalizadas.
- Optimizar la interfaz para mejorar usabilidad y accesibilidad.

