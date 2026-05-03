from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('api/milestones/', views.milestone_list_api, name='milestone_list_api'),
    path('api/milestones/delete/<int:pk>/', views.delete_milestone_api, name='delete_milestone_api'),
    path('api/milestones/update/<int:pk>/', views.update_milestone_api, name='update_milestone_api'),
]