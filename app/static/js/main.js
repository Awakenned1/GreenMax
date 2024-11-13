document.addEventListener('DOMContentLoaded', function() {
    // Initialize Particles.js
    if (document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            particles: {
                number: {
                    value: 80,
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    value: '#FF69B4'
                },
                shape: {
                    type: 'circle'
                },
                opacity: {
                    value: 0.5,
                    random: false
                },
                size: {
                    value: 3,
                    random: true
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#FF69B4',
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: 'none',
                    random: false,
                    straight: false,
                    out_mode: 'out',
                    bounce: false
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: {
                        enable: true,
                        mode: 'grab'
                    },
                    onclick: {
                        enable: true,
                        mode: 'push'
                    },
                    resize: true
                }
            },
            retina_detect: true
        });
    }

    // Animate stats numbers
    const stats = document.querySelectorAll('.stat-number[data-target]');
    stats.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        const increment = target / 50;
        let current = 0;

        const updateCount = () => {
            if (current < target) {
                current += increment;
                stat.textContent = Math.ceil(current);
                setTimeout(updateCount, 30);
            } else {
                stat.textContent = target;
            }
        };

        // Start animation when element is in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCount();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(stat);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Animate elements on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.feature-card, .impact-card, .testimonial-card');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            const isVisible = elementTop < window.innerHeight && elementBottom >= 0;

            if (isVisible) {
                element.classList.add('animate');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check

    // GSAP Animations
    gsap.from('.hero-badge', {
        duration: 1,
        y: -50,
        opacity: 0,
        ease: 'power3.out'
    });

    gsap.from('.hero h1', {
        duration: 1.2,
        y: 30,
        opacity: 0,
        ease: 'power3.out',
        delay: 0.3
    });

    gsap.from('.hero-subtitle', {
        duration: 1.2,
        y: 30,
        opacity: 0,
        ease: 'power3.out',
        delay: 0.5
    });

    gsap.from('.cta-buttons', {
        duration: 1,
        y: 30,
        opacity: 0,
        ease: 'power3.out',
        delay: 0.7
    });

    // Feature cards hover effect
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                duration: 0.3,
                y: -10,
                scale: 1.02,
                boxShadow: '0 20px 30px rgba(0, 0, 0, 0.1)'
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                duration: 0.3,
                y: 0,
                scale: 1,
                boxShadow: '0 10px 20px rgba(0, 0, 0, 0.1)'
            });
        });
    });

    // Testimonial slider animation
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    let currentCard = 0;

    const showNextTestimonial = () => {
        gsap.to(testimonialCards[currentCard], {
            duration: 0.5,
            opacity: 0,
            x: -50,
            onComplete: () => {
                testimonialCards[currentCard].style.display = 'none';
                currentCard = (currentCard + 1) % testimonialCards.length;
                testimonialCards[currentCard].style.display = 'block';
                gsap.fromTo(testimonialCards[currentCard], 
                    { opacity: 0, x: 50 },
                    { duration: 0.5, opacity: 1, x: 0 }
                );
            }
        });
    };

    if (testimonialCards.length > 1) {
        setInterval(showNextTestimonial, 5000);
    }
});
