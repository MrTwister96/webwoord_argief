"""webwoord URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from frontend.views import HomeView, ArgiefView, NewPreekView, AdministrationView, NewReeksView, NewPredikerView, DeletePreekView, DeleteReeksView, ListPreekView, ListReeksView, ListPredikerView, GemeenteView

urlpatterns = [
    # User Views
    path('', HomeView.as_view(), name='home'),
    path('argief/', ArgiefView.as_view(), name='argief'),
    path('gemeente/<pk>/', GemeenteView.as_view(), name='gemeente_view'),




    # Administration
    path('administration/', AdministrationView, name='admin_view'),
    path('list_preek/', ListPreekView, name='list_preek'),
    path('new_preek/', NewPreekView, name='new_preek'),
    path('delete_preek/<pk>/', DeletePreekView, name='delete_preek'),
    path('list_reeks/', ListReeksView, name='list_reeks'),
    path('new_reeks/', NewReeksView, name='new_reeks'),
    path('delete_reeks/<pk>/', DeleteReeksView, name='delete_reeks'),
    path('new_prediker/', NewPredikerView, name='new_prediker'),
    path('list_prediker/', ListPredikerView, name='list_prediker'),
]
