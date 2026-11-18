import re
from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError


class EntidadGeneral(ABC):
    """Clase abstracta base: toda entidad debe poder describirse."""

    @abstractmethod
    def obtener_descripcion(self):
        pass


class Cliente(EntidadGeneral):
    """Cliente de Software FJ con datos encapsulados y validados."""

    def __init__(self, id_cliente, nombre, email, telefono):
        self._id_cliente = None
        self._nombre = None
        self._email = None
        self._telefono = None
        self.set_id_cliente(id_cliente)
        self.set_nombre(nombre)
        self.set_email(email)
        self.set_telefono(telefono)

    # Getters
    def get_id_cliente(self):
        return self._id_cliente

    def get_nombre(self):
        return self._nombre

    def get_email(self):
        return self._email

    def get_telefono(self):
        return self._telefono

    # Setters con validación
    def set_id_cliente(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            raise ClienteInvalidoError("El ID del cliente debe ser un entero positivo.")
        self._id_cliente = id_cliente

    def set_nombre(self, nombre):
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = nombre.strip()

    def set_email(self, email):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not isinstance(email, str) or not re.match(patron, email):
            raise ClienteInvalidoError(f"El email '{email}' no es válido.")
        self._email = email

    def set_telefono(self, telefono):
        if not isinstance(telefono, str) or not telefono.isdigit() or not (7 <= len(telefono) <= 10):
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos numéricos.")
        self._telefono = telefono

    def obtener_descripcion(self):
        return f"Cliente #{self._id_cliente}: {self._nombre} | {self._email} | {self._telefono}"

    def __str__(self):
        return self.obtener_descripcion()