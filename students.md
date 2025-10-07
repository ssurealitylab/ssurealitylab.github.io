---
layout: page
title: Students
---

# Students

## Master's Students

<div class="members-grid">
  {% for student in site.data.members.students.ms_students %}
  <div class="member-card clickable-card" onclick="openMemberModal('{{ student.name | slugify }}')">
    <div class="member-photo">
      <img src="{{ student.photo }}" alt="{{ student.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
    </div>
    <div class="member-info">
      <h3 class="member-name">{{ student.name }}</h3>
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
        <a href="#" onclick="event.preventDefault(); event.stopPropagation()" title="GitHub">
          <i class="fab fa-github"></i>
        </a>
        <a href="#" onclick="event.preventDefault(); event.stopPropagation()" title="LinkedIn">
          <i class="fab fa-linkedin"></i>
        </a>
      </div>
    </div>
  </div>

  <!-- Modal for {{ student.name }} -->
  <div id="modal-{{ student.name | slugify }}" class="member-modal">
    <div class="modal-content">
      <span class="close-modal" onclick="closeMemberModal('{{ student.name | slugify }}')">&times;</span>
      <div class="modal-photo">
        <img src="{{ student.photo }}" alt="{{ student.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
      </div>
      <div class="modal-info">
        <h2 class="modal-name">{{ student.name }}</h2>
        {% if student.research %}
        <p class="modal-research"><strong>Research:</strong> {{ student.research }}</p>
        {% endif %}
        {% if student.achievements and student.achievements.size > 0 %}
        <div class="modal-achievements">
          <strong>Achievements:</strong>
          <ul>
          {% for achievement in student.achievements %}
            <li>{{ achievement }}</li>
          {% endfor %}
          </ul>
        </div>
        {% endif %}
        <div class="modal-social">
          <a href="#" onclick="event.preventDefault()" title="GitHub">
            <i class="fab fa-github"></i>
          </a>
          <a href="#" onclick="event.preventDefault()" title="LinkedIn">
            <i class="fab fa-linkedin"></i>
          </a>
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

## Research Interns

<div class="members-grid">
  {% for intern in site.data.members.students.interns %}
  <div class="member-card clickable-card" onclick="openMemberModal('intern-{{ intern.name | slugify }}')">
    <div class="member-photo">
      <img src="{{ intern.photo }}" alt="{{ intern.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
    </div>
    <div class="member-info">
      <h3 class="member-name">{{ intern.name }}</h3>
      {% if intern.research %}
      <p class="member-research">{{ intern.research }}</p>
      {% endif %}
      <div class="member-social">
        <a href="#" onclick="event.preventDefault(); event.stopPropagation()" title="GitHub">
          <i class="fab fa-github"></i>
        </a>
        <a href="#" onclick="event.preventDefault(); event.stopPropagation()" title="LinkedIn">
          <i class="fab fa-linkedin"></i>
        </a>
      </div>
    </div>
  </div>

  <!-- Modal for {{ intern.name }} -->
  <div id="modal-intern-{{ intern.name | slugify }}" class="member-modal">
    <div class="modal-content">
      <span class="close-modal" onclick="closeMemberModal('intern-{{ intern.name | slugify }}')">&times;</span>
      <div class="modal-photo">
        <img src="{{ intern.photo }}" alt="{{ intern.name }}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmNGY2Ii8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzllYTNhOCIvPgo8cGF0aCBkPSJNNjAgMTYwYzAtMjIuMDkgMTcuOTEtNDAgNDAtNDBzNDAgMTcuOTEgNDAgNDB2MjBINjB2LTIweiIgZmlsbD0iIzllYTNhOCIvPgo8L3N2Zz4K'">
      </div>
      <div class="modal-info">
        <h2 class="modal-name">{{ intern.name }}</h2>
        {% if intern.research %}
        <p class="modal-research"><strong>Research:</strong> {{ intern.research }}</p>
        {% endif %}
        <div class="modal-social">
          <a href="#" onclick="event.preventDefault()" title="GitHub">
            <i class="fab fa-github"></i>
          </a>
          <a href="#" onclick="event.preventDefault()" title="LinkedIn">
            <i class="fab fa-linkedin"></i>
          </a>
        </div>
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

.clickable-card {
  cursor: pointer;
}

.clickable-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

/* Modal Styles */
.member-modal {
  display: none;
  position: fixed;
  z-index: 9999;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  width: 450px;
  height: 450px;
  border-radius: 20px;
  padding: 40px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.close-modal {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 28px;
  font-weight: bold;
  color: #999;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-modal:hover {
  color: #333;
}

.modal-photo {
  margin-bottom: 25px;
}

.modal-photo img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #f8f9fa;
}

.modal-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 15px;
}

.modal-research {
  font-size: 1rem;
  color: #6c757d;
  margin-bottom: 20px;
  line-height: 1.5;
}

.modal-achievements {
  text-align: left;
  margin-bottom: 25px;
  width: 100%;
}

.modal-achievements strong {
  color: #2c3e50;
  font-size: 1rem;
  display: block;
  margin-bottom: 10px;
}

.modal-achievements ul {
  margin: 0;
  padding-left: 20px;
}

.modal-achievements li {
  color: #495057;
  font-size: 0.9rem;
  margin-bottom: 5px;
  line-height: 1.4;
}

.modal-social {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.modal-social a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #f8f9fa;
  color: #6c757d;
  text-decoration: none;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.modal-social a:hover {
  background: #3498db;
  color: white;
  transform: translateY(-3px);
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

<script>
function openMemberModal(memberId) {
  const modal = document.getElementById('modal-' + memberId);
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
  }
}

function closeMemberModal(memberId) {
  const modal = document.getElementById('modal-' + memberId);
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore scrolling
  }
}

// Close modal when clicking outside of it
document.addEventListener('click', function(event) {
  if (event.target.classList.contains('member-modal')) {
    event.target.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
});

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    const modals = document.querySelectorAll('.member-modal');
    modals.forEach(modal => {
      if (modal.style.display === 'flex') {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
      }
    });
  }
});
</script>