class ErrorSoftwareFJ(Exception):
    """Error base de todo el sistema Software FJ."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un cliente no son válidos."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando un servicio tiene parámetros inválidos."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se usa cuando una reserva no se puede crear o procesar."""

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se usa cuando se intenta reservar un servicio que no está disponible."""