from django.db import models

class chat(models.Model):
    query=models.CharField(max_length=1000,default="")
    response=models.CharField(max_length=1000,default="")
    class Meta:
        db_table="chat"