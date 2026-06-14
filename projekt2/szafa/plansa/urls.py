from django.urls import path
from .views import ListaGierView, MasowyView, SzukanieNazwaView, SzczegolyGryView, NowaGraView

urlpatterns = [
    path('api/lista/', ListaGierView.as_view(), name='lista'),
    path('api/nowa/', NowaGraView.as_view(), name='nowa'),
    path('api/gra/<int:pk>/', SzczegolyGryView.as_view(), name='detal'),
    path('api/import/masowy/', MasowyView.as_view(), name='import'),
    path('api/nazwa/', SzukanieNazwaView.as_view(), name='nazwa'),
]