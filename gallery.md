---
layout: page
title: Gallery - Reality Lab | 갤러리 - 리얼리티랩
description: Photos from Reality Lab at Soongsil University — conferences, awards, seminars, robots, and lab life. 숭실대학교 김희원 교수 연구실 갤러리.
keywords: Reality Lab gallery, 리얼리티랩 갤러리, 연구실 사진, Soongsil University, 숭실대학교, 숭실대, SSU, CVPR, AAAI, KCCV, ARNOLD Challenge, lab photos, 김희원, Heewon Kim, 연구실 활동
image: /assets/img/header.png
---

{% assign episodes = site.data.gallery.episodes %}
{% assign photo_total = 0 %}
{% for ep in episodes %}{% assign photo_total = photo_total | plus: ep.photos.size %}{% endfor %}

<!-- Gallery Header -->
<section class="gallery-header text-center py-5">
  <div class="container">
    <h1 class="section-heading text-uppercase">Gallery</h1>
    <h3 class="section-subheading text-muted">Conferences, awards, seminars, robots, and lab life</h3>
    <p class="gallery-count">{{ episodes.size }} episodes · {{ photo_total }} photos</p>
    <p class="gallery-hint">Click an episode to browse its photos</p>
  </div>
</section>

<!-- Gallery Content -->
<section class="gallery-content py-5">
  <div class="container">
    <div class="gallery-grid">
      {% for ep in episodes %}
      <figure class="gallery-card" tabindex="0" role="button"
              data-episode="{{ forloop.index0 }}"
              aria-label="{{ ep.title | escape }}, {{ ep.photos.size }} photo{% if ep.photos.size != 1 %}s{% endif %}">
        <div class="gallery-card-img">
          <img src="{{ site.baseurl }}/{{ ep.photos[0].image }}" alt="{{ ep.title | escape }}" loading="lazy">
          {% if ep.photos.size > 1 %}
          <span class="gallery-badge" title="{{ ep.photos.size }} photos" aria-hidden="true">
            <span class="gallery-badge-n">{{ ep.photos.size }}</span><span class="gallery-badge-label">photos</span>
          </span>
          {% endif %}
        </div>
        <figcaption>
          <strong>{{ ep.title }}</strong>
          {% if ep.date %}<span class="gallery-date">{{ ep.date }}</span>{% endif %}
          {% if ep.description %}<span class="gallery-desc">{{ ep.description }}</span>{% endif %}
        </figcaption>
      </figure>
      {% endfor %}
    </div>
  </div>
</section>

<!-- Episode viewer -->
<div id="galleryViewer" class="gallery-viewer" role="dialog" aria-modal="true" aria-labelledby="galleryViewerTitle">
  <div class="gallery-viewer-backdrop" data-close></div>
  <div class="gallery-viewer-dialog" role="document">
    <button class="gallery-viewer-close" type="button" data-close aria-label="Close">&times;</button>
    <h2 id="galleryViewerTitle"></h2>
    <p id="galleryViewerMeta" class="gallery-viewer-meta"></p>

    <div class="gallery-stage">
      <button class="gallery-nav gallery-prev" type="button" aria-label="Previous photo">&#10094;</button>
      <img id="galleryStageImg" alt="">
      <button class="gallery-nav gallery-next" type="button" aria-label="Next photo">&#10095;</button>
    </div>

    <p id="galleryCaption" class="gallery-caption"></p>
    <div id="galleryThumbs" class="gallery-thumbs"></div>
  </div>
</div>

<script>
(function () {
  var EPISODES = {{ episodes | jsonify }};
  var BASE = "{{ site.baseurl }}";

  var viewer  = document.getElementById('galleryViewer');
  var titleEl = document.getElementById('galleryViewerTitle');
  var metaEl  = document.getElementById('galleryViewerMeta');
  var stage   = document.getElementById('galleryStageImg');
  var capEl   = document.getElementById('galleryCaption');
  var thumbs  = document.getElementById('galleryThumbs');

  var episode = null;   // the episode being viewed
  var index   = 0;      // which of its photos is on the stage

  function src(photo) { return BASE + '/' + photo.image; }

  function show(i) {
    if (!episode) return;
    index = (i + episode.photos.length) % episode.photos.length;
    var photo = episode.photos[index];
    stage.src = src(photo);
    stage.alt = photo.caption || episode.title;
    capEl.textContent = photo.caption || '';
    // a single-photo episode has nothing to page through
    var many = episode.photos.length > 1;
    metaEl.textContent = [episode.date, episode.description].filter(Boolean).join(' · ')
      + (many ? (episode.date || episode.description ? '  ·  ' : '') + (index + 1) + ' / ' + episode.photos.length : '');
    Array.prototype.forEach.call(thumbs.children, function (t, n) {
      t.classList.toggle('active', n === index);
    });
  }

  function open(epIndex) {
    episode = EPISODES[epIndex];
    if (!episode) return;
    titleEl.textContent = episode.title;

    var many = episode.photos.length > 1;
    viewer.classList.toggle('single', !many);
    thumbs.innerHTML = '';
    if (many) {
      episode.photos.forEach(function (photo, n) {
        var img = document.createElement('img');
        img.src = src(photo);
        img.alt = photo.caption || (episode.title + ' ' + (n + 1));
        img.loading = 'lazy';
        img.addEventListener('click', function () { show(n); });
        thumbs.appendChild(img);
      });
    }

    show(0);
    viewer.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    viewer.classList.remove('open');
    document.body.style.overflow = '';
    episode = null;
    // drop the attribute rather than blanking it: src="" makes some browsers
    // re-request the page itself as an image
    stage.removeAttribute('src');
  }

  document.querySelectorAll('.gallery-card').forEach(function (card) {
    function go() { open(parseInt(card.getAttribute('data-episode'), 10)); }
    card.addEventListener('click', go);
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
    });
  });

  viewer.querySelectorAll('[data-close]').forEach(function (el) {
    el.addEventListener('click', close);
  });
  viewer.querySelector('.gallery-prev').addEventListener('click', function () { show(index - 1); });
  viewer.querySelector('.gallery-next').addEventListener('click', function () { show(index + 1); });

  document.addEventListener('keydown', function (e) {
    if (!viewer.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(index - 1);
    else if (e.key === 'ArrowRight') show(index + 1);
  });

  // The homepage sends visitors here with #<episode slug-ish index> never used;
  // ?episode=N opens one straight away, which is what the More Images button
  // would use if we ever want to deep-link a specific occasion.
  var want = new URLSearchParams(window.location.search).get('episode');
  if (want !== null && EPISODES[want]) open(parseInt(want, 10));
})();
</script>

<style>
/* ─── Header ─── */
.gallery-header {
  background: white;
  color: #2c3e50;
  padding: 80px 0;
}
.gallery-header h1 { color: #2c3e50; margin-bottom: 20px; }
.gallery-header h3 { color: #7f8c8d; }
.gallery-count {
  color: #4f6bd8;
  font-weight: 600;
  font-size: 0.95rem;
  margin-top: 14px;
  margin-bottom: 4px;
}
.gallery-hint { color: #95a5a6; font-size: 0.85rem; margin: 0; }

/* ─── Episode grid ─── */
.gallery-content { background-color: #f8f9fa; }
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
.gallery-card {
  margin: 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}
.gallery-card:hover,
.gallery-card:focus-visible {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  outline: none;
}
.gallery-card-img { position: relative; background: #eef1f5; }
.gallery-card-img img {
  width: 100%;
  height: 190px;
  object-fit: cover;
  display: block;
}
/* Photo count, bottom-right of the cover. A bare number is ambiguous, so the
   badge grows into "3 photos" while the card is hovered or focused; episodes of
   one photo have no badge at all. */
.gallery-badge {
  position: absolute;
  bottom: 12px;
  right: 12px;
  height: 34px;
  min-width: 34px;          /* with the padding below this keeps it a circle */
  box-sizing: border-box;
  padding: 0 9px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.82);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.92),
              0 2px 8px rgba(15, 23, 42, 0.3);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}
.gallery-badge-label {
  max-width: 0;
  opacity: 0;
  overflow: hidden;
  white-space: nowrap;
  font-size: 11px;
  font-weight: 600;
  transition: max-width .22s ease, opacity .22s ease, margin-left .22s ease;
}
.gallery-card:hover .gallery-badge-label,
.gallery-card:focus-visible .gallery-badge-label {
  max-width: 54px;
  opacity: 1;
  margin-left: 5px;
}
@media (prefers-reduced-motion: reduce) {
  .gallery-badge-label { transition: none; }
}
.gallery-card figcaption {
  padding: 16px 18px 18px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.gallery-card figcaption strong {
  font-size: 15px;
  color: #0f172a;
  line-height: 1.3;
}
.gallery-date { color: #4f6bd8; font-size: 12px; font-weight: 600; }
.gallery-desc { color: #64748b; font-size: 12.5px; line-height: 1.4; }

@media (max-width: 1100px) { .gallery-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 820px)  { .gallery-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 520px)  {
  .gallery-grid { grid-template-columns: 1fr; gap: 18px; }
  .gallery-card-img img { height: 210px; }
}

/* ─── Episode viewer ─── */
.gallery-viewer {
  display: none;
  position: fixed; inset: 0;
  z-index: 9999;
  align-items: center;
  justify-content: center;
}
.gallery-viewer.open { display: flex; }
.gallery-viewer-backdrop {
  position: absolute; inset: 0;
  /* the page behind was showing through far too much at 0.78 */
  background: rgba(10, 16, 32, 0.94);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.gallery-viewer-dialog {
  position: relative;
  background: #fff;
  border-radius: 16px;
  width: 92vw;
  max-width: 1100px;
  max-height: 92vh;
  padding: 28px 28px 22px;
  box-shadow: 0 24px 72px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
  /* a flex child will not shrink below its content without this, which is what
     keeps a tall photo from pushing the thumbnails off the dialog */
  min-height: 0;
}
.gallery-viewer-dialog h2 {
  margin: 0 0 2px;
  font-size: 21px;
  font-weight: 700;
  color: #0f172a;
  padding-right: 40px;
}
.gallery-viewer-meta {
  margin: 0 0 14px;
  color: #64748b;
  font-size: 13px;
}
.gallery-viewer-close {
  position: absolute;
  top: 12px; right: 16px;
  background: none;
  border: none;
  font-size: 32px;
  line-height: 1;
  color: #475569;
  cursor: pointer;
  padding: 2px 10px;
  border-radius: 8px;
  transition: background .15s;
}
.gallery-viewer-close:hover { background: #f1f5f9; color: #0f172a; }

.gallery-stage {
  position: relative;
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  /* light, not navy: the dark stage was the same colour as the scrim behind the
     dialog, so the letterbox bars read as a see-through hole in the panel */
  background: #eef1f5;
  border-radius: 10px;
  overflow: hidden;
}
.gallery-stage img {
  max-width: 100%;
  max-height: 62vh;
  object-fit: contain;
  display: block;
}
.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: #ffffff;        /* opaque: nothing inside the panel is see-through */
  border: 1px solid #dbe1ea;
  color: #0f172a;
  font-size: 20px;
  line-height: 1;
  width: 42px; height: 42px;
  border-radius: 50%;
  cursor: pointer;
  transition: background .15s;
}
.gallery-nav:hover { background: #fff; }
.gallery-prev { left: 12px; }
.gallery-next { right: 12px; }
/* one photo means nothing to page through */
.gallery-viewer.single .gallery-nav,
.gallery-viewer.single .gallery-thumbs { display: none; }

.gallery-caption {
  margin: 12px 0 0;
  color: #1f2937;
  font-size: 13.5px;
  text-align: center;
  line-height: 1.45;
}
.gallery-caption:empty { margin: 0; }

.gallery-thumbs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 12px 2px 2px;
  flex-shrink: 0;
}
.gallery-thumbs img {
  width: 76px;
  height: 54px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  opacity: 0.82;             /* the blue border marks the active one, so these
                                need only be slightly held back, not faded out */
  border: 2px solid transparent;
  transition: opacity .15s, border-color .15s;
  flex-shrink: 0;
}
.gallery-thumbs img:hover { opacity: 0.95; }
.gallery-thumbs img.active { opacity: 1; border-color: #4f6bd8; }

@media (max-width: 640px) {
  .gallery-viewer-dialog { width: 96vw; padding: 22px 16px 16px; max-height: 94vh; }
  .gallery-stage img { max-height: 54vh; }
  .gallery-nav { width: 36px; height: 36px; font-size: 17px; }
}
</style>
