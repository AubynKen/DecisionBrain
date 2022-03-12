import pandas as pd
import numpy as np
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from utils import parse_time, parse_time_minute


class Employee:
    list = []  # initialized to empty list
    count = 0
    speed = 50 * 1000 / 60  # unit: meter/minute
    __name_employee_correspondance = {}

    def __init__(self, name: str, latitude: float, longitude: float, skill: str, level: int, start_time, end_time):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.skill = skill
        self.level = level
        self.start_time_str = parse_time(start_time)  # parse time into datetime object for printing
        self.end_time_str = parse_time(end_time)
        self.start_time = parse_time_minute(start_time)  # parse time into minutes
        self.end_time = parse_time_minute(end_time)
        Employee.count += 1
        Employee.list.append(self)
        Employee.__name_employee_correspondance[name] = self

    @classmethod
    def find_by_name(cls, name):
        return cls.__name_employee_correspondance[name]

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

    def __repr__(self):
        return f"Employee(name={self.name}, " \
               f"position=[{self.longitude}, {self.latitude}], " \
               f"skill_requirement=level {self.level} {self.skill}," \
               f"available=[{self.start_time_str.strftime('%I:%M%p')}, {self.end_time_str.strftime('%I:%M%p')}] )"


class Node:
    list = []
    count = 0
    count_task = 0
    count_unavail = 0
    distance: np.array = None
    __is_initialized = False

    def __init__(self, task_id, latitude, longitude, duration, skill, level, opening_time, closing_time,
                 node_type: str):
        if Node.__is_initialized:
            raise Exception("Cannot instantiate new task after initializing the distance matrix")
        self.id = task_id
        self.latitude = latitude
        self.longitude = longitude
        self.duration = duration
        self.skill = skill
        self.level = level
        self.opening_time_str = parse_time(opening_time)
        self.closing_time_str = parse_time(closing_time)
        self.opening_time = parse_time_minute(opening_time)
        self.closing_time = parse_time_minute(closing_time)
        self.node_type = node_type
        Node.list.append(self)
        Node.count += 1

    @classmethod
    def load_excel(cls, path, initialize_distance=False):

        # create a dummy task for each home on top of the list
        df_employees = pd.read_excel(path, sheet_name="Employees")
        df_employees.set_index("EmployeeName")
        for _, row in df_employees.iterrows():
            Node(row["EmployeeName"] + "'s Home", row["Latitude"], row["Longitude"], 0, None, 0, None, None, "home")

        # load tasks
        df = pd.read_excel(path, sheet_name="Tasks")
        df.set_index("TaskId")
        for index, row in df.iterrows():
            # parse the start time and end time into datetime object
            opening_time = datetime.strptime(row["OpeningTime"], '%I:%M%p')
            closing_time = datetime.strptime(row["ClosingTime"], '%I:%M%p')

            Node(row["TaskId"],
                 row["Latitude"],
                 row["Longitude"],
                 row["TaskDuration"],
                 row["Skill"],
                 row["Level"],
                 opening_time,
                 closing_time, node_type="task")

        # create a task for each unavailability at the bottom of the list
        df_employees_unavailabilities = pd.read_excel(path, sheet_name="Employees Unavailabilities")
        df_employees_unavailabilities.set_index("EmployeeName")
        for _, row in df_employees_unavailabilities.iterrows():
            open_time = row["Start"]
            close_time = row["End"]
            duration = parse_time_minute(close_time) - parse_time_minute(open_time)
            Node(row["EmployeeName"], row["Latitude"], row["Longitude"], duration, None, 0, open_time, close_time,
                 node_type="unavail")

        # create a dummy task for each lunch at the bottom of the list
        df_employees = pd.read_excel(path, sheet_name="Employees")
        df_employees.set_index("EmployeeName")
        for _, row in df_employees.iterrows():
            Node(row["EmployeeName"] + "'s Lunch", None, None, 60, None, 0, "12:00am", "2:00pm", "lunch")

        if initialize_distance:
            cls.initialize_distance()

    @staticmethod
    def calculate_distance(task1, task2):
        if task1.node_type == "lunch" or task2.node_type == "lunch":
            return 0
        lon1, lat1 = radians(task1.longitude), radians(task1.latitude)
        lon2, lat2 = radians(task2.longitude), radians(task2.latitude)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371 * 1000  # radius of earth
        return c * r

    @classmethod
    def initialize_distance(cls):
        if cls.__is_initialized:
            print("Warning: trying to reinitialize an initialized task list, recalculating the distance matrix")
        cls.__is_initialized = True
        cls.distance = np.zeros((len(Node.list), len(Node.list)), dtype=np.float64)

        for i in range(cls.count):
            for j in range(i):
                task_i, task_j = cls.list[i], cls.list[j]
                cls.distance[i, j] = cls.distance[j, i] = cls.calculate_distance(task_i, task_j)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        opening_time = self.opening_time_str.strftime('%I:%M%p')
        closing_time = self.closing_time_str.strftime('%I:%M%p')

        if self.node_type == "task":
            return f"Task(id={self.id}, " \
                   f"position=[{self.longitude}, {self.latitude}], " \
                   f"duration={self.duration}, " \
                   f"skill_requirement=level {self.level} {self.skill}," \
                   f"opening_time=[{opening_time} to {closing_time}] "

        if self.node_type == "lunch":
            return f"Lunch({self.id})"

        if self.node_type == "home":
            return f"Home({self.id})"
