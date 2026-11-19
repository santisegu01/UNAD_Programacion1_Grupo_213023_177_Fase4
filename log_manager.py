import logging


def configurar_log(nombre_archivo="registro_softwarefj.log"):
    """Configura el registro de eventos y errores en un archivo .log."""
    # Guarda los mensajes desde nivel INFO hacia arriba en el archivo de log
    logging.basicConfig(
        filename=nombre_archivo,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        # Usamos utf-8 para que tildes y caracteres especiales no den problema al escribir el log
        encoding="utf-8",
    )
