from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Rank
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",  # Ajout de related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions_set", # Ajout de related_name
        related_query_name="user",
    )

    def __str__(self):
        return self.username
    

class Inscription_solo(models.Model):
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('valide', 'Validé'),
    ]

    nom_prenom = models.CharField(max_length=255)
    age = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    groupe = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')

    def __str__(self):
        return f"{self.nom_prenom} - {self.statut}"
    

class Inscription_groupe(models.Model):
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('valide', 'Validé'),
    ]

    capitaine = models.CharField(max_length=255)
    nom_equipe = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    effectif = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')

    def __str__(self):
        return f"{self.nom_prenom} - {self.statut}"
