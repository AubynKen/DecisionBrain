m = Model("DB")

# an arbitrarily big variable
M = 1000000

# decision variables
X = {(i, j) : m.addVar(vtype = GRB.BINARY, name = f'x{i}_{j}') for i in nodes for j in nodes if i != j}
Y = {(k, i) : m.addVar(vtype = GRB.BINARY, name = f'y{k}_{i}') for k in employees for i in nodes}
B = {i : m.addVar(vtype = GRB.INTEGER, name = f'b{i}', lb = 0, ub = 24*60) for i in nodes}
L = {(k, i) : m.addVar(vtype = GRB.BINARY) for k in employees for i in nodes}
P = {k : m.addVar(vtype = GRB.INTEGER, lb = 12*60, ub = 13*60) for k in employees}
t = {(i,l) : m.addVar(vtype = GRB.BINARY, name = f't{l}') for i in tasks for l in range(len(open_intervals(i)))}

# constraints

# C1
for i in nodes:
    m.addConstr(quicksum([X[(i,j)] for j in nodes if i != j]) == quicksum([X[(j,i)] for j in nodes if i != j]))

# C2
for j in homes + tasks:
    m.addConstr(quicksum([X[(i,j)] for i in nodes if i != j]) <= 1)

# C3_a
for j in unavails:
    m.addConstr(quicksum([X[(i,j)] for i in nodes if i != j]) == 1)

# C3_b
for i in homes + unavails:
    employee = Node.list[i].employee
    for k in employees:
        if employee == Employee.list[k] :
            m.addConstr(Y[(k,i)] == 1)
        else:
            m.addConstr(Y[(k,i)] == 0)
          
# C4
for i in nodes:
    for j in nodes:
        if i != j:
            for k in employees:
                m.addConstr(Y[(k,i)] <= Y[(k,j)] + 1-X[(i,j)])
                m.addConstr(Y[(k,i)] >= Y[(k,j)] - 1+X[(i,j)])

# C5
for i in tasks:
    m.addConstr(B[i] >= Node.list[i].opening_time)
    m.addConstr(Node.list[i].duration + B[i] <= Node.list[i].closing_time)
    
# C6_a
for k in employees:
    m.addConstr(B[k] >= Employee.list[k].start_time)

# C6_b
for i in unavails:
    m.addConstr(B[i] == Node.list[i].opening_time)

# C7
for i in tasks:
    intervals = open_intervals(i)
    m.addConstr(quicksum([t[(i,l)] for l in range(len(intervals))]) == quicksum([X[(i,j)] for j in nodes if i != j]))
    
    for l in range(len(intervals)):
        start, end = intervals[l]
        m.addConstr(B[i] >= start - (1-t[(i,l)])*M)
        m.addConstr(B[i] + Node.list[i].duration <= end + (1-t[(i,l)])*M)

# C8
for k in employees:
    m.addConstr(B[k] - (1 - L[(k,k)])*M <= P[k])
    for i in tasks + unavails:
        m.addConstr(B[k] + ceil(Node.distance[k,i]/Employee.speed) - (1 - X[(k,i)]) * M <= B[i])
        m.addConstr(P[k] + 60 + ceil(Node.distance[k,i]/Employee.speed) - (2 - X[(k,i)] - L[(k,k)]) * M <= B[i])

# C9
for k in employees:
    for i in tasks + unavails:
        m.addConstr(B[i] + Node.list[i].duration + ceil(Node.distance[i,k]/Employee.speed) <= Employee.list[k].end_time + M*(1 - X[(i,k)]))
        m.addConstr(B[i] + Node.list[i].duration <= P[k] + M*(2-L[(k,i)]-X[(i,k)]))
        m.addConstr(P[k] + 60 + ceil(Node.distance[i,k]/Employee.speed) <= Employee.list[k].end_time + M*(2 - X[(i,k)]- L[(k,i)]))

# C10_a
for k in employees:
    m.addConstr(quicksum([L[(k,i)] for i in nodes]) == 1)

# C10_b
for k in employees:
    for i in nodes:
        m.addConstr(Y[(k,i)] >= L[(k,i)])

# C11
for i in tasks + unavails:
    m.addConstr(quicksum([Y[(k,i)] for k in employees]) <= quicksum([X[(j,i)] for j in nodes if j != i]))

# C12
for i in tasks + unavails:
    for j in tasks + unavails:
        if i != j:
            pause_en_i = quicksum([L[(k,i)] for k in employees])
            m.addConstr(B[i] + Node.list[i].duration + ceil(Node.distance[i,j]/Employee.speed) <= B[j] + M * (1-X[(i,j)]) )
            m.addConstr(B[i] + Node.list[i].duration <= P[k] + M*(2-X[(i,j)]-pause_en_i))
            m.addConstr(P[k] + 60 + ceil(Node.distance[i,j]/Employee.speed) <= B[j] + M * (2-X[(i,j)]-pause_en_i) )
            

# C13
for k in employees:
    for i in tasks:
        m.addConstr(Employee.list[k].level >= Node.list[i].level - M * (1 - Y[(k,i)]))
