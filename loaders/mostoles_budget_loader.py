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
        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': self.clean(line[1]).zfill(4),    # Fill with zeroes on the left if needed
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

