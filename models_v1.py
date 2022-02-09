import pandas as pd
import numpy as np
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from utils import parse_time


class Employee:
    list = []  # initialized to empty list
    count = 0
    speed = 50  # unit: km/h

    def __init__(self, name: str, latitude: float, longitude: float, skill: str, level: int, start_time, end_time):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.skill = skill
        self.level = level
        self.start_time = parse_time(start_time)
        self.end_time = parse_time(end_time)
        Employee.count += 1
        Employee.list.append(self)

    @classmethod
    def load_excel(cls, path):
        df_employees = pd.read_excel(path, sheet_name="Employees")
        df_employees.set_index("EmployeeName")

        for index, row in df_employees.iterrows():
            Employee(row["EmployeeName"],
                     row["Latitude"],
                     row["Longitude"],
                     row["Skill"],
                     row["Level"],
                     row["WorkingStartTime"],
                     row["WorkingEndTime"])

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __start_time_string(self):
        return self.start_time.strftime('%I:%M%p')

    def __end_time_string(self):
        return self.end_time.strftime('%I:%M%p')

    def __repr__(self):
        return f"Employee(name={self.name}, " \
               f"position=[{self.longitude}, {self.latitude}], " \
               f"skill={self.skill}," \
               f"level={self.level}," \
               f"available=[{self.__start_time_string()}, {self.__end_time_string()}] )"


class Task:
    list = []
    count = 0
    distance: np.array = None
    __is_initialized = False

    def __init__(self, task_id, latitude, longitude, duration, skill, level, opening_time, closing_time):
        if Task.__is_initialized:
            raise Exception("Cannot instantiate new task after initializing the distance matrix")
        self.id = task_id
        self.latitude = latitude
        self.longitude = longitude
        self.duration = duration
        self.skill = skill
        self.level = level
        self.opening_time = parse_time(opening_time)
        self.closing_time = parse_time(closing_time)

        Task.list.append(self)
        Task.count += 1

    @classmethod
    def load_excel(cls, path):
        df = pd.read_excel(path, sheet_name="Tasks")
        df.set_index("TaskId")

        for index, row in df.iterrows():
            # parse the start time and end time into datetime object
            opening_time = datetime.strptime(row["OpeningTime"], '%I:%M%p')
            closing_time = datetime.strptime(row["ClosingTime"], '%I:%M%p')

            Task(row["TaskId"],
                 row["Latitude"],
                 row["Longitude"],
                 row["TaskDuration"],
                 row["Skill"],
                 row["Level"],
                 opening_time,
                 closing_time)

    @staticmethod
    def calculate_distance(task1, task2):
        lon1, lat1 = radians(task1.longitude), radians(task1.latitude)
        lon2, lat2 = radians(task2.longitude), radians(task2.latitude)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371
        return c * r

    @classmethod
    def initialize_distance(cls):
        if cls.__is_initialized:
            raise Exception("Distance has already been initialized")
        cls.__is_initialized = True
        cls.distance = np.zeros((cls.count, cls.count), dtype=np.float64)

        for i in range(cls.count):
            for j in range(i):
                task_i, task_j = cls.list[i], cls.list[j]
                cls.distance[i, j] = cls.distance[j, i] = cls.calculate_distance(task_i, task_j)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
