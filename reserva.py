import logging
from cliente import EntidadGeneral
from excepciones import ServicioNoDisponibleError, ReservaInvalidaError


class Reserva(EntidadGeneral):
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        # Toda reserva arranca pendiente y sin costo calculado hasta confirmarse
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def confirmar(self):
        # Si el servicio no está disponible, cortamos y lanzamos el error correspondiente
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio " + self.servicio.nombre + " no esta disponible por el momento.")

        self.estado = "Confirmada"
        # Calculamos el costo según la duración del servicio aplicando impuesto
        self.costo_total = self.servicio.calcular_costo(self.duracion, impuesto=True)

        logging.info("Reserva " + str(self.id_reserva) + " confirmada para el cliente " + self.cliente.get_nombre())
        return True

    def cancelar(self):
        # Evitamos cancelar dos veces la misma reserva
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("No se puede cancelar una reserva que ya fue cancelada.")

        self.estado = "Cancelada"
        logging.info("Reserva " + str(self.id_reserva) + " cancelada exitosamente.")
        return True

    def procesar(self):
        try:
            self.confirmar()
        except ServicioNoDisponibleError as e:
            # Marcamos la reserva como fallida y encadenamos el error para no perder el motivo original
            self.estado = "Fallida"
            logging.error("No se pudo procesar la reserva " + str(self.id_reserva) + ": " + str(e))
            raise ReservaInvalidaError("Error al procesar la reserva.") from e

    def obtener_descripcion(self):
        return "Reserva #" + str(self.id_reserva) + " | Estado: " + self.estado + " | Costo Total: $" + str(self.costo_total)
