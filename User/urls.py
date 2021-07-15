from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from User.forms import UserLoginForm
from . import views


app_name = 'User'

urlpatterns = [
        path('',RedirectView.as_view(pattern_name='User:login')),
    #Login
        path('login/', auth_views.LoginView.as_view(
                                            template_name="login/login.html",
                                            authentication_form=UserLoginForm,
                                            redirect_authenticated_user=True
                                          ), name='login'),
    #Logout
        path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    #HomePage as Dashboard
        path('dashboard/', views.DashboardView, name='dashboard'),
    #New Schema
        path('newSchema/', views.NewSchemaView, name='NewSchema'),
    #Edit Schema
        path('editSchema/<int:pk>', views.EditSchemaView, name='EditSchema'),
    #Edit Schema
        path('deleteSchema/<int:pk>', views.DeleteSchemaView, name='DeleteSchema'),
    #List of Schemas
        path('myschema/<int:pk>', views.MySchemaView, name='MySchema'),
    #Generate CSV
        path('genereteCSV/<int:pk>', views.GenerateView, name='GenerateCSV'),
    #Create row to see status and to be able download on ready
        path('createRow/<int:pk>', views.CreateRow, name='CreateRow'),

]
