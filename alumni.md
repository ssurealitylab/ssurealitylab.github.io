---
layout: page
title: Alumni
---

# Alumni

## Former Research Interns

<div class="members-grid">
  {% for alumnus in site.data.members.alumni.former_interns %}
  <div class="member-card">
    <div class="member-photo">
      <img src="{{ alumnus.photo }}" alt="{{ alumnus.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
    </div>
    <div class="member-info">
      <h3 class="member-name">{{ alumnus.name }}</h3>
      {% if alumnus.name_ko %}
      <p class="member-name-ko">{{ alumnus.name_ko }}</p>
      {% endif %}
      {% if alumnus.university %}
      <p class="member-university">{{ alumnus.university }}</p>
      {% endif %}
      {% if alumnus.research %}
      <p class="member-research">{{ alumnus.research }}</p>
      {% endif %}
      {% if alumnus.period %}
      <p class="member-period">{{ alumnus.period }}</p>
      {% endif %}
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

.member-university {
  font-size: 0.85rem;
  color: #495057;
  margin-bottom: 10px;
  line-height: 1.4;
  font-weight: 500;
}

.member-research {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 10px;
  line-height: 1.4;
}

.member-period {
  font-size: 0.85rem;
  color: #28a745;
  font-weight: 600;
  background: #f8f9fa;
  padding: 5px 10px;
  border-radius: 15px;
  display: inline-block;
  margin-top: 5px;
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