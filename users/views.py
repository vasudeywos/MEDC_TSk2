from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import login,authenticate
from django.shortcuts import redirect, render
from allauth.socialaccount.models import SocialAccount
from django.views.generic import TemplateView
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.views.generic import CreateView
from .models import User,Profile,PatientTable
from .forms import StaffSignUpForm
from django.contrib.auth.decorators import login_required
from .forms import PatientUpdateForm,StaffUpdateForm
from django.contrib import messages
from django.views.generic import ListView
from Med.models import Appointment,Doctor_Profiles,Bill
from chat.models import Message


class Home(TemplateView):
    template_name = 'Med/home.html'

class StaffProf(ListView):
    model = Appointment
    template_name = 'Med/staff.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'appointments'


class PatientProf(TemplateView):
    template_name = 'Med/patient.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        staffs=User.objects.filter(is_staff=True)
        profile=Profile.objects.get(user=user)
        context = super().get_context_data(**kwargs)
        appointments = Appointment.objects.filter(patient=user)
        bills=Bill.objects.filter(appointment__in=appointments)
        doctors = Doctor_Profiles.objects.filter(appointments__in=appointments)
        unseen_message_counts = {}
        unseen_message_count=0
        for staff in staffs:
            room_name = f"{staff.username}_{user.username}"
            unseen_message_count = Message.objects.filter(room_name=room_name, is_seen=False).exclude(author=user).count()
            unseen_message_count += unseen_message_count

        context['unseen_message_count'] = unseen_message_count
        context['doctors'] = doctors
        context['user'] = user
        context['bills'] = bills
        context['profile'] = profile
        context['appointemnts']=appointments
        context['staffs'] = staffs
        return context


@receiver(user_signed_up)
def set_user_as_patient(sender, request, user, **kwargs):
    if 'google' in user.socialaccount_set.values_list('provider', flat=True):
        if not user.is_staff:
            user.is_patient = True
            user.save()

@login_required
def home(request):
    if request.user.is_staff:
        return redirect('staff_pg')
    elif request.user.is_patient:
        return redirect('patient_pg')
    else:
        return render(request, 'Med/home.html')

class StaffSignUpView(CreateView):
    model = User
    form_class = StaffSignUpForm
    template_name = 'Med/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        authenticated_user = authenticate(self.request, username=user.username, password=form.cleaned_data['password1'])
        login(self.request, authenticated_user)

        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user, name=user.username)

        return redirect('staff_pg')

def patient_google_login(request):
    if request.user.is_authenticated and request.user.is_patient:
        return redirect('patient_pg')
    if request.user.is_authenticated and not request.user.is_patient:
        # Unlink existing social account if it exists and user is not a patient
        SocialAccount.objects.filter(user=request.user).delete()


    adapter = GoogleOAuth2Adapter(request)
    provider_url = adapter.get_login_url(request, OAuth2Client)
    return redirect(provider_url)


@login_required
def profile(request):
    if request.method == 'POST':
        if request.user.is_staff:
            p_form = StaffUpdateForm(request.POST, instance=request.user.profile)
        else:
            p_form = PatientUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid() and request.user.is_staff:
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('staff_pg')
        if p_form.is_valid() and request.user.is_patient:
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('patient_pg')
    else:
        if request.user.is_staff:
            p_form = StaffUpdateForm(instance=request.user.profile)
        else:
            p_form = PatientUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
        'user': request.user
    }

    return render(request, 'Med/profileupdt.html', context)


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('staff_pg')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login2')

    return render(request, 'registration/login.html')


def PatientTablist(request):
    table = PatientTable(Profile.objects.filter(user__is_patient=True))
    context={"table": table}
    return render(request, "Med/pattablist.html", context)