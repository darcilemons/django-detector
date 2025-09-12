from django.db import models

class conds(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    relatos = models.CharField(max_length=200)

    def __str__(self):
        return self.name