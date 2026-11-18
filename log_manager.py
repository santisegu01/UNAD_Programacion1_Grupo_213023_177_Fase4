import logging


def configurar_log(nombre_archivo="registro_softwarefj.log"):
    """Configura el registro de eventos y errores en un archivo .log."""
    logging.basicConfig(
        filename=nombre_archivo,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )