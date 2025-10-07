---
layout: page
title: Faculty
---

# Faculty

<div class="faculty-container">
  {% for member in site.data.members.faculty %}
  <div class="faculty-card">
    <div class="member-photo">
      <img src="{{ member.photo }}" alt="{{ member.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
    </div>
    <div class="member-info">
      <h3 class="member-name">{{ member.name }}</h3>
      {% if member.name_ko %}
      <p class="member-name-ko">{{ member.name_ko }}</p>
      {% endif %}
      <p class="member-position">{{ member.position }}</p>
      <p class="member-affiliation">{{ member.affiliation }}</p>
      {% if member.email %}
      <p class="member-email">
        <i class="fas fa-envelope"></i> 
        <a href="mailto:{{ member.email }}">{{ member.email }}</a>
      </p>
      {% endif %}
      
      <div class="member-social">
        {% if member.github and member.github != "" %}
        <a href="{{ member.github }}" target="_blank" title="GitHub">
          <i class="fab fa-github"></i>
        </a>
        {% endif %}
        {% if member.linkedin and member.linkedin != "" %}
        <a href="{{ member.linkedin }}" target="_blank" title="LinkedIn">
          <i class="fab fa-linkedin"></i>
        </a>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<style>
.faculty-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.faculty-card {
  display: flex;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 30px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.faculty-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.member-photo {
  flex-shrink: 0;
  margin-right: 30px;
}

.member-photo img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #f8f9fa;
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 5px;
}

.member-name-ko {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 10px;
  font-style: italic;
}

.member-position {
  font-size: 1.2rem;
  color: #3498db;
  font-weight: 600;
  margin-bottom: 10px;
}

.member-affiliation {
  font-size: 1rem;
  color: #6c757d;
  margin-bottom: 15px;
  line-height: 1.5;
}

.member-email {
  font-size: 1rem;
  margin-bottom: 20px;
}

.member-email i {
  color: #3498db;
  margin-right: 8px;
}

.member-email a {
  color: #2c3e50;
  text-decoration: none;
}

.member-email a:hover {
  color: #3498db;
  text-decoration: underline;
}

.member-social {
  display: flex;
  gap: 15px;
}

.member-social a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f8f9fa;
  color: #6c757d;
  text-decoration: none;
  transition: all 0.3s ease;
}

.member-social a:hover {
  background: #3498db;
  color: white;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .faculty-card {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }
  
  .member-photo {
    margin-right: 0;
    margin-bottom: 20px;
    align-self: center;
  }
  
  .member-photo img {
    width: 120px;
    height: 120px;
  }
  
  .member-name {
    font-size: 1.5rem;
  }
}
</style>