"""Actividad 3.4. Ejecutar con Python 3; solo usa biblioteca estándar.
Las tasas incompletas de la guía se dejan pendientes de confirmación.
"""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

D = Decimal
ARCHIVO = Path(__file__).resolve().with_name('03_Registros_Nomina.txt')
# Cargo: horas de referencia, tarifa ARL expresada como fracción.
CARGOS = {'Conductor': (160, D('0.01044')),
          'Oficios Generales': (100, D('0.00522')),
          'Vigilancia': (336, D('0.04350'))}
COLUMNAS = ['Nombre', 'Tipo', 'Cargo', 'HT', 'Salario', 'HE', 'TPHE',
            'IBC', 'Salud', 'Pensión', 'ARL', 'Total a pagar', 'Estado']


def numero(valor):
    try:
        resultado = D(str(valor))
    except InvalidOperation as exc:
        raise ValueError('Ingrese un número válido, con punto decimal.') from exc
    if not resultado.is_finite() or resultado < 0:
        raise ValueError('El valor debe ser finito y no negativo.')
    return resultado


def dinero(valor):
    return valor.quantize(D('0.01'), rounding=ROUND_HALF_UP)


def calcular(nombre, tipo, cargo='', horas=0, extras=0):
    nombre = nombre.strip()
    if not nombre or any(c in nombre for c in '\n\r\t|'):
        raise ValueError('Nombre obligatorio, sin saltos de línea, tabuladores ni |.')
    horas, extras = numero(horas), numero(extras)
    if tipo == 'Administrativo':
        cargo = 'Administrativo'
        salario, tphe = dinero(horas * 20000), dinero(extras * 25000)
        ibc = salud = pension = arl = total = None
        estado = ('PARCIAL: devengado ' + str(salario + tphe)
                  + '; pendientes IBC, base ARL, salud, pensión, prestaciones y neto. ARL indicada: 0.522%.')
    elif tipo == 'Operativo' and cargo in CARGOS:
        if extras:
            raise ValueError('La guía no define horas extra operativas.')
        if horas != D(CARGOS[cargo][0]):
            raise ValueError('Use las horas mensuales indicadas para este cargo.')
        salario, tphe = dinero(horas * 40000), D('0.00')
        ibc = dinero(salario * D('0.40'))
        salud, pension = dinero(ibc * D('0.125')), dinero(ibc * D('0.16'))
        # Base ARL operativa pendiente: no se supone que sea el IBC.
        arl = total = None
        estado = ('PARCIAL: ARL ' + str(CARGOS[cargo][1] * 100)
                  + '%; confirmar base ARL y quién asume aportes antes de calcular neto.')
    else:
        raise ValueError('Tipo o cargo no válido.')
    return [nombre, tipo, cargo, horas, salario, extras, tphe,
            ibc, salud, pension, arl, total, estado]


def comprobante(registro):
    return '\n'.join(f'{campo}: {"PENDIENTE" if valor is None else valor}'
                     for campo, valor in zip(COLUMNAS, registro))


def guardar(registros, ruta=ARCHIVO):
    """Añade un lote de registros; conserva los lotes anteriores."""
    ruta = Path(ruta)
    with ruta.open('a', encoding='utf-8') as archivo:
        for registro in registros:
            archivo.write('TRANSCARIBECOL - COMPROBANTE ACADÉMICO\n')
            archivo.write(comprobante(registro) + '\n' + '-' * 72 + '\n')


def pedir_numero(mensaje):
    while True:
        try:
            return numero(input(mensaje))
        except ValueError as error:
            print(error)


def main():
    registros = []  # Matriz: cada fila sigue el orden de COLUMNAS.
    guardados = 0
    while True:
        print('\nTRANSCARIBECOL\n1. Registrar trabajador\n2. Ver comprobantes\n3. Guardar TXT\n4. Leer TXT\n0. Salir')
        opcion = input('Opción: ').strip()
        if opcion == '1':
            nombre = input('Nombre: ')
            tipo = input('Tipo (1 Administrativo / 2 Operativo): ').strip()
            try:
                if tipo == '1':
                    fila = calcular(nombre, 'Administrativo', horas=pedir_numero('Horas ordinarias: '),
                                    extras=pedir_numero('Horas extra: '))
                elif tipo == '2':
                    cargos = list(CARGOS)
                    print('\n'.join(f'{i+1}. {c}' for i, c in enumerate(cargos)))
                    seleccion = input('Cargo: ').strip()
                    if seleccion not in ('1', '2', '3'):
                        raise ValueError('Cargo no válido.')
                    cargo = cargos[int(seleccion)-1]
                    fila = calcular(nombre, 'Operativo', cargo, CARGOS[cargo][0])
                else:
                    raise ValueError('Tipo no válido.')
                registros.append(fila)
                print(comprobante(fila))
            except ValueError as error:
                print(error)
        elif opcion == '2':
            print('\n\n'.join(map(comprobante, registros)) or 'No hay registros en esta sesión.')
        elif opcion == '3':
            try:
                guardar(registros[guardados:])
                guardados = len(registros)
                print(f'Registros guardados. Archivo: {ARCHIVO}')
            except OSError as error:
                print(f'No se pudo guardar: {error}. Puede volver a intentar.')
        elif opcion == '4':
            try:
                print(ARCHIVO.read_text(encoding='utf-8'))
            except OSError as error:
                print(f'No se pudo leer: {error}')
        elif opcion == '0':
            try:
                guardar(registros[guardados:])
                print('Registros guardados. Fin.')
                break
            except OSError as error:
                print(f'No se pudo guardar: {error}. Reintente con la opción 3.')
        else:
            print('Opción no válida.')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nEntrada interrumpida. Use 3 o 0 para guardar antes de cerrar.')
