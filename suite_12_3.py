# Модуль suite_12_3.py для описания объекта TestSuite

import unittest
import tests_12_3

# Описание объекта TestSuite. Указываем на него переменной с произвольным названием (RunnerTS)
RunnerTS = unittest.TestSuite()

# Добавляем тесты RunnerTest и TournamentTest в этот TestSuite
RunnerTS.addTest(unittest.TestLoader().loadTestsFromTestCase(tests_12_3.RunnerTest))
RunnerTS.addTest(unittest.TestLoader().loadTestsFromTestCase(tests_12_3.TournamentTest))

# Создаем объект класса TextTestRunner, с аргументом verbosity=2
runner = unittest.TextTestRunner(verbosity = 2)

# Запускаем TestSuite
runner.run(RunnerTS)