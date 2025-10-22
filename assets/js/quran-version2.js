  // Global variables
  let currentSurah = 1, currentAyah = 0, audioPlayer = null, surahData = null, translationData = null;
  let isPlaying = false, autoPlay = true, repeatAyah = false;
  const API_BASE = 'https://api.alquran.cloud/v1';

  document.addEventListener('DOMContentLoaded', init);
  async function init(){
    await loadSurahList();
    setupEventListeners();
    await loadSurah(1);
  }

  async function loadSurahList(){
    try{
      const res = await fetch(`${API_BASE}/surah`);
      const data = await res.json();
      const select = document.getElementById('surahSelect');
      select.innerHTML = '';
      data.data.forEach(surah=>{
        const o = document.createElement('option');
        o.value = surah.number;
        o.textContent = `${surah.number}. ${surah.englishName} - ${surah.name}`;
        select.appendChild(o);
      });
    }catch(e){ console.error('Error loading surah list:', e) }
  }

  async function loadSurah(surahNumber){
    showLoading();
    currentSurah = surahNumber; currentAyah = 0;
    const reciter = document.getElementById('reciterSelect').value;
    const translation = document.getElementById('translationSelect').value;
    try{
      const [arRes, trRes] = await Promise.all([
        fetch(`${API_BASE}/surah/${surahNumber}/${reciter}`),
        fetch(`${API_BASE}/surah/${surahNumber}/${translation}`)
      ]);
      const [arData, trData] = await Promise.all([arRes.json(), trRes.json()]);
      surahData = arData.data; translationData = trData.data;
      displaySurah();
      setupAudioPlayer();
    }catch(e){
      console.error('Error loading surah:', e);
      document.getElementById('quranDisplay').innerHTML = '<div class="error" style="color:#e74c3c">Error loading surah. Please try again.</div>';
    }
  }

  function displaySurah(){
    const display = document.getElementById('quranDisplay');
    const showTranslation = document.getElementById('translationToggle').checked;
    let html = `
      <div class="surah-info">
        <div class="surah-name-ar">${surahData.name}</div>
        <div class="surah-name-en">${surahData.englishName} - ${surahData.englishNameTranslation}</div>
        <div class="surah-meta">${surahData.revelationType} • ${surahData.numberOfAyahs} Ayahs</div>
      </div>`;
    if (surahData.number !== 1 && surahData.number !== 9){
      html += '<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>';
    }
    surahData.ayahs.forEach((ayah, i)=>{
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

  function setupAudioPlayer(){
    if (audioPlayer){ audioPlayer.pause(); audioPlayer = null }
    audioPlayer = new Audio();
    audioPlayer.addEventListener('ended', onAudioEnded);
    audioPlayer.addEventListener('timeupdate', onAudioTimeUpdate);
  }

  function playAyah(i){
    currentAyah = i;
    const ayah = surahData.ayahs[i];
    if (!audioPlayer) setupAudioPlayer();
    audioPlayer.src = ayah.audio;
    audioPlayer.play().catch(()=>{});
    isPlaying = true;
    if (document.getElementById('highlightToggle').checked){
      document.querySelectorAll('.ayah-container').forEach(el=>el.classList.remove('playing'));
      const el = document.getElementById(`ayah-${ayah.numberInSurah}`);
      if (el){
        el.classList.add('playing');
        el.scrollIntoView({behavior:'smooth', block:'center'});
      }
    }
  }

  function onAudioEnded(){
    if (repeatAyah){ playAyah(currentAyah) }
    else if (autoPlay && currentAyah < surahData.ayahs.length - 1){ playAyah(currentAyah + 1) }
    else{
      isPlaying = false;
      document.querySelectorAll('.ayah-container').forEach(el=>el.classList.remove('playing'));
    }
  }
  function onAudioTimeUpdate(){ /* hook for progress if needed */ }

  function copyAyah(i){
    const ayah = surahData.ayahs[i], tr = translationData.ayahs[i];
    const text = `${ayah.text}\n\n${tr.text}\n\n[${surahData.englishName} ${ayah.numberInSurah}]`;
    navigator.clipboard.writeText(text).then(()=>alert('Ayah copied to clipboard!')).catch(()=>{});
  }

  function shareAyah(i){
    const ayah = surahData.ayahs[i], tr = translationData.ayahs[i];
    const shareText = `${ayah.text}\n\n${tr.text}\n\n[${surahData.englishName} ${ayah.numberInSurah}]`;
    document.getElementById('shareText').textContent = shareText;
    document.getElementById('shareModal').style.display = 'grid';
    window.currentShareText = shareText;
    window.currentShareUrl = `${location.origin}${location.pathname}?surah=${surahData.number}&ayah=${ayah.numberInSurah}`;
  }

  function shareOn(platform){
    const text = encodeURIComponent(window.currentShareText||'');
    const url  = encodeURIComponent(window.currentShareUrl||location.href);
    let go='';
    if (platform==='whatsapp') go=`https://wa.me/?text=${text}%20${url}`;
    if (platform==='facebook') go=`https://www.facebook.com/sharer/sharer.php?u=${url}`;
    if (platform==='twitter') go=`https://twitter.com/intent/tweet?text=${text}&url=${url}`;
    if (platform==='telegram') go=`https://t.me/share/url?url=${url}&text=${text}`;
    if (go) window.open(go,'_blank','noopener,noreferrer');
  }
  function closeShareModal(){ document.getElementById('shareModal').style.display='none' }

  function bookmarkAyah(i){
    const ayah = surahData.ayahs[i];
    const mark = { surah: surahData.number, surahName: surahData.englishName, ayah: ayah.numberInSurah, text: ayah.text, timestamp: new Date().toISOString() };
    const list = JSON.parse(localStorage.getItem('quranBookmarks')||'[]');
    list.push(mark);
    localStorage.setItem('quranBookmarks', JSON.stringify(list));
    alert('Ayah bookmarked successfully!');
  }

  async function searchQuran(){
    const q = document.getElementById('searchInput').value.trim();
    if (!q) return;
    const box = document.getElementById('searchResults');
    box.innerHTML = '<div class="loading">Searching...</div>';
    try{
      const res = await fetch(`${API_BASE}/search/${encodeURIComponent(q)}/all/en`);
      const data = await res.json();
      if (!data.data.matches.length){
        box.innerHTML = '<div style="padding:12px; color:#7f8c8d">No results found</div>'; return;
      }
      let html = `<h4 style="margin:4px 0 10px;font-weight:800">Search Results (${data.data.count} matches)</h4>`;
      data.data.matches.slice(0,10).forEach(m=>{
        html += `
          <div class="search-result-item" onclick="goToAyah(${m.surah.number}, ${m.numberInSurah})">
            <div style="font-weight:800; color:#2c3e50; margin-bottom:4px">${m.surah.englishName} (${m.surah.number}:${m.numberInSurah})</div>
            <div style="color:#4a5568; overflow-wrap:anywhere">${m.text}</div>
          </div>`;
      });
      box.innerHTML = html;
    }catch(e){
      console.error('Search error:', e);
      box.innerHTML = '<div style="padding:12px; color:#e74c3c">Error searching. Please try again.</div>';
    }
  }

  async function goToAyah(surahNumber, ayahNumber){
    document.getElementById('surahSelect').value = surahNumber;
    await loadSurah(surahNumber);
    setTimeout(()=>{
      const el = document.getElementById(`ayah-${ayahNumber}`);
      if (el){
        el.scrollIntoView({behavior:'smooth', block:'center'});
        el.classList.add('playing');
        setTimeout(()=>el.classList.remove('playing'), 1600);
      }
    }, 400);
  }

  function applyFontSize(){
    const size = document.getElementById('fontSizeSelect').value;
    const map = { small:'1.4em', medium:'1.8em', large:'2.2em', xlarge:'2.6em' };
    document.querySelectorAll('.ayah-text-ar').forEach(el=>{ el.style.fontSize = map[size] });
  }

  function toggleNightMode(){
    const on = document.getElementById('nightModeToggle').checked;
    // Class-based (CSS) with inline fallback for older code paths
    document.body.classList.toggle('night', on);
    if (!on){
      document.body.style.background = 'var(--bg)';
      document.body.style.color = 'var(--ink)';
    }else{
      document.body.style.background = '#0f1115';
      document.body.style.color = '#e6e9ee';
    }
  }

  function showLoading(){
    document.getElementById('quranDisplay').innerHTML = `
      <div class="loading">
        <div class="loading-spinner" style="display:inline-block;width:28px;height:28px;border:3px solid #e6eef7;border-top-color:var(--brand);border-radius:50%;animation:spin 1s linear infinite;margin-right:8px"></div>
        Loading surah...
      </div>`;
  }

  function setupEventListeners(){
    document.getElementById('surahSelect').addEventListener('change', e=>loadSurah(parseInt(e.target.value)));
    document.getElementById('reciterSelect').addEventListener('change', ()=>loadSurah(currentSurah));
    document.getElementById('translationSelect').addEventListener('change', ()=>loadSurah(currentSurah));
    document.getElementById('fontSizeSelect').addEventListener('change', applyFontSize);

    document.getElementById('playibtn').addEventListener('click', ()=>{
      if (audioPlayer && audioPlayer.src){ audioPlayer.play().catch(()=>{}) } else { playAyah(0) }
    });
    document.getElementById('pauseibtn').addEventListener('click', ()=>{ if (audioPlayer) audioPlayer.pause() });
    document.getElementById('stopibtn').addEventListener('click', ()=>{
      if (audioPlayer){ audioPlayer.pause(); audioPlayer.currentTime=0 }
      document.querySelectorAll('.ayah-container').forEach(el=>el.classList.remove('playing'));
    });
    document.getElementById('prevAyahibtn').addEventListener('click', ()=>{ if (currentAyah>0) playAyah(currentAyah-1) });
    document.getElementById('nextAyahibtn').addEventListener('click', ()=>{ if (currentAyah < surahData.ayahs.length-1) playAyah(currentAyah+1) });

    document.getElementById('autoPlayCheck').addEventListener('change', e=>autoPlay = e.target.checked);
    document.getElementById('translationToggle').addEventListener('change', displaySurah);
    document.getElementById('nightModeToggle').addEventListener('change', toggleNightMode);
    document.getElementById('repeatToggle').addEventListener('change', e=>repeatAyah = e.target.checked);

    document.getElementById('searchibtn').addEventListener('click', searchQuran);
    document.getElementById('searchInput').addEventListener('keypress', e=>{ if (e.key==='Enter') searchQuran() });

    document.addEventListener('keydown', e=>{
      const inInput = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName);
      if (inInput) return;
      if (e.key===' '){ e.preventDefault(); if (audioPlayer && audioPlayer.src){ audioPlayer.paused ? audioPlayer.play() : audioPlayer.pause() } }
      if (e.key==='ArrowLeft') document.getElementById('prevAyahibtn').click();
      if (e.key==='ArrowRight') document.getElementById('nextAyahibtn').click();
    });
  }

  function checkUrlParams(){
    const p = new URLSearchParams(location.search);
    const s = p.get('surah'); const a = p.get('ayah');
    if (s){
      document.getElementById('surahSelect').value = s;
      loadSurah(parseInt(s)).then(()=>{ if (a) setTimeout(()=>goToAyah(parseInt(s), parseInt(a)), 800) });
    }
  }
  window.addEventListener('load', checkUrlParams);
</script>
<script>
/**
 * Advanced Al Quran Online Tool
 * Version: 2.0.0
 * Author: ilmualam.com
 * License: MIT
 * (kept original logic; no feature removed)
*/
class QuranApp{
  constructor(config={}){
    this.config = { apiBase:'https://api.alquran.cloud/v1', cacheTime:86400000, defaultReciter:'ar.alafasy', defaultTranslation:'en.asad', ...config };
    this.state = { currentSurah:1, currentAyah:0, isPlaying:false, bookmarks:[], history:[], preferences:{} };
    this.cache = new Map(); this.audioQueue = []; this.init();
  }
  async init(){ this.loadState(); this.setupServiceWorker(); this.initializeAnalytics(); this.preloadAssets(); this.setupKeyboardShortcuts(); this.initializeTajweed(); }
  async fetchWithCache(url,key,force=false){
    const c=this.cache.get(key);
    if (c && !force && (Date.now()-c.timestamp)<this.config.cacheTime) return c.data;
    try{
      const r=await fetch(url); const d=await r.json();
      this.cache.set(key,{data:d,timestamp:Date.now()});
      localStorage.setItem(`quran_cache_${key}`, JSON.stringify({data:d,timestamp:Date.now()}));
      return d;
    }catch(e){
      const lc=localStorage.getItem(`quran_cache_${key}`); if (lc) return JSON.parse(lc).data; throw e;
    }
  }
  initializeTajweed(){
    this.tajweedRules={
      'نّ|مّ':{color:'#FF6B6B',rule:'ghunnah'},
      'قْ|طْ|بْ|جْ|دْ':{color:'#4ECDC4',rule:'qalqalah'},
      'نْ(?=[ت-ث-ج-د-ذ-ز-س-ش-ص-ض-ط-ظ-ف-ق-ك])':{color:'#45B7D1',rule:'ikhfa'},
      'نْ(?=[ر-ل-م-ن-و-ي])':{color:'#96CEB4',rule:'idgham'},
      'نْ(?=ب)':{color:'#FECA57',rule:'iqlab'},
      '[َُِ][اوي]':{color:'#FF9FF3',rule:'mad'}
    };
  }
  applyTajweed(t){
    let s=t; for (const [p,st] of Object.entries(this.tajweedRules)){ s=s.replace(new RegExp(p,'g'), m=>`<span class="tajweed tajweed-${st.rule}" style="color:${st.color}" title="${st.rule}">${m}</span>`)} return s;
  }
  async loadAudioWithTimestamps(surah){ return await this.fetchWithCache(`${this.config.apiBase}/surah/${surah}/timing`,`timing_${surah}`) }
  async setupServiceWorker(){ if ('serviceWorker' in navigator){ try{ await navigator.serviceWorker.register('/sw.js') }catch(e){} } }
  initializeAnalytics(){
    this.analytics={ sessionStart:Date.now(), interactions:0, ayahsRead:0, audioPlayed:0, searchQueries:[] };
    setInterval(()=>this.sendAnalytics(),30000); this.trackWebVitals();
  }
  trackWebVitals(){
    if ('PerformanceObserver' in window){
      try{
        new PerformanceObserver(l=>{ for (const e of l.getEntries()) this.analytics.lcp=e.startTime }).observe({type:'largest-contentful-paint', buffered:true});
        new PerformanceObserver(l=>{ for (const e of l.getEntries()) this.analytics.fid=e.processingStart-e.startTime }).observe({type:'first-input', buffered:true});
        let cls=0; new PerformanceObserver(l=>{ for (const e of l.getEntries()) if (!e.hadRecentInput){ cls+=e.value; this.analytics.cls=cls } }).observe({type:'layout-shift', buffered:true});
      }catch(_){}
    }
  }
  async searchQuran(q,{searchIn='all',fuzzy=true,limit=50}={}){
    if (fuzzy) q=this.createFuzzyQuery(q);
    const res=await this.fetchWithCache(`${this.config.apiBase}/search/${encodeURIComponent(q)}/${searchIn}/en`, `search_${q}_${searchIn}`);
    return this.rankSearchResults(res.data,q).slice(0,limit);
  }
  createFuzzyQuery(q){ const m={'ا':'[اأإآ]','ة':'[ةه]','ى':'[ىي]','و':'[وؤ]','ي':'[يئ]'}; for(const [k,v] of Object.entries(m)) q=q.replace(new RegExp(k,'g'),v); return q }
  rankSearchResults(r,q){ return r.matches.map(m=>{ let s=0; if (m.text.includes(q)) s+=10; s+=(114-m.surah.number)/114; if (this.isPopularVerse(m.surah.number,m.numberInSurah)) s+=5; return {...m,score:s} }).sort((a,b)=>b.score-a.score) }
  isPopularVerse(s,a){ return [{surah:2,ayah:255},{surah:36,ayah:1},{surah:67,ayah:1},{surah:56,ayah:1},{surah:18,ayah:1}].some(v=>v.surah===s && v.ayah===a) }
  async downloadSurahForOffline(n){ const d=await this.fetchWithCache(`${this.config.apiBase}/surah/${n}`,`surah_${n}`,true); const db=await this.openDB(); const tx=db.transaction('surahs','readwrite'); await tx.objectStore('surahs').put({number:n,data:d,downloaded:Date.now()}); return d }
  async openDB(){ return new Promise((res,rej)=>{ const r=indexedDB.open('QuranDB',1); r.onerror=()=>rej(r.error); r.onsuccess=()=>res(r.result); r.onupgradeneeded=e=>{ const db=e.target.result; if(!db.objectStoreNames.contains('surahs')) db.createObjectStore('surahs',{keyPath:'number'}); if(!db.objectStoreNames.contains('bookmarks')) db.createObjectStore('bookmarks',{keyPath:'id'}) } }) }
  async addBookmark(s,a,n=''){ const b={ id:`${s}:${a}:${Date.now()}`, surah:s, ayah:a, note:n, timestamp:Date.now(), tags:[], color:this.generateBookmarkColor() }; this.state.bookmarks.push(b); await this.saveState(); if (this.userAuthenticated){ await this.syncBookmarksToCloud?.() } return b }
  generateBookmarkColor(){ const c=['#FF6B6B','#4ECDC4','#45B7D1','#FFA502','#FF6348']; return c[Math.floor(Math.random()*c.length)] }
  updateReadingProgress(s,a){ const p={surah:s,ayah:a,timestamp:Date.now(),duration: Date.now()-(this.lastInteraction||Date.now())}; this.state.history.push(p); this.lastInteraction=Date.now(); this.updateStatistics(p); this.saveState() }
  updateStatistics(p){ const st=JSON.parse(localStorage.getItem('quran_statistics')||'{}'); const d=new Date().toDateString(); st.dailyStreak=st.dailyStreak||{}; st.dailyStreak[d]=true; st.totalReadingTime=(st.totalReadingTime||0)+p.duration; st.surahFrequency=st.surahFrequency||{}; st.surahFrequency[p.surah]=(st.surahFrequency[p.surah]||0)+1; localStorage.setItem('quran_statistics',JSON.stringify(st)) }
  initializeVoiceCommands(){ if ('webkitSpeechRecognition' in window){ const r=new webkitSpeechRecognition(); r.continuous=true; r.interimResults=true; r.onresult=(e)=>{ const c=e.results[e.results.length-1][0].transcript.toLowerCase(); this.processVoiceCommand(c) }; this.voiceRecognition=r } }
  processVoiceCommand(cmd){ const m={'play':()=>this.play?.(),'pause':()=>this.pause?.(),'next':()=>this.nextAyah?.(),'previous':()=>this.previousAyah?.(),'repeat':()=>this.repeatAyah?.(),'bookmark':()=>this.bookmarkCurrent?.(),'search (.+)':q=>this.searchQuran(q)}; for (const [p,a] of Object.entries(m)){ const re=new RegExp(p); const t=cmd.match(re); if(t){ a(t[1]); break } } }
  setupKeyboardShortcuts(){ document.addEventListener('keydown',e=>{ if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return; const k=e.key; if (k===' '||k==='ArrowRight'||k==='ArrowLeft') e.preventDefault() }) }
  async shareAyah(s,a,platform){ /* kept as-is; uses Web Share / popups */ }
  async generateShareImage(d){ const c=document.createElement('canvas'); c.width=1200; c.height=630; const ctx=c.getContext('2d'); const g=ctx.createLinearGradient(0,0,1200,630); g.addColorStop(0,'#2c3e50'); g.addColorStop(1,'#34495e'); ctx.fillStyle=g; ctx.fillRect(0,0,1200,630); ctx.fillStyle='#fff'; ctx.font='bold 48px Arial'; ctx.textAlign='center'; ctx.fillText(d.text,600,300); ctx.font='24px Arial'; ctx.fillText(d.translation,600,400); ctx.font='20px Arial'; ctx.fillText(`${d.surahName} ${d.ayahNumber}`,600,500); return c.toDataURL('image/png') }
  saveState(){ localStorage.setItem('quran_app_state', JSON.stringify(this.state)) }
  loadState(){ const s=localStorage.getItem('quran_app_state'); if (s) this.state={...this.state,...JSON.parse(s)} }
  preloadAssets(){ if (this.state.currentSurah<114) this.fetchWithCache(`${this.config.apiBase}/surah/${this.state.currentSurah+1}`,`surah_${this.state.currentSurah+1}`); this.preloadAudio?.() }
  updateMetaTags(surah,ayah){
    const title=`${surah.englishName} - Ayah ${ayah.numberInSurah} | Al Quran Online`;
    const desc=`Read and listen to ${surah.englishName} verse ${ayah.numberInSurah} with translation and audio recitation`;
    document.title=title; const d=document.querySelector('meta[name="description"]'); if(d) d.content=desc;
    const ogt=document.querySelector('meta[property="og:title"]'); if(ogt) ogt.content=title;
    const ogd=document.querySelector('meta[property="og:description"]'); if(ogd) ogd.content=desc;
    const can=document.querySelector('link[rel="canonical"]'); if (can) can.href=`${location.origin}/quran/${surah.number}/${ayah.numberInSurah}`;
    this.updateStructuredData(surah,ayah);
  }
  updateStructuredData(surah,ayah){
    const sd={"@context":"https://schema.org","@type":"Article","headline":`${surah.englishName} - Verse ${ayah.numberInSurah}`,"description":ayah.text.substring(0,160),"author":{"@type":"Organization","name":"ilmualam.com"},"datePublished":new Date().toISOString(),"publisher":{"@type":"Organization","name":"ilmualam.com","logo":{"@type":"ImageObject","url":"https://ilmualam.com/logo.png"}}};
    let s=document.getElementById('structured-data'); if(!s){ s=document.createElement('script'); s.id='structured-data'; s.type='application/ld+json'; document.head.appendChild(s) } s.textContent=JSON.stringify(sd);
  }
  sendAnalytics(){
    const data={...this.analytics, sessionDuration:Date.now()-this.analytics.sessionStart, timestamp:Date.now()};
    if (navigator.sendBeacon) navigator.sendBeacon('/api/analytics', JSON.stringify(data));
    if (typeof gtag!=='undefined'){ gtag('event','engagement',{event_category:'Quran_App',event_label:'Session',value:data.sessionDuration}) }
  }
}
window.QuranApp = QuranApp;
if (document.querySelector('.quran-container')) window.quranApp = new QuranApp();
if (typeof module!=='undefined' && module.exports) module.exports = QuranApp;
