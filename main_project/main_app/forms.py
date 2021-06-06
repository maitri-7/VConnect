from django import forms
from django.contrib.auth.models import User
from main_app.models import Hospital,UserModel,RequestModel,DateCaseModel,CitizenModel,ReviewModel


class HospitalForm(forms.ModelForm):

    class Meta():
        model = Hospital
        fields = ('name','address','beds','oxygen_cylinders','wards','curr_patients')

class CitizenForm(forms.ModelForm):

    class Meta():
        model = CitizenModel
        fields = ('gender','is_cough','is_fever','is_sore_throat','is_shortness_of_breath','is_head_ache','is_age_60_and_above','is_contact')

class DateCaseForm(forms.ModelForm):

    class Meta():
        model = DateCaseModel
        fields = ('date','cases')

class RequestForm(forms.ModelForm):

    class Meta():
        model = RequestModel
        fields = ('beds_requested','oxygen_cylinders_requested','contact_email','contact_phone')

class UserForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','password','email')

class UserExtraForm(forms.ModelForm):

    class Meta():
        model = UserModel
        fields = ('unit','unit_name')

class ReviewForm(forms.ModelForm):
    class Meta():
        model = ReviewModel
        fields = ('comments','rating')
