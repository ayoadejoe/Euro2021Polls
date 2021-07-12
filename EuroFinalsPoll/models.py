from django.db import models
# I import datetime because I need to enter
# the date that the poll question was created
import datetime
# importing timezone will ensure that location based timezone is used
from django.utils import timezone


# Here I define the poll question field. This is where the
# questions are stored in the database
class Question(models.Model):
    question_text = models.CharField(max_length=200)  # Question can't be more than 200 characters
    pub_date = models.DateTimeField('date published')  # Date question was published is also included

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


# The choice class applies the nature of the fields in the database
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
