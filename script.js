/* ===== PDF AI TOOL - ENHANCED INTERACTIONS ===== */
(function() {
  'use strict';

  /* ===== GSAP SETUP ===== */
  gsap.registerPlugin(ScrollTrigger);

  /* ===== THEME SYSTEM ===== */
  const ThemeManager = {
    STORAGE_KEY: 'pdf-ai-tool-theme',

    init() {
      // Check localStorage first
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (stored) {
        document.documentElement.setAttribute('data-theme', stored);
        return;
      }
      // Otherwise rely on CSS media query (prefers-color-scheme)
    },

    toggle() {
      const html = document.documentElement;
      const isDark = html.getAttribute('data-theme') === 'dark' ||
                     (!html.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);

      const newTheme = isDark ? 'light' : 'dark';
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem(this.STORAGE_KEY, newTheme);
    },

    setupToggle() {
      const toggle = document.getElementById('theme-toggle');
      if (toggle) {
        toggle.addEventListener('click', () => this.toggle());
      }

      // Listen for system theme changes
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem(this.STORAGE_KEY)) {
          // Only auto-switch if user hasn't set a preference
          document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
        }
      });
    }
  };

  /* ===== HERO ANIMATIONS ===== */
  function initHeroAnimations() {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    tl.to('.hero-badge', {
      opacity: 1,
      y: 0,
      duration: 0.6,
      delay: 0.3
    })
    .to('.hero-title', {
      opacity: 1,
      y: 0,
      duration: 0.8
    }, '-=0.3')
    .to('.hero-subtitle', {
      opacity: 1,
      y: 0,
      duration: 0.6
    }, '-=0.5')
    .to('.hero-actions', {
      opacity: 1,
      y: 0,
      duration: 0.6
    }, '-=0.4')
    .to('.hero-meta', {
      opacity: 1,
      y: 0,
      duration: 0.6
    }, '-=0.4')
    .to('.hero-visual', {
      opacity: 1,
      scale: 1,
      duration: 0.8,
      ease: 'back.out(1.2)'
    }, '-=0.6')
    .from('.scroll-indicator', {
      opacity: 0,
      y: -20,
      duration: 0.5
    }, '-=0.3');
  }

  /* ===== SCROLL-TRIGGERED ANIMATIONS ===== */
  function initScrollAnimations() {
    // Section headers
    gsap.utils.toArray('[data-animate="section-title"]').forEach(el => {
      gsap.fromTo(el,
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    gsap.utils.toArray('[data-animate="section-desc"]').forEach(el => {
      gsap.fromTo(el,
        { opacity: 0, y: 20 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          delay: 0.1,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    // Feature cards - staggered
    gsap.utils.toArray('.feature-card').forEach((card, i) => {
      gsap.fromTo(card,
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          delay: i * 0.1,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: '.features-grid',
            start: 'top 80%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    // Screenshots - staggered from right
    gsap.utils.toArray('.screenshot-item').forEach((item, i) => {
      gsap.fromTo(item,
        { opacity: 0, x: 40 },
        {
          opacity: 1,
          x: 0,
          duration: 0.7,
          delay: i * 0.15,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: '.screenshots-grid',
            start: 'top 80%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    // FAQ items
    gsap.utils.toArray('.faq-item').forEach((item, i) => {
      gsap.fromTo(item,
        { opacity: 0, y: 20 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          delay: i * 0.08,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: '.faq-list',
            start: 'top 80%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    // CTA section
    gsap.fromTo('.cta-title',
      { opacity: 0, y: 30 },
      {
        opacity: 1,
        y: 0,
        duration: 0.6,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 80%',
          toggleActions: 'play none none none'
        }
      }
    );

    gsap.fromTo('.cta-desc',
      { opacity: 0, y: 30 },
      {
        opacity: 1,
        y: 0,
        duration: 0.6,
        delay: 0.1,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 80%',
          toggleActions: 'play none none none'
        }
      }
    );

    gsap.fromTo('.btn-cta',
      { opacity: 0, y: 30 },
      {
        opacity: 1,
        y: 0,
        duration: 0.6,
        delay: 0.2,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 80%',
          toggleActions: 'play none none none'
        }
      }
    );
  }

  /* ===== FAQ ACCORDION ===== */
  function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
      const question = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');

      if (!question || !answer) return;

      question.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');

        // Close all other items
        faqItems.forEach(otherItem => {
          if (otherItem !== item && otherItem.classList.contains('open')) {
            otherItem.classList.remove('open');
            otherItem.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
            // Reset height via GSAP
            gsap.to(otherItem.querySelector('.faq-answer'), {
              maxHeight: '0',
              duration: 0.3,
              ease: 'power2.inOut'
            });
          }
        });

        // Toggle current item
        if (isOpen) {
          item.classList.remove('open');
          question.setAttribute('aria-expanded', 'false');
          gsap.to(answer, {
            maxHeight: '0',
            duration: 0.3,
            ease: 'power2.inOut'
          });
        } else {
          item.classList.add('open');
          question.setAttribute('aria-expanded', 'true');
          gsap.fromTo(answer,
            { maxHeight: '0' },
            {
              maxHeight: '200px',
              duration: 0.35,
              ease: 'power2.inOut'
            }
          );
        }
      });
    });
  }

  /* ===== DOWNLOAD MODAL ===== */
  function initModal() {
    const modal = document.getElementById('download-modal');
    const modalClose = document.getElementById('modal-close');
    const modalOverlay = modal;

    // Open modal
    document.querySelectorAll('.btn-download, [data-target="download-modal"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    // Close modal
    if (modalClose) {
      modalClose.addEventListener('click', closeModal);
    }

    // Close on backdrop click
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        closeModal();
      }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modalOverlay.classList.contains('open')) {
        closeModal();
      }
    });

    function openModal() {
      modalOverlay.classList.add('open');
      document.body.classList.add('modal-open');

      // GSAP animation
      gsap.fromTo('.modal',
        { y: 60, scale: 0.92, opacity: 0 },
        {
          y: 0,
          scale: 1,
          opacity: 1,
          duration: 0.4,
          ease: 'back.out(1.2)'
        }
      );

      gsap.fromTo(modalOverlay,
        { opacity: 0 },
        {
          opacity: 1,
          duration: 0.25,
          ease: 'power2.out'
        }
      );

      // Focus trap
      modalOverlay.querySelector('.modal').focus();
    }

    function closeModal() {
      gsap.to(modalOverlay, {
        opacity: 0,
        duration: 0.2,
        ease: 'power2.in',
        onComplete: () => {
          modalOverlay.classList.remove('open');
          document.body.classList.remove('modal-open');
        }
      });

      gsap.to('.modal', {
        y: 40,
        scale: 0.95,
        opacity: 0,
        duration: 0.2,
        ease: 'power2.in'
      });
    }
  }

  /* ===== SMOOTH SCROLL ===== */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        if (targetId === '#') return;

        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          const headerOffset = 80;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  /* ===== PARALLAX EFFECTS ===== */
  function initParallax() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    // Hero shapes parallax
    gsap.to('.shape-1', {
      y: -60,
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: 1
      }
    });

    gsap.to('.shape-2', {
      y: -30,
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: 1.5
      }
    });

    gsap.to('.shape-3', {
      y: -80,
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: 2
      }
    });
  }

  /* ===== SCROLL REVEAL FOR STICKY HEADER ===== */
  function initScrollReveal() {
    let lastScroll = 0;
    const hero = document.querySelector('.hero');

    window.addEventListener('scroll', () => {
      const currentScroll = window.pageYOffset;

      // Add/remove class based on scroll position for header styling
      if (currentScroll > 100) {
        document.body.classList.add('scrolled');
      } else {
        document.body.classList.remove('scrolled');
      }

      lastScroll = currentScroll;
    }, { passive: true });
  }

  /* ===== DOWNLOAD BUTTON ANALYTICS (placeholder) ===== */
  function initDownloadTracking() {
    const downloadBtn = document.getElementById('download-btn');
    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => {
        // Track download event (placeholder for analytics)
        console.log('Download button clicked');
      });
    }
  }

  /* ===== INITIALIZE ===== */
  function init() {
    // Initialize theme system
    ThemeManager.init();
    ThemeManager.setupToggle();

    // Initialize animations
    initHeroAnimations();
    initScrollAnimations();

    // Initialize components
    initFAQ();
    initModal();
    initSmoothScroll();
    initParallax();
    initScrollReveal();
    initDownloadTracking();

    // Refresh ScrollTrigger after images load
    window.addEventListener('load', () => {
      ScrollTrigger.refresh();
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
