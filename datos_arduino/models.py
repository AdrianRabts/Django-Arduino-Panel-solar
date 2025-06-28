from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ldr_left_top = models.IntegerField()
    ldr_right_top = models.IntegerField()
    ldr_left_bottom = models.IntegerField()
    ldr_right_bottom = models.IntegerField()
    solar_value = models.IntegerField()

    def __str__(self):
        return f"{self.timestamp}: LDRs {self.ldr_left_top}, {self.ldr_right_top}, {self.ldr_left_bottom}, {self.ldr_right_bottom} | Solar: {self.solar_value}"
