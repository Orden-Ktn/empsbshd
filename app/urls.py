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
    path('inscription/', views.register, name='register'),
    path('déconnexion/', views.deconnexion, name='deconnexion'),
    path('tb_st2026/', views.dashboard, name='tb_st2026'),
    path('participant en solo/', views.liste_participant_solo, name='liste_participant_solo'),
    path('groupe participant/', views.liste_participant_groupe, name='liste_participant_groupe'),

    path('liste des inscriptions/', views.liste_inscriptions, name='liste_inscriptions'),
    path('inscription en solo/', views.inscription_solo, name='inscription_solo'),
    path('inscription en groupe/', views.inscription_groupe, name='inscription_groupe'),

    # path('fichiers solo/', views.fichiers_solo, name='fichiers_solo'),
    # path('fichiers groupe/', views.fichiers_groupe, name='fichiers_groupe'),

    # path('liste des enfants/', views.liste_enfants, name='liste_enfants'),

    # path('solo/modifier/<int:id>/', views.modifier_solo, name='modifier_solo'),
    # path('solo/supprimer/<int:id>/', views.supprimer_solo, name='supprimer_solo'),

    # path('groupe/<int:id>/modifier/', views.modifier_groupe, name='modifier_groupe'),
    # path('groupe/<int:id>/supprimer/', views.supprimer_groupe, name='supprimer_groupe'),


    path('accepter inscription solo/<int:id>/', views.accepter_inscription_solo, name='accepter_inscription_solo'),
    path('accepter inscription groupe/<int:id>/', views.accepter_inscription_groupe, name='accepter_inscription_groupe'),
    path('rejeter inscription solo/<int:id>/', views.rejeter_inscription_solo, name='rejeter_inscription_solo'),
    path('rejeter inscription groupe/<int:id>/', views.rejeter_inscription_groupe, name='rejeter_inscription_groupe'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
