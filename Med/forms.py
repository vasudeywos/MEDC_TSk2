from django import forms
from django.contrib.admin import widgets
from .models import Appointment,Prescription,Bill

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time_wanted','description']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time','status','description','Doctors_for_appnt','Prescription','Pay_amount']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Check if user is a staff member
        if user and user.is_staff:
            self.fields.pop('description')
            self.fields.pop('Pay_amount')

        else:  # User is a patient
            self.fields.pop('appointment_time')
            self.fields.pop('status')
            self.fields.pop('Doctors_for_appnt')
            self.fields.pop('Prescription')

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('description', 'document','name')

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['amount']