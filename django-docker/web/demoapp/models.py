from django.db import models

class send_task(models.Model):
    project_id = models.CharField(max_length=20)


