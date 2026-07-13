from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('', views.accueil, name='accueil'),
    path('connexion/', views.login_view, name='login_view'),
    path('st2026/', views.st2026, name='st2026'),
    path('fichiers/', views.fichiers, name='fichiers'),


    path('inscription/', views.register, name='register'),
    path('déconnexion/', views.deconnexion, name='deconnexion'),
    path('tb_st2026/', views.dashboard, name='tb_st2026'),


    path('liste des inscriptions/', views.liste_inscriptions, name='liste_inscriptions'),
    path('inscription en solo/', views.inscription_solo, name='inscription_solo'),
    path('inscription en groupe/', views.inscription_groupe, name='inscription_groupe'),

    path('participants/solo/', views.liste_participant_solo, name='liste_participant_solo'),
    path('participants/solo/pdf/', views.export_participant_solo_pdf, name='export_participant_solo_pdf'),

    path('participants/groupe/', views.liste_participant_groupe, name='liste_participant_groupe'),
    path('participants/groupe/pdf/', views.export_participant_groupe_pdf, name='export_participant_groupe_pdf'),


    path('accepter inscription solo/<int:id>/', views.accepter_inscription_solo, name='accepter_inscription_solo'),
    path('accepter inscription groupe/<int:id>/', views.accepter_inscription_groupe, name='accepter_inscription_groupe'),
    path('rejeter inscription solo/<int:id>/', views.rejeter_inscription_solo, name='rejeter_inscription_solo'),
    path('rejeter inscription groupe/<int:id>/', views.rejeter_inscription_groupe, name='rejeter_inscription_groupe'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
