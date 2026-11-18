# Archivo: main.py
# Script ejecutable que simula 18 operaciones de Software FJ (el enunciado pide
# mínimo 10): unas correctas y otras con errores controlados. Sirve para demostrar
# que el sistema nunca se cae y que todo queda registrado en el archivo .log.

import logging  # Para escribir en el log desde este archivo
from log_manager import configurar_log  # Prepara el archivo .log
from gestor import GestorSoftwareFJ  # El gestor que ejecuta las operaciones


def titulo(numero, texto):
    """Muestra y registra el encabezado de cada operación."""
    print(f"\n--- Operacion {numero}: {texto} ---")  # Lo muestra en pantalla
    logging.info(f"Operacion {numero}: {texto}")  # Lo guarda en el log


def main():
    configurar_log()  # Debe llamarse una sola vez, al inicio
    logging.info("=== INICIO DE LA SIMULACION SOFTWARE FJ ===")
    gestor = GestorSoftwareFJ()  # Crea el gestor (listas vacías)

    print("=== SIMULACION DE 18 OPERACIONES ===")

    # ----- Clientes -----
    titulo(1, "Registrar cliente valido (Ana)")
    gestor.registrar_cliente(1, "Ana Perez", "ana@correo.com", "3001234567")

    titulo(2, "Registrar cliente valido (Carlos)")
    gestor.registrar_cliente(2, "Carlos Ruiz", "carlos@correo.com", "3109876543")

    titulo(3, "Registrar cliente con telefono invalido (ERROR esperado)")
    gestor.registrar_cliente(3, "Luis Mora", "luis@correo.com", "12ab")

    # ----- Servicios -----
    titulo(4, "Crear servicio valido: sala de juntas")
    gestor.crear_servicio("sala", "S01", "Sala de juntas", 50000, 10)

    titulo(5, "Crear servicio valido: alquiler de portatil")
    gestor.crear_servicio("equipo", "E01", "Portatil", 30000, "Computador")

    titulo(6, "Crear servicio valido: asesoria en Python")
    gestor.crear_servicio("asesoria", "A01", "Asesoria en Python", 80000, "Programacion")

    titulo(7, "Crear proyector y dejarlo no disponible")
    proyector = gestor.crear_servicio("equipo", "E02", "Proyector", 20000, "Video")
    if proyector is not None:  # Solo si se creó bien
        proyector.disponible = False  # Lo marcamos como no disponible

    titulo(8, "Crear servicio con precio negativo (ERROR esperado)")
    gestor.crear_servicio("sala", "S02", "Sala VIP", -5000, 8)

    # ----- Reservas -----
    titulo(9, "Reservar sala de juntas 3 horas")
    gestor.crear_reserva(1, 1, "S01", 3)

    titulo(10, "Reservar portatil 2 dias")
    gestor.crear_reserva(2, 2, "E01", 2)

    titulo(11, "Reservar asesoria 2 horas")
    gestor.crear_reserva(3, 1, "A01", 2)

    titulo(12, "Reservar con cliente inexistente (ERROR esperado)")
    gestor.crear_reserva(4, 99, "S01", 1)

    titulo(13, "Asesoria de 10 horas (ERROR esperado)")
    gestor.crear_reserva(5, 1, "A01", 10)

    titulo(14, "Reservar servicio no disponible (ERROR encadenado esperado)")
    gestor.crear_reserva(6, 2, "E02", 1)

    # ----- Cotizaciones (variantes del cálculo de costos) -----
    titulo(15, "Cotizar la sala 3 horas: sin extras, con impuesto, con descuento y con ambos")
    gestor.cotizar("S01", 3)
    gestor.cotizar("S01", 3, impuesto=True)
    gestor.cotizar("S01", 3, descuento=0.10)
    gestor.cotizar("S01", 3, impuesto=True, descuento=0.10)

    titulo(16, "Cotizar con descuento inconsistente de 150 % (ERROR esperado)")
    gestor.cotizar("S01", 3, descuento=1.5)

    # ----- Cancelaciones -----
    titulo(17, "Cancelar la reserva 1")
    gestor.cancelar_reserva(1)

    titulo(18, "Cancelar de nuevo la reserva 1 (ERROR esperado)")
    gestor.cancelar_reserva(1)

    # ----- Resumen final -----
    print("\n=== RESUMEN ===")
    print("Clientes registrados:", len(gestor.clientes))
    print("Servicios en catalogo:", len(gestor.servicios))
    print("Reservas creadas:", len(gestor.reservas))
    logging.info("=== FIN DE LA SIMULACION: el sistema no colapso ===")


# Este bloque hace que main() solo corra al ejecutar este archivo directamente
if __name__ == "__main__":
    main()