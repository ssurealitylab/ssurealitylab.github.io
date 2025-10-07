---
layout: page
title: Students
---

# Students

## Master's Students

<div class="members-grid">
  {% for student in site.data.members.students.ms_students %}
  <div class="member-card">
    <div class="member-photo">
      <img src="{{ student.photo }}" alt="{{ student.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
    </div>
    <div class="member-info">
      <h3 class="member-name">{{ student.name }}</h3>
      {% if student.name_ko %}
      <p class="member-name-ko">{{ student.name_ko }}</p>
      {% endif %}
      {% if student.research %}
      <p class="member-research">{{ student.research }}</p>
      {% endif %}
      {% if student.achievements and student.achievements.size > 0 %}
      <div class="member-achievements">
        <h4>Achievements:</h4>
        <ul>
        {% for achievement in student.achievements %}
          <li>{{ achievement }}</li>
        {% endfor %}
        </ul>
      </div>
      {% endif %}
      <div class="member-social">
        {% if student.github and student.github != "" %}
        <a href="{{ student.github }}" target="_blank" title="GitHub">
          <i class="fab fa-github"></i>
        </a>
        {% endif %}
        {% if student.linkedin and student.linkedin != "" %}
        <a href="{{ student.linkedin }}" target="_blank" title="LinkedIn">
          <i class="fab fa-linkedin"></i>
        </a>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>

## Research Interns

<div class="members-grid">
  {% for intern in site.data.members.students.interns %}
  <div class="member-card">
    <div class="member-photo">
      <img src="{{ intern.photo }}" alt="{{ intern.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
    </div>
    <div class="member-info">
      <h3 class="member-name">{{ intern.name }}</h3>
      {% if intern.name_ko %}
      <p class="member-name-ko">{{ intern.name_ko }}</p>
      {% endif %}
      {% if intern.research %}
      <p class="member-research">{{ intern.research }}</p>
      {% endif %}
      <div class="member-social">
        {% if intern.github and intern.github != "" %}
        <a href="{{ intern.github }}" target="_blank" title="GitHub">
          <i class="fab fa-github"></i>
        </a>
        {% endif %}
        {% if intern.linkedin and intern.linkedin != "" %}
        <a href="{{ intern.linkedin }}" target="_blank" title="LinkedIn">
          <i class="fab fa-linkedin"></i>
        </a>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<style>
.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 50px;
  padding: 20px 0;
}

.member-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.member-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.member-photo {
  margin-bottom: 20px;
}

.member-photo img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f8f9fa;
}

.member-name {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
}

.member-name-ko {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 10px;
  font-style: italic;
}

.member-research {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 15px;
  line-height: 1.4;
}

.member-achievements {
  text-align: left;
  margin-bottom: 15px;
}

.member-achievements h4 {
  font-size: 0.9rem;
  color: #2c3e50;
  margin-bottom: 8px;
  font-weight: 600;
}

.member-achievements ul {
  font-size: 0.85rem;
  color: #495057;
  margin: 0;
  padding-left: 20px;
}

.member-achievements li {
  margin-bottom: 3px;
}

.member-social {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.member-social a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
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

h2 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 20px;
  margin-top: 40px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

h2:first-of-type {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .members-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .member-card {
    padding: 20px;
  }
  
  .member-photo img {
    width: 100px;
    height: 100px;
  }
  
  .member-name {
    font-size: 1.2rem;
  }
}
</style>