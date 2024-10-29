import threading
import random
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None  # Изначально стол свободен

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Гость сидит за столом от 3 до 10 секунд
        time.sleep(random.randint(3, 10))

class Cafe:
    def __init__(self, *tables):
        self.tables = list(tables)  # Коллекция столов
        self.queue = Queue()  # Очередь гостей

    def guest_arrival(self, *guests):
        # Процесс посадки гостей
        for guest in guests:
            # Ищем свободный стол
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:
                # Сажаем гостя за стол
                free_table.guest = guest
                guest.start()  # Запускаем поток гостя
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                # Если нет свободного стола, добавляем гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        # Обслуживаем гостей, пока есть гости за столами или в очереди
        while any(table.guest is not None for table in self.tables) or not self.queue.empty():
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    # Если гость закончил прием пищи, освобождаем стол
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                    # Если есть гости в очереди, пересаживаем первого гостя за освободившийся стол
                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()  # Запускаем поток гостя
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

            time.sleep(0.1)  # Даем время другим потокам для завершения

# Тестирование программы
if __name__ == "__main__":
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]

    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    # Создание гостей
    guests = [Guest(name) for name in guests_names]

    # Заполнение кафе столами
    cafe = Cafe(*tables)

    # Приём гостей
    cafe.guest_arrival(*guests)

    # Обслуживание гостей
    cafe.discuss_guests()
