/* ===== PDF AI TOOL - REDESIGNED JS with PROGRESSIVE ENHANCEMENT =====

   KEY PRINCIPLES:
   1. Content is ALWAYS visible (CSS-first)
   2. JS only ENHANCES animations, never required
   3. If GSAP fails, CSS animations still work
   4. Graceful degradation - page works without JS

   ============================================================ */
(function() {
  'use strict';

  /* ===== CHECK GSAP AVAILABILITY ===== */
  var gsapAvailable = typeof gsap !== 'undefined' && gsap;

  if (gsapAvailable) {
    // GSAP loaded successfully - enable enhanced animations
    document.documentElement.classList.add('js-enabled');
    gsap.registerPlugin(ScrollTrigger);

    /* ===== 1. HERO PAGE LOAD ANIMATIONS (ENHANCED) ===== */
    function initHeroAnimations() {
      var heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } });

      heroTl
        .from('.hero-badge', {
          opacity: 0,
          y: 30,
          scale: 0.9,
          duration: 0.8
        })
        .from('.hero-title .title-line', {
          opacity: 0,
          y: 60,
          stagger: 0.15,
          duration: 1
        }, '-=0.4')
        .from('.hero-subtitle', {
          opacity: 0,
          y: 30,
          duration: 0.8
        }, '-=0.5')
        .from('.hero-actions .btn', {
          opacity: 0,
          y: 20,
          stagger: 0.1,
          duration: 0.6
        }, '-=0.4')
        .from('.hero-meta', {
          opacity: 0,
          duration: 0.6
        }, '-=0.3')
        .from('.hero-screenshot', {
          opacity: 0,
          x: 80,
          scale: 0.95,
          duration: 1.2
        }, '-=1');

      // Scroll indicator - wheel bounce animation
      gsap.to('.scroll-wheel', {
        y: 8,
        duration: 0.8,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
      });

      // Scroll indicator fade out on scroll
      ScrollTrigger.create({
        trigger: '.hero',
        start: 'top top',
        end: '+=200',
        onUpdate: function(self) {
          gsap.to('.scroll-indicator', {
            opacity: 1 - self.progress,
            y: self.progress * 20,
            duration: 0.1
          });
        }
      });
    }

    /* ===== 2. SECTION HEADER ANIMATIONS ===== */
    function initSectionAnimations() {
      gsap.utils.toArray('.section-header').forEach(function(section) {
        gsap.from(section.querySelector('.section-tag'), {
          scrollTrigger: {
            trigger: section,
            start: 'top 80%'
          },
          opacity: 0,
          y: 20,
          duration: 0.6
        });

        gsap.from(section.querySelector('.section-title'), {
          scrollTrigger: {
            trigger: section,
            start: 'top 75%'
          },
          opacity: 0,
          y: 40,
          duration: 0.8,
          ease: 'power3.out'
        });

        gsap.from(section.querySelector('.section-desc'), {
          scrollTrigger: {
            trigger: section,
            start: 'top 70%'
          },
          opacity: 0,
          y: 30,
          duration: 0.6,
          delay: 0.15
        });
      });
    }

    /* ===== 3. FEATURE CARDS - STAGGERED ENTRY ===== */
    function initFeatureAnimations() {
      gsap.from('.feature-card', {
        scrollTrigger: {
          trigger: '.features-grid',
          start: 'top 75%'
        },
        opacity: 0,
        y: 60,
        stagger: 0.12,
        duration: 0.8,
        ease: 'back.out(1.4)'
      });
    }

    /* ===== 4. SCREENSHOTS - HORIZONTAL SCROLL (PIN + SCRUB) ===== */
    function initScreenshotsAnimation() {
      // Only on desktop
      if (window.innerWidth <= 1024) return;

      var screenshotWrapper = document.querySelector('.screenshots-grid');
      if (!screenshotWrapper) return;

      gsap.to(screenshotWrapper, {
        x: function() {
          return -(screenshotWrapper.scrollWidth - window.innerWidth + 200);
        },
        ease: 'none',
        scrollTrigger: {
          trigger: '.screenshots',
          start: 'top top',
          end: function() {
            return '+=' + (screenshotWrapper.scrollWidth - window.innerWidth + 200);
          },
          pin: true,
          scrub: 1,
          anticipatePin: 1,
          invalidateOnRefresh: true
        }
      });
    }

    /* ===== 5. FAQ ACCORDION ANIMATIONS ===== */
    function initFAQ() {
      document.querySelectorAll('.faq-item').forEach(function(item) {
        var question = item.querySelector('.faq-question');
        var answer = item.querySelector('.faq-answer');
        var icon = item.querySelector('.faq-icon');

        // Initial: closed state
        gsap.set(answer, { height: 0, overflow: 'hidden' });
        gsap.set(icon, { rotation: 0 });

        question.addEventListener('click', function() {
          var isOpen = item.classList.contains('open');

          // Close all other items
          document.querySelectorAll('.faq-item.open').forEach(function(openItem) {
            if (openItem !== item) {
              openItem.classList.remove('open');
              gsap.to(openItem.querySelector('.faq-answer'), {
                height: 0,
                duration: 0.4,
                ease: 'power2.inOut'
              });
              gsap.to(openItem.querySelector('.faq-icon'), {
                rotation: 0,
                duration: 0.3
              });
            }
          });

          if (!isOpen) {
            item.classList.add('open');
            gsap.to(answer, {
              height: 'auto',
              duration: 0.5,
              ease: 'power2.out'
            });
            gsap.to(icon, {
              rotation: 45,
              duration: 0.4,
              ease: 'back.out(2)'
            });
          } else {
            item.classList.remove('open');
            gsap.to(answer, {
              height: 0,
              duration: 0.4,
              ease: 'power2.inOut'
            });
            gsap.to(icon, {
              rotation: 0,
              duration: 0.3
            });
          }
        });
      });
    }

    /* ===== 6. CTA SECTION ANIMATION ===== */
    function initCTAAnimations() {
      var ctaTl = gsap.timeline({
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 70%'
        }
      });

      ctaTl
        .from('.cta-title', {
          opacity: 0,
          y: 40,
          duration: 1,
          ease: 'power3.out'
        })
        .from('.cta-desc', {
          opacity: 0,
          y: 30,
          duration: 0.6
        }, '-=0.5')
        .from('.btn-cta', {
          opacity: 0,
          scale: 0.8,
          duration: 0.8,
          ease: 'back.out(1.7)'
        }, '-=0.3');

      // Pulse breathing animation (infinite loop)
      gsap.to('.btn-cta', {
        scale: 1.03,
        duration: 1.2,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
      });
    }

    /* ===== 7. PARALLAX SCROLLING ===== */
    function initParallax() {
      // Hero background shapes parallax
      gsap.to('.shape-1', {
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 1.5
        },
        y: -120,
        scale: 1.1,
        ease: 'none'
      });

      gsap.to('.shape-2', {
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 2
        },
        y: -200,
        rotation: 15,
        ease: 'none'
      });

      gsap.to('.hero-grid-overlay', {
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 0.5
        },
        opacity: 0,
        ease: 'none'
      });

      gsap.to('.hero-screenshot', {
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 1.5
        },
        y: -60,
        ease: 'none'
      });
    }

    /* ===== 8. HOVER EFFECTS - MAGNETIC BUTTONS ===== */
    function initHoverEffects() {
      // Magnetic button effect
      document.querySelectorAll('.btn').forEach(function(btn) {
        btn.addEventListener('mousemove', function(e) {
          var rect = btn.getBoundingClientRect();
          var x = e.clientX - rect.left - rect.width / 2;
          var y = e.clientY - rect.top - rect.height / 2;

          gsap.to(btn, {
            x: x * 0.3,
            y: y * 0.3,
            duration: 0.3,
            ease: 'power2.out'
          });
        });

        btn.addEventListener('mouseleave', function() {
          gsap.to(btn, {
            x: 0,
            y: 0,
            duration: 0.5,
            ease: 'elastic.out(1, 0.3)'
          });
        });
      });

      // Feature cards hover lift
      document.querySelectorAll('.feature-card').forEach(function(card) {
        card.addEventListener('mouseenter', function() {
          gsap.to(card, { y: -8, duration: 0.4, ease: 'power2.out' });
          gsap.to(card.querySelector('.feature-icon'), { scale: 1.15, duration: 0.4, ease: 'back.out(1.5)' });
        });
        card.addEventListener('mouseleave', function() {
          gsap.to(card, { y: 0, duration: 0.5, ease: 'power2.out' });
          gsap.to(card.querySelector('.feature-icon'), { scale: 1, duration: 0.5, ease: 'power2.out' });
        });
      });

      // Screenshot hover zoom
      document.querySelectorAll('.screenshot-box').forEach(function(box) {
        box.addEventListener('mouseenter', function() {
          gsap.to(box, { scale: 1.03, duration: 0.4, ease: 'power2.out' });
        });
        box.addEventListener('mouseleave', function() {
          gsap.to(box, { scale: 1, duration: 0.5, ease: 'back.out(1.4)' });
        });
      });
    }

    /* ===== 9. SCROLL BAR PROGRESS ===== */
    function initScrollProgress() {
      gsap.from('.scroll-progress', {
        scaleX: 0,
        transformOrigin: 'left center',
        ease: 'none',
        scrollTrigger: {
          trigger: document.body,
          start: 'top top',
          end: 'bottom bottom',
          scrub: 0.3
        }
      });
    }

    /* ===== 10. MODAL ANIMATIONS ===== */
    function initModal() {
      var modal = document.getElementById('download-modal');
      var modalClose = document.getElementById('modal-close');

      document.querySelectorAll('.btn-download, [data-target="download-modal"]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          openModal();
        });
      });

      if (modalClose) {
        modalClose.addEventListener('click', closeModal);
      }

      if (modal) {
        modal.addEventListener('click', function(e) {
          if (e.target === modal) closeModal();
        });
      }

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.classList.contains('open')) closeModal();
      });

      function openModal() {
        modal.classList.add('open');
        document.body.classList.add('modal-open');
        gsap.fromTo('.modal',
          { scale: 0.8, opacity: 0, y: 50 },
          { scale: 1, opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.4)' }
        );
        gsap.fromTo(modal, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: 'power2.out' });
      }

      function closeModal() {
        gsap.to(modal, {
          opacity: 0,
          duration: 0.2,
          ease: 'power2.in',
          onComplete: function() {
            modal.classList.remove('open');
            document.body.classList.remove('modal-open');
          }
        });
        gsap.to('.modal', { scale: 0.9, opacity: 0, duration: 0.25, ease: 'power2.in' });
      }
    }

    /* ===== 11. SMOOTH SCROLL ===== */
    function initSmoothScroll() {
      document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
          var targetId = anchor.getAttribute('href');
          if (targetId === '#') return;
          var target = document.querySelector(targetId);
          if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
    }

    /* ===== 12. THEME TOGGLE ===== */
    function initThemeToggle() {
      var ThemeManager = {
        STORAGE_KEY: 'pdf-ai-tool-theme',

        init: function() {
          var stored = localStorage.getItem(this.STORAGE_KEY);
          if (stored) {
            document.documentElement.setAttribute('data-theme', stored);
            return;
          }
        },

        toggle: function() {
          var html = document.documentElement;
          var isDark = html.getAttribute('data-theme') === 'dark' ||
                       (!html.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
          var newTheme = isDark ? 'light' : 'dark';
          html.setAttribute('data-theme', newTheme);
          localStorage.setItem(this.STORAGE_KEY, newTheme);
        }
      };

      ThemeManager.init();

      var toggle = document.getElementById('theme-toggle');
      if (toggle) {
        toggle.addEventListener('click', function() {
          ThemeManager.toggle();
        });
      }
    }

    /* ===== RESPONSIVE: MATCH MEDIA ===== */
    function initResponsiveAnimations() {
      gsap.matchMedia({
        '(min-width: 768px)': function() {
          // Desktop: full animations
          initHeroAnimations();
          initSectionAnimations();
          initFeatureAnimations();
          initScreenshotsAnimation();
          initParallax();
          initHoverEffects();
          initScrollProgress();
        },
        '(max-width: 767px)': function() {
          // Mobile: simplified animations
          initHeroAnimations();
          initSectionAnimations();
          initFeatureAnimations();
          initHoverEffects();
          gsap.from('.screenshots-grid', {
            opacity: 0,
            y: 30,
            duration: 0.8,
            scrollTrigger: {
              trigger: '.screenshots',
              start: 'top 80%'
            }
          });
        }
      });
    }

    /* ===== INITIALIZE ===== */
    function init() {
      initThemeToggle();
      initFAQ();
      initModal();
      initSmoothScroll();
      initCTAAnimations();
      initResponsiveAnimations();

      // Refresh ScrollTrigger after images load
      window.addEventListener('load', function() {
        ScrollTrigger.refresh();
      });

      // Cleanup on unload
      window.addEventListener('beforeunload', function() {
        ScrollTrigger.getAll().forEach(function(t) { t.kill(); });
      });
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }

  } else {
    // ============================================================
    // GSAP FAILED TO LOAD - BUT THAT'S OK!
    // CSS animations are already running, page is fully functional
    // Just initialize the interactive features (FAQ, Modal, Theme)
    // ============================================================

    console.log('GSAP not available - using CSS-only animations (page still works perfectly)');

    /* ===== CSS ANIMATIONS HANDLE ALL ENTRANCE ANIMATIONS ===== */

    /* ===== FAQ ACCORDION (CSS + minimal JS) ===== */
    function initFAQ() {
      document.querySelectorAll('.faq-item').forEach(function(item) {
        var question = item.querySelector('.faq-question');
        var answer = item.querySelector('.faq-answer');

        question.addEventListener('click', function() {
          var isOpen = item.classList.contains('open');

          // Close all other items
          document.querySelectorAll('.faq-item.open').forEach(function(openItem) {
            if (openItem !== item) {
              openItem.classList.remove('open');
            }
          });

          if (!isOpen) {
            item.classList.add('open');
          } else {
            item.classList.remove('open');
          }
        });
      });
    }

    /* ===== MODAL (CSS + minimal JS) ===== */
    function initModal() {
      var modal = document.getElementById('download-modal');
      var modalClose = document.getElementById('modal-close');

      document.querySelectorAll('.btn-download, [data-target="download-modal"]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          modal.classList.add('open');
          document.body.classList.add('modal-open');
        });
      });

      if (modalClose) {
        modalClose.addEventListener('click', function() {
          modal.classList.remove('open');
          document.body.classList.remove('modal-open');
        });
      }

      if (modal) {
        modal.addEventListener('click', function(e) {
          if (e.target === modal) {
            modal.classList.remove('open');
            document.body.classList.remove('modal-open');
          }
        });
      }

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.classList.contains('open')) {
          modal.classList.remove('open');
          document.body.classList.remove('modal-open');
        }
      });
    }

    /* ===== THEME TOGGLE ===== */
    function initThemeToggle() {
      var ThemeManager = {
        STORAGE_KEY: 'pdf-ai-tool-theme',

        init: function() {
          var stored = localStorage.getItem(this.STORAGE_KEY);
          if (stored) {
            document.documentElement.setAttribute('data-theme', stored);
            return;
          }
        },

        toggle: function() {
          var html = document.documentElement;
          var isDark = html.getAttribute('data-theme') === 'dark' ||
                       (!html.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
          var newTheme = isDark ? 'light' : 'dark';
          html.setAttribute('data-theme', newTheme);
          localStorage.setItem(this.STORAGE_KEY, newTheme);
        }
      };

      ThemeManager.init();

      var toggle = document.getElementById('theme-toggle');
      if (toggle) {
        toggle.addEventListener('click', function() {
          ThemeManager.toggle();
        });
      }
    }

    /* ===== SMOOTH SCROLL ===== */
    function initSmoothScroll() {
      document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
          var targetId = anchor.getAttribute('href');
          if (targetId === '#') return;
          var target = document.querySelector(targetId);
          if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
    }

    /* ===== INITIALIZE (NO GSAP VERSION) ===== */
    function init() {
      initThemeToggle();
      initFAQ();
      initModal();
      initSmoothScroll();
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  }
})();
