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
from django.http import HttpResponse
from fpdf import FPDF


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


def fichiers(request):
    return render(request, 'fichiers.html')

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
    restauration = Inscription_solo.objects.filter(Q(categorie='Restauration') & Q(statut='valide'))
    total_restauration = restauration.count()
    ao = Inscription_solo.objects.filter(Q(categorie='Art Oratoire') & Q(statut='valide'))
    total_ao = ao.count()
    ac = Inscription_solo.objects.filter(Q(categorie='A Capella') & Q(statut='valide'))
    total_ac = ac.count()
    trico = Inscription_solo.objects.filter(Q(categorie='Tricotage') & Q(statut='valide'))
    total_trico = trico.count()
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
        'total_restauration':total_restauration,
        'total_ao':total_ao,
        'total_ac':total_ac,
        'total_trico':total_trico
    }
    return render(request, 'dashboard.html', context)



# --- Participants solo ---
@login_required
def liste_participant_solo(request):
    solo = None
    categorie = None

    if request.method == 'POST':
        categorie = request.POST.get('categorie')
        solo = Inscription_solo.objects.filter(categorie=categorie, statut='valide')

    return render(request, 'all_participant_solo.html', {
        'solo': solo,
        'categorie': categorie,
    })


@login_required
def export_participant_solo_pdf(request):
    categorie = request.GET.get('categorie')
    solo = Inscription_solo.objects.filter(categorie=categorie, statut='valide')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Liste des participants - {categorie}", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 10)
    headers = ["N°", "Enfant", "Age", "Mouvement", "Categorie", "Contact"]
    widths = [12, 45, 15, 35, 40, 35]
    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for i, s in enumerate(solo, start=1):
        pdf.cell(widths[0], 8, str(i), border=1)
        pdf.cell(widths[1], 8, str(s.nom_prenom), border=1)
        pdf.cell(widths[2], 8, str(s.age), border=1)
        pdf.cell(widths[3], 8, str(s.groupe), border=1)
        pdf.cell(widths[4], 8, str(s.categorie), border=1)
        pdf.cell(widths[5], 8, str(s.contact), border=1)
        pdf.ln()

    response = HttpResponse(bytes(pdf.output()), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="participants_{categorie}.pdf"'
    return response


# --- Groupes participants ---
@login_required
def liste_participant_groupe(request):
    groupe = None
    categorie = None

    if request.method == 'POST':
        categorie = request.POST.get('categorie')
        groupe = Inscription_groupe.objects.filter(categorie=categorie, statut='valide')

    return render(request, 'all_participant_groupe.html', {
        'groupe': groupe,
        'categorie': categorie,
    })


@login_required
def export_participant_groupe_pdf(request):
    categorie = request.GET.get('categorie')
    groupe = Inscription_groupe.objects.filter(categorie=categorie, statut='valide')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Liste des groupes - {categorie}", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 10)
    headers = ["N°", "Capitaine", "Equipe", "Effectif", "Categorie", "Contact"]
    widths = [15, 40, 40, 25, 35, 35]
    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for i, g in enumerate(groupe, start=1):
        pdf.cell(widths[0], 8, str(i), border=1)
        pdf.cell(widths[1], 8, str(g.capitaine), border=1)
        pdf.cell(widths[2], 8, str(g.nom_equipe), border=1)
        pdf.cell(widths[3], 8, str(g.effectif), border=1)
        pdf.cell(widths[4], 8, str(g.categorie), border=1)
        pdf.cell(widths[5], 8, str(g.contact), border=1)
        pdf.ln()

    response = HttpResponse(bytes(pdf.output()), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="groupes_{categorie}.pdf"'
    return response


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