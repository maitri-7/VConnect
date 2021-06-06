from django.contrib import admin
from main_app.models import Hospital, UserModel, RequestModel, DateCaseModel, CitizenModel,ReviewModel

admin.site.register(Hospital)
admin.site.register(UserModel)
admin.site.register(RequestModel)
admin.site.register(DateCaseModel)
admin.site.register(CitizenModel)
admin.site.register(ReviewModel)
