from report.views import HomeCarteInfo, juridition_list, get_detail_juridiction,tableCarteInfo
from django.urls import path

from .vue import HomeView

urlpatterns = [

    path('', HomeCarteInfo.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='juridition_list'),
    #path('juridiction', ReportCarteInfoJuridction.as_view(), name='home'),
    path('juridiction-list', juridition_list, name='list-juridiction'),
    path('juridiction-detail/<str:juridiction_name>/', get_detail_juridiction, name='list-juridiction-detail'),
    path('home/tables', tableCarteInfo.as_view(), name='table'),
]
