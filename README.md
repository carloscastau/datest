# Solución Prueba Técnica
## Introducción
Este proyecto aborda dos aspectos clave: la creación de un modelo de datos que permita compartir valores numéricos entre "Forecasts" de manera eficiente y la implementación de un dashboard web interactivo para comparar la evolución de ingresos y costos de servicios de una compañía.

El primer desafío consiste en diseñar un modelo de datos que facilite la gestión de múltiples "Forecasts" mientras se garantiza la coherencia de los datos numéricos compartidos entre ellos. Para ello, se propone una estructura de base de datos relacional que permite actualizar los valores numéricos de manera centralizada, asegurando que los cambios se reflejen automáticamente en todos los "Forecasts" relacionados.

Por otro lado, se desarrollará un dashboard web utilizando Dash (plotly) en Python para visualizar la evolución mensual de los ingresos y costos de servicios de la compañía. Este dashboard proporcionará una herramienta interactiva para analizar y comparar fácilmente los datos, permitiendo al usuario filtrar y seleccionar las líneas de negocio de interés.

El objetivo de este proyecto es demostrar la capacidad para diseñar soluciones eficientes y prácticas para problemas comunes en el análisis de datos y la visualización de información empresarial.

1. **Modelo de Datos**
Para abordar el requerimiento de compartir los valores numéricos entre los "Forecasts" de manera que los cambios en un "Forecast" se reflejen en los "Forecasts" precedentes, se propone el siguiente modelo de datos:

- Se utilizará una estructura de base de datos relacional.
- Habrá una tabla principal para los "Forecasts", que contendrá los datos generales de cada previsión.
- Se creará una tabla adicional para almacenar los valores numéricos de los rectángulos azul claro.
- Los "Forecasts" tendrán una relación uno a uno con los valores numéricos, utilizando una clave externa para mantener la integridad referencial.
- Al actualizar un valor numérico en un "Forecast", se propagará automáticamente a los "Forecasts" precedentes mediante un mecanismo de trigger o procedimiento almacenado en la base de datos.

2. **Dashboard Web**
El dashboard web se desarrollará utilizando Dash (plotly) en Python, cumpliendo con los siguientes requisitos:

- Se creará una sola gráfica que muestre la evolución mes a mes de los ingresos y costos de servicios de una compañía.
- Se incluirá un filtro de selección múltiple que permita al usuario actualizar la gráfica incluyendo o descartando líneas de negocio.
- Se utilizarán los archivos CSV proporcionados con los datos de ingresos y costos de servicios.
- El código fuente del proyecto se alojará en un repositorio en GitHub.

## Repositorio GitHub
El código fuente del proyecto se encontrará en un repositorio público en GitHub. El cual se puede acceder como repositorio.