from django.urls import path,include
from . import views
from .views import DoctorCreateView,DoctorListView,DoctorDetailView,DoctorUpdateView,DoctorDeleteView,PresciptionCreateView

urlpatterns = [
    path('', include('users.urls')),
    path('apply_appointment/', views.createappointment, name='apply'),
    path('update_appointment/<int:pk>', views.updtappointment, name='updateAppnt'),
    path('doc/', DoctorListView.as_view(), name='doc_list'),
    path('doc/<int:pk>/', DoctorDetailView.as_view(), name='doc-detail'),
    path('doc/new/', DoctorCreateView.as_view(), name='doc-create'),
    path('doc/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doc-delete'),
    path('doc/<int:pk>/update/', DoctorUpdateView.as_view(), name='doc-update'),
    path('presc/upload', PresciptionCreateView.as_view(), name ='presc-up'),
    path('download/<int:presc_id>/', views.download, name='download'),
    path('bill/<int:appnt_id>/', views.Createbill, name='createbill'),
    path('account/', views.all_Bills, name='allbill'),
    path('patientlist/', views.PatientListView, name='patient_list'),
    path('patientsearch/', views.PatientSearchView, name='patient_search'),
    path('doctablelist/', views.DocTablist, name='doctablist'),
]
