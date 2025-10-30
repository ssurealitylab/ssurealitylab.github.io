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
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: white;
  height: 100%;
  position: relative;
}

.member-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.member-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto 15px;
  border: 4px solid #f8f9fa;
  transition: border-color 0.3s ease;
}

.member-card:hover .member-photo {
  border-color: #007bff;
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

.member-email {
  color: #495057;
  font-size: 0.85em;
  margin-bottom: 8px;
  line-height: 1.4;
  font-weight: 500;
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
  justify-content: center;
  gap: 10px;
  position: relative;
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

.social-link.email {
  background-color: #d44638;
  cursor: pointer;
}

.social-link.email:hover {
  background-color: #b23121;
  transform: scale(1.1);
}

.social-link.bio {
  background-color: #28a745;
}

.social-link.bio:hover {
  background-color: #218838;
  transform: scale(1.1);
}

.social-link.scholar {
  background-color: #4285f4;
}

.social-link.scholar:hover {
  background-color: #357ae8;
  transform: scale(1.1);
}

.social-link.disabled {
  background-color: #dee2e6;
  color: #6c757d;
  cursor: not-allowed;
}

.member-university {
  color: #6c757d;
  font-size: 0.85em;
  margin-bottom: 10px;
  line-height: 1.4;
}

.email-copied-tooltip {
  position: absolute;
  bottom: -35px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.8em;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  z-index: 1000;
  animation: tooltipFadeIn 0.2s ease-out;
  pointer-events: none;
}

.email-copied-tooltip::before {
  content: '';
  position: absolute;
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 6px solid #667eea;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
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

.faculty-card-clickable {
  cursor: pointer;
}

.faculty-card-clickable:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

.external-scholar-icon {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 35px;
  height: 35px;
  background-color: #4285f4;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  z-index: 10;
}

.external-scholar-icon:hover {
  background-color: #357ae8;
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(66, 133, 244, 0.4);
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
  <div class="col-lg-4 col-md-6 col-sm-12">
    <div class="member-card faculty-card-clickable" onclick="window.open('{{ member.bio }}', '_blank')">
      {% if member.scholar and member.scholar != "" %}
        <a href="{{ member.scholar }}" target="_blank" class="external-scholar-icon" onclick="event.stopPropagation()" title="Google Scholar Profile">
          <i class="fas fa-graduation-cap"></i>
        </a>
      {% endif %}

      <img src="{{ site.baseurl }}/{{ member.photo }}"
           alt="{{ member.name }}"
           class="member-photo"
           onerror="this.src='{{ site.baseurl }}/assets/img/members/placeholder.svg'">

      <div class="member-name">{{ member.name }}</div>
      <div class="member-name-ko">{{ member.name_ko }}</div>
      <div class="member-position">{{ member.position }}</div>
      <div class="member-research">{{ member.affiliation }}</div>
      {% if member.affiliation_detail %}
      <div class="member-university">
        {% for detail in member.affiliation_detail %}
          {{ detail }}<br>
        {% endfor %}
      </div>
      {% endif %}
      {% if member.phone %}
      <div class="member-email">Phone: {{ member.phone }}</div>
      {% endif %}
      {% if member.email %}
      <div class="member-email">E-mail: {{ member.email }}</div>
      {% endif %}

      <div class="social-links">
        {% if member.email and member.email != "" %}
          <span class="social-link email" onclick="event.stopPropagation(); copyEmail('{{ member.email }}', event)">
            <i class="fas fa-envelope"></i>
          </span>
        {% else %}
          <span class="social-link disabled">
            <i class="fas fa-envelope"></i>
          </span>
        {% endif %}

        {% if member.github and member.github != "" %}
          <a href="{{ member.github }}" target="_blank" class="social-link github" onclick="event.stopPropagation()">
            <i class="fab fa-github"></i>
          </a>
        {% endif %}

        {% if member.linkedin and member.linkedin != "" %}
          <a href="{{ member.linkedin }}" target="_blank" class="social-link linkedin" onclick="event.stopPropagation()">
            <i class="fab fa-linkedin-in"></i>
          </a>
        {% endif %}
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
  <div class="col-lg-4 col-md-6 col-sm-12">
    <div class="member-card">
      <img src="{{ site.baseurl }}/{{ member.photo }}" 
           alt="{{ member.name }}" 
           class="member-photo"
           onerror="this.src='{{ site.baseurl }}/assets/img/members/placeholder.svg'">
      
      <div class="member-name">{{ member.name }}</div>
      <div class="member-name-ko">{{ member.name_ko }}</div>
      {% if member.email %}
      <div class="member-email">{{ member.email }}</div>
      {% endif %}
      {% if member.university %}
      <div class="member-university">{{ member.university }}</div>
      {% endif %}
      <div class="member-research">{{ member.research }}</div>

      {% if member.achievements and member.achievements.size > 0 %}
      <div class="member-achievements">
        {% for achievement in member.achievements %}
          <span class="achievement-badge">{{ achievement }}</span>
        {% endfor %}
      </div>
      {% endif %}

      <div class="social-links">
        {% if member.email and member.email != "" %}
          <span class="social-link email" onclick="copyEmail('{{ member.email }}', event)">
            <i class="fas fa-envelope"></i>
          </span>
        {% else %}
          <span class="social-link disabled">
            <i class="fas fa-envelope"></i>
          </span>
        {% endif %}

        {% if member.github and member.github != "" %}
          <a href="{{ member.github }}" target="_blank" class="social-link github">
            <i class="fab fa-github"></i>
          </a>
        {% endif %}

        {% if member.linkedin and member.linkedin != "" %}
          <a href="{{ member.linkedin }}" target="_blank" class="social-link linkedin">
            <i class="fab fa-linkedin-in"></i>
          </a>
        {% endif %}
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
  <div class="col-lg-4 col-md-6 col-sm-12">
    <div class="member-card">
      <img src="{{ site.baseurl }}/{{ member.photo }}" 
           alt="{{ member.name }}" 
           class="member-photo"
           onerror="this.src='{{ site.baseurl }}/assets/img/members/placeholder.svg'">
      
      <div class="member-name">{{ member.name }}</div>
      <div class="member-name-ko">{{ member.name_ko }}</div>
      {% if member.email %}
      <div class="member-email">{{ member.email }}</div>
      {% endif %}
      {% if member.university %}
      <div class="member-university">{{ member.university }}</div>
      {% endif %}
      <div class="member-research">{{ member.research }}</div>

      <div class="social-links">
        {% if member.email and member.email != "" %}
          <span class="social-link email" onclick="copyEmail('{{ member.email }}', event)">
            <i class="fas fa-envelope"></i>
          </span>
        {% else %}
          <span class="social-link disabled">
            <i class="fas fa-envelope"></i>
          </span>
        {% endif %}

        {% if member.github and member.github != "" %}
          <a href="{{ member.github }}" target="_blank" class="social-link github">
            <i class="fab fa-github"></i>
          </a>
        {% endif %}

        {% if member.linkedin and member.linkedin != "" %}
          <a href="{{ member.linkedin }}" target="_blank" class="social-link linkedin">
            <i class="fab fa-linkedin-in"></i>
          </a>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<script>
function copyEmail(email, event) {
  // Create a temporary textarea element
  const textarea = document.createElement('textarea');
  textarea.value = email;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();

  try {
    // Copy to clipboard
    document.execCommand('copy');

    // Show tooltip below the clicked icon
    showEmailTooltip(event.currentTarget);
  } catch (err) {
    console.error('Failed to copy email:', err);
  }

  document.body.removeChild(textarea);
}

function showEmailTooltip(element) {
  // Remove any existing tooltip
  const existingTooltip = document.querySelector('.email-copied-tooltip');
  if (existingTooltip) {
    existingTooltip.remove();
  }

  // Find the parent social-links container
  const socialLinks = element.closest('.social-links');
  if (!socialLinks) return;

  // Create new tooltip
  const tooltip = document.createElement('div');
  tooltip.className = 'email-copied-tooltip';
  tooltip.textContent = '이메일이 복사되었습니다';

  // Append to social-links container
  socialLinks.appendChild(tooltip);

  // Remove tooltip after 2 seconds
  setTimeout(() => {
    tooltip.remove();
  }, 2000);
}
</script>

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