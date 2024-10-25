from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.study_list, name='study_list'),  # Default page for study list
    path('<int:study_id>/', views.study_detail, name='study_detail'),
    path('add/', views.add_study, name='add_study'),
    path('<int:study_id>/edit/', views.edit_study, name='edit_study'),
    # path('<int:study_id>/delete/', views.delete_study, name='delete_study'),
    path('delete_selected_studies/', views.delete_selected_studies, name='delete_selected_studies'), 
    
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_page, name='logout'),  # Show logout confirmation page
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),  # Handle logout confirmation
    # path('home/', views.home_view, name='home'),  # Assuming you have a home page
]
