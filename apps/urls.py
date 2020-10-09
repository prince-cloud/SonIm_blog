from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/', views.event, name='events'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('login/', LoginView.as_view(), name="login"),
    path('our-team/', views.our_team, name='our_team'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('add-event/', views.add_event, name="add_event"),
    path('be-a-member/', views.be_a_member, name='be_a_member'),
    path('createprofile/', views.create_profile, name='create_profile'),
    path('add-relatedPictre/<int:id>', views.add_picture, name='add_picture'),
    path('event/detail/<slug:event_slug>/', views.eventdetail, name='eventdetail'),
    path('resteredmembers/', views.registered_members, name='registered_members'),
    path('add/upcoming/event/', views.add_upcoming_event, name="add_upcoming_event"),
]