import logging
from log_manager import configurar_log
from gestor import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada


def titulo(numero, texto):
    """Muestra y registra el encabezado de cada operación."""
    print(f"\n--- Operacion {numero}: {texto} ---")
    logging.info(f"Operacion {numero}: {texto}")


def main():
    configurar_log()
    logging.info("=== INICIO DE LA SIMULACION SOFTWARE FJ ===")
    gestor = GestorSoftwareFJ()

    # Preparación: catálogo de servicios
    print("=== CATALOGO DE SERVICIOS ===")
    gestor.agregar_servicio(ReservaSala("S01", "Sala de juntas", 50000, 10))
    gestor.agregar_servicio(AlquilerEquipo("E01", "Portatil", 30000, "Computador"))
    gestor.agregar_servicio(AsesoriaEspecializada("A01", "Asesoria en Python", 80000, "Programacion"))
    proyector = AlquilerEquipo("E02", "Proyector", 20000, "Video")
    proyector.disponible = False
    gestor.agregar_servicio(proyector)

    print("\n=== SIMULACION DE 10 OPERACIONES ===")

    titulo(1, "Registrar cliente valido (Ana)")
    gestor.registrar_cliente(1, "Ana Perez", "ana@correo.com", "3001234567")

    titulo(2, "Registrar cliente valido (Carlos)")
    gestor.registrar_cliente(2, "Carlos Ruiz", "carlos@correo.com", "3109876543")

    titulo(3, "Registrar cliente con telefono invalido (ERROR esperado)")
    gestor.registrar_cliente(3, "Luis Mora", "luis@correo.com", "12ab")

    titulo(4, "Reservar sala de juntas 3 horas")
    gestor.crear_reserva(1, 1, "S01", 3)

    titulo(5, "Reservar portatil 2 dias")
    gestor.crear_reserva(2, 2, "E01", 2)

    titulo(6, "Reservar asesoria 2 horas")
    gestor.crear_reserva(3, 1, "A01", 2)

    titulo(7, "Reservar con cliente inexistente (ERROR esperado)")
    gestor.crear_reserva(4, 99, "S01", 1)

    titulo(8, "Asesoria de 10 horas (ERROR esperado)")
    gestor.crear_reserva(5, 1, "A01", 10)

    titulo(9, "Reservar servicio no disponible (ERROR encadenado esperado)")
    gestor.crear_reserva(6, 2, "E02", 1)

    titulo(10, "Cancelar la reserva 1")
    gestor.cancelar_reserva(1)

    print("\n=== RESUMEN ===")
    print("Clientes registrados:", len(gestor.clientes))
    print("Servicios en catalogo:", len(gestor.servicios))
    print("Reservas creadas:", len(gestor.reservas))
    logging.info("=== FIN DE LA SIMULACION: el sistema no colapso ===")


if __name__ == "__main__":
    main()