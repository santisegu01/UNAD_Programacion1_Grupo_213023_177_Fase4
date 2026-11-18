from abc import ABC, abstractmethod
from cliente import EntidadGeneral
from excepciones import ServicioInvalidoError


class Servicio(EntidadGeneral, ABC):
    def __init__(self, codigo, nombre, precio_base):
        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = precio_base
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    def aplicar_descuento_e_impuesto(self, subtotal, impuesto, descuento):
        """Parte común: descuento opcional e IVA del 19 %."""
        total = subtotal
        if descuento > 0:
            total = total - (total * descuento)
        if impuesto:
            total = total + (total * 0.19)
        return total

    def obtener_descripcion(self):
        return "Servicio: " + self.nombre + " | Codigo: " + self.codigo + " | Precio base: $" + str(self.precio_base)


class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ServicioInvalidoError("La reserva de la sala debe ser de al menos 1 hora.")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)
        subtotal = self.precio_base * duracion
        if duracion >= 4:
            subtotal = subtotal * 0.90  # 10 % de descuento por reserva larga
        return self.aplicar_descuento_e_impuesto(subtotal, impuesto, descuento)


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, precio_base, tipo_equipo):
        super().__init__(codigo, nombre, precio_base)
        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):
        if duracion < 1:
            raise ServicioInvalidoError("El alquiler del equipo es por dias completos (minimo 1).")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)
        subtotal = self.precio_base * duracion
        subtotal = subtotal * 1.10  # recargo del 10 % por seguro del equipo
        return self.aplicar_descuento_e_impuesto(subtotal, impuesto, descuento)


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, precio_base, area):
        super().__init__(codigo, nombre, precio_base)
        self.area = area

    def validar_parametros(self, duracion):
        if duracion <= 0 or duracion > 8:
            raise ServicioInvalidoError("Una asesoria debe durar entre 1 y 8 horas en un mismo dia.")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)
        horas_normales = min(duracion, 4)
        horas_extra = max(duracion - 4, 0)
        subtotal = (self.precio_base * horas_normales) + (self.precio_base * 1.25 * horas_extra)
        return self.aplicar_descuento_e_impuesto(subtotal, impuesto, descuento)