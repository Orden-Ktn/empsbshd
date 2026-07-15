document.addEventListener('DOMContentLoaded', function () {
    const maintenant = new Date();

    // Fenêtre Solo & Groupe
    const soloGroupeDebut = new Date('2026-06-25T00:00:00');
    const soloGroupeFin   = new Date('2026-08-14T00:00:00'); // clôture le 13 août à minuit

    // Fenêtre Prestation Libre
    const libreDebut = new Date('2026-08-16T00:00:00');
    const libreFin   = new Date('2026-08-27T18:00:00');

    // --- Cartes Solo & Groupe ---
    const cardSolo = document.getElementById('card-solo');
    const cardGroupe = document.getElementById('card-groupe');
    const boutonsSoloGroupe = document.querySelectorAll('.btn-solo-groupe');

    if (maintenant >= soloGroupeFin) {
        // Après le 13 août : on cache complètement les cartes Solo et Groupe
        if (cardSolo) cardSolo.classList.add('hidden');
        if (cardGroupe) cardGroupe.classList.add('hidden');
    } else {
        boutonsSoloGroupe.forEach(function (btn) {
            if (maintenant < soloGroupeDebut) {
                btn.disabled = true;
                btn.textContent = "Inscription à partir du 25 Juin";
                btn.classList.add('opacity-50', 'cursor-not-allowed');
            } else {
                btn.disabled = false;
                btn.textContent = "S'inscrire";
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        });
    }

    // --- Carte Prestation Libre ---
    const btnLibre = document.getElementById('btn-libre');
    if (btnLibre) {
        if (maintenant < libreDebut) {
            btnLibre.disabled = true;
            btnLibre.textContent = "A partir du 16 Août";
            btnLibre.classList.add('opacity-50', 'cursor-not-allowed');
        } else if (maintenant >= libreDebut && maintenant <= libreFin) {
            btnLibre.disabled = false;
            btnLibre.textContent = "S'inscrire";
            btnLibre.classList.remove('opacity-50', 'cursor-not-allowed');
            btnLibre.removeAttribute('data-toggle');
        } else {
            btnLibre.disabled = true;
            btnLibre.textContent = "Inscriptions clôturées";
            btnLibre.classList.add('opacity-50', 'cursor-not-allowed');
            btnLibre.removeAttribute('data-toggle');
            btnLibre.removeAttribute('data-target');
        }
    }
});
    

const selectCategorie = document.getElementById('categorie');
const autreCategorieContainer = document.getElementById('autre-categorie-container');
const autreCategorieInput = document.getElementById('autre_categorie');

if (selectCategorie) {
    selectCategorie.addEventListener('change', function () {
        if (this.value === 'Autre') {
            autreCategorieContainer.classList.remove('hidden');
            autreCategorieInput.setAttribute('required', 'required');
        } else {
            autreCategorieContainer.classList.add('hidden');
            autreCategorieInput.removeAttribute('required');
            autreCategorieInput.value = '';
        }
    });
}

const selectCategorieGroupe = document.getElementById('categorie_groupe');
const autreCategorieGroupeContainer = document.getElementById('autre-categorie-groupe-container');
const autreCategorieGroupeInput = document.getElementById('autre_categorie_groupe');

if (selectCategorieGroupe) {
    selectCategorieGroupe.addEventListener('change', function () {
        if (this.value === 'Autre') {
            autreCategorieGroupeContainer.classList.remove('hidden');
            autreCategorieGroupeInput.setAttribute('required', 'required');
        } else {
            autreCategorieGroupeContainer.classList.add('hidden');
            autreCategorieGroupeInput.removeAttribute('required');
            autreCategorieGroupeInput.value = '';
        }
    });
}

function openModal(id) {
    document.getElementById(id).classList.remove('hidden');
    document.getElementById(id).classList.add('flex');
}

function closeModal(id) {
    document.getElementById(id).classList.add('hidden');
    document.getElementById(id).classList.remove('flex');
}

// Scroll Progress Bar
window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('progressBar').style.width = scrolled + '%';
});

// Hero Background Slider
// Hero Background Slider
const hero = document.getElementById("accueil");

if (hero && hero.dataset.images) {
    const images = JSON.parse(hero.dataset.images);
    let current = 0;

    function loadHeroImage(index) {
        const img = new Image();
        img.onload = function() {
            hero.style.backgroundImage = `url('${images[index]}')`;
        };
        img.src = images[index];
    }

    loadHeroImage(0);

    setInterval(() => {
        current = (current + 1) % images.length;
        loadHeroImage(current);
    }, 6000);
}

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.category-card, .inscription-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});

setTimeout(function() {
    let alerts = document.querySelectorAll('.alert-fill');
    alerts.forEach(function(alert) {
        alert.style.display = 'none';
    });
}, 5000);

document.addEventListener('DOMContentLoaded', function () {
    // Gallery modal functionality
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const closeBtn = document.getElementsByClassName('close')[0];
    const galleryImages = document.querySelectorAll('.gallery-image img');
    
    galleryImages.forEach(img => {
        img.addEventListener('click', function () {
            modal.style.display = 'flex';
            modalImg.src = this.src;
        });
    });
    
    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }
    
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('#tabBar .tab-btn');
    const panels  = document.querySelectorAll('.tab-panel');

    buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const target = btn.dataset.tab;

            // Désactiver tous
            buttons.forEach(function (b) { b.classList.remove('active'); });
            panels.forEach(function (p)  { p.classList.remove('active'); });

            // Activer le bon
            btn.classList.add('active');
            var panel = document.getElementById('tab-' + target);
            if (panel) { panel.classList.add('active'); }
        });
    });
});