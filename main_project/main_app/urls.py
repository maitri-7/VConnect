from django.urls import path
from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('vconnect/',views.Landingview.as_view(), name="landing"),
    path('signup/',views.signup, name="create_user"),
    path('login/',views.user_login, name="login"),
    path('logout/',views.user_logout, name="logout"),
    path('<int:pk>/hospital_register/',views.NewHospital,name="create_hospital"),
    path('hopsitallist/',views.HospitalListView.as_view(),name="all_hopsital"),
    path('hospital/<int:pk>',views.HospitalDetailView.as_view(),name="detail_hospital"),
    path('place_request/<int:pk>',views.RequestCreateView.as_view(),name="request_hospital"),
    path('received_reqs/<int:pk>',views.RequestsReceivedDetailView.as_view(),name="request_received"),
    path('asked_reqs/<int:pk>',views.RequestsAskedDetailView.as_view(),name="request_asked"),
    path('approve_req/<int:pk>',views.ApproveRequest,name="approve_request"),
    path('decline_req/<int:pk>',views.DeclineRequest,name="decline_request"),
    path('citizen_detail/<int:pk>',views.CitizenDetailView.as_view(),name="citizen_detail"),
    path('get_covid_data/<int:pk>',views.PredictCovid,name='predict_covid'),
    path('citizen_update/<int:pk>',views.CitizenUpdateView.as_view(),name="citizen_update"),
    path('addToWatchlist/<int:pk>',views.AddToWatchlist,name="citizen_watchlist"),
    path('UserWatchlist/<int:pk>',views.CitizenWatchListView.as_view(),name="citizen_watchlist_hospital"),
    path('predict/',views.getPredictions,name='predict'),
    path('hospital_update/<int:pk>',views.HospitalUpdateView.as_view(),name='hospital_update'),
    path('update_cases/',views.DateCaseCreateView.as_view(),name='hospital_update_form'),
    path('approve_mail/<int:pk>',views.sendApprovalMail,name="approve_mail"),
    path('add_comment_form/<int:pk>',views.AddCommentCreateView.as_view(),name="add_comment_form"),
    path('daily_cases',views.DailyCasesTemplateView.as_view(),name="daily_cases"),



]
