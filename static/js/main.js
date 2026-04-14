/**
 * T&TG Trade Corp — Main JavaScript
 * Navbar scroll effect, fade-up animations, form enhancements,
 * copy-to-clipboard, currency calculator preview
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── NAVBAR SCROLL SHADOW ──
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ── MARK ACTIVE NAV LINK ──
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  // ── FADE-UP INTERSECTION OBSERVER ──
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

  // ── AUTO-STYLE ALL FORM FIELDS ──
  document.querySelectorAll(
    'input[type=text], input[type=email], input[type=password], ' +
    'input[type=tel], input[type=number], input[type=date], textarea'
  ).forEach(el => {
    if (!el.classList.contains('form-control')) el.classList.add('form-control');
  });
  document.querySelectorAll('select').forEach(el => {
    if (!el.classList.contains('form-select')) el.classList.add('form-select');
    el.classList.remove('form-control');
  });
  document.querySelectorAll('input[type=file]').forEach(el => {
    if (!el.classList.contains('form-control')) el.classList.add('form-control');
  });

  // ── MARKET TYPE SELECTOR ──
  window.selectMarketType = function(el, value) {
    document.querySelectorAll('.market-opt').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    const hiddenInput = document.getElementById('id_market_type');
    if (hiddenInput) {
      hiddenInput.value = value;
      hiddenInput.style.display = 'none';
    }
  };

  // ── COPY TO CLIPBOARD ──
  window.copyToClipboard = function(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
      const orig = btn ? btn.innerHTML : '';
      if (btn) {
        btn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        setTimeout(() => { btn.innerHTML = orig; }, 2000);
      }
    }).catch(() => {
      // Fallback
      const el = document.createElement('textarea');
      el.value = text; document.body.appendChild(el);
      el.select(); document.execCommand('copy');
      document.body.removeChild(el);
    });
  };

  // ── FOREX LIVE CALCULATOR ──
  const amountInput  = document.getElementById('forex-amount');
  const fromSelect   = document.getElementById('forex-from');
  const toSelect     = document.getElementById('forex-to');
  const resultBox    = document.getElementById('forex-result');

  if (amountInput && fromSelect && toSelect && resultBox) {
    const RATES = window.FOREX_RATES || {};
    function calcForex() {
      const amount = parseFloat(amountInput.value) || 0;
      const key = `${fromSelect.value}_${toSelect.value}`;
      const rate = RATES[key];
      if (rate && amount > 0) {
        resultBox.textContent = `≈ ${(amount * rate).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ${toSelect.value}`;
        resultBox.style.display = 'block';
      } else {
        resultBox.style.display = 'none';
      }
    }
    [amountInput, fromSelect, toSelect].forEach(el => el.addEventListener('input', calcForex));
  }

  // ── FLASH MESSAGES AUTO-DISMISS ──
  document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // ── CONFIRM DANGEROUS ACTIONS ──
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

  // ── PRODUCT IMAGE PREVIEW ──
  const prodImageInput = document.querySelector('input[type=file][name=image]');
  const prodPreview    = document.getElementById('product-image-preview');
  if (prodImageInput && prodPreview) {
    prodImageInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = ev => {
          prodPreview.src = ev.target.result;
          prodPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // ── SELFIE / ID PREVIEW ──
  ['national_id_front', 'national_id_back', 'selfie', 'profile_photo'].forEach(name => {
    const input   = document.querySelector(`input[name="${name}"]`);
    const preview = document.getElementById(`preview-${name}`);
    if (input && preview) {
      input.addEventListener('change', e => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = ev => {
            preview.src = ev.target.result;
            preview.style.display = 'block';
          };
          reader.readAsDataURL(file);
        }
      });
    }
  });

  // ── SMOOTH BACK TO TOP ──
  const topBtn = document.getElementById('back-to-top');
  if (topBtn) {
    window.addEventListener('scroll', () => {
      topBtn.style.opacity = window.scrollY > 400 ? '1' : '0';
      topBtn.style.pointerEvents = window.scrollY > 400 ? 'auto' : 'none';
    }, { passive: true });
    topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // ── COUNTRY-SPECIFIC CURRENCY HINT ──
  const countrySelect   = document.getElementById('id_country_of_residence');
  const currencyHint    = document.getElementById('currency-hint');
  const COUNTRY_CURRENCY = {
    CA: 'CAD — Canadian Dollar', UG: 'UGX — Ugandan Shilling',
    NL: 'EUR — Euro', JP: 'JPY — Japanese Yen', KE: 'KES — Kenyan Shilling',
  };
  if (countrySelect && currencyHint) {
    countrySelect.addEventListener('change', () => {
      const hint = COUNTRY_CURRENCY[countrySelect.value];
      currencyHint.textContent = hint ? `Local currency: ${hint}` : '';
    });
  }

});
