---
layout: page
title: Courses
---

<div class="courses-container">

<h2 class="section-title">학부 과정 (Undergraduate Courses)</h2>

<table class="course-table">
  <thead>
    <tr>
      <th>학년/학기</th>
      <th>과목명</th>
      <th>과목 내용</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="year-cell">-</td>
      <td class="course-name">
        <strong>데이터사이언스</strong><br>
        <span class="course-name-en">Data Science</span>
      </td>
      <td class="course-content">
        • 빅데이터 분석 및 머신러닝 기초<br>
        • 통계적 데이터 분석 방법론<br>
        • Python을 활용한 데이터 처리
      </td>
    </tr>
    <tr>
      <td class="year-cell">-</td>
      <td class="course-name">
        <strong>영상처리및실습</strong><br>
        <span class="course-name-en">Image Processing and Practice</span>
      </td>
      <td class="course-content">
        • 디지털 영상처리 이론 및 실습<br>
        • OpenCV를 활용한 영상처리 기법<br>
        • 컴퓨터 비전 기초
      </td>
    </tr>
    <tr>
      <td class="year-cell">-</td>
      <td class="course-name">
        <strong>미디어GAN</strong><br>
        <span class="course-name-en">Media GAN</span>
      </td>
      <td class="course-content">
        • 생성적 적대 신경망 이론<br>
        • 이미지 및 비디오 생성 모델<br>
        • 창작 AI 및 미디어 응용
      </td>
    </tr>
    <tr>
      <td class="year-cell">-</td>
      <td class="course-name">
        <strong>컴퓨터비전</strong><br>
        <span class="course-name-en">Computer Vision</span>
      </td>
      <td class="course-content">
        • 컴퓨터 비전 기초 이론<br>
        • 객체 검출 및 인식<br>
        • 영상 분류 및 분할
      </td>
    </tr>
    <tr>
      <td class="year-cell">-</td>
      <td class="course-name">
        <strong>기계학습</strong><br>
        <span class="course-name-en">Machine Learning</span>
      </td>
      <td class="course-content">
        • 머신러닝 알고리즘 기초<br>
        • 지도학습 및 비지도학습<br>
        • 딥러닝 기초
      </td>
    </tr>
  </tbody>
</table>

<h2 class="section-title graduate-title">대학원 과정 (Graduate Course)</h2>

<table class="course-table graduate-table">
  <thead>
    <tr>
      <th>과목명</th>
      <th>과목 내용</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="course-name">
        <strong>컴퓨터비전특론</strong><br>
        <span class="course-name-en">Advanced Computer Vision</span>
      </td>
      <td class="course-content">
        • 최신 컴퓨터 비전 연구 동향<br>
        • 딥러닝 기반 비전 시스템<br>
        • 연구 논문 분석 및 구현
      </td>
    </tr>
  </tbody>
</table>

<div class="course-info">
  <p><strong>Location:</strong> Global School of Media, Soongsil University, Seoul, Republic of Korea</p>
  <p><strong>Instructor:</strong> Prof. Heewon Kim</p>
</div>

</div>

<style>
.courses-container {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 30px;
  margin-top: 50px;
  padding-bottom: 10px;
  border-bottom: 2px solid #3b82f6;
}

.section-title:first-of-type {
  margin-top: 0;
}

.graduate-title {
  border-bottom-color: #8b5cf6;
}

.course-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 40px;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.course-table thead {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.course-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  color: #475569;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.course-table td {
  padding: 20px 15px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.course-table tbody tr:last-child td {
  border-bottom: none;
}

.course-table tbody tr:hover {
  background: #f8fafc;
}

.year-cell {
  font-weight: 600;
  color: #3b82f6;
  white-space: nowrap;
  width: 130px;
  font-size: 0.95rem;
}

.course-name {
  width: 250px;
}

.course-name strong {
  font-size: 1.05rem;
  color: #1e293b;
  display: block;
  margin-bottom: 5px;
}

.course-name-en {
  color: #64748b;
  font-size: 0.9rem;
  font-style: italic;
}

.course-content {
  color: #475569;
  font-size: 0.95rem;
  line-height: 1.8;
}

.graduate-table thead {
  background: #faf5ff;
  border-bottom-color: #c084fc;
}

.graduate-table .year-cell {
  color: #8b5cf6;
}

.course-info {
  margin-top: 50px;
  padding: 25px;
  background: #f8fafc;
  border-left: 4px solid #3b82f6;
  border-radius: 4px;
}

.course-info p {
  margin: 10px 0;
  color: #475569;
  font-size: 0.95rem;
}

.course-info strong {
  color: #1e293b;
}

/* Responsive */
@media (max-width: 768px) {
  .courses-container {
    padding: 20px 10px;
  }

  .section-title {
    font-size: 1.4rem;
  }

  .course-table {
    font-size: 0.85rem;
  }

  .course-table th,
  .course-table td {
    padding: 12px 10px;
  }

  .year-cell {
    font-size: 0.85rem;
  }

  .course-name strong {
    font-size: 0.95rem;
  }

  .course-name-en {
    font-size: 0.8rem;
  }

  .course-content {
    font-size: 0.85rem;
  }
}

@media (max-width: 576px) {
  .course-table thead {
    display: none;
  }

  .course-table,
  .course-table tbody,
  .course-table tr,
  .course-table td {
    display: block;
    width: 100%;
  }

  .course-table tr {
    margin-bottom: 20px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
  }

  .course-table td {
    border-bottom: 1px solid #e2e8f0;
    padding: 15px;
  }

  .course-table td:last-child {
    border-bottom: none;
  }

  .year-cell {
    background: #eff6ff;
    font-size: 0.9rem;
    text-align: center;
    padding: 12px;
  }

  .course-name {
    width: 100%;
    background: #f8fafc;
  }
}
</style>