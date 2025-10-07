---
layout: page
title: International Publications
---

{% include sidl-script.html %}

<!-- Publications Header -->
<section class="publications-header text-center py-5">
  <div class="container">
    <h1 class="section-heading text-uppercase">International Publications</h1>
    <h3 class="section-subheading text-muted">Global research achievements and scholarly contributions</h3>
  </div>
</section>

<!-- Publications Content -->
<section class="publications-content py-5">
  <div class="container">
    
    <!-- International Section -->
    <div class="category-section mb-5">
      <div class="row">
        <div class="col-12">
          <div class="category-header d-flex align-items-center mb-4">
            <div class="category-badge international-badge">2025</div>
            <div class="category-line flex-grow-1"></div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <!-- SIDL Benchmark - AAAI 2025 -->
        <div class="col-lg-4 mb-4">
          <div class="publication-card paper-card" onclick="openPublicationModal('sidl')" style="cursor: pointer;">
            <div class="placeholder-img d-flex align-items-center justify-content-center">
              <i class="fas fa-database fa-2x text-muted"></i>
            </div>
            <div class="card-body">
              <h5 class="card-title">SIDL Benchmark Dataset</h5>
              <p class="card-subtitle">AAAI 2025 (Accepted)</p>
              <p class="card-text">Smartphone Images with Dirty Lenses - A novel dataset for image restoration through contaminated lenses.</p>
              <div class="publication-badge">🎉 AAAI25 Accept!</div>
            </div>
          </div>
        </div>
        
        <!-- BMVC 2025 -->
        <div class="col-lg-4 mb-4">
          <div class="publication-card paper-card" onclick="openPublicationModal('bmvc')" style="cursor: pointer;">
            <div class="placeholder-img d-flex align-items-center justify-content-center">
              <i class="fas fa-eye fa-2x text-muted"></i>
            </div>
            <div class="card-body">
              <h5 class="card-title">Computer Vision Research</h5>
              <p class="card-subtitle">BMVC 2025 (Accepted)</p>
              <p class="card-text">Youngjae Choi, Hyunsuh Koh, Hojae Jeong, ByungKwan Chae</p>
            </div>
          </div>
        </div>
        
        <!-- CVPR 2025 -->
        <div class="col-lg-4 mb-4">
          <div class="publication-card paper-card" onclick="openPublicationModal('cvpr')" style="cursor: pointer;">
            <div class="placeholder-img d-flex align-items-center justify-content-center">
              <i class="fas fa-brain fa-2x text-muted"></i>
            </div>
            <div class="card-body">
              <h5 class="card-title">Advanced AI Research</h5>
              <p class="card-subtitle">CVPR 2025 (Accepted)</p>
              <p class="card-text">Sangmin Lee, Sungyong Park</p>
            </div>
          </div>
        </div>
        
        <!-- ARNOLD Challenge -->
        <div class="col-lg-4 mb-4">
          <div class="publication-card challenge-card" onclick="openPublicationModal('arnold')" style="cursor: pointer;">
            <div class="placeholder-img d-flex align-items-center justify-content-center">
              <i class="fas fa-trophy fa-2x text-muted"></i>
            </div>
            <div class="card-body">
              <h5 class="card-title">ARNOLD Challenge</h5>
              <p class="card-subtitle">CVPR 2025 Embodied AI Workshop</p>
              <p class="card-text">Reality Lab Team achieved 1st place in the ARNOLD Challenge</p>
              <div class="publication-badge">🥇 1st Place</div>
            </div>
          </div>
        </div>
        
        <!-- Placeholder 1 -->
        <div class="col-lg-4 mb-4">
          <div class="publication-card placeholder-card">
            <div class="placeholder-img d-flex align-items-center justify-content-center">
              <i class="fas fa-plus fa-2x text-muted"></i>
            </div>
            <div class="card-body">
              <h5 class="card-title">More International Publications</h5>
              <p class="card-subtitle">Coming Soon</p>
              <p class="card-text">Additional international publications will be updated.</p>
            </div>
          </div>
        </div>
        
        <!-- Placeholder 2 -->
        <div class="col-lg-4 mb-4">
          <div class="publication-card placeholder-card">
            <div class="placeholder-img d-flex align-items-center justify-content-center">
              <i class="fas fa-plus fa-2x text-muted"></i>
            </div>
            <div class="card-body">
              <h5 class="card-title">More International Publications</h5>
              <p class="card-subtitle">Coming Soon</p>
              <p class="card-text">Additional international publications will be updated.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</section>

<!-- Research Focus -->
<section class="py-5 bg-light">
  <div class="container text-center">
    <div class="row">
      <div class="col-lg-10 mx-auto">
        <h3 class="text-uppercase mb-4">International Research Focus</h3>
        <div class="row">
          <div class="col-md-6">
            <h5>Global Conferences</h5>
            <ul class="list-unstyled text-left">
              <li><i class="fas fa-trophy text-warning"></i> CVPR, BMVC, AAAI</li>
              <li><i class="fas fa-robot text-primary"></i> ICRA, IROS, RSS</li>
              <li><i class="fas fa-brain text-success"></i> NeurIPS, ICML, ICLR</li>
              <li><i class="fas fa-eye text-info"></i> ICCV, ECCV, WACV</li>
            </ul>
          </div>
          <div class="col-md-6">
            <h5>Recent Achievements</h5>
            <ul class="list-unstyled text-left">
              <li><i class="fas fa-trophy text-warning"></i> ARNOLD Challenge 1st Place</li>
              <li><i class="fas fa-file-alt text-info"></i> AAAI 2025 Paper Acceptance</li>
              <li><i class="fas fa-file-alt text-info"></i> CVPR 2025 Paper Acceptance</li>
              <li><i class="fas fa-file-alt text-info"></i> BMVC 2025 Paper Acceptance</li>
            </ul>
          </div>
        </div>
        <hr class="my-4">
        <p class="text-muted">
          <strong>Reality Lab</strong> | Global School of Media, College of IT, Soongsil University<br>
          <strong>Principal Investigator:</strong> Prof. Heewon Kim
        </p>
      </div>
    </div>
  </div>
</section>

<style>
/* Publications Content Styles */
.publications-header {
  background: linear-gradient(90deg, rgba(231, 76, 60, 0.1) 0%, rgba(192, 57, 43, 0.1) 100%);
}

/* Category Section */
.category-section {
  margin-bottom: 4rem;
}

.category-header {
  margin-bottom: 2rem;
}

.category-badge {
  color: white;
  padding: 12px 24px;
  border-radius: 50px;
  font-size: 1.3rem;
  font-weight: bold;
  margin-right: 20px;
  min-width: 140px;
  text-align: center;
}

.international-badge {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.category-line {
  height: 3px;
  background: linear-gradient(90deg, #e74c3c, rgba(231, 76, 60, 0.1));
  border-radius: 2px;
}

/* Publication Cards */
.publication-card {
  border: none;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
  background: white;
  border: 3px solid transparent;
  position: relative;
}

.publication-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

/* Category-based Border Colors */
.challenge-card {
  border-color: #ffd700 !important;
}

.challenge-card:hover {
  border-color: #ffed4a !important;
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.3);
}

.paper-card {
  border-color: #3498db !important;
}

.paper-card:hover {
  border-color: #5dade2 !important;
  box-shadow: 0 8px 30px rgba(52, 152, 219, 0.3);
}

.research-card {
  border-color: #9b59b6 !important;
}

.research-card:hover {
  border-color: #bb8fce !important;
  box-shadow: 0 8px 30px rgba(155, 89, 182, 0.3);
}

/* Card Layout - All Uniform */
.publication-card .card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.publication-card .card-subtitle {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-bottom: 10px;
  font-weight: 500;
}

.publication-card .card-text {
  font-size: 0.9rem;
  color: #5a6c7d;
  line-height: 1.4;
}

/* Publication Badge */
.publication-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a52);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.8rem;
  box-shadow: 0 2px 10px rgba(255, 107, 107, 0.3);
}

/* Placeholder Card */
.placeholder-card {
  border: 2px dashed #bdc3c7 !important;
  background: #f8f9fa;
}

.placeholder-img {
  height: 150px;
  background: #ecf0f1;
  border-radius: 8px;
  margin: 15px;
}

/* Card Body Styling */
.card-body {
  padding: 1.25rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .category-badge {
    font-size: 1.1rem;
    padding: 10px 20px;
    min-width: 120px;
  }
  
  .placeholder-img {
    height: 120px;
    margin: 10px;
  }
  
  .card-body {
    padding: 1rem;
  }
}

@media (max-width: 576px) {
  .category-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .category-badge {
    margin-bottom: 15px;
    margin-right: 0;
  }
  
  .category-line {
    height: 2px;
  }
}

/* Modal Styles */
.publication-modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  z-index: 9999;
  justify-content: center;
  align-items: center;
}

.publication-modal.active {
  display: flex;
}

.publication-modal-content {
  background: white;
  border-radius: 15px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  margin: 2rem;
  width: 90vw;
  max-width: 90vw;
}

@media (min-width: 768px) {
  .publication-modal-content {
    width: 75vw;
    max-width: 75vw;
  }
}

@media (min-width: 1200px) {
  .publication-modal-content {
    width: 70vw;
    max-width: 70vw;
  }
}

.publication-modal-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid #eee;
}

.publication-modal-body {
  padding: 2rem;
}

.publication-modal-close {
  position: absolute;
  top: 20px;
  right: 25px;
  width: 40px;
  height: 40px;
  cursor: pointer;
  background: none;
  border: none;
  font-size: 30px;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.publication-modal-close:hover {
  color: #333;
}
</style>

<!-- Publication Modals -->

<!-- SIDL Benchmark Modal -->
<div class="publication-modal" id="sidl">
  <div class="publication-modal-content">
    <button class="publication-modal-close" onclick="closePublicationModal('sidl')">&times;</button>
    <div class="publication-modal-header">
      <h2 class="text-uppercase">SIDL Benchmark</h2>
      <p class="item-intro text-muted">Smartphone Images with Dirty Lenses Dataset</p>
    </div>
    <div class="publication-modal-body">
      <!-- Contamination Type Toggles -->
      <div class="text-center mb-4">
        <div class="btn-group btn-group-toggle" data-toggle="buttons" id="contaminantTypes">
          <label class="btn btn-outline-primary active">
            <input type="radio" name="contaminant" id="dust" value="dust" checked> Dust
          </label>
          <label class="btn btn-outline-primary">
            <input type="radio" name="contaminant" id="finger" value="finger"> Fingerprint
          </label>
          <label class="btn btn-outline-primary">
            <input type="radio" name="contaminant" id="scratch" value="scratch"> Scratch
          </label>
          <label class="btn btn-outline-primary">
            <input type="radio" name="contaminant" id="water" value="water"> Water
          </label>
        </div>
      </div>

      <!-- Image Comparison Container -->
      <div class="sidl-comparison-container mb-4" style="position: relative; max-width: 500px; margin: 0 auto;">
        <div class="sidl-image-wrapper" style="position: relative; width: 100%; height: 400px; overflow: hidden; border-radius: 8px; cursor: col-resize;">
          <!-- Target Image (Base) -->
          <img id="sidlTargetImage" class="sidl-image" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;" src="{{ site.baseurl }}/assets/img/sidl/dust/target/Case073_D.png" alt="Target Image">
          
          <!-- Input Image (Overlay with clip-path) -->
          <div id="sidlInputContainer" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; clip-path: inset(0 50% 0 0);">
            <img id="sidlInputImage" class="sidl-image" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;" src="{{ site.baseurl }}/assets/img/sidl/dust/input/Case073_D.png" alt="Input Image">
          </div>
          
          <!-- Vertical Divider Line -->
          <div id="sidlDivider" style="position: absolute; top: 0; left: 50%; width: 2px; height: 100%; background: white; z-index: 10; box-shadow: 0 0 4px rgba(0,0,0,0.3);"></div>
          
          <!-- Slider Handle -->
          <div id="sidlHandle" style="position: absolute; top: 50%; left: 50%; width: 20px; height: 20px; background: white; border-radius: 50%; transform: translate(-50%, -50%); z-index: 11; box-shadow: 0 0 4px rgba(0,0,0,0.3); cursor: col-resize;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 10px; color: #666;">⟷</div>
          </div>
        </div>
        
        <!-- Labels -->
        <div class="sidl-labels mt-2">
          <div class="row">
            <div class="col-6 text-center">
              <small class="text-muted"><strong>Input (Contaminated)</strong></small>
            </div>
            <div class="col-6 text-center">
              <small class="text-muted"><strong>Target (Restored)</strong></small>
            </div>
          </div>
        </div>
      </div>

      <p><strong>Description:</strong> A novel dataset designed to restore images captured through contaminated smartphone lenses with diverse real-world contaminants.</p>
      <p><strong>Technologies:</strong> Computer Vision, Image Restoration, Machine Learning, Dataset</p>
      <p><strong>Key Features:</strong></p>
      <ul>
        <li>300 static scenes with 1,588 degraded-clean image pairs</li>
        <li>Full ProRAW resolution (4032 × 3024, 12-bit DNG)</li>
        <li>4 contaminant types: fingerprints, dust, scratches, water drops</li>
        <li>Difficulty levels: Easy, Medium, Hard</li>
        <li>Comprehensive evaluation framework</li>
      </ul>
      <div class="text-center">
        <a href="https://sidl-benchmark.github.io/" target="_blank" class="btn btn-primary">
          <i class="fas fa-globe"></i> Visit Website
        </a>
        <button class="btn btn-secondary ml-2" onclick="closePublicationModal('sidl')" type="button">
          <i class="fas fa-times"></i> Close
        </button>
      </div>
    </div>
  </div>
</div>

<!-- BMVC 2025 Modal -->
<div class="publication-modal" id="bmvc">
  <div class="publication-modal-content">
    <button class="publication-modal-close" onclick="closePublicationModal('bmvc')">&times;</button>
    <div class="publication-modal-header">
      <h2 class="text-uppercase">BMVC 2025 Paper</h2>
      <p class="item-intro text-muted">Computer Vision Research Achievement</p>
    </div>
    <div class="publication-modal-body">
      <p><strong>Authors:</strong> Youngjae Choi, Hyunsuh Koh, Hojae Jeong, ByungKwan Chae</p>
      <p><strong>Conference:</strong> British Machine Vision Conference (BMVC) 2025</p>
      <p><strong>Status:</strong> Accepted</p>
      <p><strong>Description:</strong> Our research contribution in computer vision has been accepted to BMVC 2025, one of the leading conferences in computer vision and machine learning.</p>
      <p><strong>Research Areas:</strong></p>
      <ul>
        <li>Computer Vision</li>
        <li>Deep Learning</li>
        <li>Image Processing</li>
        <li>Machine Learning</li>
      </ul>
      <div class="text-center">
        <button class="btn btn-secondary" onclick="closePublicationModal('bmvc')" type="button">
          <i class="fas fa-times"></i> Close
        </button>
      </div>
    </div>
  </div>
</div>

<!-- CVPR 2025 Modal -->
<div class="publication-modal" id="cvpr">
  <div class="publication-modal-content">
    <button class="publication-modal-close" onclick="closePublicationModal('cvpr')">&times;</button>
    <div class="publication-modal-header">
      <h2 class="text-uppercase">CVPR 2025 Paper</h2>
      <p class="item-intro text-muted">Advanced AI Research Achievement</p>
    </div>
    <div class="publication-modal-body">
      <p><strong>Authors:</strong> Sangmin Lee, Sungyong Park</p>
      <p><strong>Conference:</strong> IEEE Conference on Computer Vision and Pattern Recognition (CVPR) 2025</p>
      <p><strong>Status:</strong> Accepted</p>
      <p><strong>Description:</strong> Our advanced AI research has been accepted to CVPR 2025, the premier conference in computer vision and pattern recognition.</p>
      <p><strong>Research Areas:</strong></p>
      <ul>
        <li>Computer Vision</li>
        <li>Pattern Recognition</li>
        <li>Artificial Intelligence</li>
        <li>Machine Learning</li>
      </ul>
      <div class="text-center">
        <button class="btn btn-secondary" onclick="closePublicationModal('cvpr')" type="button">
          <i class="fas fa-times"></i> Close
        </button>
      </div>
    </div>
  </div>
</div>

<!-- ARNOLD Challenge Modal -->
<div class="publication-modal" id="arnold">
  <div class="publication-modal-content">
    <button class="publication-modal-close" onclick="closePublicationModal('arnold')">&times;</button>
    <div class="publication-modal-header">
      <h2 class="text-uppercase">ARNOLD Challenge</h2>
      <p class="item-intro text-muted">1st Place Winner at CVPR 2025 Embodied AI Workshop</p>
    </div>
    <div class="publication-modal-body">
      <p><strong>Team:</strong> Reality Lab Team</p>
      <p><strong>Event:</strong> CVPR 2025 Embodied AI Workshop</p>
      <p><strong>Achievement:</strong> 1st Place 🥇</p>
      <p><strong>Description:</strong> Our team achieved first place in the ARNOLD Challenge, demonstrating excellence in embodied AI and robotics research.</p>
      <p><strong>Challenge Areas:</strong></p>
      <ul>
        <li>Embodied AI</li>
        <li>Robotics</li>
        <li>Navigation</li>
        <li>Human-Robot Interaction</li>
        <li>Computer Vision</li>
      </ul>
      <p><strong>Key Achievements:</strong></p>
      <ul>
        <li>First place among international teams</li>
        <li>Outstanding performance in navigation tasks</li>
        <li>Advanced AI-human interaction capabilities</li>
        <li>Real-world robotic system deployment</li>
      </ul>
      <div class="text-center">
        <button class="btn btn-secondary" onclick="closePublicationModal('arnold')" type="button">
          <i class="fas fa-times"></i> Close
        </button>
      </div>
    </div>
  </div>
</div>

<script>
function openPublicationModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }
}

function closePublicationModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("active");
    document.body.style.overflow = "";
  }
}

// Close modal when clicking outside content
document.addEventListener("click", function(event) {
  if (event.target.classList.contains("publication-modal")) {
    const modalId = event.target.id;
    closePublicationModal(modalId);
  }
});

// Close modal with Escape key
document.addEventListener("keydown", function(event) {
  if (event.key === "Escape") {
    const activeModal = document.querySelector(".publication-modal.active");
    if (activeModal) {
      closePublicationModal(activeModal.id);
    }
  }
});
</script>