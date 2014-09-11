from django.conf.urls import patterns, include, url
from django.contrib import admin
from griev import views
from django.conf import settings
from django.conf.urls.static import static
from dajaxice.core import dajaxice_autodiscover, dajaxice_config


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'op_griev.views.home', name='home'),
    # url(r'^op_griev/', include('op_griev.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout_view),
    url(r'^home/$', views.home_view),
    url(r'^login_failure/$', views.login_failure),
    url(r'^cal-try/$', views.cal),
    url(r'post_grievance/$', views.post_grievance),
    url(r'my_grievances/$', views.my_grievances),
    url(r'view_grievance/(\d+)', views.view_grievance),
    url(r'mark_resolved/(\d+)', views.mark_resolved),
    url(r'update_profile/', views.update_profile),
    url(r'provide_keywords/', views.provide_keywords),
    url(r'pending_grievances/$',views.pending_grievances),
    url(r'resolved_grievances/$',views.resolved_grievances),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
