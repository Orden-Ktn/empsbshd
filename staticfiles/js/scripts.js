
// Scroll Progress Bar
window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('progressBar').style.width = scrolled + '%';
});

// Gallery Sliders
const slider1 = document.getElementById("gallerySlider1");
const slider2 = document.getElementById("gallerySlider2");
const slides1 = slider1.children;
const slides2 = slider2.children;
let index1 = 0;
let index2 = 0;

function getVisibleSlides() {
    if (window.innerWidth >= 1024) return 3;
    if (window.innerWidth >= 768) return 2;
    return 1;
}

function slideGallery1() {
    const visible = getVisibleSlides();
    const maxIndex = slides1.length - visible;
    index1 = index1 >= maxIndex ? 0 : index1 + 1;
    slider1.style.transform = `translateX(-${index1 * (100 / visible)}%)`;
}

function slideGallery2() {
    const visible = getVisibleSlides();
    const maxIndex = slides2.length - visible;
    index2 = index2 >= maxIndex ? 0 : index2 + 1;
    slider2.style.transform = `translateX(-${index2 * (100 / visible)}%)`;
}

// Défilement alterné pour un effet plus dynamique

setInterval(slideGallery1, 4000);
setInterval(slideGallery2, 4500); // Légèrement différent pour créer un mouvement distinct

window.addEventListener("resize", () => { 
    index1 = 0; 
    index2 = 0;
    slider1.style.transform = 'translateX(0)';
    slider2.style.transform = 'translateX(0)';
});

// Hero Background Slider
const hero = document.getElementById("accueil");
const images = JSON.parse(hero.dataset.images);
let current = 0;

// Fonction pour charger l'image
function loadHeroImage(index) {
    const img = new Image();
    img.onload = function() {
        hero.style.backgroundImage = `url('${images[index]}')`;
    };
    img.src = images[index];
}

// Charger la première image
loadHeroImage(0);

// Rotation automatique des images
setInterval(() => {
    current = (current + 1) % images.length;
    loadHeroImage(current);
}, 6000);

// Modal for Gallery
const modal = document.getElementById("imageModal");
const modalImg = document.getElementById("modalImage");
const galleryItems = document.querySelectorAll(".gallery-item img");
const closeBtn = document.querySelector(".close");

galleryItems.forEach(img => {
    img.addEventListener("click", function() {
        modal.style.display = "flex";
        modal.style.alignItems = "center";
        modal.style.justifyContent = "center";
        modalImg.src = this.src;
    });
});

closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});

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

document.querySelectorAll('.group-card, .activity-card, .team-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});
