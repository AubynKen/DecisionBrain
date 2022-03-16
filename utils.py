from datetime import datetime
import matplotlib.pyplot as plt
import random as rd


def parse_time(time):
    """Parse time from string into datetime object"""
    if not time:
        return
    if type(time) == str:
        return datetime.strptime(time, '%I:%M%p')
    return time


def parse_time_minute(time):
    """
    Parse time from datetime object into minutes

    :param time: datetime object representing the time
    :return: the number of minutes elapsed since midnight
    """
    if not time:
        return
    return int((parse_time(time) - datetime(year=1901, month=1, day=1, hour=0)).seconds / 60)


def store_result(target_path, employees, tasks, lunch_times, z, b):
    w, t = len(tasks), len(employees)
    with open(target_path, "w") as f:
        f.write("taskId;performed;employeeName;startTime; \n")
        for i in tasks:
            if i in z.keys() :
                f.write(f"T{i+1+2*t};1;{employees[z[i]].name};{b[i].x};\n")
            else :
                f.write(f"T{i+1+2*t};0;;;\n")
        f.write("\n")
        f.write("employeeName;lunchBreakStartTime;\n")
        for k in range(t):
            f.write(f"{employees[k].name};{lunch_times[k]};\n")
    return

def cm_to_inch(value):
    return value/2.54

def plot_map(employee_list, node_list, tasks, unavails, X, L, Z):
    plt.figure(figsize=(cm_to_inch(100),cm_to_inch(100)))

    node_pos = []
    for employee in employee_list:
        node_pos.append([employee.longitude, employee.latitude])
        rd_color = "#" + ''.join([rd.choice('0123456789ABCDEF') for _ in range(6)])
        plt.scatter([employee.longitude], [employee.latitude], label = f"Maison de {employee.name}", c=rd_color, marker = "$(T)$", s = 10000)

    t = len(employee_list)
    all_indexes = list(range(t)) + tasks + unavails

    for k in range(t):
        for i in all_indexes:
            if L[(k,i)].x == 1:
                employee = employee_list[k]
                node = node_list[i]
                plt.scatter([node.longitude], [node.latitude], label= f"Pause de {employee.name}", marker = "$(P)$", s = 10000)

    for i in tasks:
        task = node_list[i]
        node_pos.append([task.longitude, task.latitude])
        plt.scatter([task.longitude], [task.latitude], label=task.id, s = 400)

    for i in unavails:
        unavail = node_list[i]
        node_pos.append([unavail.longitude, unavail.latitude])
        plt.scatter([unavail.longitude], [unavail.latitude], label="Indisponibilité de " + unavail.employee.name, marker = "$(X)$", s = 10000)


    number_of_colors = 8  # hardcoded
    color = ["#" + ''.join([rd.choice('0123456789ABCDEF') for _ in range(6)])
             for _ in range(number_of_colors)]

    n = len(node_pos)
    for a in range(n):
        for b in range(n):
            i = all_indexes[a]
            j = all_indexes[b]
            if i != j and X[(i, j)].x == 1:
                lbl = ""
                clr = "black"
                if i in range(t):
                    lbl = f"{employee_list[Z[j]].name}"
                    clr = color[Z[i]]
                elif j in range(t):
                    clr = color[Z[j]]
                else:
                    clr = color[Z[i]]

                plt.plot([node_pos[a][0], node_pos[b][0]], [node_pos[a][1], node_pos[b][1]], c= clr, label = lbl)


    plt.legend(prop={'size': 40})
    plt.show()
