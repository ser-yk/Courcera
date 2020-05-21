import os.path
import csv

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
    def get_photo_file_ext(self):
        self.ext = os.path.splitext(self.photo_file_name)[1]    # '.jpg', '.jpeg', '.png', '.gif'
        return self.ext


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = 'car'


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_length, self.body_width, self.body_height = self.body_whl(body_whl)
        self.car_type = 'truck'

    def get_body_volume(self):
        return float(self.body_height * self.body_width * self.body_length)

    def body_whl(self, body_whl):
        try:
            self.length, self.width, self.height = [float(i) for i in body_whl.split('x')]
            return self.length, self.width, self.height
        except ValueError:
            return float(0), float(0), float(0)


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


def get_car_list(csv_filename):
    car_list = []
    with open(f'{csv_filename}', 'r', encoding='utf-8') as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            new_obj = valid(row)
            if new_obj:
                car_list.append(new_obj)

    return car_list

def valid(row):
    # шапблон строки['car_type', 'brand', 'passenger_seats_count', 'photo_file_name', 'body_whl', 'carrying', 'extra']
    #  Проверяем валидность полей
    try:
        brand = len(row[1]) > 1
        passenger_seats_count = row[2].isdigit() and int(row[2]) > 0
        photo_file_name = os.path.splitext(row[3])[1] in ('.jpg', '.jpeg', '.png', '.gif')
        carrying = float(row[5]) > 0
        extra = len(row[6]) > 1

        if row[0] == 'car' and brand and carrying and photo_file_name and passenger_seats_count:
            return Car(row[1], row[3], row[5], row[2])
        if row[0] == 'truck' and brand and carrying and photo_file_name:
            return Truck(row[1], row[3], row[5], row[4])
        if row[0] == 'spec_machine' and brand and carrying and photo_file_name and extra:
            return SpecMachine(row[1], row[3], row[5], row[6])
    except (ValueError, IndexError):
        return

# cars = get_car_list('_af3947bf3a1ba3333b0c891e7a8536fc_coursera_week3_cars.csv')
# print(cars)
# for car in cars:
#     print(type(car), car.brand, car.photo_file_name, car.carrying)
#
# print(cars[1].get_body_volume(), cars[1].car_type)
# print(cars[0].get_photo_file_ext(), cars[0].carrying)
