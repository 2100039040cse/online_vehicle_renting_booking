from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Partner
from .models import Bike,Car,Auto,Traveller,Truck,Tractor,Jcb,BorewellTruck,CombineHarvester
from .models import PaymentDetails

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2', 'email']
 
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['fullname', 'phone', 'address', 'vehicle_type', 'num_vehicles']



class BikeForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = Bike
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'location', 'station', 'status'] #, 'terms_conditions', 'driver_name', 'driver_contact', 'driver_cost'



class CarForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = Car
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status'] #, 'terms_conditions'



class AutoForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = Auto
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status'] #, 'terms_conditions'

class TravellerForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = Traveller
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status']


class TruckForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = Truck
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status']

class TractorForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = Tractor
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status']


class JcbForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = Jcb
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status']

class BorewellTruckForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = BorewellTruck
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status']

class CombineHarvesterForm(forms.ModelForm):
    LOCATIONS = [
        ('Vijayawada', 'Vijayawada'),
        ('Khammam', 'Khammam'),
    ]

    STATIONS = [
        ('A Station', 'A Station'),
        ('B Station', 'B Station'),
        
    ]

    location = forms.ChoiceField(choices=LOCATIONS)
    station = forms.ChoiceField(choices=STATIONS)
    class Meta:
        model = CombineHarvester
        fields = ['vehicle_id', 'vehicle_number', 'image', 'vehicle_name', 'rent_cost', 'driver_name', 'driver_contact', 'driver_cost', 'location', 'station', 'status']

class PaymentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    address = forms.CharField()

    class Meta:
        model = PaymentDetails
        fields = ['start_datetime', 'end_datetime', 'address', 'total_cost', 'password'] 

