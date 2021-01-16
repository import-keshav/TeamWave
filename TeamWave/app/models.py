from django.db import models


class User(models.Model):
    email =  models.TextField()
    last_time_search = models.DateTimeField()
    num_of_query = models.IntegerField()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.email