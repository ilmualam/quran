/*!
 * Al-Quran Online (Multi-Qari & Multi-Bahasa) — ilmualam.com
 * Copyright (c) 2026–present Ilmu Alam (ilmualam.com). All Rights Reserved.
 * This source code is proprietary. Unauthorized reuse on other sites is prohibited.
 */

// Global variables
let currentSurah = 1, currentAyah = 0, audioPlayer = null, surahData = null, translationData = null;
let isPlaying = false, autoPlay = true, repeatAyah = false;
let allSurahsMeta = [];
const API_BASE = 'https://api.alquran.cloud/v1';

// Curated Malay/Rumi aliases so the surah dropdown & typing are meaningful to Malaysian users
// even though this tool's core value is multi-qari / multi-language, not Rumi.
const SURAH_ALIAS_LABEL = {
  36: 'Yasin', 67: 'Al-Mulk', 18: 'Al-Kahfi', 55: 'Ar-Rahman', 56: 'Al-Waqiah',
  19: 'Maryam', 12: 'Yusuf', 11: 'Hud', 20: 'Taha', 4: 'An-Nisa',
  2: 'Al-Baqarah', 3: 'Ali-Imran', 1: 'Al-Fatihah', 94: 'Al-Insyirah', 93: 'Ad-Duha', 48: 'Al-Fath'
};

// Verified live from https://www.ilmualam.com/feeds/posts/default/-/Al-Quran — 108/114 covered.
const SURAH_POST_MAP = {
  1: "https://www.ilmualam.com/2020/03/surah-al-fatihah-rumi.html", 2: "https://www.ilmualam.com/2020/03/surah-al-baqarah.html",
  3: "https://www.ilmualam.com/2020/03/surah-ali-imran.html", 4: "https://www.ilmualam.com/2020/04/surah-an-nisa.html",
  5: "https://www.ilmualam.com/2020/05/surah-al-maidah.html", 6: "https://www.ilmualam.com/2026/01/surah-al-anam.html",
  7: "https://www.ilmualam.com/2026/01/surah-al-araf.html", 8: "https://www.ilmualam.com/2025/12/surah-al-anfal-rumi.html",
  10: "https://www.ilmualam.com/2025/12/surah-yunus-rumi.html", 11: "https://www.ilmualam.com/2025/12/surah-hud-rumi.html",
  12: "https://www.ilmualam.com/2025/11/surah-yusuf.html", 14: "https://www.ilmualam.com/2026/03/surah-ibrahim.html",
  15: "https://www.ilmualam.com/2025/12/surah-al-hijr-rumi.html", 16: "https://www.ilmualam.com/2025/12/surah-an-nahl.html",
  17: "https://www.ilmualam.com/2025/12/surah-al-isra-rumi.html", 18: "https://www.ilmualam.com/2025/11/surah-al-kahfi-rumi.html",
  19: "https://www.ilmualam.com/2022/02/surah-maryam.html", 20: "https://www.ilmualam.com/2025/11/surah-taha-rumi.html",
  21: "https://www.ilmualam.com/2025/12/surah-al-anbiya-rumi.html", 22: "https://www.ilmualam.com/2025/12/surah-al-hajj-rumi.html",
  25: "https://www.ilmualam.com/2025/12/surah-al-furqan.html", 26: "https://www.ilmualam.com/2025/12/surah-asy-syuara-rumi.html",
  27: "https://www.ilmualam.com/2026/02/surah-an-naml.html", 28: "https://www.ilmualam.com/2025/12/surah-al-qasas-rumi.html",
  30: "https://www.ilmualam.com/2026/03/surah-ar-rum.html", 31: "https://www.ilmualam.com/2026/01/surah-luqman.html",
  32: "https://www.ilmualam.com/2026/01/surah-as-sajdah.html", 33: "https://www.ilmualam.com/2025/12/surah-al-ahzab.html",
  34: "https://www.ilmualam.com/2025/12/surah-saba.html", 35: "https://www.ilmualam.com/2025/12/surah-al-fatir.html",
  36: "https://www.ilmualam.com/2020/05/surah-yassin.html", 37: "https://www.ilmualam.com/2025/12/surah-as-saffat.html",
  38: "https://www.ilmualam.com/2026/02/surah-saad.html", 39: "https://www.ilmualam.com/2026/01/surah-az-zumar.html",
  40: "https://www.ilmualam.com/2026/01/surah-ghafir.html", 41: "https://www.ilmualam.com/2025/12/surah-fussilat.html",
  43: "https://www.ilmualam.com/2026/02/surah-az-zukhruf.html", 44: "https://www.ilmualam.com/2026/01/surah-ad-dukhan.html",
  45: "https://www.ilmualam.com/2026/02/surah-al-jaathiyah.html", 46: "https://www.ilmualam.com/2026/02/surah-al-ahqaf.html",
  47: "https://www.ilmualam.com/2026/01/surah-muhammad.html", 48: "https://www.ilmualam.com/2026/02/surah-al-fath.html",
  49: "https://www.ilmualam.com/2026/01/surah-al-hujurat.html", 50: "https://www.ilmualam.com/2026/01/surah-qaaf.html",
  51: "https://www.ilmualam.com/2026/01/surah-adh-dhariyat.html", 52: "https://www.ilmualam.com/2026/02/surah-at-tur.html",
  53: "https://www.ilmualam.com/2026/03/surah-najm.html", 54: "https://www.ilmualam.com/2026/02/surah-al-qamar.html",
  55: "https://www.ilmualam.com/2025/11/surah-ar-rahman.html", 56: "https://www.ilmualam.com/2025/11/surah-al-waqiah.html",
  57: "https://www.ilmualam.com/2026/01/surah-al-hadid.html", 58: "https://www.ilmualam.com/2026/01/surah-al-mujadilah.html",
  59: "https://www.ilmualam.com/2026/01/surah-al-hashr.html", 60: "https://www.ilmualam.com/2026/02/surah-al-mumtahanah.html",
  61: "https://www.ilmualam.com/2026/02/surah-as-saff.html", 62: "https://www.ilmualam.com/2026/01/surah-al-jumuah.html",
  63: "https://www.ilmualam.com/2026/01/surah-al-munafiqun.html", 64: "https://www.ilmualam.com/2026/02/surah-at-taghaabun.html",
  65: "https://www.ilmualam.com/2026/03/surah-at-talaq.html", 66: "https://www.ilmualam.com/2026/01/surah-at-tahrim.html",
  67: "https://www.ilmualam.com/2020/05/surah-al-mulk.html", 68: "https://www.ilmualam.com/2026/01/surah-al-qalam.html",
  69: "https://www.ilmualam.com/2026/01/surah-al-haqqah.html", 70: "https://www.ilmualam.com/2026/03/surah-al-maaarij.html",
  71: "https://www.ilmualam.com/2026/01/surah-nuh.html", 72: "https://www.ilmualam.com/2025/12/surah-al-jinn-rumi.html",
  73: "https://www.ilmualam.com/2025/12/surah-al-muzzammil-rumi.html", 74: "https://www.ilmualam.com/2026/02/surah-al-muddaththir.html",
  75: "https://www.ilmualam.com/2026/01/surah-al-qiyamah.html", 76: "https://www.ilmualam.com/2026/01/surah-al-insaan.html",
  77: "https://www.ilmualam.com/2026/01/surah-al-mursalaat.html", 78: "https://www.ilmualam.com/2026/01/surah-an-naba.html",
  79: "https://www.ilmualam.com/2026/03/surah-an-naziat.html", 80: "https://www.ilmualam.com/2026/01/surah-abasa.html",
  81: "https://www.ilmualam.com/2026/02/surah-at-takwir.html", 82: "https://www.ilmualam.com/2026/02/surah-al-infitar.html",
  83: "https://www.ilmualam.com/2026/02/surah-al-mutaffifin.html", 84: "https://www.ilmualam.com/2026/03/surah-al-inshiqaq.html",
  85: "https://www.ilmualam.com/2026/02/surah-al-buruj.html", 86: "https://www.ilmualam.com/2026/02/surah-at-tariq.html",
  87: "https://www.ilmualam.com/2026/02/surah-al-alaa.html", 88: "https://www.ilmualam.com/2026/02/surah-al-ghashiyah.html",
  89: "https://www.ilmualam.com/2026/02/surah-al-fajr.html", 90: "https://www.ilmualam.com/2026/02/surah-al-balad.html",
  91: "https://www.ilmualam.com/2026/02/surah-asy-syams.html", 92: "https://www.ilmualam.com/2026/02/surah-al-lail.html",
  93: "https://www.ilmualam.com/2025/12/surah-ad-dhuha-rumi.html", 94: "https://www.ilmualam.com/2026/03/surah-ash-sharh.html",
  95: "https://www.ilmualam.com/2026/02/surah-at-tin.html", 96: "https://www.ilmualam.com/2026/03/surah-al-alaq.html",
  97: "https://www.ilmualam.com/2025/12/surah-al-qadr-rumi.html", 98: "https://www.ilmualam.com/2026/03/surah-al-bayyinah.html",
  99: "https://www.ilmualam.com/2026/03/surah-al-zalzalah.html", 100: "https://www.ilmualam.com/2026/03/surah-al-adiyat.html",
  101: "https://www.ilmualam.com/2026/03/surah-al-qariah.html", 102: "https://www.ilmualam.com/2026/03/surah-at-takathur.html",
  103: "https://www.ilmualam.com/2026/03/surah-al-asr.html", 104: "https://www.ilmualam.com/2026/03/surah-al-humazah.html",
  105: "https://www.ilmualam.com/2026/03/surah-al-fiil.html", 106: "https://www.ilmualam.com/2026/03/surah-quraisy.html",
  107: "https://www.ilmualam.com/2026/03/surah-al-maun.html", 108: "https://www.ilmualam.com/2026/03/surah-al-kautsar.html",
  109: "https://www.ilmualam.com/2025/11/surah-al-kafirun-rumi.html", 110: "https://www.ilmualam.com/2026/03/surah-an-nasr.html",
  111: "https://www.ilmualam.com/2026/03/surah-al-masad.html", 112: "https://www.ilmualam.com/2025/12/surah-al-ikhlas-rumi.html",
  113: "https://www.ilmualam.com/2025/12/surah-al-falaq-rumi.html", 114: "https://www.ilmualam.com/2025/12/surah-an-nas-rumi.html"
};

document.addEventListener('DOMContentLoaded', init);

async function init() {
  await loadSurahList();
  setupEventListeners();
  setupPageShareButton();
  const cameFromDeepLink = await checkUrlParams();
  if (!cameFromDeepLink) {
    await loadSurah(1);
  }
}

async function loadSurahList() {
  try {
    const res = await fetch(`${API_BASE}/surah`);
    const data = await res.json();
    allSurahsMeta = data.data;
    const select = document.getElementById('surahSelect');
    select.innerHTML = '';
    data.data.forEach(surah => {
      const o = document.createElement('option');
      o.value = surah.number;
      const alias = SURAH_ALIAS_LABEL[surah.number];
      o.textContent = alias
        ? `${surah.number}. ${surah.englishName} (${alias}) - ${surah.name}`
        : `${surah.number}. ${surah.englishName} - ${surah.name}`;
      select.appendChild(o);
    });
  } catch (e) { console.error('Error loading surah list:', e); }
}

async function loadSurah(surahNumber, targetAyah) {
  showLoading();
  currentSurah = surahNumber; currentAyah = 0;
  const reciter = document.getElementById('reciterSelect').value;
  const translation = document.getElementById('translationSelect').value;
  try {
    const [arRes, trRes] = await Promise.all([
      fetch(`${API_BASE}/surah/${surahNumber}/${reciter}`),
      fetch(`${API_BASE}/surah/${surahNumber}/${translation}`)
    ]);
    const [arData, trData] = await Promise.all([arRes.json(), trRes.json()]);
    surahData = arData.data; translationData = trData.data;
    document.getElementById('surahSelect').value = surahNumber;
    displaySurah();
    setupAudioPlayer();
    updatePageSEO(surahData);
    syncUrl(surahNumber, targetAyah || null);
    if (targetAyah) {
      setTimeout(() => {
        const el = document.getElementById(`ayah-${targetAyah}`);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          el.classList.add('playing');
          setTimeout(() => el.classList.remove('playing'), 1600);
        }
      }, 300);
    }
  } catch (e) {
    console.error('Error loading surah:', e);
    document.getElementById('quranDisplay').innerHTML = '<div class="error" style="color:#e74c3c">Error loading surah. Please try again.</div>';
  }
}

function displaySurah() {
  const display = document.getElementById('quranDisplay');
  const showTranslation = document.getElementById('translationToggle').checked;
  const postUrl = SURAH_POST_MAP[surahData.number];
  const banner = postUrl
    ? `<a href="${postUrl}" style="display:block;text-align:center;font-size:13px;color:#1F8A4C;background:#EEF6F0;border:1px dashed #1F8A4C;border-radius:10px;padding:8px 12px;margin:10px 0;text-decoration:none;">📖 Baca kisah, asbabun nuzul &amp; tafsir penuh Surah ${surahData.englishName} →</a>`
    : '';
  let html = `
    <div class="surah-info">
      <div class="surah-name-ar">${surahData.name}</div>
      <div class="surah-name-en">${surahData.englishName} - ${surahData.englishNameTranslation}</div>
      <div class="surah-meta">${surahData.revelationType} • ${surahData.numberOfAyahs} Ayahs</div>
    </div>
    ${banner}`;
  if (surahData.number !== 1 && surahData.number !== 9) {
    html += '<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>';
  }
  surahData.ayahs.forEach((ayah, i) => {
    const tr = translationData.ayahs[i];
    html += `
    <div class="ayah-container" id="ayah-${ayah.numberInSurah}" data-ayah="${ayah.numberInSurah}">
      <div class="ayah-content">
        <span class="ayah-number">${ayah.numberInSurah}</span>
        <div class="ayah-text-ar">${ayah.text}</div>
        ${showTranslation ? `<div class="ayah-translation">${tr.text}</div>` : ''}
      </div>
      <div class="ayah-actions">
        <button class="action-ibtn" onclick="playAyah(${i})">▶️ Play</button>
        <button class="action-ibtn" onclick="copyAyah(${i})">📋 Copy</button>
        <button class="action-ibtn" onclick="shareAyah(${i})">🔗 Share</button>
        <button class="action-ibtn" onclick="bookmarkAyah(${i})">🔖 Bookmark</button>
      </div>
    </div>`;
  });
  display.innerHTML = html;
  applyFontSize();
}

function setupAudioPlayer() {
  if (audioPlayer) { audioPlayer.pause(); audioPlayer = null; }
  audioPlayer = new Audio();
  audioPlayer.addEventListener('ended', onAudioEnded);
}

function playAyah(i) {
  currentAyah = i;
  const ayah = surahData.ayahs[i];
  if (!audioPlayer) setupAudioPlayer();
  audioPlayer.src = ayah.audio;
  audioPlayer.play().catch(() => {});
  isPlaying = true;
  if (document.getElementById('highlightToggle').checked) {
    document.querySelectorAll('.ayah-container').forEach(el => el.classList.remove('playing'));
    const el = document.getElementById(`ayah-${ayah.numberInSurah}`);
    if (el) {
      el.classList.add('playing');
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
}

function onAudioEnded() {
  if (repeatAyah) { playAyah(currentAyah); }
  else if (autoPlay && currentAyah < surahData.ayahs.length - 1) { playAyah(currentAyah + 1); }
  else {
    isPlaying = false;
    document.querySelectorAll('.ayah-container').forEach(el => el.classList.remove('playing'));
  }
}

function copyAyah(i) {
  const ayah = surahData.ayahs[i], tr = translationData.ayahs[i];
  const text = `${ayah.text}\n\n${tr.text}\n\n[${surahData.englishName} ${ayah.numberInSurah}]`;
  navigator.clipboard.writeText(text).then(() => alert('Ayah copied to clipboard!')).catch(() => {});
}

function shareAyah(i) {
  const ayah = surahData.ayahs[i], tr = translationData.ayahs[i];
  const shareText = `${ayah.text}\n\n${tr.text}\n\n[${surahData.englishName} ${ayah.numberInSurah}]`;
  document.getElementById('shareText').textContent = shareText;
  document.getElementById('shareModal').style.display = 'grid';
  window.currentShareText = shareText;
  window.currentShareUrl = `${location.origin}${location.pathname}?surah=${surahData.number}&ayah=${ayah.numberInSurah}`;
}

function shareOn(platform) {
  const text = encodeURIComponent(window.currentShareText || '');
  const url = encodeURIComponent(window.currentShareUrl || location.href);
  let go = '';
  if (platform === 'whatsapp') go = `https://wa.me/?text=${text}%20${url}`;
  if (platform === 'facebook') go = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
  if (platform === 'twitter') go = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
  if (platform === 'telegram') go = `https://t.me/share/url?url=${url}&text=${text}`;
  if (go) window.open(go, '_blank', 'noopener,noreferrer');
}
function closeShareModal() { document.getElementById('shareModal').style.display = 'none'; }

function bookmarkAyah(i) {
  const ayah = surahData.ayahs[i];
  const mark = { surah: surahData.number, surahName: surahData.englishName, ayah: ayah.numberInSurah, text: ayah.text, timestamp: new Date().toISOString() };
  const list = JSON.parse(localStorage.getItem('quranBookmarks') || '[]');
  list.push(mark);
  localStorage.setItem('quranBookmarks', JSON.stringify(list));
  alert('Ayah bookmarked successfully!');
}

// FIX: search now uses whichever translation edition the user has selected,
// so Malay/Indonesian/Urdu speakers can search in their own language instead
// of only English.
async function searchQuran() {
  const q = document.getElementById('searchInput').value.trim();
  if (!q) return;
  const box = document.getElementById('searchResults');
  box.innerHTML = '<div class="loading">Searching...</div>';
  const edition = document.getElementById('translationSelect').value || 'en.asad';
  const langCode = edition.split('.')[0]; // e.g. 'ms', 'en', 'id', 'ur'
  try {
    const res = await fetch(`${API_BASE}/search/${encodeURIComponent(q)}/all/${langCode}`);
    const data = await res.json();
    if (!data.data || !data.data.matches || !data.data.matches.length) {
      box.innerHTML = '<div style="padding:12px; color:#7f8c8d">Tiada hasil carian ditemui / No results found</div>';
      return;
    }
    let html = `<h4 style="margin:4px 0 10px;font-weight:800">Hasil Carian (${data.data.count} match)</h4>`;
    data.data.matches.slice(0, 10).forEach(m => {
      html += `
        <div class="search-result-item" onclick="goToAyah(${m.surah.number}, ${m.numberInSurah})">
          <div style="font-weight:800; color:#2c3e50; margin-bottom:4px">${m.surah.englishName} (${m.surah.number}:${m.numberInSurah})</div>
          <div style="color:#4a5568; overflow-wrap:anywhere">${m.text}</div>
        </div>`;
    });
    box.innerHTML = html;
  } catch (e) {
    console.error('Search error:', e);
    box.innerHTML = '<div style="padding:12px; color:#e74c3c">Error searching. Please try again.</div>';
  }
}

async function goToAyah(surahNumber, ayahNumber) {
  await loadSurah(surahNumber, ayahNumber);
}

function applyFontSize() {
  const size = document.getElementById('fontSizeSelect').value;
  const map = { small: '1.4em', medium: '1.8em', large: '2.2em', xlarge: '2.6em' };
  document.querySelectorAll('.ayah-text-ar').forEach(el => { el.style.fontSize = map[size]; });
}

function toggleNightMode() {
  const on = document.getElementById('nightModeToggle').checked;
  document.body.classList.toggle('night', on);
}

function showLoading() {
  document.getElementById('quranDisplay').innerHTML = `
    <div class="loading">
      <div class="loading-spinner"></div>
      Loading surah...
    </div>`;
}

function setupEventListeners() {
  document.getElementById('surahSelect').addEventListener('change', e => loadSurah(parseInt(e.target.value)));
  document.getElementById('reciterSelect').addEventListener('change', () => loadSurah(currentSurah));
  document.getElementById('translationSelect').addEventListener('change', () => loadSurah(currentSurah));
  document.getElementById('fontSizeSelect').addEventListener('change', applyFontSize);

  document.getElementById('playibtn').addEventListener('click', () => {
    if (audioPlayer && audioPlayer.src) { audioPlayer.play().catch(() => {}); } else { playAyah(0); }
  });
  document.getElementById('pauseibtn').addEventListener('click', () => { if (audioPlayer) audioPlayer.pause(); });
  document.getElementById('stopibtn').addEventListener('click', () => {
    if (audioPlayer) { audioPlayer.pause(); audioPlayer.currentTime = 0; }
    document.querySelectorAll('.ayah-container').forEach(el => el.classList.remove('playing'));
  });
  document.getElementById('prevAyahibtn').addEventListener('click', () => { if (currentAyah > 0) playAyah(currentAyah - 1); });
  document.getElementById('nextAyahibtn').addEventListener('click', () => { if (currentAyah < surahData.ayahs.length - 1) playAyah(currentAyah + 1); });

  document.getElementById('autoPlayCheck').addEventListener('change', e => autoPlay = e.target.checked);
  document.getElementById('translationToggle').addEventListener('change', displaySurah);
  document.getElementById('nightModeToggle').addEventListener('change', toggleNightMode);
  document.getElementById('repeatToggle').addEventListener('change', e => repeatAyah = e.target.checked);

  document.getElementById('searchibtn').addEventListener('click', searchQuran);
  document.getElementById('searchInput').addEventListener('keypress', e => { if (e.key === 'Enter') searchQuran(); });

  document.addEventListener('keydown', e => {
    const inInput = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName);
    if (inInput) return;
    if (e.key === ' ') { e.preventDefault(); if (audioPlayer && audioPlayer.src) { audioPlayer.paused ? audioPlayer.play() : audioPlayer.pause(); } }
    if (e.key === 'ArrowLeft') document.getElementById('prevAyahibtn').click();
    if (e.key === 'ArrowRight') document.getElementById('nextAyahibtn').click();
  });
}

// ===== Deep link (read on load) =====
async function checkUrlParams() {
  const p = new URLSearchParams(location.search);
  const s = p.get('surah');
  const a = p.get('ayah');
  if (s) {
    await loadSurah(parseInt(s), a ? parseInt(a) : null);
    return true;
  }
  return false;
}

// ===== Deep link (write on navigate) + per-surah SEO =====
function syncUrl(surahNumber, ayahNumber) {
  const url = new URL(location.href);
  url.searchParams.set('surah', surahNumber);
  if (ayahNumber) { url.searchParams.set('ayah', ayahNumber); } else { url.searchParams.delete('ayah'); }
  history.replaceState({ surah: surahNumber, ayah: ayahNumber || null }, '', url.toString());
}

var baseTitle = document.title;
var baseDescEl = document.querySelector('meta[name="description"]');
var baseDesc = baseDescEl ? baseDescEl.getAttribute('content') : '';
var canonicalEl = document.querySelector('link[rel="canonical"]');

function updatePageSEO(surah) {
  document.title = `${surah.englishName} (${surah.englishNameTranslation}) - Audio Pelbagai Qari & Terjemahan | Al-Quran Online`;
  const desc = `Dengar dan baca Surah ${surah.englishName} (${surah.englishNameTranslation}), ${surah.numberOfAyahs} ayat, dengan pilihan qari (Alafasy, Husary, Minshawi, Abdul Basit) dan terjemahan pelbagai bahasa.`;
  if (baseDescEl) baseDescEl.setAttribute('content', desc);
  const ogt = document.querySelector('meta[property="og:title"]'); if (ogt) ogt.content = document.title;
  const ogd = document.querySelector('meta[property="og:description"]'); if (ogd) ogd.content = desc;
  if (canonicalEl) {
    const url = new URL(location.pathname, location.origin);
    url.searchParams.set('surah', surah.number);
    canonicalEl.setAttribute('href', url.toString());
  }
}

// ===== Page-level share button =====
function setupPageShareButton() {
  const btn = document.getElementById('pageShareBtn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const url = location.href;
    const title = surahData ? `Al-Quran: Surah ${surahData.englishName}` : 'Al-Quran Online - Audio Pelbagai Qari & Terjemahan';
    const text = surahData
      ? `Dengar Surah ${surahData.englishName} dengan pilihan qari & terjemahan, percuma.`
      : 'Baca & dengar Al-Quran online percuma - pelbagai qari dan bahasa terjemahan.';

    if (navigator.share) {
      navigator.share({ title, text, url }).catch(() => {});
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url)
        .then(() => alert('Pautan telah disalin. Boleh tampal di WhatsApp / media sosial.'))
        .catch(() => alert('Sila salin pautan secara manual: ' + url));
    } else {
      alert('Pautan: ' + url);
    }
  });
}
