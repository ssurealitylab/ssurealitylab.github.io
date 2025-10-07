---
layout: page
title: Alumni
---

# Alumni

## Research Achievements

Our alumni have made significant contributions to the field of artificial intelligence and computer vision. Here are some of the notable achievements from Reality Lab alumni:

<div class="achievements-container">
  {% for achievement in site.data.members.alumni.achievements %}
  <div class="achievement-card">
    <h3 class="achievement-title">{{ achievement.title }}</h3>
    <p class="achievement-venue">{{ achievement.venue }}</p>
    {% if achievement.members and achievement.members.size > 0 %}
    <div class="achievement-members">
      <strong>Contributors:</strong>
      <ul>
      {% for member in achievement.members %}
        <li>{{ member }}</li>
      {% endfor %}
      </ul>
    </div>
    {% endif %}
  </div>
  {% endfor %}
</div>

## Career Paths

Reality Lab alumni have successfully transitioned to various prestigious positions in academia and industry:

<div class="career-info">
  <div class="career-section">
    <h3><i class="fas fa-graduation-cap"></i> Academic Careers</h3>
    <p>Our alumni continue their research journey in top-tier universities and research institutions worldwide, pursuing PhD programs and research positions.</p>
  </div>
  
  <div class="career-section">
    <h3><i class="fas fa-building"></i> Industry Positions</h3>
    <p>Alumni have secured positions at leading technology companies including Qualcomm, Samsung, LG, and various AI startups, applying their research expertise to real-world applications.</p>
  </div>
  
  <div class="career-section">
    <h3><i class="fas fa-rocket"></i> Entrepreneurship</h3>
    <p>Some alumni have founded their own AI and technology companies, commercializing research innovations and creating new opportunities in the field.</p>
  </div>
</div>

## Connect with Alumni

<div class="connect-section">
  <p>If you are a Reality Lab alumnus and would like to update your information or connect with current lab members, please contact us at <a href="mailto:heewon@ssu.ac.kr">heewon@ssu.ac.kr</a>.</p>
  
  <p>We encourage our alumni to stay connected with the lab and contribute to mentoring current students and sharing industry insights.</p>
</div>

<style>
.achievements-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 25px;
  margin: 30px 0;
}

.achievement-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #3498db;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.achievement-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.achievement-title {
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.achievement-venue {
  color: #7f8c8d;
  font-size: 1rem;
  font-style: italic;
  margin-bottom: 15px;
}

.achievement-members {
  margin-top: 15px;
}

.achievement-members strong {
  color: #2c3e50;
  font-size: 0.9rem;
}

.achievement-members ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.achievement-members li {
  color: #495057;
  font-size: 0.9rem;
  margin-bottom: 3px;
}

.career-info {
  margin: 40px 0;
}

.career-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 20px;
  border-left: 4px solid #28a745;
}

.career-section h3 {
  color: #2c3e50;
  font-size: 1.3rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.career-section h3 i {
  color: #28a745;
  font-size: 1.2rem;
}

.career-section p {
  color: #495057;
  line-height: 1.6;
  margin: 0;
}

.connect-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  padding: 30px;
  margin: 40px 0;
  text-align: center;
}

.connect-section a {
  color: #ffd700;
  text-decoration: none;
  font-weight: 600;
}

.connect-section a:hover {
  text-decoration: underline;
}

.connect-section p {
  margin-bottom: 15px;
  line-height: 1.6;
}

.connect-section p:last-child {
  margin-bottom: 0;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

h2 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 20px;
  margin-top: 40px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

h2:first-of-type {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .achievements-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .achievement-card,
  .career-section,
  .connect-section {
    padding: 20px;
  }
  
  .career-section h3 {
    font-size: 1.2rem;
  }
  
  .achievement-title {
    font-size: 1.2rem;
  }
}
</style>