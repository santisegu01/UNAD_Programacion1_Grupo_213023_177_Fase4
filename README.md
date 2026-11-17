# UNAD_Programacion1_Grupo_213023_177_Fase4
# Proyecto Fase 4 - Software FJ
**Curso:** Programación (213023)  
**Grupo:** 213023_177  
**Autores:** Santiago Esneider Gómez Gutiérrez y Dayan Felipe Ruiz Arias  

## Descripción
Sistema desarrollado en Python para la gestión de clientes, servicios y reservas de la empresa Software FJ. El programa aplica conceptos de Programación Orientada a Objetos (POO) como clases abstractas, herencia y polimorfismo, sin utilizar bases de datos (manejo en memoria y logs de eventos).

## Estructura del Código
- `main.py`: Archivo principal de ejecución y simulación.
- `cliente.py`: Contiene la clase base y la clase Cliente.
- `servicios.py`: Contiene la clase abstracta Servicio y sus tres clases derivadas.
- `reserva.py`: Gestiona la relación entre cliente y servicio, además de los estados.
- `excepciones.py`: Definición de excepciones personalizadas.
- `log_manager.py`: Configuración del sistema de registros (logs).

## Ejecución
1. Instalar Python 3.
2. Ubicarse en la carpeta del proyecto desde la terminal.
3. Ejecutar el comando:
```bash
python main.py