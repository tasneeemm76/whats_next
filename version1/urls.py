from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('users/', views.list_users, name='list_users'),
    path('register/', views.register_workshop_view, name='register_workshop'),
    path('dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/add/', views.add_workshop, name='add_workshop'),
    path('dashboard/upcoming/', views.upcoming_workshops, name='upcoming_workshops'),
    path('dashboard/previous/', views.previous_workshops, name='previous_workshops'),
    path('dashboard/promote/', views.promote_workshop, name='promote_workshop'),
    path('dashboard/profile/', views.organizer_profile, name='organizer_profile'),
    path('workshops/create/', views.create_workshop_view, name='create_workshop'),
    path("enroll/<int:workshop_id>/", views.enroll_workshop, name="enroll_workshop"),
    path("enroll/<int:workshop_id>/confirm/", views.confirm_enroll, name="confirm_enroll"),
    path("enroll/success/<int:booking_id>/", views.enroll_success, name="enroll_success"),
    
    ]
