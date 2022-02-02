class Employee:
    def __init__(self, name, latitude, longitude, skill, level, starttime, endtime):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.skill = skill
        self.level = level
        self.starttime = starttime
        self.endtime = endtime
    
class Task:
    
    def  __init(self, id, latitude, longitude, duration, skill, level, openingtime, closingtime):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.duration = duration
        self.skill = skill
        self.level = level
        self.openingtime = openingtime
        self.closingtime = closingtime

class Employees_Unavailabilities:
    def __init__(self,name, latitude, longitude,start,end):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.start = start
        self.end = end

class Task_Unavailabilities:
    def __init__(self,id, start, end):
        self.id = id
        self.start = start
        self.end = end
        
        