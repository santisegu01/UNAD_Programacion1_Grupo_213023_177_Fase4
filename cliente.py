import re  # Módulo para validar formatos de texto con expresiones regulares (como el correo)
from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas y métodos obligatorios
from excepciones import ClienteInvalidoError  # Excepción personalizada cuando algún dato del cliente no cumple las reglas


class EntidadGeneral(ABC):  # Clase base abstracta para entidades del sistema
    """Clase abstracta base: toda entidad debe poder describirse."""  # Contrato base que deben cumplir las subclases

    @abstractmethod  # Marca el método como obligatorio en las clases que hereden de EntidadGeneral
    def obtener_descripcion(self):  # Método para devolver una descripción legible de la entidad
        pass  # Sin implementación aquí; cada clase hija define cómo describirse


class Cliente(EntidadGeneral):  # Clase Cliente que hereda de EntidadGeneral
    """Cliente de Software FJ con datos encapsulados y validados."""  # Representa un cliente con atributos protegidos y controlados

    def __init__(self, id_cliente, nombre, email, telefono):  # Constructor al crear un nuevo cliente
        self._id_cliente = None  # Inicializa el atributo protegido del ID antes de validarlo
        self._nombre = None  # Inicializa el atributo protegido del nombre antes de validarlo
        self._email = None  # Inicializa el atributo protegido del correo antes de validarlo
        self._telefono = None  # Inicializa el atributo protegido del teléfono antes de validarlo
        self.set_id_cliente(id_cliente)  # Valida y asigna el ID del cliente
        self.set_nombre(nombre)  # Valida y asigna el nombre del cliente
        self.set_email(email)  # Valida y asigna el correo del cliente
        self.set_telefono(telefono)  # Valida y asigna el teléfono del cliente

    # Getters  # Métodos para consultar los datos encapsulados
    def get_id_cliente(self):  # Devuelve el ID del cliente
        return self._id_cliente  # Retorna el valor guardado en _id_cliente

    def get_nombre(self):  # Devuelve el nombre del cliente
        return self._nombre  # Retorna el valor guardado en _nombre

    def get_email(self):  # Devuelve el correo del cliente
        return self._email  # Retorna el valor guardado en _email

    def get_telefono(self):  # Devuelve el teléfono del cliente
        return self._telefono  # Retorna el valor guardado en _telefono

    # Setters con validación  # Métodos para modificar datos comprobando que sean correctos
    def set_id_cliente(self, id_cliente):  # Asigna y valida el ID del cliente
        if not isinstance(id_cliente, int) or id_cliente <= 0:  # Comprueba que sea entero y mayor que cero
            raise ClienteInvalidoError("El ID del cliente debe ser un entero positivo.")  # Lanza error si no cumple
        self._id_cliente = id_cliente  # Guarda el ID válido

    def set_nombre(self, nombre):  # Asigna y valida el nombre del cliente
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:  # Verifica que sea texto y tenga mínimo 3 caracteres sin espacios extra
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")  # Lanza error si el nombre es muy corto o inválido
        self._nombre = nombre.strip()  # Guarda el nombre limpio de espacios en los extremos

    def set_email(self, email):  # Asigna y valida el correo electrónico
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Expresión regular básica para validar estructura usuario@dominio.extensión
        if not isinstance(email, str) or not re.match(patron, email):  # Comprueba que sea texto y coincida con el formato de correo
            raise ClienteInvalidoError(f"El email '{email}' no es válido.")  # Lanza error indicando el correo inválido
        self._email = email  # Guarda el correo válido

    def set_telefono(self, telefono):  # Asigna y valida el número de teléfono
        if not isinstance(telefono, str) or not telefono.isdigit() or not (7 <= len(telefono) <= 10):  # Revisa que sea texto de solo dígitos y entre 7 y 10 caracteres
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos numéricos.")  # Lanza error si no cumple la longitud o es no numérico
        self._telefono = telefono  # Guarda el teléfono válido

    def obtener_descripcion(self):  # Implementa el método abstracto de EntidadGeneral para mostrar los datos del cliente
        return f"Cliente #{self._id_cliente}: {self._nombre} | {self._email} | {self._telefono}"  # Formatea la información principal del cliente

    def __str__(self):  # Define cómo se imprime el objeto Cliente con print() o str()
        return self.obtener_descripcion()  # Reutiliza obtener_descripcion() para evitar duplicar texto
