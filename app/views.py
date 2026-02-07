from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']

            user.set_password(form.cleaned_data['password1'])

            user.save()
            messages.success(request, "Inscription réussie ! Connectez-vous.")
            return redirect('login_view')
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

#vue pour la connexion
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tb_st2026')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'connexion.html', {'form': form})

#vue pour la déconnexion
def deconnexion(request):
    logout(request)
    return redirect('login_view')

#vue pour la page d'accueil
def accueil(request):
    return render(request, 'accueil.html')

def st2026(request):
    return render(request, 'page_st.html')

#vue pour le dashboard
@login_required
def dashboard(request):
    solo = Inscription_solo.objects.filter(statut='valide')
    total_inscription_solo = solo.count()
    groupe = Inscription_groupe.objects.filter(statut='valide')
    total_inscription_groupe = groupe.count()
    total_membre = sum(int(g.effectif) for g in groupe if g.effectif)
    total_participant = total_membre + total_inscription_solo
    epm = Inscription_solo.objects.filter(Q(categorie='Epelle-Moi!') & Q(statut='valide'))
    total_epm = epm.count()
    qpc = Inscription_solo.objects.filter(Q(categorie='Question Pour un Champion') & Q(statut='valide'))
    total_qpc = qpc.count()
    mm = Inscription_solo.objects.filter(Q(categorie='Miss & Mister') & Q(statut='valide'))
    total_mm = mm.count()
    danse = Inscription_groupe.objects.filter(Q(categorie='Danse') & Q(statut='valide'))
    total_danse = danse.count()
    th = Inscription_groupe.objects.filter(Q(categorie='Théâtre') & Q(statut='valide'))
    total_th = th.count()
    dessin = Inscription_solo.objects.filter(Q(categorie='Dessin') & Q(statut='valide'))
    total_dessin = dessin.count()
    couture = Inscription_solo.objects.filter(Q(categorie='Couture') & Q(statut='valide'))
    total_couture = couture.count()
    cuisine = Inscription_solo.objects.filter(Q(categorie='Cuisine') & Q(statut='valide'))
    total_cuisine = cuisine.count()
    ao = Inscription_solo.objects.filter(Q(categorie='Art Oratoire') & Q(statut='valide'))
    total_ao = ao.count()
    ac = Inscription_solo.objects.filter(Q(categorie='A Capella') & Q(statut='valide'))
    total_ac = ac.count()
    context = {
        'total_inscription_solo': total_inscription_solo,
        'total_inscription_groupe':total_inscription_groupe,
        'total_participant':total_participant,
        'total_epm':total_epm,
        'total_mm':total_mm,
        'total_qpc':total_qpc,
        'total_danse':total_danse,
        'total_th':total_th,
        'total_dessin':total_dessin,
        'total_couture':total_couture,
        'total_cuisine':total_cuisine,
        'total_ao':total_ao,
        'total_ac':total_ac
    }
    return render(request, 'dashboard.html', context)

#vue pour les participants en groupe
@login_required
def liste_participant_solo(request):
    if request.method == 'POST':
        categorie = request.POST.get('categorie')
        categorie_existe = Inscription_solo.objects.filter(categorie=categorie).exists()

        if categorie_existe:
            solo = Inscription_solo.objects.filter(statut='valide')
            return render(request, 'all_participant_solo.html', {'solo': solo})
        
    return render(request, 'all_participant_solo.html')

#vue pour les groupes participants
@login_required
def liste_participant_groupe(request):
    if request.method == 'POST':
        categorie = request.POST.get('categorie')
        categorie_existe = Inscription_groupe.objects.filter(categorie=categorie).exists()

        if categorie_existe:
            groupe = Inscription_groupe.objects.filter(statut='valide')
            return render(request, 'all_participant_groupe.html', {'groupe': groupe})
        
    return render(request, 'all_participant_groupe.html')


#vue pour les inscriptions en solo
def inscription_solo(request):
    if request.method == 'POST':
        nom_prenom = request.POST.get('nom_prenom')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        groupe = request.POST.get('groupe')
        categorie = request.POST.get('categorie')

        # Vérification de l'existence de l'inscription
        existe_deja = Inscription_solo.objects.filter(nom_prenom=nom_prenom, categorie=categorie).exists()

        if existe_deja:
            messages.warning(request, "Vous êtes déjà inscrit(e) dans cette catégorie.")
        else:
            Inscription_solo.objects.create(
                nom_prenom=nom_prenom,
                age=age,
                contact=contact,
                groupe=groupe,
                categorie=categorie,
                statut='en_attente'
            )
            messages.success(request, "Votre inscription a été enregistrée!")
        
        return redirect(request.META.get('HTTP_REFERER', '/')) 

    return render(request, 'accueil.html')


#vue pour les inscriptions en groupe
def inscription_groupe(request):
    if request.method == 'POST':
        capitaine = request.POST.get('capitaine')
        nom_equipe = request.POST.get('nom_equipe')
        contact = request.POST.get('contact')
        effectif = request.POST.get('effectif')
        categorie = request.POST.get('categorie')

        # Vérification de l'existence de l'inscription
        existe_deja = Inscription_groupe.objects.filter(capitaine=capitaine, nom_equipe=nom_equipe, categorie=categorie).exists()

        if existe_deja:
            messages.warning(request, "Vous êtes déjà inscrit(e) dans cette catégorie.")
        else:
            Inscription_groupe.objects.create(
                capitaine=capitaine,
                nom_equipe=nom_equipe,
                contact=contact,
                effectif=effectif,
                categorie=categorie,
                statut='en_attente'
            )
            messages.success(request, "Votre inscription a été enregistrée!")
        
        return redirect(request.META.get('HTTP_REFERER', '/')) 

    return render(request, 'accueil.html')

@login_required
def liste_inscriptions(request):
    solo = Inscription_solo.objects.filter(Q(statut='en_attente') | Q(statut='rejete'))
    groupe = Inscription_groupe.objects.filter(Q(statut='en_attente') | Q(statut='rejete'))
    return render(request, 'enregistrement.html', {'solo': solo, 'groupe': groupe})

@login_required
def accepter_inscription_solo(request, id):
    inscription_solo = get_object_or_404(Inscription_solo, id=id)
    inscription_solo.statut = 'valide'
    inscription_solo.save()
    return redirect('liste_inscriptions')

@login_required
def accepter_inscription_groupe(request, id):
    inscription_groupe = get_object_or_404(Inscription_groupe, id=id)
    inscription_groupe.statut = 'valide'
    inscription_groupe.save()
    return redirect('liste_inscriptions')

@login_required
def rejeter_inscription_solo(request, id):
    inscription_solo = get_object_or_404(Inscription_solo, id=id)
    inscription_solo.statut = 'rejete'
    inscription_solo.save()
    return redirect('liste_inscriptions')
    
@login_required
def rejeter_inscription_groupe(request, id):
    inscription_groupe = get_object_or_404(Inscription_groupe, id=id)
    inscription_groupe.statut = 'rejete'
    inscription_groupe.save()
    return redirect('liste_inscriptions')