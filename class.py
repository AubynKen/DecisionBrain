class Employee:
    def __init__(self, Name, Latitude, Longitude, Skill, Level, WorkingStartTime, WorkingEndTime):
        self.Name = Name
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Skill = Skill
        self.Level = Level
        self.WorkingStartTime = WorkingStartTime
        self.WorkingEndTime = WorkingEndTime
    
class Task:
    
    def  __init(self, TaskId, Latitude, Longitude, TaskDuration, Skill, Level, OpeningTime, ClosingTime):
        self.TaskId = TaskId
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Taskduration = TaskDuration
        self.Skill = Skill
        self.Level = Level
        self.OpeningTime = OpeningTime
        self.ClosingTime = ClosingTime