// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initHeader();
    renderProductCategories();
    renderFeaturedProjects();
    renderValuePropositions();
    renderProcessSteps();
    renderClientLogos();
    setCurrentYear();
    initSmoothScroll();
    initBackToTop();
});

// Header scroll effect
function initHeader() {
    const header = document.getElementById('header');
    const navbar = header.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 10) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Render Product Categories
function renderProductCategories() {
    const container = document.getElementById('productCategories');
    
    PRODUCT_CATEGORIES.forEach(category => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-3';
        
        col.innerHTML = `
            <div class="category-card position-relative overflow-hidden rounded shadow-lg">
                <img src="${category.image}" alt="${category.name}" class="img-fluid category-image">
                <div class="category-overlay position-absolute top-0 start-0 w-100 h-100"></div>
                <div class="category-title position-absolute top-50 start-50 translate-middle text-white">
                    <h4 class="fw-bold">${category.name}</h4>
                </div>
            </div>
        `;
        
        container.appendChild(col);
    });
}

// Render Featured Projects with Swiper
function renderFeaturedProjects() {
    const container = document.getElementById('projectsSlider');
    
    FEATURED_PROJECTS.forEach(project => {
        const slide = document.createElement('div');
        slide.className = 'swiper-slide';
        
        slide.innerHTML = `
            <div class="project-card position-relative overflow-hidden rounded shadow-lg">
                <img src="${project.image}" alt="${project.title}" class="img-fluid project-image">
                <div class="project-gradient position-absolute bottom-0 start-0 w-100"></div>
                <div class="project-content position-absolute bottom-0 start-0 p-4 text-white w-100">
                    <h4 class="fw-bold mb-2">${project.title}</h4>
                    <p class="project-description small mb-0">${project.description}</p>
                </div>
            </div>
        `;
        
        container.appendChild(slide);
    });
    
    // Initialize Swiper
    new Swiper('.projectsSwiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            768: {
                slidesPerView: 2,
            },
            1024: {
                slidesPerView: 3,
            }
        }
    });
}

// Render Value Propositions
function renderValuePropositions() {
    const container = document.getElementById('valuePropositions');
    
    VALUE_PROPOSITIONS.forEach(prop => {
        const col = document.createElement('div');
        col.className = 'col-md-4';
        
        col.innerHTML = `
            <div class="value-card p-4 border rounded h-100 text-center">
                <div class="mb-3">
                    ${prop.icon}
                </div>
                <h4 class="h5 fw-semibold mb-3">${prop.title}</h4>
                <p class="text-muted">${prop.description}</p>
            </div>
        `;
        
        container.appendChild(col);
    });
}

// Render Process Steps
function renderProcessSteps() {
    const container = document.getElementById('processSteps');
    
    OUR_PROCESS_STEPS.forEach(step => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-3';
        
        col.innerHTML = `
            <div class="process-card position-relative bg-secondary p-4 rounded shadow h-100">
                <div class="process-number position-absolute bg-amber text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
                    ${step.step}
                </div>
                <h4 class="h5 fw-semibold mb-3 mt-4">${step.title}</h4>
                <p class="text-light small">${step.description}</p>
            </div>
        `;
        
        container.appendChild(col);
    });
}

// Render Client Logos
function renderClientLogos() {
    const container = document.getElementById('clientLogos');
    
    CLIENT_LOGOS.forEach((logoUrl, index) => {
        const logoDiv = document.createElement('div');
        logoDiv.className = 'client-logo';
        
        logoDiv.innerHTML = `
            <img src="${logoUrl}" alt="Client Logo ${index + 1}" class="img-fluid">
        `;
        
        container.appendChild(logoDiv);
    });
}

// Set current year in footer
function setCurrentYear() {
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Don't prevent default for # only (used for non-functional links)
            if (href === '#') return;
            
            e.preventDefault();
            
            const target = document.querySelector(href);
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            }
        });
    });
}

// Back to Top Button functionality
function initBackToTop() {
    // Create the back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.id = 'backToTop';
    backToTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopBtn.setAttribute('aria-label', 'Back to top');
    backToTopBtn.setAttribute('title', 'Back to top');
    document.body.appendChild(backToTopBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    // Scroll to top when button is clicked
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}