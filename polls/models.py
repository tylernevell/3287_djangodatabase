from django.db import models
# The name of each Field instance (e.g. question_text or pub_date) is the field’s name,
# in machine-friendly format. You’ll use this value in your Python code, and your
# database will use it as the column name.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
