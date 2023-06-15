from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm,PrescriptionForm
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AppointmentUpdateForm,BillForm
from .models import Appointment,Doctor_Profiles,Prescription,Bill,DoctorTable
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from fuzzywuzzy import fuzz,process


@login_required
def createappointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment application submitted successfully!')
            return redirect('patient_pg')
    else:
        form = AppointmentForm()

    context = {
        'form': form,
    }

    return render(request, 'Med/appointment.html', context)

def all_Appointments(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments
    }
    return render(request,'Med/allappnts.html',context )


def updtappointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    patient=appointment.patient
    info=Profile.objects.get(user=patient)

    try:
        bill = Bill.objects.get(appointment=appointment)
    except Bill.DoesNotExist:
        bill = None


    if not request.user.is_staff and appointment.patient != request.user:
        return redirect('profile')

    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, user=request.user, instance=appointment)
        if form.is_valid() and request.user.is_patient:
            form.save()
            if bill and bill.amount == appointment.Pay_amount:
                appointment.status = 'completed'
                appointment.save()
            return redirect('patient_pg')
        if form.is_valid() and request.user.is_staff:
            form.save()
            if appointment.Prescription:
                info.prescriptions.add(appointment.Prescription)
            return redirect('staff_pg')
    else:
        form = AppointmentUpdateForm(instance=appointment)


    context = {
        'form': form,
        'bills':bill,
        'user':request.user,
        'info':info,
    }

    return render(request, 'Med/apptupdt.html', context)

class DoctorListView(ListView):
    model=Doctor_Profiles
    template_name = 'Med/doclist.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'docs'

class DoctorDetailView(DetailView):
        model = Doctor_Profiles
        template_name = 'Med/doc_detail.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            doctor = self.object
            appointments = Appointment.objects.filter(Doctors_for_appnt=doctor)
            context['appointments'] = appointments
            return context


class DoctorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Doctor_Profiles
    fields=['name','specialization','contact_info']
    template_name = 'Med/doc_form.html'
    success_url = reverse_lazy('doc_list')

    def form_valid(self, form):
         return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctor_Profiles
    fields = ['name', 'specialization', 'contact_info']
    template_name = 'Med/doc_update.html'
    success_url = reverse_lazy('doc_list')

    def form_valid(self, form):
         return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

class DoctorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Doctor_Profiles
    template_name = 'Med/doc_delete.html'
    success_url = reverse_lazy('doc_list')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class PresciptionCreateView(CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'Med/upload.html'
    success_url = reverse_lazy('staff_pg')


def download(request, presc_id):
    appointment = get_object_or_404(Appointment, pk=presc_id)
    document =appointment.Prescription
    response = HttpResponse(document.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document.name}"'
    return response



def Createbill(request, appnt_id):
    appointment = get_object_or_404(Appointment, pk=appnt_id)

    try:
        bill = Bill.objects.get(appointment=appointment)
    except Bill.DoesNotExist:
        bill = None

    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.appointment = appointment
            bill.amount = form.cleaned_data['amount']
            bill.save()
            return redirect('staff_pg')
    else:
        initial_data = {'amount': appointment.Pay_amount} if bill else {}
        form = BillForm(instance=bill, initial=initial_data)

    context = {
        'form': form,
        'appointment': appointment
    }

    return render(request, 'Med/createbill.html', context)



def all_Bills(request):
    bills = Bill.objects.all()
    context = {
        'bills': bills
    }
    return render(request,'Med/allbills.html',context )

def PatientListView(request):
    patients = Profile.objects.filter(user__is_patient=True)
    user=request.user
    context = {
        'patients': patients,
        'user':user
    }
    return render(request, 'Med/patientlist.html', context)

def PatientSearchView(request):
    search_query = request.GET.get('search')

    patients = Profile.objects.filter(user__is_patient=True)

    if search_query:
        best_match = process.extractOne(search_query, patients, scorer=fuzz.token_sort_ratio)

        if best_match is not None:
            best_match_profile = best_match[0]
            patients = [best_match_profile]
        else:
            patients = []

    context = {
        'patients': patients,
        'search_query': search_query,
    }

    return render(request, 'Med/patientsearch.html', context)

def DocTablist(request):
    table = DoctorTable(Doctor_Profiles.objects.all())
    context={"table": table}
    return render(request, "Med/doctablist.html", context)



