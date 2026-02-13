// Mobile Menu Toggle - Updated
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');
const body = document.body;

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        navMenu.classList.toggle('active');
        
        // Toggle icon
        const icon = this.querySelector('i');
        if (icon) {
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
                body.classList.add('menu-open'); // Prevent scrolling when menu is open
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
                body.classList.remove('menu-open');
            }
        }
    });
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function() {
        if (window.innerWidth <= 992) {
            navMenu.classList.remove('active');
            const icon = mobileMenuBtn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
            body.classList.remove('menu-open');
        }
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    if (window.innerWidth <= 992) {
        if (!navMenu.contains(event.target) && !mobileMenuBtn.contains(event.target)) {
            navMenu.classList.remove('active');
            const icon = mobileMenuBtn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
            body.classList.remove('menu-open');
        }
    }
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 992) {
        // Desktop view - hide mobile menu and reset
        navMenu.classList.remove('active');
        const icon = mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
        body.classList.remove('menu-open');
        
        // Remove inline styles
        navMenu.style.transform = '';
        navMenu.style.opacity = '';
        navMenu.style.visibility = '';
    }
});

// Fix for Book Now button - ensure it's clickable
document.addEventListener('DOMContentLoaded', function() {
    // Ensure the floating card button is clickable
    const cardCta = document.querySelector('.card-cta');
    if (cardCta) {
        cardCta.addEventListener('click', function(e) {
            e.preventDefault();
            openBookingModal();
        });
    }
    
    // Ensure hero button is clickable
    const heroBtn = document.querySelector('.btn-primary');
    if (heroBtn) {
        heroBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openBookingModal();
        });
    }
});

// Modal Functions
const bookingModal = document.getElementById('bookingModal');
const contactForm = document.getElementById('contactForm');
const bookingForm = document.getElementById('bookingForm');

function openBookingModal(service = '') {
    if (service && document.getElementById('bookingService')) {
        document.getElementById('bookingService').value = service;
    }
    bookingModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeBookingModal() {
    bookingModal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
bookingModal.addEventListener('click', (e) => {
    if (e.target === bookingModal) {
        closeBookingModal();
    }
});

// Toast Notification
const toast = document.getElementById('successToast');
const toastMessage = document.getElementById('toastMessage');

function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 5000);
}

// Contact Form Submission
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            service: document.getElementById('service').value,
            message: document.getElementById('message').value
        };
        
        try {
            const response = await fetch('/submit_contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showToast(result.message);
                contactForm.reset();
                closeBookingModal();
            } else {
                showToast(result.message, 'error');
            }
        } catch (error) {
            showToast('Network error. Please try again.', 'error');
            console.error('Error:', error);
        }
    });
}

// Booking Form Submission
if (bookingForm) {
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('bookingName').value,
            email: document.getElementById('bookingEmail').value,
            phone: document.getElementById('bookingPhone').value,
            service: document.getElementById('bookingService').value,
            date: document.getElementById('bookingDate').value
        };
        
        // Validate date is in future
        const selectedDate = new Date(formData.date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            showToast('Please select a future date', 'error');
            return;
        }
        
        try {
            const response = await fetch('/book_consultation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showToast(result.message);
                bookingForm.reset();
                closeBookingModal();
            } else {
                showToast(result.message, 'error');
            }
        } catch (error) {
            showToast('Network error. Please try again.', 'error');
            console.error('Error:', error);
        }
    });
}

// Newsletter Subscription
function subscribeNewsletter() {
    const email = document.getElementById('newsletterEmail').value;
    
    if (!email || !email.includes('@')) {
        showToast('Please enter a valid email address', 'error');
        return;
    }
    
    // In a real application, you would send this to your server
    console.log('Newsletter subscription:', email);
    showToast('Thank you for subscribing to our newsletter!');
    document.getElementById('newsletterEmail').value = '';
}

// Set minimum date for booking to today
window.addEventListener('load', () => {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('bookingDate');
    if (dateInput) {
        dateInput.min = today;
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                e.preventDefault();
                const targetElement = document.querySelector(href);
                
                if (targetElement) {
                    const headerOffset = 80;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Add hover effects to service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
    
    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.service-card, .partner-card, .feature').forEach(el => {
        observer.observe(el);
    });
});

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\+]?[1-9][\d]{0,15}$/;
    return re.test(phone.replace(/[\s\-\(\)\.]/g, ''));
}

// Add input validation
document.addEventListener('input', (e) => {
    if (e.target.type === 'email') {
        if (e.target.value && !validateEmail(e.target.value)) {
            e.target.style.borderColor = 'var(--vibrant-red)';
        } else {
            e.target.style.borderColor = 'var(--medium-gray)';
        }
    }
    
    if (e.target.type === 'tel') {
        if (e.target.value && !validatePhone(e.target.value)) {
            e.target.style.borderColor = 'var(--vibrant-red)';
        } else {
            e.target.style.borderColor = 'var(--medium-gray)';
        }
    }
});

// ==================== CAROUSEL FUNCTIONS ====================

// Carousel variables
let currentSlide = 0;
let slideInterval;
const slides = document.querySelectorAll('.carousel-slide');
const indicators = document.querySelectorAll('.indicator');
const totalSlides = slides.length;

// Initialize carousel
function initCarousel() {
    if (slides.length === 0) return;
    
    // Show first slide
    showSlide(currentSlide);
    
    // Start auto-slide
    startAutoSlide();
    
    // Add hover pause
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', pauseAutoSlide);
        carouselContainer.addEventListener('mouseleave', startAutoSlide);
    }
}

// Show specific slide
function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => {
        slide.classList.remove('active');
        slide.style.opacity = '0';
        slide.style.transform = 'translateX(100%)';
    });
    
    // Remove active class from all indicators
    indicators.forEach(indicator => {
        indicator.classList.remove('active');
    });
    
    // Show current slide with animation
    currentSlide = (index + totalSlides) % totalSlides;
    
    slides[currentSlide].classList.add('active');
    slides[currentSlide].style.opacity = '1';
    slides[currentSlide].style.transform = 'translateX(0)';
    
    // Update indicator
    if (indicators[currentSlide]) {
        indicators[currentSlide].classList.add('active');
    }
    
    // Animate previous slide out
    const prevIndex = (currentSlide - 1 + totalSlides) % totalSlides;
    if (slides[prevIndex]) {
        slides[prevIndex].style.transform = 'translateX(-100%)';
    }
}

// Next slide
function nextSlide() {
    showSlide(currentSlide + 1);
    restartAutoSlide();
}

// Previous slide
function prevSlide() {
    showSlide(currentSlide - 1);
    restartAutoSlide();
}

// Go to specific slide
function goToSlide(index) {
    showSlide(index);
    restartAutoSlide();
}

// Start auto slide
function startAutoSlide() {
    if (slideInterval) {
        clearInterval(slideInterval);
    }
    
    slideInterval = setInterval(() => {
        nextSlide();
    }, 5000); // Change slide every 5 seconds
}

// Pause auto slide
function pauseAutoSlide() {
    if (slideInterval) {
        clearInterval(slideInterval);
        slideInterval = null;
    }
}

// Restart auto slide
function restartAutoSlide() {
    pauseAutoSlide();
    startAutoSlide();
}

// Add keyboard navigation
function addKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            prevSlide();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
        }
    });
}

// Add touch/swipe support for mobile
function addTouchSupport() {
    const carousel = document.querySelector('.carousel');
    if (!carousel) return;
    
    let startX = 0;
    let endX = 0;
    const threshold = 50; // Minimum swipe distance
    
    carousel.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        pauseAutoSlide();
    });
    
    carousel.addEventListener('touchmove', (e) => {
        endX = e.touches[0].clientX;
    });
    
    carousel.addEventListener('touchend', () => {
        const diff = startX - endX;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                // Swipe left - next slide
                nextSlide();
            } else {
                // Swipe right - previous slide
                prevSlide();
            }
        }
        
        startAutoSlide();
    });
}

// Add progress bar for auto-slide
function addProgressBar() {
    // Remove existing progress bar if any
    const existingProgress = document.querySelector('.slide-progress');
    if (existingProgress) {
        existingProgress.remove();
    }
    
    // Create progress bar container
    const progressContainer = document.createElement('div');
    progressContainer.className = 'slide-progress-container';
    progressContainer.style.cssText = `
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 0 0 var(--radius-xl) var(--radius-xl);
        overflow: hidden;
    `;
    
    // Create progress bar
    const progressBar = document.createElement('div');
    progressBar.className = 'slide-progress';
    progressBar.style.cssText = `
        height: 100%;
        width: 100%;
        background: var(--vibrant-red);
        transform: translateX(-100%);
        transition: transform 5s linear;
    `;
    
    progressContainer.appendChild(progressBar);
    
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.appendChild(progressContainer);
        
        // Restart progress bar animation on slide change
        const restartProgress = () => {
            progressBar.style.transition = 'none';
            progressBar.style.transform = 'translateX(-100%)';
            
            // Force reflow
            progressBar.offsetHeight;
            
            progressBar.style.transition = 'transform 5s linear';
            progressBar.style.transform = 'translateX(0)';
        };
        
        // Start progress bar
        setTimeout(restartProgress, 100);
        
        // Restart on slide change
        const observer = new MutationObserver(() => {
            if (progressBar.style.transform === 'translateX(0)') {
                restartProgress();
            }
        });
        
        observer.observe(progressBar, { attributes: true, attributeFilter: ['style'] });
    }
}

// Initialize carousel when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Wonderland Educational Consultancy Website loaded successfully!');
    
    // Add current year to footer
    const yearSpan = document.getElementById('currentYear');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
    
    // Initialize carousel
    initCarousel();
    addKeyboardNavigation();
    addTouchSupport();
    addProgressBar();
    
    // Pause auto-slide when modal is open
    const bookingModal = document.getElementById('bookingModal');
    if (bookingModal) {
        bookingModal.addEventListener('mouseenter', pauseAutoSlide);
        bookingModal.addEventListener('mouseleave', startAutoSlide);
    }
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    pauseAutoSlide();
});

// ==================== ENHANCED CAROUSEL FUNCTIONS ====================

// Toggle auto slide play/pause
function toggleAutoSlide() {
    const playPauseBtn = document.querySelector('.play-pause-btn');
    const icon = playPauseBtn.querySelector('i');
    
    if (slideInterval) {
        pauseAutoSlide();
        icon.classList.remove('fa-pause');
        icon.classList.add('fa-play');
        playPauseBtn.title = 'Play';
    } else {
        startAutoSlide();
        icon.classList.remove('fa-play');
        icon.classList.add('fa-pause');
        playPauseBtn.title = 'Pause';
    }
}

// Update slide counter
function updateSlideCounter() {
    const slideCounter = document.getElementById('slideCounter');
    if (slideCounter) {
        slideCounter.textContent = `${currentSlide + 1} / ${totalSlides}`;
    }
}

// Enhanced showSlide function
function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => {
        slide.classList.remove('active');
        slide.style.opacity = '0';
        slide.style.transform = 'translateX(100%)';
    });
    
    // Remove active class from all indicators
    indicators.forEach(indicator => {
        indicator.classList.remove('active');
    });
    
    // Calculate new slide index
    currentSlide = (index + totalSlides) % totalSlides;
    
    // Show current slide with animation
    const currentSlideElement = slides[currentSlide];
    currentSlideElement.classList.add('active');
    currentSlideElement.style.opacity = '1';
    currentSlideElement.style.transform = 'translateX(0)';
    
    // Animate out previous slide
    const prevIndex = (currentSlide - 1 + totalSlides) % totalSlides;
    if (slides[prevIndex]) {
        slides[prevIndex].style.transform = 'translateX(-100%)';
    }
    
    // Update indicator
    if (indicators[currentSlide]) {
        indicators[currentSlide].classList.add('active');
    }
    
    // Update slide counter
    updateSlideCounter();
    
    // Reset progress bar
    resetProgressBar();
}

// Reset progress bar animation
function resetProgressBar() {
    const progressBar = document.querySelector('.slide-progress');
    if (progressBar) {
        // Reset animation
        progressBar.style.transition = 'none';
        progressBar.style.transform = 'translateX(-100%)';
        
        // Force reflow
        progressBar.offsetHeight;
        
        // Restart animation
        progressBar.style.transition = 'transform 5s linear';
        progressBar.style.transform = 'translateX(0)';
    }
}

// Initialize enhanced carousel
function initCarousel() {
    if (slides.length === 0) return;
    
    // Show first slide
    showSlide(0);
    
    // Start auto-slide
    startAutoSlide();
    
    // Add hover pause
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', () => {
            pauseAutoSlide();
            // Show pause icon when hovering
            const playPauseBtn = document.querySelector('.play-pause-btn');
            if (playPauseBtn) {
                const icon = playPauseBtn.querySelector('i');
                if (slideInterval) {
                    icon.classList.remove('fa-pause');
                    icon.classList.add('fa-play');
                }
            }
        });
        
        carouselContainer.addEventListener('mouseleave', () => {
            const playPauseBtn = document.querySelector('.play-pause-btn');
            if (playPauseBtn) {
                const icon = playPauseBtn.querySelector('i');
                // Only restart if it was playing before hover
                if (icon.classList.contains('fa-play') && !slideInterval) {
                    startAutoSlide();
                    icon.classList.remove('fa-play');
                    icon.classList.add('fa-pause');
                }
            }
        });
    }
}

// Update DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', () => {
    console.log('Wonderland Educational Consultancy Website loaded successfully!');
    
    // Add current year to footer
    const yearSpan = document.getElementById('currentYear');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
    
    // Initialize enhanced carousel
    initCarousel();
    addKeyboardNavigation();
    addTouchSupport();
    addProgressBar();
    
    // Initialize slide counter
    updateSlideCounter();
    
    // Pause auto-slide when modal is open
    const bookingModal = document.getElementById('bookingModal');
    if (bookingModal) {
        bookingModal.addEventListener('mouseenter', () => {
            pauseAutoSlide();
            const playPauseBtn = document.querySelector('.play-pause-btn');
            if (playPauseBtn && slideInterval) {
                const icon = playPauseBtn.querySelector('i');
                icon.classList.remove('fa-pause');
                icon.classList.add('fa-play');
            }
        });
        
        bookingModal.addEventListener('mouseleave', () => {
            const playPauseBtn = document.querySelector('.play-pause-btn');
            if (playPauseBtn) {
                const icon = playPauseBtn.querySelector('i');
                if (icon.classList.contains('fa-play')) {
                    startAutoSlide();
                    icon.classList.remove('fa-play');
                    icon.classList.add('fa-pause');
                }
            }
        });
    }
});