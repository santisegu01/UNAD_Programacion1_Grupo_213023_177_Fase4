# Archivo: excepciones.py
# Aquí se definen las excepciones personalizadas del sistema Software FJ.
# Una excepción personalizada es un tipo de error propio, que nos permite
# distinguir los problemas del negocio de los errores genéricos de Python.


# Excepción base: todas las demás heredan de ella.
# Hereda de Exception, la clase de error general de Python.
class ErrorSoftwareFJ(Exception):
    """Error base de todo el sistema Software FJ."""


# Se lanza cuando los datos de un cliente no cumplen las validaciones.
# Hereda de ErrorSoftwareFJ, así se puede atrapar junto con las demás.
class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un cliente no son válidos."""


# Se lanza cuando un servicio recibe parámetros incorrectos (por ejemplo, una duración inválida).
class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando un servicio tiene parámetros inválidos."""


# Se lanza cuando una reserva no se puede crear, procesar o cancelar.
class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se usa cuando una reserva no se puede crear o procesar."""


# Se lanza cuando se intenta reservar un servicio que está marcado como no disponible.
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se usa cuando se intenta reservar un servicio que no está disponible."""