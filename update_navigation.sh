#!/bin/bash

# Update base template navigation to match PDF specifications

cat > templates/base_new.html << 'BASE_EOF'
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="T&TG Trade Corp — Global trading, financial services, import/export, and investment from Toronto to the world.">
  <title>{% block title %}T&TG Trade Corp{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
  <style>
    /* Per-page overrides only — global styles in static/css/main.css */
    :root {
      --navy: #0a0f1e;
      --navy-mid: #111827;
      --navy-light: #1a2540;
      --gold: #c9a84c;
      --gold-light: #e4c472;
      --gold-pale: #f5e6b8;
      --cream: #fdf8ef;
      --white: #ffffff;
      --text-muted: #8a9ab5;
      --border: rgba(201,168,76,0.18);
      --card-bg: rgba(26,37,64,0.7);
    }
    * { box-sizing: border-box; }
    body {
      font-family: 'DM Sans', sans-serif;
      background: var(--navy);
      color: var(--cream);
      min-height: 100vh;
    }
    h1, h2, h3, h4, h5 { font-family: 'Cormorant Garamond', serif; }

    /* ── NAVBAR ── */
    .navbar {
      background: rgba(10,15,30,0.97);
      border-bottom: 1px solid var(--border);
      backdrop-filter: blur(12px);
      padding: 0.9rem 0;
      position: sticky; top: 0; z-index: 1000;
    }
    .navbar-brand {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.6rem; font-weight: 700;
      color: var(--gold) !important;
      letter-spacing: 0.04em;
    }
    .navbar-brand span { color: var(--cream); }
    .nav-link {
      color: var(--text-muted) !important;
      font-size: 0.85rem; font-weight: 500;
      letter-spacing: 0.08em; text-transform: uppercase;
      padding: 0.5rem 1rem !important;
      transition: color 0.2s;
    }
    .nav-link:hover, .nav-link.active { color: var(--gold) !important; }
    
    /* Dropdown styles */
    .dropdown-menu {
      background: var(--navy-mid);
      border: 1px solid var(--border);
      border-radius: 4px;
      margin-top: 0.5rem;
    }
    .dropdown-item {
      color: var(--text-muted);
      font-size: 0.85rem;
      padding: 0.6rem 1.2rem;
      transition: all 0.2s;
    }
    .dropdown-item:hover {
      background: var(--navy-light);
      color: var(--gold);
    }
    .dropdown-toggle::after {
      margin-left: 0.3rem;
      vertical-align: 0.1em;
    }
    
    .btn-nav-cta {
      background: var(--gold); color: var(--navy) !important;
      border-radius: 2px; font-weight: 600;
      padding: 0.4rem 1.2rem !important;
      transition: background 0.2s;
    }
    .btn-nav-cta:hover { background: var(--gold-light); }

    /* ── BUTTONS ── */
    .btn-gold {
      background: var(--gold); color: var(--navy);
      border: none; border-radius: 2px;
      font-weight: 600; font-size: 0.9rem;
      letter-spacing: 0.06em; text-transform: uppercase;
      padding: 0.75rem 2rem;
      transition: all 0.25s;
    }
    .btn-gold:hover { background: var(--gold-light); color: var(--navy); transform: translateY(-1px); }
    .btn-outline-gold {
      background: transparent; color: var(--gold);
      border: 1px solid var(--gold); border-radius: 2px;
      font-weight: 500; font-size: 0.9rem;
      letter-spacing: 0.06em; text-transform: uppercase;
      padding: 0.7rem 1.8rem;
      transition: all 0.25s;
    }
    .btn-outline-gold:hover { background: var(--gold); color: var(--navy); }

    /* ── CARDS ── */
    .ttg-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 4px;
      backdrop-filter: blur(8px);
      transition: transform 0.25s, box-shadow 0.25s;
    }
    .ttg-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(201,168,76,0.12); }

    /* ── SECTION HEADERS ── */
    .section-label {
      font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
      color: var(--gold); font-weight: 600; margin-bottom: 0.5rem;
    }
    .section-title {
      font-size: 2.8rem; font-weight: 600; color: var(--cream);
      line-height: 1.2; margin-bottom: 1rem;
    }
    .section-subtitle {
      font-size: 1.05rem; color: var(--text-muted);
      max-width: 700px; margin: 0 auto 2.5rem;
    }

    /* ── HERO ── */
    .hero {
      background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%);
      padding: 5rem 0 4rem;
      position: relative; overflow: hidden;
    }
    .hero::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
      background: radial-gradient(circle at 20% 50%, rgba(201,168,76,0.06) 0%, transparent 50%);
    }
    .hero-title {
      font-size: 3.5rem; font-weight: 700; color: var(--cream);
      margin-bottom: 1.2rem; line-height: 1.1;
    }
    .hero-subtitle {
      font-size: 1.3rem; color: var(--text-muted);
      margin-bottom: 2rem; max-width: 650px;
    }

    /* ── STATS ── */
    .stat-card {
      background: var(--card-bg); border: 1px solid var(--border);
      border-radius: 6px; padding: 1.8rem; text-align: center;
    }
    .stat-number {
      font-family: 'Cormorant Garamond', serif;
      font-size: 2.8rem; font-weight: 700; color: var(--gold);
      display: block; margin-bottom: 0.3rem;
    }
    .stat-label {
      font-size: 0.85rem; color: var(--text-muted);
      text-transform: uppercase; letter-spacing: 0.08em;
    }

    /* ── FOOTER ── */
    footer {
      background: var(--navy);
      border-top: 1px solid var(--border);
      padding: 3.5rem 0 1.5rem;
      margin-top: 5rem;
    }
    footer h6 {
      color: var(--gold); font-family: 'DM Sans', sans-serif;
      font-size: 0.75rem; letter-spacing: 0.18em; text-transform: uppercase;
      margin-bottom: 1rem;
    }
    footer a { color: var(--text-muted); text-decoration: none; font-size: 0.88rem; }
    footer a:hover { color: var(--gold); }
    footer li { margin-bottom: 0.5rem; }
    .footer-brand {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.8rem; color: var(--gold); font-weight: 700;
    }
    .footer-divider { border-color: var(--border); }
    .footer-legal { color: var(--text-muted); font-size: 0.78rem; }

    /* ── ALERTS ── */
    .alert { border-radius: 3px; border: none; }
    .alert-success { background: rgba(34,197,94,0.12); color: #86efac; border-left: 3px solid #22c55e; }
    .alert-danger { background: rgba(239,68,68,0.12); color: #fca5a5; border-left: 3px solid #ef4444; }
    .alert-info { background: rgba(201,168,76,0.12); color: var(--gold-pale); border-left: 3px solid var(--gold); }

    /* ── COUNTRY PILLS ── */
    .country-pill {
      display: inline-flex; align-items: center; gap: 0.4rem;
      background: var(--navy-light); border: 1px solid var(--border);
      border-radius: 20px; padding: 0.3rem 0.9rem;
      font-size: 0.8rem; color: var(--text-muted);
      transition: all 0.2s; text-decoration: none;
    }
    .country-pill:hover, .country-pill.active {
      border-color: var(--gold); color: var(--gold);
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--navy); }
    ::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 3px; }

    /* ── TABLE ── */
    .ttg-table { color: var(--cream); }
    .ttg-table thead th {
      background: var(--navy-light); color: var(--gold);
      border-color: var(--border); font-size: 0.78rem;
      letter-spacing: 0.1em; text-transform: uppercase; font-weight: 500;
    }
    .ttg-table tbody td { border-color: var(--border); color: var(--cream); }
    .ttg-table tbody tr:hover td { background: rgba(201,168,76,0.04); }

    @media (max-width: 768px) {
      .section-title { font-size: 2rem; }
      .hero-title { font-size: 2.5rem; }
    }
  </style>
  {% block extra_css %}{% endblock %}
</head>
<body>

<!-- NAVBAR -->
<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand" href="/">T&TG <span>Trade Corp</span></a>
    <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <i class="fas fa-bars" style="color:var(--gold)"></i>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav mx-auto gap-1">
        <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="{% url 'about' %}">About</a></li>
        <li class="nav-item"><a class="nav-link" href="{% url 'marketplace' %}">Marketplace</a></li>
        
        <!-- Financial Services & Investments Dropdown -->
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="financialDropdown" role="button" 
             data-bs-toggle="dropdown" aria-expanded="false">
            Financial Services
          </a>
          <ul class="dropdown-menu" aria-labelledby="financialDropdown">
            <li><a class="dropdown-item" href="{% url 'insurance_products' %}">
              <i class="fas fa-shield-alt me-2"></i>Insurance
            </a></li>
            <li><a class="dropdown-item" href="{% url 'marketplace' %}">
              <i class="fas fa-shopping-cart me-2"></i>Online Shopping Platform
            </a></li>
            <li><a class="dropdown-item" href="{% url 'forex_home' %}">
              <i class="fas fa-chart-line me-2"></i>T&TG Brokerage
            </a></li>
          </ul>
        </li>
        
        <li class="nav-item"><a class="nav-link" href="{% url 'programs' %}">Training</a></li>
        <li class="nav-item"><a class="nav-link" href="{% url 'coffee_roasting' %}">Coffee</a></li>
        <li class="nav-item"><a class="nav-link" href="{% url 'contact' %}">Contact</a></li>
      </ul>
      <ul class="navbar-nav gap-2 align-items-center">
        {% if user.is_authenticated %}
          <!-- Avon Points Badge -->
          <li class="nav-item">
            <a class="nav-link" href="{% url 'avon_dashboard' %}" style="position:relative; padding:0.45rem 0.9rem !important;">
              <i class="fas fa-coins text-warning"></i>
              <span style="font-size:0.75rem; margin-left:0.3rem;">
                {% if user.avon_account %}{{ user.avon_account.available_points|floatformat:0 }}{% else %}0{% endif %} pts
              </span>
            </a>
          </li>
          <!-- Notification Bell -->
          <li class="nav-item">
            <a class="nav-link" href="{% url 'notifications' %}" style="position:relative; padding:0.45rem 0.7rem !important;">
              <i class="fas fa-bell"></i>
              <span id="notif-badge" style="
                position:absolute; top:2px; right:2px;
                width:16px; height:16px; border-radius:50%;
                background:var(--gold); color:var(--navy);
                font-size:0.6rem; font-weight:700;
                display:none; align-items:center; justify-content:center;
              "></span>
            </a>
          </li>
          <li class="nav-item"><a class="nav-link" href="{% url 'dashboard' %}"><i class="fas fa-tachometer-alt me-1"></i>Dashboard</a></li>
          <li class="nav-item"><a class="nav-link btn-nav-cta" href="{% url 'logout' %}">Sign Out</a></li>
        {% else %}
          <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Sign In</a></li>
          <li class="nav-item"><a class="nav-link btn-nav-cta" href="{% url 'register' %}">Register</a></li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>

<!-- MESSAGES -->
{% if messages %}
  <div class="container mt-3">
    {% for message in messages %}
      <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    {% endfor %}
  </div>
{% endif %}

<!-- MAIN CONTENT -->
{% block content %}{% endblock %}

<!-- FOOTER -->
<footer>
  <div class="container">
    <div class="row g-4">
      <!-- Brand Column -->
      <div class="col-lg-4">
        <div class="footer-brand mb-3">T&TG Trade Corp</div>
        <p style="color:var(--text-muted); font-size:0.9rem;">
          Global trading, financial services, and investment solutions connecting 
          Canada, Uganda, USA, Netherlands, and Kenya.
        </p>
        <div class="mt-3">
          <a href="#" class="me-3"><i class="fab fa-linkedin fa-lg"></i></a>
          <a href="#" class="me-3"><i class="fab fa-twitter fa-lg"></i></a>
          <a href="#"><i class="fab fa-facebook fa-lg"></i></a>
        </div>
      </div>

      <!-- Services Column -->
      <div class="col-lg-2 col-md-4">
        <h6>Services</h6>
        <ul class="list-unstyled">
          <li><a href="{% url 'marketplace' %}">Marketplace</a></li>
          <li><a href="{% url 'insurance_products' %}">Insurance</a></li>
          <li><a href="{% url 'forex_home' %}">Brokerage</a></li>
          <li><a href="{% url 'coffee_roasting' %}">Coffee Roasting</a></li>
        </ul>
      </div>

      <!-- Company Column -->
      <div class="col-lg-2 col-md-4">
        <h6>Company</h6>
        <ul class="list-unstyled">
          <li><a href="{% url 'about' %}">About Us</a></li>
          <li><a href="{% url 'leadership' %}">Leadership</a></li>
          <li><a href="{% url 'contact' %}">Contact</a></li>
          <li><a href="#">Careers</a></li>
        </ul>
      </div>

      <!-- Resources Column -->
      <div class="col-lg-2 col-md-4">
        <h6>Resources</h6>
        <ul class="list-unstyled">
          <li><a href="{% url 'programs' %}">Training</a></li>
          <li><a href="{% url 'avon_dashboard' %}">Avon Points</a></li>
          <li><a href="#">Help Center</a></li>
          <li><a href="#">Terms</a></li>
        </ul>
      </div>

      <!-- Markets Column -->
      <div class="col-lg-2 col-md-4">
        <h6>Markets</h6>
        <ul class="list-unstyled">
          <li><a href="#">Canada</a></li>
          <li><a href="#">Uganda</a></li>
          <li><a href="#">USA</a></li>
          <li><a href="#">Netherlands</a></li>
          <li><a href="#">Kenya</a></li>
        </ul>
      </div>
    </div>

    <hr class="footer-divider my-4">
    
    <div class="row">
      <div class="col-md-6">
        <p class="footer-legal mb-0">
          © 2026 T&TG Trade Corporation. All rights reserved.
        </p>
      </div>
      <div class="col-md-6 text-md-end">
        <p class="footer-legal mb-0">
          Toronto, Canada | Kampala, Uganda | Nairobi, Kenya
        </p>
      </div>
    </div>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="{% static 'js/main.js' %}"></script>
{% block extra_js %}{% endblock %}
</body>
</html>
BASE_EOF

mv templates/base.html templates/base_old_backup.html
mv templates/base_new.html templates/base.html

echo "Navigation updated successfully"
