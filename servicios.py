from abc import ABC, abstractmethod
from cliente import EntidadGeneral 

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

    def obtener_descripcion(self):
        return "Servicio: " + self.nombre + " | Codigo: " + self.codigo + " | Precio base: $" + str(self.precio_base)

class ReservaSalas(Servicio):
    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ValueError("La reserva de la sala debe ser de al menos 1 hora.")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)
        total = self.precio_base * duracion
        
        if descuento > 0:
            total = total - (total * descuento)
        if impuesto:
            total = total + (total * 0.19)
            
        return total

class AlquilerEquipos(Servicio):
    def __init__(self, codigo, nombre, precio_base, tipo_equipo):
        super().__init__(codigo, nombre, precio_base)
        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):
        if duracion < 1:
            raise ValueError("El alquiler del equipo es por dias completos (minimo 1).")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)
        total = self.precio_base * duracion
        
        if descuento > 0:
            total = total - (total * descuento)
        if impuesto:
            total = total + (total * 0.19)
            
        return total

class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, precio_base, area):
        super().__init__(codigo, nombre, precio_base)
        self.area = area

    def validar_parametros(self, duracion):
        if duracion > 8:
            raise ValueError("Una asesoria no puede durar mas de 8 horas en un mismo dia.")

    def calcular_costo(self, duracion, impuesto=False, descuento=0.0):
        self.validar_parametros(duracion)
        total = self.precio_base * duracion
        
        if descuento > 0:
            total = total - (total * descuento)
        if impuesto:
            total = total + (total * 0.19)
            
        return total