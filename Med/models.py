from django.db import models
from users.models import User

TIME_CHOICES = [('M', 'Morning'),('E', 'Evening'),('A','Either Morning or Evening')]
SPECIALIZATION_CHOICES = [('N','None'),('ENT', 'ENT'), ('CD', 'Cardiologist'), ('NE', 'Neurologist'),('ONC', 'Oncologist'),('ORT', 'Orthologist'),('DNT', 'Dentist'),('PHY', 'Physician')]


class Prescription(models.Model):
    name=models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('CN', 'Canceled'),
        ('CMP', 'Completed'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time_wanted = models.CharField(max_length=1, choices=TIME_CHOICES)
    appointment_time = models.TimeField(default='12:00')
    description = models.TextField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='P')
    Doctors_for_appnt= models.ForeignKey('Doctor_Profiles', related_name='appointments', blank=True, null=True,on_delete=models.CASCADE)
    Prescription=models.OneToOneField(Prescription,related_name='prescription',on_delete=models.CASCADE,blank=True,null=True)
    Pay_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Appointment for {self.patient.username} on {self.appointment_date}"

class Doctor_Profiles(models.Model):
    name= models.CharField(max_length=50)
    specialization = models.CharField(max_length=3, blank=True, null=True, choices=SPECIALIZATION_CHOICES)
    contact_info=models.IntegerField()

    def __str__(self):
        return self.name


class Bill(models.Model):
    amount = models.IntegerField()
    appointment = models.OneToOneField(Appointment, related_name='appoints', on_delete=models.CASCADE)

    def __str__(self):
        return f"Bill for {self.appointment.patient} on {self.appointment_date}"