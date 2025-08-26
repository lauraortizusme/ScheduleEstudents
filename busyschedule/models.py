from django.db import models

DAYS = [
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miércoles', 'Miércoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sábado', 'Sábado'),
    ('Domingo', 'Domingo'),
]

DAY_ORDER = {
    'Lunes': 1,
    'Martes': 2,
    'Miércoles': 3,
    'Jueves': 4,
    'Viernes': 5,
    'Sábado': 6,
    'Domingo': 7,
}

class ClassSchedule(models.Model):
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.day}: {self.start_time} - {self.end_time} ({self.subject})"

    def day_index(self):
        return DAY_ORDER.get(self.day, 99)  

class AvailableBlock(models.Model):
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day}: {self.start_time} - {self.end_time}"

    def day_index(self):
        return DAY_ORDER.get(self.day, 99)
