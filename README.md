# Sistema de Puntuación de Cartas para Juegos con Streamlit

## Descripción general

Este proyecto es una aplicación web interactiva desarrollada con [Streamlit](https://streamlit.io/) que permite gestionar y contabilizar la puntuación de jugadores en juegos de cartas con modalidades variables. 

La aplicación facilita la selección dinámica de cartas jugadas por cada jugador y calcula automáticamente los puntos obtenidos, permitiendo también la adición manual de puntos extra.

---

## Objetivos del proyecto

- **Gestionar partidas de juegos de cartas** con reglas personalizables, donde los jugadores acumulan puntos según cartas jugadas.
- **Permitir la selección y contabilización rápida y visual** de cartas jugadas mediante botones que reflejan la cantidad de cartas seleccionadas.
- **Modos de edición y confirmación**, que permiten modificar y corregir cantidades de cartas seleccionadas antes de finalizar el conteo.
- **Registro y almacenamiento automático de los puntos acumulados** para cada jugador, permitiendo llevar un historial durante la partida.
- **Flexibilidad para añadir puntos manualmente**, que no dependen de cartas, para contemplar situaciones especiales o reglas adicionales.
- **Guardar y gestionar sesiones de juego**, permitiendo crear, cargar, modificar y eliminar sesiones para mantener un historial completo y facilitar la continuidad entre partidas.

---

## Funcionalidades principales

- **Selección dinámica de cartas:** Los usuarios pueden seleccionar cartas jugadas mediante botones agrupados en columnas.
- **Visualización en tiempo real:** Se muestra un resumen de cartas seleccionadas, su cantidad y los puntos acumulados.
- **Modo edición:** Permite modificar las cantidades antes de confirmar la suma final.
- **Confirmación de puntajes:** Al confirmar, los puntos se suman al total del jugador seleccionado y se almacena el resultado.
- **Interfaz estilizada con CSS:** Botones con estilos personalizados para una mejor experiencia visual.- 
- **Historial de partidas:** Registro automático y consulta del historial de partidas para revisión y análisis posterior.
- **Control de sesiones:** Capacidad para guardar, cargar y eliminar sesiones de juego completas.
- **Detección y anuncio de ganador:** Lógica para determinar automáticamente el ganador según reglas definidas y mostrar mensajes destacados.
- **Soporte para diferentes modalidades de juego:** Posibilidad de configurar distintas reglas y modos.
- **Persistencia en la nube:** Uso de una base de datos en la nube para guardar datos y facilitar el acceso desde diferentes dispositivos.

---

## Tecnologías usadas

- **Python 3.12.4**
- **Streamlit:** Framework para construir la interfaz web.
- **Supabase:** Backend en la nube para almacenamiento y gestión de bases de datos.
- **CSS embebido:** para personalizar estilos de botones.

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

- Mejorar la detección automática del dispositivo (desktop vs móvil).
- Añadir soporte para más modalidades de juego y reglas personalizadas.
- Optimizar la interfaz para mejorar usabilidad y accesibilidad.
- Integrar un sistema de estadísticas y análisis históricos para seguimiento de rendimiento.
- ¿Añadir soporte multilingüe para que la aplicación pueda mostrarse en varios idiomas (español, inglés, francés, alemán, chino, etc.) con detección automática y opción de cambio manual?

---
<!--
## Demo en línea

Puedes probar la aplicación en línea aquí:  
[https://puntoslive.streamlit.app/](https://puntoslive.streamlit.app/)
-->

