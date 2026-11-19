import re
from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError


class EntidadGeneral(ABC):
    """Clase base abstracta: obliga a las entidades del sistema a tener una descripción."""

    @abstractmethod
    def obtener_descripcion(self):
        # Cada clase hija define cómo se muestra su información
        pass


class Cliente(EntidadGeneral):
    """Representa un cliente con datos protegidos y validados antes de guardarlos."""

    def __init__(self, id_cliente, nombre, email, telefono):
        # Arrancamos en None y pasamos por los setters para que todo pase por validación
        self._id_cliente = None
        self._nombre = None
        self._email = None
        self._telefono = None
        self.set_id_cliente(id_cliente)
        self.set_nombre(nombre)
        self.set_email(email)
        self.set_telefono(telefono)

    # Getters para leer los atributos encapsulados
    def get_id_cliente(self):
        return self._id_cliente

    def get_nombre(self):
        return self._nombre

    def get_email(self):
        return self._email

    def get_telefono(self):
        return self._telefono

    # Setters con validaciones para evitar datos inconsistentes en memoria
    def set_id_cliente(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            raise ClienteInvalidoError("El ID del cliente debe ser un entero positivo.")
        self._id_cliente = id_cliente

    def set_nombre(self, nombre):
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        # Quitamos espacios sobrantes al inicio y al final
        self._nombre = nombre.strip()

    def set_email(self, email):
        # Validación básica de estructura usuario@dominio.extension
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not isinstance(email, str) or not re.match(patron, email):
            raise ClienteInvalidoError(f"El email '{email}' no es válido.")
        self._email = email

    def set_telefono(self, telefono):
        # Solo se aceptan números de 7 a 10 dígitos en formato texto
        if not isinstance(telefono, str) or not telefono.isdigit() or not (7 <= len(telefono) <= 10):
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos numéricos.")
        self._telefono = telefono

    def obtener_descripcion(self):
        return f"Cliente #{self._id_cliente}: {self._nombre} | {self._email} | {self._telefono}"

    def __str__(self):
        # Permite imprimir el objeto directamente usando la misma descripción
        return self.obtener_descripcion()
