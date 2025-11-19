---
layout: page
title: News & Updates - Reality Lab
description: Latest news, achievements, and milestones from Reality Lab at Soongsil University. CVPR, AAAI paper acceptances, ARNOLD Challenge wins, grants, and new members.
keywords: Reality Lab news, WACV 2026, CVPR 2025, AAAI 2025, BMVC 2025, ARNOLD Challenge, AI research news, Soongsil University achievements, NRF grant, research awards, 연구실 소식
image: /assets/img/header.png
---

<!-- Timeline Header -->
<section class="news-timeline-header text-center py-5">
  <div class="container">
    <h1 class="section-heading text-uppercase">News & Updates</h1>
    <h3 class="section-subheading text-muted">Latest achievements and milestones from Reality Lab</h3>
  </div>
</section>

<!-- News Content -->
<section class="news-content py-5">
  <div class="container">
    <div class="row news-row">
      {% for item in site.data.news.news %}
        <div class="col-lg-4 mb-4">
          <div class="news-card {% if item.category == 'Publication' %}paper-card{% elsif item.category == 'Awards' %}challenge-card{% else %}research-card{% endif %}">
            <div class="news-img-wrapper">
              {% if item.image %}
              <img src="{{ site.baseurl }}/img/news/{{ item.image }}?v=7" alt="{{ item.title }}" class="news-img">
              {% else %}
              <img src="{{ site.baseurl }}/img/news/default.png?v=7" alt="{{ item.title }}" class="news-img">
              {% endif %}
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ item.title }}</h5>
              <p class="card-subtitle">{{ item.participants | join: ", " }}</p>
              <p class="card-text">{{ item.description }}</p>
              <div class="card-date-category">
                <small class="text-muted">{{ item.date | date: "%b %-d, %Y" }} | {{ item.category }}</small>
              </div>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
</section>

<style>
/* News Timeline Header */
.news-timeline-header {
  background: white;
  color: #2c3e50;
  padding: 80px 0;
}

.news-timeline-header h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.news-timeline-header h3 {
  color: #7f8c8d;
}

/* News Content */
.news-content {
  background-color: #f8f9fa;
}

/* News Row - Align card heights in same row */
.news-row {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
}

.news-row > [class*="col-"] {
  display: flex;
}

/* News Cards */
.news-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.news-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* Image wrapper to maintain aspect ratio */
.news-img-wrapper {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  overflow: hidden;
}

.news-img {
  width: 100%;
  height: auto;
  max-width: 3500px;
  max-height: 300px;
  object-fit: contain;
  object-position: center;
  display: block;
}

.news-card .card-body {
  padding: 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.news-card .card-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
  line-height: 1.4;
}

.news-card .card-subtitle {
  font-size: 0.95rem;
  color: #7f8c8d;
  margin-bottom: 12px;
  font-weight: 500;
}

.news-card .card-text {
  font-size: 0.95rem;
  color: #5a6c7d;
  line-height: 1.6;
  flex: 1;
  margin-bottom: 16px;
}

.card-date-category {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #e0e0e0;
}

/* Card Type Specific Styles */
.paper-card {
  border-top: 4px solid #3b82f6;
}

.challenge-card {
  border-top: 4px solid #10b981;
}

.research-card {
  border-top: 4px solid #8b5cf6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .news-timeline-header {
    padding: 60px 0;
  }

  .news-img {
    max-height: 200px;
  }

  .news-card .card-title {
    font-size: 1.1rem;
  }
}
</style>
