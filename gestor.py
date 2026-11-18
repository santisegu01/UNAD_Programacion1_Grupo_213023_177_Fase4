# Archivo: gestor.py
# El gestor es el "jefe de operaciones" de Software FJ: guarda clientes, servicios
# y reservas en listas (en memoria) y ejecuta cada operación dentro de un try/except
# para que ningún error detenga el programa. Todo queda anotado en el log.

import logging  # Módulo estándar para escribir eventos y errores en el archivo .log
from cliente import Cliente  # Clase Cliente, con sus validaciones
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # Los 3 servicios
from reserva import Reserva  # Clase que une cliente + servicio + duración
from excepciones import (  # Excepciones propias del sistema
    ErrorSoftwareFJ,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
)


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en memoria."""

    def __init__(self):
        self.clientes = []  # Lista de objetos Cliente
        self.servicios = []  # Lista de objetos Servicio
        self.reservas = []  # Lista de objetos Reserva
        # Tipos de servicio que el gestor sabe crear: texto -> clase
        self.tipos_servicio = {
            "sala": ReservaSala,
            "equipo": AlquilerEquipo,
            "asesoria": AsesoriaEspecializada,
        }

    # ---------- Búsquedas ----------
    def buscar_cliente(self, id_cliente):
        for c in self.clientes:  # Recorre la lista de clientes
            if c.get_id_cliente() == id_cliente:  # Compara el ID
                return c  # Lo encontró: devuelve el cliente
        return None  # No lo encontró

    def buscar_servicio(self, codigo):
        for s in self.servicios:  # Recorre la lista de servicios
            if s.codigo == codigo:  # Compara el código
                return s  # Lo encontró: devuelve el servicio
        return None  # No lo encontró

    def buscar_reserva(self, id_reserva):
        for r in self.reservas:  # Recorre la lista de reservas
            if r.id_reserva == id_reserva:  # Compara el ID
                return r  # La encontró: devuelve la reserva
        return None  # No la encontró

    # ---------- Operaciones ----------
    def registrar_cliente(self, id_cliente, nombre, email, telefono):
        """Registra un cliente. Si los datos son inválidos, lo anota en el log y sigue."""
        try:  # Intenta crear el cliente
            if self.buscar_cliente(id_cliente) is not None:  # No se permiten IDs repetidos
                raise ClienteInvalidoError("Ya existe un cliente con el ID " + str(id_cliente))
            cliente = Cliente(id_cliente, nombre, email, telefono)  # Aquí corren las validaciones
        except ClienteInvalidoError as e:  # Error propio: datos del cliente inválidos
            logging.error("No se pudo registrar el cliente: " + str(e))
            print("ERROR (cliente):", e)
            return None
        except Exception as e:  # Red de seguridad: cualquier error que no previmos
            logging.error("Error inesperado al registrar cliente: " + str(e))
            print("ERROR inesperado:", e)
            return None
        else:  # Solo se ejecuta si NO hubo error
            self.clientes.append(cliente)  # Guarda el cliente en la lista
            logging.info("Cliente registrado: " + cliente.get_nombre())
            print("OK:", cliente.obtener_descripcion())
            return cliente
        finally:  # Se ejecuta SIEMPRE, haya error o no
            logging.info("Fin de la operación: registrar cliente")

    def crear_servicio(self, tipo, codigo, nombre, precio_base, dato_extra):
        """Crea un servicio ('sala', 'equipo' o 'asesoria'). dato_extra es la capacidad,
        el tipo de equipo o el área, según el servicio."""
        try:  # Intenta crear el servicio
            if tipo not in self.tipos_servicio:  # Tipo que no existe en el catálogo
                raise ServicioInvalidoError("Tipo de servicio desconocido: " + str(tipo))
            if self.buscar_servicio(codigo) is not None:  # No se permiten códigos repetidos
                raise ServicioInvalidoError("Ya existe un servicio con el codigo " + str(codigo))
            clase = self.tipos_servicio[tipo]  # Elige la clase según el tipo
            servicio = clase(codigo, nombre, precio_base, dato_extra)  # Aquí corren las validaciones
        except ErrorSoftwareFJ as e:  # Error propio del sistema
            logging.error("No se pudo crear el servicio " + str(codigo) + ": " + str(e))
            print("ERROR (servicio):", e)
            return None
        except Exception as e:  # Red de seguridad
            logging.error("Error inesperado al crear servicio: " + str(e))
            print("ERROR inesperado:", e)
            return None
        else:  # Solo si NO hubo error
            self.servicios.append(servicio)  # Guarda el servicio en la lista
            logging.info("Servicio creado: " + servicio.nombre)
            print("OK:", servicio.obtener_descripcion())
            return servicio
        finally:  # Se ejecuta SIEMPRE
            logging.info("Fin de la operación: crear servicio " + str(codigo))

    def cotizar(self, codigo_servicio, duracion, impuesto=False, descuento=0.0):
        """Calcula el costo de un servicio. impuesto y descuento son opcionales, así que
        el mismo método se puede llamar de varias formas (variantes del cálculo)."""
        try:  # Intenta calcular el costo
            servicio = self.buscar_servicio(codigo_servicio)  # Busca el servicio
            if servicio is None:
                raise ServicioInvalidoError("No existe el servicio " + str(codigo_servicio))
            costo = servicio.calcular_costo(duracion, impuesto, descuento)  # Polimorfismo
        except ErrorSoftwareFJ as e:  # Error propio (duración o descuento inválidos)
            logging.error("No se pudo cotizar " + str(codigo_servicio) + ": " + str(e))
            print("ERROR (cotizacion):", e)
            return None
        except Exception as e:  # Red de seguridad (por ejemplo, una duración escrita como texto)
            logging.error("Error inesperado al cotizar: " + str(e))
            print("ERROR inesperado:", e)
            return None
        else:  # Solo si NO hubo error
            costo = round(costo, 2)  # Redondea a 2 decimales
            mensaje = ("Cotizacion " + servicio.nombre + " x " + str(duracion)
                       + " (impuesto=" + str(impuesto) + ", descuento=" + str(descuento)
                       + "): $" + str(costo))
            logging.info(mensaje)
            print("OK:", mensaje)
            return costo
        finally:  # Se ejecuta SIEMPRE
            logging.info("Fin de la operación: cotizar " + str(codigo_servicio))

    def crear_reserva(self, id_reserva, id_cliente, codigo_servicio, duracion):
        """Crea una reserva y la procesa (confirma)."""
        try:  # Intenta crear y procesar la reserva
            if self.buscar_reserva(id_reserva) is not None:  # No se permiten IDs repetidos
                raise ReservaInvalidaError("Ya existe una reserva con el ID " + str(id_reserva))
            cliente = self.buscar_cliente(id_cliente)  # Busca al cliente
            if cliente is None:
                raise ClienteInvalidoError("No existe el cliente " + str(id_cliente))
            servicio = self.buscar_servicio(codigo_servicio)  # Busca el servicio
            if servicio is None:
                raise ServicioInvalidoError("No existe el servicio " + str(codigo_servicio))
            servicio.validar_parametros(duracion)  # Valida la duración según el servicio
            reserva = Reserva(id_reserva, cliente, servicio, duracion)  # Une todo en una reserva
            reserva.procesar()  # Confirma la reserva (puede lanzar errores encadenados)
        except ErrorSoftwareFJ as e:  # Cualquier error propio del sistema
            logging.error("No se pudo crear la reserva " + str(id_reserva) + ": " + str(e))
            print("ERROR (reserva):", e)
            return None
        except Exception as e:  # Red de seguridad
            logging.error("Error inesperado al crear reserva: " + str(e))
            print("ERROR inesperado:", e)
            return None
        else:  # Solo si NO hubo error
            self.reservas.append(reserva)  # Guarda la reserva en la lista
            print("OK:", reserva.obtener_descripcion())
            return reserva
        finally:  # Se ejecuta SIEMPRE
            logging.info("Fin de la operación: crear reserva " + str(id_reserva))

    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva existente."""
        try:  # Intenta cancelar
            reserva = self.buscar_reserva(id_reserva)  # Busca la reserva
            if reserva is None:
                raise ReservaInvalidaError("No existe la reserva " + str(id_reserva))
            reserva.cancelar()  # Lanza error si ya estaba cancelada
        except ErrorSoftwareFJ as e:  # Error propio del sistema
            logging.error("No se pudo cancelar la reserva " + str(id_reserva) + ": " + str(e))
            print("ERROR (cancelar):", e)
            return False
        except Exception as e:  # Red de seguridad
            logging.error("Error inesperado al cancelar: " + str(e))
            print("ERROR inesperado:", e)
            return False
        else:  # Solo si NO hubo error
            print("OK: reserva " + str(id_reserva) + " cancelada")
            return True
        finally:  # Se ejecuta SIEMPRE
            logging.info("Fin de la operación: cancelar reserva " + str(id_reserva))