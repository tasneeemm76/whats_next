/**
 * What's Next — Theme: loading animation, scroll reveal
 */
(function () {
  'use strict';

  // Page loader: hide when DOM is ready and a short delay for smoothness
  function initLoader() {
    var loader = document.getElementById('page-loader');
    if (!loader) return;

    function hide() {
      loader.classList.add('hidden');
      setTimeout(function () {
        loader.remove();
      }, 400);
    }

    if (document.readyState === 'complete') {
      setTimeout(hide, 400);
    } else {
      window.addEventListener('load', function () {
        setTimeout(hide, 400);
      });
    }
  }

  // Scroll reveal: add .revealed when element enters viewport
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
          }
        });
      },
      { rootMargin: '0px 0px -40px 0px', threshold: 0.1 }
    );

    els.forEach(function (el) {
      observer.observe(el);
    });
  }

  // Mobile nav toggle (optional: for base navbar)
  function initNavToggle() {
    var toggle = document.getElementById('nav-toggle');
    var nav = document.getElementById('nav-menu');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('is-open'));
    });
  }

  // Auto-dismiss flash messages
  function initAutoDismissAlerts() {
    var alerts = document.querySelectorAll('.wn-alert');
    if (!alerts.length) return;

    alerts.forEach(function (alert) {
      var timeoutId = setTimeout(function () {
        alert.classList.add('wn-alert--hide');
        alert.addEventListener(
          'transitionend',
          function handleTransitionEnd() {
            alert.removeEventListener('transitionend', handleTransitionEnd);
            if (alert.parentNode) {
              alert.parentNode.removeChild(alert);
            }
          }
        );
      }, 4000);

      // Optional: if user clicks the alert, dismiss immediately
      alert.addEventListener('click', function () {
        clearTimeout(timeoutId);
        alert.classList.add('wn-alert--hide');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initLoader();
      initReveal();
      initNavToggle();
      initAutoDismissAlerts();
    });
  } else {
    initLoader();
    initReveal();
    initNavToggle();
    initAutoDismissAlerts();
  }
})();
