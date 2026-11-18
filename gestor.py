import logging
from cliente import Cliente
from reserva import Reserva
from excepciones import (
    ErrorSoftwareFJ,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
)


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en memoria."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # ---------- Búsquedas ----------
    def buscar_cliente(self, id_cliente):
        for c in self.clientes:
            if c.get_id_cliente() == id_cliente:
                return c
        return None

    def buscar_servicio(self, codigo):
        for s in self.servicios:
            if s.codigo == codigo:
                return s
        return None

    def buscar_reserva(self, id_reserva):
        for r in self.reservas:
            if r.id_reserva == id_reserva:
                return r
        return None

    # ---------- Operaciones ----------
    def registrar_cliente(self, id_cliente, nombre, email, telefono):
        try:
            cliente = Cliente(id_cliente, nombre, email, telefono)
        except ClienteInvalidoError as e:
            logging.error("No se pudo registrar el cliente: " + str(e))
            print("ERROR (cliente):", e)
            return None
        except Exception as e:
            logging.error("Error inesperado al registrar cliente: " + str(e))
            print("ERROR inesperado:", e)
            return None
        else:
            self.clientes.append(cliente)
            logging.info("Cliente registrado: " + cliente.get_nombre())
            print("OK:", cliente.obtener_descripcion())
            return cliente
        finally:
            logging.info("Fin de la operación: registrar cliente")

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        logging.info("Servicio agregado: " + servicio.nombre)
        print("OK:", servicio.obtener_descripcion())

    def crear_reserva(self, id_reserva, id_cliente, codigo_servicio, duracion):
        try:
            cliente = self.buscar_cliente(id_cliente)
            if cliente is None:
                raise ClienteInvalidoError("No existe el cliente " + str(id_cliente))

            servicio = self.buscar_servicio(codigo_servicio)
            if servicio is None:
                raise ServicioInvalidoError("No existe el servicio " + str(codigo_servicio))

            servicio.validar_parametros(duracion)
            reserva = Reserva(id_reserva, cliente, servicio, duracion)
            reserva.procesar()
        except ErrorSoftwareFJ as e:
            logging.error("No se pudo crear la reserva " + str(id_reserva) + ": " + str(e))
            print("ERROR (reserva):", e)
            return None
        except Exception as e:
            logging.error("Error inesperado al crear reserva: " + str(e))
            print("ERROR inesperado:", e)
            return None
        else:
            self.reservas.append(reserva)
            print("OK:", reserva.obtener_descripcion())
            return reserva
        finally:
            logging.info("Fin de la operación: crear reserva " + str(id_reserva))

    def cancelar_reserva(self, id_reserva):
        try:
            reserva = self.buscar_reserva(id_reserva)
            if reserva is None:
                raise ReservaInvalidaError("No existe la reserva " + str(id_reserva))
            reserva.cancelar()
        except ErrorSoftwareFJ as e:
            logging.error("No se pudo cancelar la reserva " + str(id_reserva) + ": " + str(e))
            print("ERROR (cancelar):", e)
            return False
        except Exception as e:
            logging.error("Error inesperado al cancelar: " + str(e))
            print("ERROR inesperado:", e)
            return False
        else:
            print("OK: reserva " + str(id_reserva) + " cancelada")
            return True
        finally:
            logging.info("Fin de la operación: cancelar reserva " + str(id_reserva))