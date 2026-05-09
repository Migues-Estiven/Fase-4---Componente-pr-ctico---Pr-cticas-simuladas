from abc import ABC, abstractmethod

#  EXCEPCIONES

class ErrorSistema(Exception):
    """Excepción base del sistema"""
    pass

class ErrorCliente(ErrorSistema):
    pass

class ErrorServicio(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass


#  LOGS 

def log_evento(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")


#  CLASE ABSTRACTA GENERAL 

class Entidad(ABC):
    @abstractmethod
    def descripcion(self):
        pass


#  CLIENTE 

class Cliente(Entidad):
    def __init__(self, nombre, documento):
        if not nombre or not documento:
            raise ErrorCliente("Datos del cliente inválidos")
        self.__nombre = nombre
        self.__documento = documento

    def descripcion(self):
        return f"Cliente: {self.__nombre} - {self.__documento}"


#  SERVICIO ABSTRACTO 

class Servicio(ABC):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ErrorServicio("Precio del servicio inválido")
        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass

    @abstractmethod
    def descripcion(self):
        pass


#  SERVICIOS 

class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        return self.precio * horas

    def descripcion(self):
        return "Servicio de reserva de salas"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias):
        return (self.precio * dias) + 50

    def descripcion(self):
        return "Servicio de alquiler de equipos"


class Asesoria(Servicio):
    def calcular_costo(self, horas):
        return self.precio * horas * 1.2

    def descripcion(self):
        return "Servicio de asesoría especializada"


#  RESERVA 

class Reserva:
    def __init__(self, cliente, servicio, cantidad):
        if cantidad <= 0:
            raise ErrorReserva("Cantidad inválida para la reserva")
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.cantidad)
            self.estado = "Confirmada"
            log_evento(f"Reserva confirmada | {self.servicio.descripcion()} | Costo: {costo}")
            return costo

        except Exception as e:
            self.estado = "Error"
            log_evento(f"Error en reserva: {str(e)}")
            raise ErrorReserva("No se pudo procesar la reserva") from e

        finally:
            log_evento("Proceso de reserva finalizado")


#  MAIN  (PRUEBAS) 

def main():
    print("=== PRUEBAS DEL SISTEMA SOFTWARE FJ ===")

    # 1. Operación correcta
    try:
        c1 = Cliente("Juan", "123")
        s1 = ReservaSala("Sala de Reuniones", 100)
        r1 = Reserva(c1, s1, 2)
        print("Costo:", r1.procesar())
    except Exception as e:
        log_evento(str(e))

    # 2. Error cliente
    try:
        Cliente("", "456")
    except Exception as e:
        log_evento(str(e))

    # 3. Error servicio
    try:
        AlquilerEquipo("Equipo", -50)
    except Exception as e:
        log_evento(str(e))

    # 4. Error reserva
    try:
        r2 = Reserva(c1, s1, -1)
    except Exception as e:
        log_evento(str(e))

    # Más operaciones mixtas
    for i in range(6):
        try:
            c = Cliente(f"Cliente{i}", str(i))
            s = Asesoria("Asesoría TI", 80)
            r = Reserva(c, s, i + 1)
            print("Costo:", r.procesar())
        except Exception as e:
            log_evento(str(e))

    print("Sistema ejecutado correctamente.")


if __name__ == "__main__":
    main() 
