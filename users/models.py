from django.db import models
from django.contrib.auth.models import AbstractUser
import django_tables2 as tables



class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Profile.objects.create(user=self,name=self.username)

class Profile(models.Model):
    GENDER_CHOICES = [('M', 'Male'),('F', 'Female'),('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    history_of_illness = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    prescriptions = models.ManyToManyField('Med.Prescription', related_name='profiles', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if 'force_insert' in kwargs:
            kwargs.pop('force_insert')
        super().save()

class PatientTable(tables.Table):
    class Meta:
        model = Profile