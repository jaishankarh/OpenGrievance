from django.contrib import admin
from griev.models import GrievanceOfficer, GrievanceRedressed, GrievanceRegistration
from griev.models import ClientDetails, Organisation, UserType

admin.site.register(GrievanceOfficer)
admin.site.register(GrievanceRedressed)
admin.site.register(GrievanceRegistration)
admin.site.register(ClientDetails)
admin.site.register(Organisation)
admin.site.register(UserType)