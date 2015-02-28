# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url

MAIN_ENTITY_LEVEL = 'municipio'
MAIN_ENTITY_NAME = 'Móstoles'

BUDGET_LOADER = 'MostolesBudgetLoader'

FEATURED_PROGRAMMES = ['1321', '3347', '1711']

OVERVIEW_INCOME_NODES = [['11', '113'], '42', '45', '29', '13']
OVERVIEW_EXPENSE_NODES = ['23', '92', '13', '16', '15', '33', '32']

# Show an extra tab with institutional breakdown. Default: True.
# SHOW_INSTITUTIONAL_TAB = True

# Show an extra tab with funding breakdown (only applicable to some budgets). Default: False.
# SHOW_FUNDING_TAB = False

# Show an extra column with actual revenues/expenses. Default: True.
# Warning: the execution data still gets shown in the summary chart and in downloads.
#SHOW_ACTUAL = True

# Search in entity names. Default: True.
SEARCH_ENTITIES = False
