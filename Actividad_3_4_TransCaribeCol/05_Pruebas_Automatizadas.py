"""Pruebas reproducibles: python3 05_Pruebas_Automatizadas.py."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('nomina', BASE / '02_Programa_Nomina.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


class PruebasNomina(unittest.TestCase):
    def test_administrativo(self):
        r = n.calcular('Ana Ejemplo', 'Administrativo', horas=160, extras=8)
        self.assertEqual(r[4], n.D('3200000.00'))
        self.assertEqual(r[6], n.D('200000.00'))
        self.assertEqual(r[4] + r[6], n.D('3400000.00'))
        self.assertIsNone(r[10])
        self.assertIsNone(r[11])

    def test_operativos(self):
        casos = [('Conductor', 160, '6400000', '2560000', '320000', '409600'),
                 ('Oficios Generales', 100, '4000000', '1600000', '200000', '256000'),
                 ('Vigilancia', 336, '13440000', '5376000', '672000', '860160')]
        for cargo, horas, salario, ibc, salud, pension in casos:
            with self.subTest(cargo=cargo):
                r = n.calcular('Persona Ejemplo', 'Operativo', cargo, horas)
                self.assertEqual(r[4], n.D(salario))
                self.assertEqual(r[7:10], list(map(n.D, [ibc, salud, pension])))
                self.assertIsNone(r[10])
                self.assertIsNone(r[11])

    def test_validaciones(self):
        for valor in ['-1', 'NaN', 'Infinity', 'abc']:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                n.numero(valor)
        for nombre in ['', 'A\nB', 'A|B']:
            with self.assertRaises(ValueError):
                n.calcular(nombre, 'Administrativo')
        for cargo, horas, extras in [('Otro', 160, 0), ('Conductor', 100, 0), ('Conductor', 160, 1)]:
            with self.assertRaises(ValueError):
                n.calcular('Ejemplo', 'Operativo', cargo, horas, extras)

    def test_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / 'registros.txt'
            r = n.calcular('Ana Ejemplo', 'Administrativo', horas=160, extras=8)
            n.guardar([r], ruta)
            n.guardar([], ruta)
            texto = ruta.read_text(encoding='utf-8')
            self.assertEqual(texto.count('Nombre: Ana Ejemplo'), 1)
            self.assertIn('Total a pagar: PENDIENTE', texto)
            n.guardar([r], ruta)
            self.assertEqual(ruta.read_text(encoding='utf-8').count('Nombre: Ana Ejemplo'), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
