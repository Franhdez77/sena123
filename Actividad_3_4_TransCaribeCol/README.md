# Actividad 3.4 — TransCaribeCol

Aplicación académica de consola para registrar personal administrativo y operativo, calcular los conceptos definidos por la guía y guardar comprobantes en TXT.

## Ejecutar

Requisito: Python 3.8 o superior. No necesita instalar paquetes.

Abra una terminal en esta carpeta:

```bash
python3 02_Programa_Nomina.py
```

En Windows puede usar `py 02_Programa_Nomina.py`.

1. **Registrar trabajador:** escriba nombre y tipo. Para administrativo indique horas ordinarias y extra; use punto decimal cuando sea necesario. Para operativo elija cargo; se cargan las horas mensuales establecidas en la guía.
2. **Ver comprobantes:** muestra los registros de la sesión actual.
3. **Guardar TXT:** añade los registros pendientes a `03_Registros_Nomina.txt` junto al programa. Puede guardar varias veces sin duplicar los mismos registros de la sesión.
4. **Leer TXT:** muestra los registros guardados, incluidas sesiones anteriores.
0. **Salir:** guarda los registros pendientes y termina.

Los cuatro ejemplos entregados son ficticios y fueron generados ejecutando el programa. Los nuevos registros se añaden al archivo existente. Para probar sin modificar los ejemplos, trabaje sobre una copia de la carpeta.

## Reglas incompletas

La guía omite tasas y fórmulas de prestaciones administrativas, bases para ARL y convenciones del neto. Esos campos aparecen como **PENDIENTE**. Las tasas de ARL indicadas se muestran en el estado, sin inventar la base. Salud y pensión operativas se calculan sobre el IBC, sin asumir que ambos importes se descuentan del trabajador. Las horas extra administrativas forman parte del devengado que deberá considerarse al definir prestaciones.

No se ha consultado a la instructora ni se presenta ninguna suposición como autorizada. Las preguntas están en el documento de análisis. Una vez confirmadas las reglas, habrá que incorporarlas al programa y actualizar las pruebas. No usar esta solución como liquidación legal.

## Archivos

- `01_Analisis_y_Diseno.docx`: problema, requisitos, reglas, dudas, pseudocódigo, variables, matriz y menú.
- `02_Programa_Nomina.py`: aplicación completa y ejecutable para las reglas disponibles.
- `03_Registros_Nomina.txt`: cuatro comprobantes producidos por el programa.
- `04_Pruebas_y_Evidencias.docx`: resultados esperados y obtenidos, observaciones e imágenes de comprobantes.
- `05_Pruebas_Automatizadas.py`: pruebas reproducibles de cálculos, validación y TXT.
- `evidencias/`: entrada y salida reales de consola, resultado de pruebas e imágenes que renderizan los comprobantes. Son renderizados de texto, no capturas de una ventana de terminal.

## Verificar

```bash
python3 05_Pruebas_Automatizadas.py
```

Las pruebas usan un TXT temporal y no modifican los ejemplos entregados. Para reproducir la sesión completa, en una **copia** de la carpeta:

```bash
python3 02_Programa_Nomina.py < evidencias/01_Entrada_consola.txt
```

Esa sesión añade cuatro registros nuevos. Una sesión nueva no identifica duplicados por persona o período.

## Antes de entregar

Completar los nombres de los integrantes en el análisis; revisar juntos código y documentos; consultar las reglas pendientes con la instructora y actualizar la liquidación cuando se definan. La guía pide trabajo en pareja y sustentación individual: esta carpeta no acredita esas actividades. Si la instructora exige capturas literales de terminal, ejecutar el menú y añadirlas al documento de evidencias.
