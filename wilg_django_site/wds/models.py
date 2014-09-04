from django.db import models

# Create your models here.

class Exec(models.Model):
    member_id=models.IntegerField(null=False, unique=True)
    position=models.CharField(max_length=1000)
    year=models.IntegerField(null=False, unique=False) # year position held
    semester=models.BooleanField() # 0 = fall, 1 = spring semester

class Member(models.Model):
    name=models.CharField(max_length=1000)
    year=models.IntegerField(null=False, unique=False)
    major1=models.CharField(max_length=1000)
    major2=models.CharField(max_length=1000)
    minor1=models.CharField(max_length=1000)
    minor2=models.CharField(max_length=1000)
    oww=models.IntegerField(null=False, unique=False) # member id
    ydo=models.CommaSeparatedIntegerField(max_length=10000) # member ids
    blurb=models.TextField()
    hometown=models.CharField(max_length=1000)
    photo=models.CharField(max_length=1000) # a url

class Course(models.Model):
    '''
    represents a guess: an unordered set of numbers
    '''
    number=models.CharField(max_length=1000)
    name=models.CharField(max_length=1000)
