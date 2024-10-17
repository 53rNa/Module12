# Задача "Логирование бегунов"

import unittest
import logging

# Настройка логирования с использованием модуля logging

# Создание объекта логгера, который можно использовать для регистрации сообщений
logger = logging.getLogger()

# Устанавливаем уровень логирования для созданного логгера на INFO. Все сообщения с уровнем INFO и выше
# (например, WARNING, ERROR, и CRITICAL) будут обрабатываться и записываться. Сообщения с более низким уровнем,
# такими как DEBUG, будут игнорироваться
logger.setLevel(logging.INFO)

# создаем объект форматировщика (Formatter). Формат сообщения в логе:
##     %(asctime)s: Время, когда было записано сообщение
#     %(levelname)s: Уровень важности сообщения (например, INFO, WARNING)
#     %(message)s: Само сообщение
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# Создаем объект обработчика (FileHandler) для записи лога в файл с именем runner_tests.log
handler = logging.FileHandler('runner_tests.log','w','utf-8')

# Все сообщения, которые обрабатываются созданным выше обработчиком (FileHandler),
# будут отформатированы в соответствии с заданным форматом
handler.setFormatter(formatter)

# Все сообщения, которые будут записываться через созданный ранее логгер, будут переданы в обработчик (FileHandler)
# и записаны в файл runner_tests.log
logger.addHandler(handler)

# Декоратор, который при значении is_frozen = False выполняет тесты,
# а is_frozen = True - пропускает и выводить сообщение 'Тесты в этом кейсе заморожены'
def skip_if_frozen(func):
    def wrapper(*args, **kwargs):
        if args[0].is_frozen:
            raise unittest.SkipTest('Тесты в этом кейсе заморожены')
        return func(*args, **kwargs)
    return wrapper

class Runner:
    def __init__(self, name, speed=5):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError(f'Имя может быть только строкой, передано {type(name).__name__}')
        self.distance = 0
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError(f'Скорость не может быть отрицательной, сейчас {speed}')

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name

class RunnerTest(unittest.TestCase):

    is_frozen = False  # При значении is_frozen = False - выполнить тесты

    @skip_if_frozen
    # Метод, в котором создаём объект класса Runner с произвольным именем (Roman). Далее вызваем метод walk у этого
    # объекта 10 раз. После чего, методом assertEqual сравниваем distance этого объекта со значением 50
    def test_walk(self):
        try:
            runner = Runner("Roman", -5)
            for i in range(10):
                runner.walk()
            logging.info('"test_walk" выполнен успешно')
            self.assertEqual(runner.distance, 50)
        except Exception:
            logging.warning("Неверная скорость для Runner", exc_info=True)

    @skip_if_frozen
    # Метод, в котором создаём объект класса Runner с произвольным именем (Dmitry). Далее вызываем метод run у этого
    # объекта 10 раз. После чего, методом assertEqual сравниваем distance этого объекта со значением 100
    def test_run(self):
        try:
            runner = Runner(12345, 10)
            for i in range(10):
                runner.run()
            logging.info('"test_run" выполнен успешно')
            self.assertEqual(runner.distance, 100)
        except Exception:
            # Записываем предупреждение с трассировкой
            logging.warning("Неверный тип данных для объекта Runner", exc_info=True)

    @skip_if_frozen
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


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers

# first = Runner('Вося', 10)
# second = Runner('Илья', 5)
# third = Runner('Арсен', 10)
#
# t = Tournament(101, first, second, third)
# print(t.start())


