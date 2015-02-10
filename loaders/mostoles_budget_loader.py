# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class MostolesBudgetLoader(SimpleBudgetLoader):

    # An artifact of the in2csv conversion of the original XLS files is a trailing '.0', which we remove here
    def clean(self, s):
        return s.split('.')[0]

    def parse_item(self, filename, line):
        # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
        # mapping to be constant over time, we are forced to amend budget data prior to 2015.
        # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
        programme_mapping = {
            '1341': '1351',     # Protección Civil
            '1351': '1361',     # Extinción de incendios y salvamento
            '1511': '1501',     # Servicios generales de urbanismo y arquitectura
            '1621': '1623',     # Tratamiento de residuos
            '1791': '1722',     # Educación ambiental
            '2301': '2311',     # Servicios sociales generales
            '2321': '2315',     # Promoción de la igualdad
            '2322': '2316',     # Programa contra la violencia de género
            '2323': '2312',     # Cooperación
            '2331': '2313',     # Mayores
            '2332': '2314',     # Atención a asociaciones sociosanitarias
            '3131': '3111',     # Promoción de la salud
            '3242': '3261',     # Servicios complementarios a la educación
            '3243': '3231',     # Otras enseñanzas
            '3351': '3346',     # Teatro del Bosque
            '3391': '3347',     # Juventud
            '9271': '9261',     # Servicios informáticos
            '9272': '9262'      # Infraestructuras para las nuevas tecnologías
        }

        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            fc_code = self.clean(line[1]).zfill(4)          # Fill with zeroes on the left if needed

            # For years before 2015 we check whether we need to amend the programme code
            year = re.search('municipio/(\d+)/', filename).group(1)
            if year in ['2011', '2012', '2013', '2014']:
                new_programme = programme_mapping.get(fc_code)
                if new_programme:
                    fc_code = new_programme

            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': fc_code,
                'ec_code': self.clean(line[2]),
                'ic_code': self.clean(line[0]).zfill(4),    # Fill with zeroes on the left if needed
                'item_number': self.clean(line[2])[-2:],    # Last two digits
                'description': line[3],
                'amount': self._parse_amount(line[10 if is_actual else 7])
            }

        else:
            return {
                'is_expense': False,
                'is_actual': is_actual,
                'ec_code': self.clean(line[2]),
                'ic_code': '000',                           # All income goes to the root node
                'description': line[3],
                'amount': self._parse_amount(line[7 if is_actual else 4])
            }

