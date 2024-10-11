import unittest

class Runner:
    def __init__(self, name):

        # Имя бегуна
        self.name = name

        # Дистанция, пройденная бегуном (по умолчанию 0)
        self.distance = 0

    # Увеличиваем дистанцию на 10 (БЕГ)
    def run(self):
        self.distance += 10

    # Увеличиваем дистанцию на 5 (ХОДЬБА)
    def walk(self):
        self.distance += 5

    # Возвращаем имя бегуна
    def __str__(self):
        return self.name

# Класс RunnerTest, наследуемый от класса TestCase из модуля unittest
class RunnerTest(unittest.TestCase):

    # Метод, в котором создаём объект класса Runner с произвольным именем (Roman). Далее вызваем метод walk у этого
    # объекта 10 раз. После чего, методом assertEqual сравниваем distance этого объекта со значением 50
    def test_walk(self):
        runner = Runner("Roman")
        for i in range(10):
            runner.walk()
        self.assertEqual(runner.distance, 50)
      # self.assertEqual(runner.distance, 20) Тест не пройден!

    # Метод, в котором создаём объект класса Runner с произвольным именем (Dmitry). Далее вызываем метод run у этого
    # объекта 10 раз. После чего, методом assertEqual сравниваем distance этого объекта со значением 100
    def test_run(self):
        runner = Runner("Dmitry")
        for i in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    # Метод в котором создаем 2 объекта класса Runner с произвольными именами (Andrey и Marina). Далее 10 раз у
    # объектов вызываем методы run и walk соответственно
    def test_challenge(self):
        runner1 = Runner("Andrey")
        runner2 = Runner("Marina")

        for i in range(10):
            runner1.run()  # Andrey бежит
            runner2.walk()  # Marina идет

        # Т.к. дистанции должны быть разными, используем метод assertNotEqual, чтобы убедится в неравенстве результатов
        self.assertNotEqual(runner1.distance, runner2.distance)

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
