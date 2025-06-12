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
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "+2": 20, "BLOQUEO": 20, "DIRECCION": 20,
            "COLOR": 50, "+4": 50
        },
        "UNO FLIP": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
            "+1": 10, "+5": 20, "DIRECCION": 20,"BLOQUEO": 20, "FLIP": 20, "SALTA A TODOS": 30, "COLOR": 40, "+2": 50, "COMODÍN": 60
        },

        "DOS": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "#": 40, "COMODIN": 20
        },

        "UNO ALL WILD": {"COLOR": 20, "DIRECCION": 50, "BLOQUEO": 50, "BLOQUEO DOBLE": 50, "+2": 50, "+4": 50, "CAMBIO FORZOSO": 50, "COMODIN +2": 50
        },

        "UNO_TEAMS": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "ESPECIAL": 20, "COMODIN": 50,
        },

        "UNO_FLEX": {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
            "ESPECIAL": 20, "COMODIN": 20
        }
    }

    @staticmethod
    def obtener_cartas(juego):
        return Cartas.cartas.get(juego, {})
