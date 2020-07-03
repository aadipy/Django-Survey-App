from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class UserData(models.Model):

    user_id = models.OneToOneField(User, on_delete= models.CASCADE)
    name       = models.CharField(max_length = 25)
    email      = models.CharField(max_length = 30)

    def __str__(self):
        return self.name + "|" + self.email

class Question(models.Model):

    category = models.CharField(max_length=50)
    question = models.TextField()
    

    def __str__(self):
        return self.question

class Survey(models.Model):

    question_id = models.ForeignKey(Question, on_delete = models.CASCADE)
    feedback    = models.TextField()
    rating      = models.IntegerField()
    user_id     = models.ForeignKey(UserData, on_delete= models.CASCADE)


