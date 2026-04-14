#!/bin/bash

# Create Avon Points Dashboard
cat > templates/ecommerce/avon_dashboard.html << 'EOF'
{% extends 'base.html' %}
{% load humanize %}

{% block title %}Avon Points Dashboard - T&TG Trade Corp{% endblock %}

{% block content %}
<div class="container my-5">
  <div class="row mb-4">
    <div class="col">
      <h1 class="section-title mb-2">Avon Points Dashboard</h1>
      <p class="section-subtitle">Manage your rewards and convert points to funds</p>
    </div>
  </div>

  <!-- Points Summary Cards -->
  <div class="row g-4 mb-5">
    <div class="col-md-3">
      <div class="ttg-card p-4 text-center">
        <div class="stat-number">{{ account.available_points|floatformat:0 }}</div>
        <div class="stat-label">Available Points</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="ttg-card p-4 text-center">
        <div class="stat-number">{{ account.total_earned_points|floatformat:0 }}</div>
        <div class="stat-label">Total Earned</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="ttg-card p-4 text-center">
        <div class="stat-number">{{ account.total_redeemed_points|floatformat:0 }}</div>
        <div class="stat-label">Total Redeemed</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="ttg-card p-4 text-center">
        <div class="stat-number">${{ account.available_points|floatformat:2 }}</div>
        <div class="stat-label">Estimated Value</div>
      </div>
    </div>
  </div>

  <!-- Action Buttons -->
  <div class="row mb-5">
    <div class="col-md-12">
      <div class="ttg-card p-4">
        <h5 class="mb-3" style="color:var(--gold)">Quick Actions</h5>
        <div class="d-flex gap-3 flex-wrap">
          <a href="{% url 'create_sell_order' %}" class="btn btn-gold">
            <i class="fas fa-dollar-sign me-2"></i>Create Sell Order
          </a>
          <a href="{% url 'redeem_points' %}" class="btn btn-outline-gold">
            <i class="fas fa-gift me-2"></i>Redeem Points
          </a>
          <a href="{% url 'referral_info' %}" class="btn btn-outline-gold">
            <i class="fas fa-users me-2"></i>My Referrals
          </a>
          <a href="{% url 'avon_transactions' %}" class="btn btn-outline-gold">
            <i class="fas fa-list me-2"></i>View All Transactions
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- How Avon Points Work -->
  <div class="row mb-5">
    <div class="col-md-12">
      <div class="ttg-card p-4">
        <h5 class="mb-3" style="color:var(--gold)"><i class="fas fa-info-circle me-2"></i>How Avon Points Work</h5>
        <div class="row">
          <div class="col-md-6">
            <h6 style="color:var(--cream)">Earning Points</h6>
            <ul style="color:var(--text-muted)">
              <li><strong>5.5%</strong> of purchase amount as end user/consumer</li>
              <li><strong>8.5%</strong> of purchase amount when you refer a buyer</li>
              <li>Points earned on delivered orders only</li>
            </ul>
          </div>
          <div class="col-md-6">
            <h6 style="color:var(--cream)">Using Points</h6>
            <ul style="color:var(--text-muted)">
              <li>Convert to funds through quarterly sell orders (Q1-Q4)</li>
              <li>Minimum 3-month execution period</li>
              <li>Pay insurance premiums</li>
              <li>Transfer to trading platform</li>
              <li>Invest in real estate</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Recent Transactions -->
  <div class="row mb-5">
    <div class="col-md-12">
      <div class="ttg-card p-4">
        <h5 class="mb-3" style="color:var(--gold)">Recent Transactions</h5>
        {% if transactions %}
        <div class="table-responsive">
          <table class="table ttg-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Amount</th>
                <th>Source</th>
                <th>Balance After</th>
              </tr>
            </thead>
            <tbody>
              {% for txn in transactions %}
              <tr>
                <td>{{ txn.created_at|date:"M d, Y" }}</td>
                <td>
                  {% if txn.transaction_type == 'earn' %}
                  <span class="badge bg-success">Earned</span>
                  {% else %}
                  <span class="badge bg-warning text-dark">Redeemed</span>
                  {% endif %}
                </td>
                <td>{{ txn.amount|floatformat:2 }}</td>
                <td>{{ txn.source }}</td>
                <td>{{ txn.balance_after|floatformat:2 }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <p style="color:var(--text-muted)">No transactions yet. Start earning by making purchases or referring buyers!</p>
        {% endif %}
      </div>
    </div>
  </div>

  <!-- Pending Sell Orders -->
  {% if sell_orders %}
  <div class="row">
    <div class="col-md-12">
      <div class="ttg-card p-4">
        <h5 class="mb-3" style="color:var(--gold)">Pending Sell Orders</h5>
        <div class="table-responsive">
          <table class="table ttg-table">
            <thead>
              <tr>
                <th>Date Created</th>
                <th>Quarter</th>
                <th>Points</th>
                <th>USD Amount</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {% for order in sell_orders %}
              <tr>
                <td>{{ order.created_at|date:"M d, Y" }}</td>
                <td>{{ order.get_quarter_display }}</td>
                <td>{{ order.points_amount|floatformat:2 }}</td>
                <td>${{ order.usd_amount|floatformat:2 }}</td>
                <td>
                  <span class="badge 
                    {% if order.status == 'completed' %}bg-success
                    {% elif order.status == 'processing' %}bg-info
                    {% elif order.status == 'cancelled' %}bg-danger
                    {% else %}bg-warning text-dark{% endif %}">
                    {{ order.get_status_display }}
                  </span>
                </td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  {% endif %}

</div>
{% endblock %}
EOF

# Create Coffee Home Template
cat > templates/coffee/home.html << 'EOF'
{% extends 'base.html' %}
{% load humanize %}

{% block title %}Coffee Roasting - T&TG Trade Corp{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="hero text-center">
  <div class="container">
    <div class="section-label">Premium Coffee Roasting</div>
    <h1 class="hero-title">Organic Arabica Coffee<br>From Uganda to the World</h1>
    <p class="hero-subtitle mx-auto">
      Roasted to perfection. Delivered fresh. Special texture and organic quality.
    </p>
    <div class="d-flex gap-3 justify-content-center mt-4">
      <a href="{% url 'coffee_products' %}" class="btn btn-gold">Shop Coffee</a>
      <a href="#production" class="btn btn-outline-gold">Our Production</a>
    </div>
  </div>
</div>

<!-- Why Our Coffee is Special -->
<div class="container my-5 py-5">
  <div class="text-center mb-5">
    <div class="section-label">What Makes Us Different</div>
    <h2 class="section-title">Special About Our Coffee</h2>
  </div>
  
  <div class="row g-4">
    <div class="col-md-4">
      <div class="ttg-card p-4 text-center h-100">
        <div class="mb-3">
          <i class="fas fa-leaf fa-3x" style="color:var(--gold)"></i>
        </div>
        <h5 style="color:var(--cream)">100% Organic</h5>
        <p style="color:var(--text-muted)">
          Grown without pesticides or chemicals. Pure, natural coffee beans from Ugandan highlands.
        </p>
      </div>
    </div>
    <div class="col-md-4">
      <div class="ttg-card p-4 text-center h-100">
        <div class="mb-3">
          <i class="fas fa-fire fa-3x" style="color:var(--gold)"></i>
        </div>
        <h5 style="color:var(--cream)">Superior Texture</h5>
        <p style="color:var(--text-muted)">
          Unique texture and flavor profile. Carefully roasted to bring out rich, smooth notes.
        </p>
      </div>
    </div>
    <div class="col-md-4">
      <div class="ttg-card p-4 text-center h-100">
        <div class="mb-3">
          <i class="fas fa-shipping-fast fa-3x" style="color:var(--gold)"></i>
        </div>
        <h5 style="color:var(--cream)">Fresh Roasted</h5>
        <p style="color:var(--text-muted)">
          Roasted on demand and shipped immediately. Maximum freshness guaranteed.
        </p>
      </div>
    </div>
  </div>
</div>

<!-- Production Levels -->
<div id="production" class="container my-5 py-5">
  <div class="text-center mb-5">
    <div class="section-label">Growth & Capacity</div>
    <h2 class="section-title">Production Levels</h2>
    <p class="section-subtitle">
      Our scalable roasting operation with clear revenue projections
    </p>
  </div>
  
  <div class="row g-4">
    {% for level in levels %}
    <div class="col-md-6 col-lg-3">
      <div class="ttg-card p-4 {% if level.is_current %}border border-warning{% endif %}">
        {% if level.is_current %}
        <span class="badge bg-warning text-dark mb-2">Current Level</span>
        {% endif %}
        <h3 style="color:var(--gold); font-family:'Cormorant Garamond',serif">
          Level {{ level.level_number }}
        </h3>
        <p style="color:var(--cream); font-size:1.1rem; margin:0.5rem 0">
          {{ level.kg_per_week }}kg/week
        </p>
        <hr style="border-color:var(--border)">
        <div style="color:var(--text-muted); font-size:0.9rem">
          <p class="mb-1"><strong>Monthly:</strong></p>
          <p class="mb-2">${{ level.monthly_revenue_min|floatformat:0|intcomma }} - ${{ level.monthly_revenue_max|floatformat:0|intcomma }}</p>
          <p class="mb-1"><strong>Annual:</strong></p>
          <p class="mb-0">${{ level.annual_revenue_min|floatformat:0|intcomma }} - ${{ level.annual_revenue_max|floatformat:0|intcomma }}</p>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
  
  <div class="text-center mt-4">
    <p style="color:var(--text-muted); font-size:0.9rem">
      Price range: $35 - $55 per kg | Current projection based on 25kg/week
    </p>
  </div>
</div>

<!-- Featured Products -->
<div class="container my-5 py-5">
  <div class="text-center mb-5">
    <div class="section-label">Our Selection</div>
    <h2 class="section-title">Available Coffee</h2>
  </div>
  
  <div class="row g-4">
    {% for product in products|slice:":3" %}
    <div class="col-md-4">
      <div class="ttg-card h-100">
        {% if product.image %}
        <img src="{{ product.image.url }}" class="card-img-top" alt="{{ product.name }}" 
             style="height:200px; object-fit:cover">
        {% else %}
        <div style="height:200px; background:var(--navy-light); display:flex; align-items:center; justify-content:center">
          <i class="fas fa-coffee fa-4x" style="color:var(--gold)"></i>
        </div>
        {% endif %}
        <div class="p-4">
          <h5 style="color:var(--cream)">{{ product.name }}</h5>
          <p style="color:var(--text-muted); font-size:0.85rem">
            {{ product.get_roast_level_display }} | {{ product.get_coffee_type_display }}
          </p>
          <p style="color:var(--gold); font-size:1.2rem; font-weight:600">
            ${{ product.price_per_kg|floatformat:2 }}/kg
          </p>
          <a href="{% url 'order_coffee' product.id %}" class="btn btn-gold w-100">
            Order Now
          </a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
  
  <div class="text-center mt-4">
    <a href="{% url 'coffee_products' %}" class="btn btn-outline-gold">
      View All Coffee Products
    </a>
  </div>
</div>
{% endblock %}
EOF

echo "Key templates created successfully"
