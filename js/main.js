// Buy The Building, Keep The Profits - Main JS

document.addEventListener('DOMContentLoaded', function() {
  // Mobile navigation toggle
  const mobileToggle = document.querySelector('.nav__mobile-toggle');
  const navLinks = document.querySelector('.nav__links');

  if (mobileToggle) {
    mobileToggle.addEventListener('click', function() {
      navLinks.classList.toggle('active');
      this.textContent = navLinks.classList.contains('active') ? '✕' : '☰';
    });
  }

  // Scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.card, .blog-card, .chapter-item, .stat').forEach(function(el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });

  // Add animate-in class styles
  const style = document.createElement('style');
  style.textContent = '.animate-in { opacity: 1 !important; transform: translateY(0) !important; }';
  document.head.appendChild(style);

  // Navbar background on scroll
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      nav.style.background = 'rgba(28, 25, 23, 0.98)';
    } else {
      nav.style.background = 'rgba(28, 25, 23, 0.95)';
    }
  });

  // Calculator functionality
  const calcForm = document.getElementById('calc-form');
  if (calcForm) {
    calcForm.addEventListener('submit', function(e) {
      e.preventDefault();
      calculateComparison();
    });
  }
});

function calculateComparison() {
  const monthlyRent = parseFloat(document.getElementById('monthly-rent').value) || 0;
  const buildingPrice = parseFloat(document.getElementById('building-price').value) || 0;
  const downPayment = parseFloat(document.getElementById('down-payment').value) || 20;
  const interestRate = parseFloat(document.getElementById('interest-rate').value) || 6.5;
  const loanTerm = parseFloat(document.getElementById('loan-term').value) || 25;

  // Calculations
  const annualRent = monthlyRent * 12;
  const fiveYearRent = annualRent * 5;
  const tenYearRent = annualRent * 10;

  const loanAmount = buildingPrice * (1 - downPayment / 100);
  const monthlyRate = interestRate / 100 / 12;
  const numPayments = loanTerm * 12;
  const monthlyMortgage = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / (Math.pow(1 + monthlyRate, numPayments) - 1);
  const annualMortgage = monthlyMortgage * 12;

  // Equity after 5 years (simplified)
  let balance = loanAmount;
  for (let i = 0; i < 60; i++) {
    const interest = balance * monthlyRate;
    const principal = monthlyMortgage - interest;
    balance -= principal;
  }
  const equityFiveYear = buildingPrice - balance + (buildingPrice * downPayment / 100);

  // Appreciation (3% annually)
  const appreciatedValue5 = buildingPrice * Math.pow(1.03, 5);
  const appreciatedValue10 = buildingPrice * Math.pow(1.03, 10);

  // Display results
  const results = document.getElementById('calc-results');
  results.classList.add('active');
  results.innerHTML = `
    <h4 style="margin-bottom: 1.5rem; color: var(--charcoal);">Your Comparison Results</h4>
    <div class="result-row">
      <span>Monthly Rent Payment</span>
      <span>$${monthlyRent.toLocaleString()}</span>
    </div>
    <div class="result-row">
      <span>Monthly Mortgage Payment</span>
      <span>$${Math.round(monthlyMortgage).toLocaleString()}</span>
    </div>
    <div class="result-row">
      <span>5-Year Total Rent Cost</span>
      <span style="color: #dc2626;">-$${fiveYearRent.toLocaleString()}</span>
    </div>
    <div class="result-row">
      <span>5-Year Equity Built</span>
      <span style="color: #16a34a;">+$${Math.round(equityFiveYear).toLocaleString()}</span>
    </div>
    <div class="result-row">
      <span>Building Value (5 years, 3% growth)</span>
      <span>$${Math.round(appreciatedValue5).toLocaleString()}</span>
    </div>
    <div class="result-row">
      <span>Building Value (10 years, 3% growth)</span>
      <span>$${Math.round(appreciatedValue10).toLocaleString()}</span>
    </div>
    <div class="result-row">
      <span><strong>Net Wealth Advantage of Owning (5 yr)</strong></span>
      <span><strong>$${Math.round(equityFiveYear + (appreciatedValue5 - buildingPrice) - fiveYearRent * 0).toLocaleString()}</strong></span>
    </div>
  `;
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
