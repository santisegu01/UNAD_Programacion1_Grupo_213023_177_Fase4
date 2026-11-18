# Archivo: servicios.py
# Define la clase abstracta Servicio y sus tres servicios especializados.
# Aquí se aplican la herencia, el polimorfismo y la sobrescritura de métodos.

from abc import ABC, abstractmethod  # Herramientas para crear clases y métodos abstractos
from cliente import EntidadGeneral  # Clase abstracta base de todas las entidades
from excepciones import ServicioInvalidoError  # Error propio para servicios inválidos


class Servicio(EntidadGeneral, ABC):
    """Clase abstracta: define lo que todo servicio debe tener y hacer."""

    def __init__(self, codigo, nombre, precio_base):
        # Validación: el código debe ser un texto que no esté vacío
        if not isinstance(codigo, str) or not codigo.strip():
            raise ServicioInvalidoError("El codigo del servicio no puede estar vacio.")
        # Validación: el nombre debe ser un texto que no esté vacío
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacio.")
        # Validación: el precio debe ser un número mayor que cero
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ServicioInvalidoError("El precio base debe ser un numero mayor que cero.")
        self.codigo = codigo  # Identificador único del servicio
        self.nombre = nombre  # Nombre que verá el cliente
        self.precio_base = precio_base  # Precio por hora o por día, según el servicio
        self.disponible = True  # Si es False, el servicio no se puede reservar

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        """Cada hija define su propia regla de cobro (polimorfismo)."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        """Cada hija define qué duraciones acepta."""
        pass

    def aplicar_descuento_e_impuesto(self, subtotal, impuesto, descuento):
        """Parte común del cálculo: descuento opcional e IVA del 19 %."""
        # Un descuento fuera del rango 0 a 1 (0 % a 100 %) es un cálculo inconsistente
        if descuento < 0 or descuento > 1:
            raise ServicioInvalidoError("El descuento debe estar entre 0 y 1.")
        total = subtotal  # Se parte del subtotal ya calculado por la clase hija
        if descuento > 0:
            total = total - (total * descuento)  # Resta el porcentaje de descuento
        if impuesto:
            total = total + (total * 0.19)  # Suma el IVA del 19 %
        return total

    def obtener_descripcion(self):
        """Descripción general; las hijas la sobrescriben para añadir sus datos."""
        return "Servicio: " + self.nombre + " | Codigo: " + self.codigo + " | Precio base: $" + str(self.precio_base)


class ReservaSala(Servicio):
    """Reserva de salas, cobrada por hora."""

    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)  # Reutiliza el constructor del padre
        # La capacidad debe ser un entero positivo
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad  # Número de personas que caben en la sala

    def validar_parametros(self, duracion):
        # La sala se reserva por horas, mínimo una
        if duracion <= 0:
            raise ServicioInvalidoError("La reserva de la sala debe ser de al menos 1 hora.")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)  # Primero se valida la duración
        subtotal = self.precio_base * duracion  # Precio por hora x horas
        if duracion >= 4:
            subtotal = subtotal * 0.90  # Regla propia: 10 % de descuento desde 4 horas
        return self.aplicar_descuento_e_impuesto(subtotal, impuesto, descuento)

    def obtener_descripcion(self):
        # Sobrescribe la descripción del padre y le suma la capacidad
        return super().obtener_descripcion() + " | Capacidad: " + str(self.capacidad) + " personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos, cobrado por día."""

    def __init__(self, codigo, nombre, precio_base, tipo_equipo):
        super().__init__(codigo, nombre, precio_base)  # Reutiliza el constructor del padre
        # El tipo de equipo debe ser un texto no vacío
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo no puede estar vacio.")
        self.tipo_equipo = tipo_equipo  # Por ejemplo: Computador, Video

    def validar_parametros(self, duracion):
        # El equipo se alquila por días completos, mínimo uno
        if duracion < 1:
            raise ServicioInvalidoError("El alquiler del equipo es por dias completos (minimo 1).")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)  # Primero se valida la duración
        subtotal = self.precio_base * duracion  # Precio por día x días
        subtotal = subtotal * 1.10  # Regla propia: recargo del 10 % por seguro del equipo
        return self.aplicar_descuento_e_impuesto(subtotal, impuesto, descuento)

    def obtener_descripcion(self):
        # Sobrescribe la descripción del padre y le suma el tipo de equipo
        return super().obtener_descripcion() + " | Tipo de equipo: " + self.tipo_equipo


class AsesoriaEspecializada(Servicio):
    """Asesorías por hora, con recargo después de las primeras 4 horas."""

    def __init__(self, codigo, nombre, precio_base, area):
        super().__init__(codigo, nombre, precio_base)  # Reutiliza el constructor del padre
        # El área debe ser un texto no vacío
        if not isinstance(area, str) or not area.strip():
            raise ServicioInvalidoError("El area de la asesoria no puede estar vacia.")
        self.area = area  # Área de conocimiento de la asesoría

    def validar_parametros(self, duracion):
        # Una asesoría dura entre 1 y 8 horas en un mismo día
        if duracion <= 0 or duracion > 8:
            raise ServicioInvalidoError("Una asesoria debe durar entre 1 y 8 horas en un mismo dia.")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)  # Primero se valida la duración
        horas_normales = min(duracion, 4)  # Las primeras 4 horas van a tarifa normal
        horas_extra = max(duracion - 4, 0)  # Las demás horas llevan recargo
        # Regla propia: las horas extra cuestan 25 % más
        subtotal = (self.precio_base * horas_normales) + (self.precio_base * 1.25 * horas_extra)
        return self.aplicar_descuento_e_impuesto(subtotal, impuesto, descuento)

    def obtener_descripcion(self):
        # Sobrescribe la descripción del padre y le suma el área
        return super().obtener_descripcion() + " | Area: " + self.area