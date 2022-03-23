# The classes corresponding to employees and nodes in this phase are similar to that of version 2

class Solution:
    print_warning = True  # whether to print warning or not when validating

    def __init__(self):
        """instantiate new solution instance that adapts to the Employee and Node data"""
        self.x = np.zeros((V, V), dtype=np.intc)
        self.y = np.zeros((T, W), dtype=np.intc)
        self.b = np.zeros(W, dtype=np.intc)
        self.l = np.zeros((T, V), dtype=np.intc)

    @classmethod
    def set_warning(cls, print_warning: bool):
        """set whether to print warning when validating data"""
        cls.print_warning = print_warning

    @classmethod
    def warn(cls, warning: str, print_color="yellow"):
        """
        Print a text in yellow if print_warning set to True
        :param warning: the warning message we want to print
        :param print_color: the color of the printed message, defaulted to yellow
        """
        if not cls.print_warning: return # does nothing if print_warning set to False
        correspondance = {
            "yellow": Colors.WARNING,
            "cyan": Colors.CYAN,
            "green": Colors.GREEN,
            "red": Colors.FAIL
        }
        color = correspondance[print_color] if print_color in correspondance.keys() else Colors.WARNING
        print(f"{color}Error: {warning}{Colors.NORMAL}")

    def copy(self):
        """Return a deep copy of the instance"""
        return deepcopy(self)

    def validate_binary_vars(self):
        """Verify that x, y and l only contain binary variables"""

        def is_binary(arr: np.array):
            return np.min(arr) >= 0 and np.max(arr) <= 1

        to_verify = [(self.x, "x"), (self.y, "y"), (self.l, "l")]
        for arr, name in to_verify:
            if is_binary(arr):
                continue
            Solution.warn(f"{name} should contain binary variables, values other than 0 and 1 detected.")
            return False
        return True

    def validate(self):
        """
        validate the modifications
        :return: whether the constraints are verified
        """

        # verify that x, y and l contain only 0 and 1
        if not self.validate_binary_vars(): return False

        # verify that a node is not linked to itself
        for i in nodes:
            if not self.x[i, i]: continue
            Solution.warn("A node can't be linked to itself.")
            Solution.warn(f"Condition violated by node {i}.")
            return False

        entrance_count = self.x.sum(axis=0)
        exit_count = self.x.sum(axis=1)
        # C1
        if not np.all(entrance_count == exit_count):
            Solution.warn("C1: The number of entrance of each node should be equal to the number of exit.")
            node_idx = np.argwhere(entrance_count != exit_count)[0]
            Solution.warn(
                f"Condition violated by node {node_idx} with {entrance_count[node_idx]} entrance(s) and {exit_count[node_idx]} exit(s).")
            return False

        # C2
        less_than_one_entrance = entrance_count <= 1
        if not np.all(less_than_one_entrance[tasks + homes]):
            Solution.warn("C2: Each task should be done by at most one employee.")
            for i in tasks:
                if not less_than_one_entrance[i]:
                    Solution.warn(f"Condition violated by node {i} done by {entrance_count[i]} employees.", "cyan")
            return False

        # C3.a
        exactly_one_entrance = entrance_count == 1
        if not np.all(exactly_one_entrance[unavails]):
            Solution.warn("C3.a: Unavailabilities should be visited.")
            unavail_indices = np.argwhere(~exactly_one_entrance)
            idx = unavail_indices[0]
            Solution.warn(f"Condition violated by node {idx}", "cyan")
            return False

        # C3.b
        for k in employees:
            if self.x[k, Employee.list[k].home()]:
                continue
            Solution.warn(f"C3.b: Each employee should visits their home.")
            Solution.warn(f"Condition violated by employee {k}.", "cyan")

            return False

        for idx in unavails:
            employee = Node.list[idx].employee
            employee_idx = Employee.index_of(employee)
            if self.x[employee_idx, idx] == 1:
                continue
            Solution.warn(f"C3.b: Each employee should visit his unavailabilities.")
            Solution.warn(f"Condition violated by employee {employee_idx}.", "cyan")
            return False

        # C4
        for i in nodes:
            for j in nodes:
                if i == j or not self.x[i, j]: continue
                if self.y[:, i] == self.y[:, j]: continue
                Solution.warn(f"C4: Two consecutive tasks should be done by the same employee")
                Solution.warn(f"Condition violated by task {i} and {j}", "cyan")
                return False

        # C5
        for i in tasks:
            task: Task = Node.list[i]
            opening, closing = task.opening_time, task.closing_time
            if self.b[i] >= opening and self.b[i] + task.duration <= closing: continue
            Solution.warn(f"C5: A task should be worked on between its opening time and closing time")
            Solution.warn(f"Condition violated by task {i}", "cyan")
            return False

        # C6.a
        for k in employees:
            employee: Employee = Employee.list[k]
            employee_start = employee.start_time
            if employee_start == self.b[k]: continue
            Solution.warn(f"C6.a: Employees' start times should be respected")
            Solution.warn(f"Condition violated by employee {k}", "cyan")
            return False

        # C6.b
        for i in unavails:
            if self.b[i] == Node.list[i].opening_time: continue
            Solution.warn(f"C6.b: The beginning and end of unavailabilities should be respected")
            Solution.warn(f"Condition violated by Node {i}", "cyan")
            return False

        # C7
        # TODO: verify C7

        # C8
        # TODO: verify C8

        # C9
        for k in employees:
            for i in tasks:
                if not self.x[i, k]: continue
                task: Task = Node.list[i]
                employee: Employee = Employee.list[k]
                if self.b[k] + task.duration + (Node.distance[i, k] / Employee.speed) + self.l[
                    k, i] * 60 <= employee.end_time: continue
                Solution.warn("C9: An employee should have enough time to go back home.")
                Solution.warn(f"Condition violated by employee {k} after task {i}", "cyan")
                return False

        # C10.a
        for k in employees:
            if sum(self.l[k, :]) == 1: continue
            Solution.warn("C10.a: Each employee has one unique lunch")
            Solution.warn(f"Condition violated by employee {k}", "cyan")
            return False

        # C10.b
        for k in employees:
            for i in nodes:
                if not self.l[k, i]: continue
                if self.y[k, i]: continue
                Solution.warn(f"C10.b: Constraint violated")
                Solution.warn(f"Condition violated by employee {k} after lunch at node {i}")
                return False

        # C10.c
        for i in nodes:
            for k in employees:
                if not self.l[k, i]: continue
                task_duration = Node.list[i].duration
                if self.b[i] + task_duration + self.l[k, i] * 60 <= 14 * 60 and self.b[
                    i] + task_duration >= 12 * 60: continue
                Solution.warn("C10.c A task should be taken between 12AM and 2PM")
                Solution.warn(f"Condition violated by employee {k} after node {i}", "cyan")
                return False

        # C11
        for i in tasks + unavails:
            if sum(self.y[:, i]) <= sum(self.x[:, i]): continue
            Solution.warn("C11: This constraint is violated")
            Solution.warn(f"Condition violated by node {i}", "cyan")
            return False

        # C12
        for i in tasks + unavails:
            for j in tasks + unavails:
                if i == j or self.x[i, j]: continue
                if self.b[i] + Node.list[i].duration + (Node.distance[i, j] / Employee.speed) + sum(
                        self.l[:, i]) * 60 <= self.b[j]: continue
                Solution.warn("C12: The traveling time between two nodes should be sufficient.")
                Solution.warn(f"Condition violated between node {i} and {j}", "cyan")
                return False

        # C13
        for k in employees:
            for i in tasks:
                if not self.y[k, i]: continue
                employee: Employee = Employee.list[k]
                task: Task = Node.list[i]
                if employee.level >= task.level: continue
                Solution.warn("C13: An employee can only do tasks that they are able to do.")
                Solution.warn(f"Condition violated by employee {k} at node {i}", "cyan")
                Solution.warn(repr(employee), "green")
                Solution.warn(repr(task), "green")
                return False

        # Every condition is verified
        return True