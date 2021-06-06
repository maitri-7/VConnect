from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.utils import timezone
import datetime
import joblib
from django.core.validators import MinValueValidator, MaxValueValidator
from phone_field import PhoneField

# Create your models here.


class UserModel(models.Model):
    UNIT_CHOICES = (('Hospital','Hospital'),('Citizen','Citizen'),('NA','NA'))
    user = models.OneToOneField(User,related_name="user_profile",on_delete=models.CASCADE)

    is_Hospital = models.BooleanField(default=False)
    is_Citizen = models.BooleanField(default=False)
    unit = models.CharField(max_length=100,choices=UNIT_CHOICES,default='NA')
    unit_name = models.CharField(max_length=200,default='None')

    def get_absolute_url(self):
        return reverse("main_app:landing")


    def __str__(self):
        return self.user.username

class CitizenModel(models.Model):
    GENDER_CHOICES = (('Male','Male'),('Female','Female'),('Other','Other'),('NA','NA'))
    user = models.OneToOneField(UserModel,on_delete=models.CASCADE,null=True,related_name="assigned_citizen")
    gender = models.CharField(max_length=100,choices=GENDER_CHOICES,default='NA')
    is_cough = models.BooleanField(default=False)
    is_fever = models.BooleanField(default=False)
    is_sore_throat = models.BooleanField(default=False)
    is_shortness_of_breath = models.BooleanField(default=False)
    is_head_ache = models.BooleanField(default=False)
    is_age_60_and_above = models.BooleanField(default=False)
    is_contact = models.BooleanField(default=False)
    used_prediction = models.BooleanField(default=False)
    prediction_score = models.DecimalField(decimal_places=5,max_digits=10,default=0.0)

    def get_absolute_url(self):
        return reverse("main_app:landing")

    def __str__(self):
        return self.user.user.username

    def get_prediction(self):
        scaled = joblib.load("covidpred.model")
        #Major doubt order of array
        gender_var = False
        if self.gender == 'Male':
            gender_var = False
        elif self.gender == 'Female':
            gender_var = True

        prediction = scaled.predict_proba([[self.is_cough,self.is_fever,self.is_sore_throat,self.is_shortness_of_breath,self.is_head_ache,self.is_age_60_and_above,gender_var,self.is_contact]])
        result = prediction[0][1]*100
        print(result)
        self.used_prediction = True
        self.prediction_score = result

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(UserModel,on_delete=models.CASCADE,null=True,related_name="assigned_hospital")
    citizen_watchlist = models.ForeignKey(CitizenModel,on_delete=models.CASCADE,null=True,related_name="watchlist")
    # requests_received = models.ForeignKey(RequestModel,on_delete=models.CASCADE,null=True,related_name='received_requests')
    # requests_asked = models.ForeignKey(RequestModel,on_delete=models.CASCADE,null=True,related_name='asked_requests')
    address = models.CharField(max_length=200)
    beds = models.IntegerField()
    oxygen_cylinders = models.IntegerField(null=True)
    wards = models.IntegerField(null=True)
    curr_patients = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse("main_app:landing")

    def __str__(self):
        return self.name

class RequestModel(models.Model):
    hospital_received = models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True,related_name='received_requests')
    hospital_asked = models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True,related_name='asked_requests')
    name_requested = models.CharField(max_length=200,null=True)
    name_received = models.CharField(max_length=200,null=True)
    beds_requested = models.IntegerField()
    approved_status = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    oxygen_cylinders_requested = models.IntegerField()
    contact_email = models.EmailField(max_length=200,null=True)
    contact_phone = PhoneField(blank=True, help_text='Contact phone number')

    def approve_request(self):
        self.is_approved = True
        self.approved_status = True
        self.save()
        # return reverse_lazy("landing")

    def decline_request(self):
        self.is_approved = False
        self.approved_status = True
        self.save()
        # return reverse_lazy("landing")

    def get_absolute_url(self):
        return reverse("main_app:landing")

    def __str__(self):
        return self.name_requested

class DateCaseModel(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True,related_name='hospital_case')
    date = models.DateField(default=datetime.date.today)
    cases = models.IntegerField()

    def __str__(self):
        return "{}-{}".format(self.date,self.cases)

    def get_absolute_url(self):
        return reverse("main_app:landing")

class ReviewModel(models.Model):
    comments = models.CharField(max_length=200,null=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True,related_name='review_hospital')
    author = models.CharField(max_length=200)
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(5)],null=True)

    def get_absolute_url(self):
        return reverse("main_app:landing")
