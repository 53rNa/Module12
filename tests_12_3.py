import unittest

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

        # Имя бегуна
        self.name = name

        # Дистанция, пройденная бегуном (по умолчанию 0)
        self.distance = 0

        # Скорость бегуна
        self.speed = speed

        # Времч бегуна (по умолчанию 0)
        self.time = 0

    # В методах run (БЕГ) и walk (ХОДЬБА) изменение дистанции зависит от скорости
    def run(self):
        self.distance += self.speed * 2
        self.time += 1

    def walk(self):
        self.distance += self.speed
        self.time += 1

    # Возвращаем имя бегуна
    def __str__(self):
        return self.name

    # Метод для сравнивания имён бегунов
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
        runner = Runner("Roman")
        for i in range(10):
            runner.walk()
        self.assertEqual(runner.distance, 50)
      # self.assertEqual(runner.distance, 20) Тест не пройден!

    @skip_if_frozen
    # Метод, в котором создаём объект класса Runner с произвольным именем (Dmitry). Далее вызываем метод run у этого
    # объекта 10 раз. После чего, методом assertEqual сравниваем distance этого объекта со значением 100
    def test_run(self):
        runner = Runner("Dmitry")
        for i in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

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

# Класс Tournament представляет собой класс соревнований, где есть дистанция, которую нужно пробежать и список участников
class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    # ИСПРАВЛЕНО: В данном методе моделируем забег во времени, позволяя каждому бегуну продвигаться вперед в
    # зависимости от его скорости, пока один из них не финиширует
    def start(self):
        finishers = {}
        time_elapsed = 0

        while len(finishers) < len(self.participants):
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance and participant not in finishers.values():
                    finishers[len(finishers) + 1] = participant
            time_elapsed += 1
        return finishers

class TournamentTest(unittest.TestCase):
    all_results = {}
    is_frozen = True  # При значении is_frozen = True - пропускать тесты

    @classmethod
    # Метод, где создаётся атрибут класса all_results
    def setUpClass(cls):
        # Словарь, в который будут сохраняться результаты всех тестов
        cls.all_results = {}

    # Метод, где создаются 3 объекта
    def setUp(self):
        self.runner_usain = Runner("Усэйн", speed=10)
        self.runner_andrei = Runner("Андрей", speed=9)
        self.runner_nik = Runner("Ник", speed=3)

    @classmethod
    # Метод, где выводятся all_results по очереди в столбец
    def tearDownClass(cls):
        for key in sorted(cls.all_results.keys()):
            result_dict = cls.all_results[key]
            formatted_result = {k: v.name for k, v in result_dict.items()}
            print(formatted_result)

    @skip_if_frozen
    # Методы тестирования забегов, в которых создаётся объект Tournament на дистанцию 90
    # Метод, где в забеге участвуют Усэйн и Ник
    def test_race_usain_and_nik(self):
        tournament = Tournament(90, self.runner_usain, self.runner_nik)

        # У объекта класса Tournament запускается метод start
        results = tournament.start()
        # который возвращает словарь в переменную all_results
        TournamentTest.all_results[len(TournamentTest.all_results) + 1] = results

        # Метод assertTrue, в котором сравниваются последний объект из all_results (взят по наибольшему ключу)
        # и предполагаемое имя последнего бегуна
        last_finisher_name = results[max(results.keys())].name
        self.assertTrue(last_finisher_name == "Ник")

    @skip_if_frozen
    # Метод, где в забеге участвуют Андрей и Ник
    def test_race_andrei_and_nik(self):
        tournament = Tournament(90, self.runner_andrei, self.runner_nik)
        results = tournament.start()
        TournamentTest.all_results[len(TournamentTest.all_results) + 1] = results

        last_finisher_name = results[max(results.keys())].name
        self.assertTrue(last_finisher_name == "Ник")

    @skip_if_frozen
    # Метод, где в забеге участвуют Усэйн, Андрей и Ник
    def test_race_usain_andrei_and_nik(self):
        tournament = Tournament(90, self.runner_usain, self.runner_andrei, self.runner_nik)
        results = tournament.start()
        TournamentTest.all_results[len(TournamentTest.all_results) + 1] = results

        last_finisher_name = results[max(results.keys())].name
        self.assertTrue(last_finisher_name == "Ник")

    @skip_if_frozen
    # Добавляем дополнительные тесты. В них проверяем, что бегуны с более высокой скоростью финишируют раньше бегунов
    # с более низкой скоростью
    def test_race_usain_andrei(self):
        tournament = Tournament(90, self.runner_usain, self.runner_andrei)
        results = tournament.start()
        TournamentTest.all_results[len(TournamentTest.all_results) + 1] = results
        last_finisher_name = results[max(results.keys())].name
        first_finisher_name = results[1].name

        self.assertTrue(first_finisher_name == "Усэйн")
        self.assertTrue(last_finisher_name == "Андрей")

    @skip_if_frozen
    def test_race_andrei_nik(self):
        tournament = Tournament(90, self.runner_andrei, self.runner_nik)
        results = tournament.start()
        TournamentTest.all_results[len(TournamentTest.all_results) + 1] = results

        last_finisher_name = results[max(results.keys())].name
        first_finisher_name = results[1].name

        self.assertTrue(first_finisher_name == "Андрей")
        self.assertTrue(last_finisher_name == "Ник")


if __name__ == "__main__":
    unittest.main()
