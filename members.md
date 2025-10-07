---
layout: page
title: Members
---

<style>
.member-card {
  border: 1px solid #e9ecef;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: white;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 20px;
}

.member-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.member-photo {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #f8f9fa;
  transition: border-color 0.3s ease;
  flex-shrink: 0;
}

.member-card:hover .member-photo {
  border-color: #007bff;
}

.member-info {
  flex: 1;
  text-align: left;
}

.member-name {
  font-size: 1.2em;
  font-weight: bold;
  color: #212529;
  margin-bottom: 5px;
}

.member-name-ko {
  font-size: 0.9em;
  color: #6c757d;
  margin-bottom: 10px;
}

.member-position {
  color: #007bff;
  font-weight: 500;
  margin-bottom: 10px;
}

.member-research {
  color: #6c757d;
  font-size: 0.9em;
  margin-bottom: 15px;
  line-height: 1.4;
}

.member-achievements {
  margin-bottom: 15px;
}

.achievement-badge {
  display: inline-block;
  background: #e7f3ff;
  color: #0056b3;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.75em;
  margin: 2px;
}

.social-links {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  margin-top: 10px;
}

.social-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  text-decoration: none;
  transition: all 0.3s ease;
  color: white;
}

.social-link.github {
  background-color: #333;
}

.social-link.github:hover {
  background-color: #000;
  transform: scale(1.1);
}

.social-link.linkedin {
  background-color: #0077b5;
}

.social-link.linkedin:hover {
  background-color: #005885;
  transform: scale(1.1);
}

.social-link.disabled {
  background-color: #dee2e6;
  color: #6c757d;
  cursor: not-allowed;
}

.section-header {
  text-align: center;
  margin: 50px 0 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.section-title {
  color: #212529;
  font-size: 2.5em;
  margin-bottom: 10px;
}

.section-subtitle {
  color: #6c757d;
  font-size: 1.1em;
}

.achievements-section {
  background: #f8f9fa;
  padding: 40px 20px;
  border-radius: 10px;
  margin-top: 50px;
}

.achievement-item {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 15px;
  border-left: 4px solid #007bff;
}

.achievement-title {
  font-weight: bold;
  color: #212529;
  margin-bottom: 5px;
}

.achievement-venue {
  color: #6c757d;
  font-size: 0.9em;
  margin-bottom: 10px;
}

.achievement-members {
  color: #007bff;
  font-size: 0.9em;
}
</style>

# Lab Members

## Faculty {#faculty}

<div class="section-header">
  <h2 class="section-title">Faculty</h2>
  <p class="section-subtitle">Research Leadership</p>
</div>

<div class="row">
  {% for member in site.data.members.faculty %}
  <div class="col-lg-6 col-md-12">
    <div class="member-card">
      <img src="{{ site.baseurl }}/{{ member.photo }}" 
           alt="{{ member.name }}" 
           class="member-photo"
           onerror="this.src='{{ site.baseurl }}/assets/img/members/placeholder.svg'">
      
      <div class="member-info">
        <div class="member-name">{{ member.name }}</div>
        <div class="member-name-ko">{{ member.name_ko }}</div>
        <div class="member-position">{{ member.position }}</div>
        <div class="member-research">{{ member.affiliation }}</div>
        
        <div class="social-links">
          {% if member.github and member.github != "" %}
            <a href="{{ member.github }}" target="_blank" class="social-link github">
              <i class="fab fa-github"></i>
            </a>
          {% else %}
            <span class="social-link disabled">
              <i class="fab fa-github"></i>
            </span>
          {% endif %}
          
          {% if member.linkedin and member.linkedin != "" %}
            <a href="{{ member.linkedin }}" target="_blank" class="social-link linkedin">
              <i class="fab fa-linkedin-in"></i>
            </a>
          {% else %}
            <span class="social-link disabled">
              <i class="fab fa-linkedin-in"></i>
            </span>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

## Current Students {#students}

<div class="section-header">
  <h2 class="section-title">Current Students</h2>
  <p class="section-subtitle">M.S. Course Students</p>
</div>

<div class="row">
  {% for member in site.data.members.students.ms_students %}
  <div class="col-lg-6 col-md-12">
    <div class="member-card">
      <img src="{{ site.baseurl }}/{{ member.photo }}" 
           alt="{{ member.name }}" 
           class="member-photo"
           onerror="this.src='{{ site.baseurl }}/assets/img/members/placeholder.svg'">
      
      <div class="member-info">
        <div class="member-name">{{ member.name }}</div>
        <div class="member-name-ko">{{ member.name_ko }}</div>
        <div class="member-research">{{ member.research }}</div>
        
        {% if member.achievements and member.achievements.size > 0 %}
        <div class="member-achievements">
          {% for achievement in member.achievements %}
            <span class="achievement-badge">{{ achievement }}</span>
          {% endfor %}
        </div>
        {% endif %}
        
        <div class="social-links">
          {% if member.github and member.github != "" %}
            <a href="{{ member.github }}" target="_blank" class="social-link github">
              <i class="fab fa-github"></i>
            </a>
          {% else %}
            <span class="social-link disabled">
              <i class="fab fa-github"></i>
            </span>
          {% endif %}
          
          {% if member.linkedin and member.linkedin != "" %}
            <a href="{{ member.linkedin }}" target="_blank" class="social-link linkedin">
              <i class="fab fa-linkedin-in"></i>
            </a>
          {% else %}
            <span class="social-link disabled">
              <i class="fab fa-linkedin-in"></i>
            </span>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<div class="section-header">
  <h3 class="section-title">Interns</h3>
  <p class="section-subtitle">Undergraduate Research Assistants</p>
</div>

<div class="row">
  {% for member in site.data.members.students.interns %}
  <div class="col-lg-6 col-md-12">
    <div class="member-card">
      <img src="{{ site.baseurl }}/{{ member.photo }}" 
           alt="{{ member.name }}" 
           class="member-photo"
           onerror="this.src='{{ site.baseurl }}/assets/img/members/placeholder.svg'">
      
      <div class="member-info">
        <div class="member-name">{{ member.name }}</div>
        <div class="member-name-ko">{{ member.name_ko }}</div>
        <div class="member-research">{{ member.research }}</div>
        
        <div class="social-links">
          {% if member.github and member.github != "" %}
            <a href="{{ member.github }}" target="_blank" class="social-link github">
              <i class="fab fa-github"></i>
            </a>
          {% else %}
            <span class="social-link disabled">
              <i class="fab fa-github"></i>
            </span>
          {% endif %}
          
          {% if member.linkedin and member.linkedin != "" %}
            <a href="{{ member.linkedin }}" target="_blank" class="social-link linkedin">
              <i class="fab fa-linkedin-in"></i>
            </a>
          {% else %}
            <span class="social-link disabled">
              <i class="fab fa-linkedin-in"></i>
            </span>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

## Alumni {#alumni}

<div class="section-header">
  <h2 class="section-title">Recent Achievements</h2>
  <p class="section-subtitle">Major Awards & Recognition</p>
</div>

<div class="achievements-section">
  {% for achievement in site.data.members.alumni.achievements %}
  <div class="achievement-item">
    <div class="achievement-title">{{ achievement.title }}</div>
    <div class="achievement-venue">{{ achievement.venue }}</div>
    {% if achievement.members and achievement.members.size > 0 %}
    <div class="achievement-members">
      Contributors: {{ achievement.members | join: ", " }}
    </div>
    {% endif %}
  </div>
  {% endfor %}
</div>

---

**Research Lab:** Reality Lab, Global School of Media, College of IT, Soongsil University  
**Principal Investigator:** Prof. Heewon Kim