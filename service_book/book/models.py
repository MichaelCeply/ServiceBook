from django.db import models

# Create your models here.
class Person(models.Model):
    login = models.CharField(max_length=8)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name
    
class Car(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Record(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    datetime = models.DateTimeField('created', auto_now_add=True)
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.datetime.year}-{self.datetime.month}-{self.datetime.day} {self.datetime.hour}:{self.datetime.minute}:{self.datetime.second}"
