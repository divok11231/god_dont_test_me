import pulp

class Task:
    def __init__(self, name, duration, start_time, end_time, value, dependencies=None):
        self.name = name
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time
        self.value = value
        self.dependencies = dependencies or []

tasks = [
    Task("Task1", duration=2, start_time=0, end_time=8, value=10),
    Task("Task2", duration=4, start_time=0, end_time=12, value=20, dependencies=["Task1"]),
    Task("Task3", duration=3, start_time=2, end_time=15, value=15),
]

prob = pulp.LpProblem("Industry_4.0_Task_Scheduling", pulp.LpMaximize)

task_start_vars = {task.name: pulp.LpVariable(f"start_{task.name}", lowBound=task.start_time, upBound=task.end_time - task.duration, cat="Continuous") for task in tasks}
task_completion_vars = {task.name: pulp.LpVariable(f"complete_{task.name}", cat="Binary") for task in tasks}

prob += pulp.lpSum([task.value * task_completion_vars[task.name] for task in tasks])

big_M = 1000

for task in tasks:
    prob += task_start_vars[task.name] >= task.start_time * task_completion_vars[task.name], f"StartBound_{task.name}"
    prob += task_start_vars[task.name] + task.duration <= task.end_time + big_M * (1 - task_completion_vars[task.name]), f"EndBound_{task.name}"

for task in tasks:
    for dep in task.dependencies:
        dep_task = next(t for t in tasks if t.name == dep)
        
        prob += task_start_vars[task.name] >= (task_start_vars[dep] + dep_task.duration) - big_M * (1 - task_completion_vars[dep]), f"Dependency_{task.name}_{dep}"

prob.solve()

for task in tasks:
    start_time = pulp.value(task_start_vars[task.name])
    is_completed = pulp.value(task_completion_vars[task.name])
    if is_completed:
        print(f"{task.name} - Start at: {start_time}, Duration: {task.duration}, Completed: Yes, Value: {task.value}")
    else:
        print(f"{task.name} - Cannot be scheduled within given constraints.")

