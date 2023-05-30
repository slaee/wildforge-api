from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    sections = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    
    def setName(self, name):
        self.name = name
    
    def setSections(self, sections):
        self.sections = sections
    
    def setSchedule(self, schedule):
        self.schedule = schedule

    def getName(self):
        return self.name
    
    def getSections(self):
        return self.sections
    
    def getSchedule(self):
        return self.schedule