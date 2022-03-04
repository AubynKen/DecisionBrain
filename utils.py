from datetime import datetime
import matplotlib.pyplot as plt
import random as rd


def parse_time(time):
    if not time:
        return
    if type(time) == str:
        return datetime.strptime(time, '%I:%M%p')
    return time


def parse_time_minute(time):
    if time is None:
        return
    return int((parse_time(time) - datetime(year=1901, month=1, day=1, hour=0)).seconds / 60)


def store_result(target_path, employees, tasks, z, b):
    v, t = len(tasks), len(employees)
    with open(target_path, "w") as f:
        f.write("taskId;performed;employeeName;startTime; \n")
        for i in range(1, v):
            f.write(f"T{i};1;{employees[z[i]].name};{b[i].x};\n")
        f.write("\n")
        f.write("employeeName;lunchBreakStartTime;\n")
        for k in range(t):
            f.write(f"{employees[k].name};0;\n")
    return


def plot_map(n_task, employees, tasks, x, z):
    task_pos = [[employees[0].longitude, employees[0].latitude]]
    plt.scatter([employees[0].longitude], [employees[0].latitude], label="Dépôt", c="black")
    for j in range(1, n_task):
        # recording task completion
        task_pos.append([tasks[j].longitude, tasks[j].latitude])
        # Adding dots to the tasks
        plt.scatter([tasks[j].longitude], [tasks[j].latitude], label=f"Tâche {j}")

    number_of_colors = 8  # hardcoded
    color = ["#" + ''.join([rd.choice('0123456789ABCDEF') for _ in range(6)])
             for _ in range(number_of_colors)]

    for i in range(n_task):
        for j in range(n_task):
            if i == j or x[(i, j)].x != 1:
                continue
            if i == 0:
                plt.plot([task_pos[i][0], task_pos[j][0]], [task_pos[i][1], task_pos[j][1]], c=color[z[j]],
                         label=f"{employees[z[j]].name}")
            else:
                plt.plot([task_pos[i][0], task_pos[j][0]], [task_pos[i][1], task_pos[j][1]], c=color[z[i]])

    plt.legend()
    plt.show()
