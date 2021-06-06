from django.shortcuts import render,get_object_or_404,redirect
from main_app.forms import HospitalForm,UserForm,UserExtraForm,RequestForm,DateCaseForm,CitizenForm,ReviewForm
from main_app.models import Hospital, UserModel, RequestModel, DateCaseModel, CitizenModel,ReviewModel
from django.views.generic import TemplateView,CreateView,ListView,DetailView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date
import joblib
import smtplib
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
class Landingview(TemplateView):
    template_name = "landing.html"

class DailyCasesTemplateView(TemplateView):
    template_name = "daily_cases.html"

class HospitalListView(ListView):
    model = Hospital
    context_object_name = 'hospitals'
    template_name = 'hospital_list.html'

    def get_queryset(self):
        order = self.request.GET.get('orderby', '-beds')
        return Hospital.objects.order_by(order)

    def get_context_data(self, **kwargs):
        context = super(HospitalListView, self).get_context_data(**kwargs)
        context['orderby'] = self.request.GET.get('orderby')
        return context

class HospitalDetailView(DetailView):
    model = Hospital
    template_name = 'hospital_detail.html'
    context_object_name = 'curr_hospital'

    def get_context_data(self, **kwargs):
        # hosp_id = self.kwargs.get('pk')
        # hospital_curr = get_object_or_404(Hospital,pk=hosp_id)
        # print(hospital_curr.beds)
        print(self.request.user)
        context = super(HospitalDetailView, self).get_context_data(**kwargs)
        context['form'] = RequestForm
        return context

class HospitalUpdateView(UpdateView):
    model = Hospital
    context_object_name = 'curr_hospital'
    fields = ('beds','oxygen_cylinders','wards','curr_patients')
    template_name = 'update_hospital.html'

class RequestCreateView(CreateView):
    model = RequestModel
    form_class = RequestForm

    def form_valid(self,form):
        hosp_id = self.kwargs.get('pk')
        hospital_curr = get_object_or_404(Hospital,pk=hosp_id)
        # print(hospital_curr.beds)
        new_request = form.save(commit=False)
        # new_request.name = self.request.user.user_profile.unit_name
        new_request.name_requested = self.request.user.user_profile.assigned_hospital.name
        new_request.name_received = hospital_curr.name
        new_request.save()

        hospital_logged = self.request.user.user_profile.assigned_hospital

        hospital_curr.received_requests.add(new_request)
        hospital_logged.asked_requests.add(new_request)
        hospital_curr.save()
        hospital_logged.save()
        # new_request.beds_requested = form.instance.beds_requested
        # new_request.oxygen_cylinders_requested = form.instance.oxygen_cylinders_requested
        # new_request.name =
        return super(RequestCreateView, self).form_valid(form)

class RequestsReceivedDetailView(DetailView):
    model = Hospital
    template_name = 'requests_receive.html'
    context_object_name = 'hospital'

class RequestsAskedDetailView(DetailView):
    model = Hospital
    template_name = 'requests_ask.html'
    context_object_name = 'hospital'

class CitizenDetailView(DetailView):
    model = CitizenModel
    template_name = 'user_detail.html'
    context_object_name = 'citizen'

class CitizenUpdateView(UpdateView):
    model = CitizenModel
    fields = ('is_cough','is_fever','is_sore_throat','is_shortness_of_breath','is_head_ache','is_age_60_and_above','is_contact')
    template_name = 'user_update.html'

class CitizenWatchListView(ListView):
    model = CitizenModel
    template_name = 'user_watchlist.html'
    context_object_name = 'citizen'

    def get_queryset(self):
        order = self.request.GET.get('orderby', '-beds')
        return Hospital.objects.order_by(order)

    def get_context_data(self, **kwargs):
        context = super(CitizenWatchListView, self).get_context_data(**kwargs)
        context['orderby'] = self.request.GET.get('orderby')
        return context

def AddToWatchlist(request,pk):
    hospital = get_object_or_404(Hospital,pk=pk)
    citizen = request.user.user_profile.assigned_citizen
    citizen.watchlist.add(hospital)
    citizen.save()

    return redirect('main_app:citizen_detail',pk=citizen.pk)

def PredictCovid(request,pk):
    citizen = get_object_or_404(CitizenModel,pk=pk)
    citizen.get_prediction()
    citizen.save()
    # print('here')
    return redirect('main_app:landing')

def ApproveRequest(request,pk):
    Request = get_object_or_404(RequestModel,pk=pk)
    Hospital = request.user.user_profile.assigned_hospital

    Request.approve_request()
    Hospital.beds = Hospital.beds - Request.beds_requested
    Hospital.oxygen_cylinders = Hospital.oxygen_cylinders - Request.oxygen_cylinders_requested
    Hospital.save()

    return redirect('main_app:landing')

def DeclineRequest(request,pk):
    Request = get_object_or_404(RequestModel,pk=pk)
    Request.decline_request()

    return redirect("main_app:landing")


@login_required
def NewHospital(request,pk):
    main_user = get_object_or_404(User,pk=pk)
    hospital_made = False
    if hasattr(main_user.user_profile,'assigned_hospital'):
        hospital_made = True

    if request.method == 'POST' and hospital_made==False:
        hospital_form = HospitalForm(data=request.POST)
        datecase_form = DateCaseForm(data=request.POST)

        if hospital_form.is_valid() and datecase_form.is_valid():
            hospital = hospital_form.save(commit=False)
            hospital.user = main_user.user_profile
            hospital.save()

            datacase = datecase_form.save(commit=False)
            datacase.hospital = hospital
            datacase.save()

        else:
            print(hospital_form.errors,datacase.errors)

    else:
        hospital_form = HospitalForm()
        datecase_form = DateCaseForm()

    return render(request,"register_hospital.html",{'hospital_form':hospital_form,'hospital_made':hospital_made,'datecase_form':datecase_form})

def signup(request):

    registered = False
    UnitName = "Connect and Contribute"
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_extra_form = UserExtraForm(data=request.POST)
        citizen_form = CitizenForm(data=request.POST)

        if user_form.is_valid() and user_extra_form.is_valid() and citizen_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            extra = user_extra_form.save(commit=False)
            print(extra.unit)
            extra.user = user

            if extra.unit == 'Hospital':
                print(extra.unit)
                extra.is_Hospital = True
            elif extra.unit == 'Citizen':
                print(extra.unit)
                extra.is_Citizen = True


            extra.save()
            print(extra.unit)
            citizen = citizen_form.save(commit=False)
            citizen.user = user.user_profile
            citizen.save()

            UnitName = extra.unit_name
            registered = True

        else:
            print(user_form.errors,user_extra_form.errors,citizen_form.errors)

    else:
        user_form = UserForm()
        user_extra_form = UserExtraForm()
        citizen_form = CitizenForm()

    return render(request,'signup.html',{'user_form':user_form,'user_extra_form':user_extra_form,
    'registered':registered,'UnitName':UnitName,'citizen_form':citizen_form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('main_app:landing'))

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse_lazy('main_app:landing'))
            else:
                return HttpResponseRedirect("ACCOUNT NOT ACTIVE")

        else:
            print("Someone Tried to login and failed")
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request,'login.html')

def getPredictions(request):
    scaled = joblib.load("covidpred.model")
    prediction = scaled.predict_proba([[True,True,True,0,0,0,0,0]])
    result = prediction[0][1]*100
    print(prediction[0][1])
    return render(request,'result.html', {'result':result})


class DateCaseCreateView(CreateView):
    model = DateCaseModel
    form_class = DateCaseForm
    template_name='update_cases.html'

    def form_valid(self,form):
        hospital_curr = self.request.user.user_profile.assigned_hospital
        new_request = form.save(commit=False)
        new_request.save()
        hospital_curr.hospital_case.add(new_request)

        return super(DateCaseCreateView, self).form_valid(form)

def sendApprovalMail(request,pk):

    request_main = get_object_or_404(RequestModel,pk=pk)

    text = 'Greetings from {} \n This is the approval mail for your logistics request. Please get in touch with our Hospital Vconnect Admin to further dicsuss the transfer of logistics \n Email: {}'.format(request.user.user_profile.unit_name,request.user.email)

    send_mail('Approval Mail for Logistics Transfer',text,'vconnectofficialapproval@gmail.com'
    ,[request_main.contact_email],fail_silently=False,)

    return HttpResponseRedirect(reverse_lazy('main_app:landing'))

class AddCommentCreateView(CreateView):
    model = ReviewModel
    form_class = ReviewForm
    template_name='add_comment_form.html'

    def form_valid(self,form):
        hosp_id = self.kwargs.get('pk')
        hospital_curr = get_object_or_404(Hospital,pk=hosp_id)
        new_comment = form.save(commit=False)
        new_comment.author = self.request.user.username
        new_comment.save()
        hospital_curr.review_hospital.add(new_comment)
        return super(AddCommentCreateView, self).form_valid(form)
