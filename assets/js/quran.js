/**
 * Waktu Solat Malaysia - Professional Prayer Times Tool
 * Version: 2.0.0
 * Author: IlmuAlam.com
 * License: MIT
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    API_BASE: 'https://api.aladhan.com/v1',
    OVERPASS_API: 'https://overpass-api.de/api/interpreter',
    JAKIM_ZONES: {
      'JHR01': { state: 'Johor', lat: 2.0167, lon: 104.5333 },
      'JHR02': { state: 'Johor', lat: 1.4655, lon: 103.7578 },
      'JHR03': { state: 'Johor', lat: 2.0333, lon: 103.3167 },
      'JHR04': { state: 'Johor', lat: 1.8542, lon: 103.0594 },
      'KDH01': { state: 'Kedah', lat: 6.1248, lon: 100.3678 },
      'KDH02': { state: 'Kedah', lat: 5.7759, lon: 100.4928 },
      'KDH03': { state: 'Kedah', lat: 6.4414, lon: 100.8014 },
      'KDH04': { state: 'Kedah', lat: 5.6837, lon: 100.9186 },
      'KDH05': { state: 'Kedah', lat: 5.3648, lon: 100.5692 },
      'KDH06': { state: 'Kedah', lat: 6.3500, lon: 99.8000 },
      'KDH07': { state: 'Kedah', lat: 5.8000, lon: 100.4167 },
      'KTN01': { state: 'Kelantan', lat: 6.1379, lon: 102.2381 },
      'KTN03': { state: 'Kelantan', lat: 5.1667, lon: 101.9667 },
      'MLK01': { state: 'Melaka', lat: 2.1896, lon: 102.2501 },
      'NGS01': { state: 'Negeri Sembilan', lat: 2.7308, lon: 102.4267 },
      'NGS02': { state: 'Negeri Sembilan', lat: 2.7258, lon: 101.9424 },
      'PHG01': { state: 'Pahang', lat: 2.8167, lon: 104.1667 },
      'PHG02': { state: 'Pahang', lat: 3.8077, lon: 103.3260 },
      'PHG03': { state: 'Pahang', lat: 3.4667, lon: 102.4167 },
      'PHG04': { state: 'Pahang', lat: 3.4000, lon: 101.9000 },
      'PHG05': { state: 'Pahang', lat: 3.4167, lon: 101.6833 },
      'PHG06': { state: 'Pahang', lat: 3.7167, lon: 101.7333 },
      'PLS01': { state: 'Perlis', lat: 6.4449, lon: 100.2048 },
      'PNG01': { state: 'Pulau Pinang', lat: 5.4141, lon: 100.3288 },
      'PRK01': { state: 'Perak', lat: 4.0833, lon: 101.3833 },
      'PRK02': { state: 'Perak', lat: 4.5921, lon: 101.0901 },
      'PRK03': { state: 'Perak', lat: 5.1000, lon: 100.9833 },
      'PRK04': { state: 'Perak', lat: 5.4833, lon: 101.3833 },
      'PRK05': { state: 'Perak', lat: 4.0167, lon: 101.0167 },
      'PRK06': { state: 'Perak', lat: 5.0000, lon: 100.7333 },
      'PRK07': { state: 'Perak', lat: 4.8500, lon: 100.7833 },
      'SBH01': { state: 'Sabah', lat: 5.8333, lon: 118.0833 },
      'SBH02': { state: 'Sabah', lat: 6.9167, lon: 116.8167 },
      'SBH03': { state: 'Sabah', lat: 5.9788, lon: 116.0753 },
      'SBH04': { state: 'Sabah', lat: 6.0833, lon: 116.5583 },
      'SBH05': { state: 'Sabah', lat: 5.3500, lon: 115.7500 },
      'SBH06': { state: 'Sabah', lat: 5.3333, lon: 116.1667 },
      'SBH07': { state: 'Sabah', lat: 6.3833, lon: 116.6667 },
      'SBH08': { state: 'Sabah', lat: 5.4667, lon: 116.2667 },
      'SBH09': { state: 'Sabah', lat: 4.2500, lon: 117.8833 },
      'SGR01': { state: 'Selangor', lat: 3.0738, lon: 101.5183 },
      'SGR02': { state: 'Selangor', lat: 3.6667, lon: 101.0833 },
      'SGR03': { state: 'Selangor', lat: 3.0333, lon: 101.4500 },
      'SWK01': { state: 'Sarawak', lat: 1.5500, lon: 110.3333 },
      'SWK02': { state: 'Sarawak', lat: 2.2945, lon: 111.8270 },
      'SWK03': { state: 'Sarawak', lat: 2.1896, lon: 111.8270 },
      'SWK04': { state: 'Sarawak', lat: 4.3895, lon: 113.9917 },
      'SWK05': { state: 'Sarawak', lat: 4.8333, lon: 115.0000 },
      'SWK06': { state: 'Sarawak', lat: 3.1667, lon: 113.0333 },
      'SWK07': { state: 'Sarawak', lat: 1.6667, lon: 109.8333 },
      'SWK08': { state: 'Sarawak', lat: 1.4000, lon: 110.4167 },
      'SWK09': { state: 'Sarawak', lat: 2.8333, lon: 113.8333 },
      'TRG01': { state: 'Terengganu', lat: 5.3302, lon: 103.1408 },
      'TRG02': { state: 'Terengganu', lat: 5.8167, lon: 102.5667 },
      'TRG03': { state: 'Terengganu', lat: 5.1667, lon: 102.8667 },
      'TRG04': { state: 'Terengganu', lat: 4.7667, lon: 103.4333 },
      'WLY01': { state: 'W.P. Kuala Lumpur', lat: 3.1390, lon: 101.6869 },
      'WLY02': { state: 'W.P. Labuan', lat: 5.2831, lon: 115.2308 }
    },
    PRAYER_NAMES: {
      imsak: 'Imsak',
      fajr: 'Subuh',
      sunrise: 'Syuruk',
      dhuhr: 'Zohor',
      asr: 'Asar',
      maghrib: 'Maghrib',
      isha: 'Isyak'
    }
  };

  // State Management
  const State = {
    currentLocation: null,
    currentZone: null,
    prayerTimes: null,
    nextPrayer: null,
    countdownInterval: null,
    compassInterval: null,
    userLat: null,
    userLon: null
  };

  // DOM Elements
  const Elements = {
    locationName: null,
    locationZone: null,
    dateGregorian: null,
    dateHijri: null,
    stateSelect: null,
    prayerTimes: null,
    nextName: null,
    countdown: null,
    mosqueSection: null,
    mosqueList: null,
    qiblaSection: null,
    compass: null,
    qiblaAngle: null,
    overlay: null
  };

  // Initialize
  function init() {
    cacheElements();
    attachEventListeners();
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Auto-detect location on load
    getUserLocation();
  }

  // Cache DOM Elements
  function cacheElements() {
    Elements.locationName = document.getElementById('wsLocationName');
    Elements.locationZone = document.getElementById('wsLocationZone');
    Elements.dateGregorian = document.getElementById('wsDateGregorian');
    Elements.dateHijri = document.getElementById('wsDateHijri');
    Elements.stateSelect = document.getElementById('wsStateSelect');
    Elements.prayerTimes = document.getElementById('wsPrayerTimes');
    Elements.nextName = document.getElementById('wsNextName');
    Elements.countdown = document.getElementById('wsCountdown');
    Elements.mosqueSection = document.getElementById('wsMosqueSection');
    Elements.mosqueList = document.getElementById('wsMosqueList');
    Elements.qiblaSection = document.getElementById('wsQiblaSection');
    Elements.compass = document.getElementById('wsCompass');
    Elements.qiblaAngle = document.getElementById('wsQiblaAngle');
    Elements.overlay = document.getElementById('wsOverlay');
  }

  // Attach Event Listeners
  function attachEventListeners() {
    document.getElementById('wsGetLocation')?.addEventListener('click', getUserLocation);
    Elements.stateSelect?.addEventListener('change', handleZoneChange);
    document.getElementById('wsFindMosque')?.addEventListener('click', findNearbyMosques);
    document.getElementById('wsQibla')?.addEventListener('click', toggleQibla);
    document.getElementById('wsDownloadPDF')?.addEventListener('click', downloadPDF);
    document.getElementById('wsShare')?.addEventListener('click', shareTimes);
  }

  // Get User Location
  function getUserLocation() {
    if (!navigator.geolocation) {
      showNotification('Pelayar anda tidak menyokong geolokasi', 'error');
      return;
    }

    showLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        State.userLat = position.coords.latitude;
        State.userLon = position.coords.longitude;
        
        // Find nearest zone
        const nearestZone = findNearestZone(State.userLat, State.userLon);
        Elements.stateSelect.value = nearestZone;
        
        await loadPrayerTimes(nearestZone, State.userLat, State.userLon);
        showLoading(false);
      },
      (error) => {
        showLoading(false);
        showNotification('Tidak dapat mengesan lokasi. Sila pilih zon secara manual.', 'warning');
        console.error('Geolocation error:', error);
        
        // Default to Kuala Lumpur
        Elements.stateSelect.value = 'WLY01';
        handleZoneChange();
      }
    );
  }

  // Find Nearest Zone
  function findNearestZone(lat, lon) {
    let nearest = 'WLY01';
    let minDistance = Infinity;

    for (const [zone, data] of Object.entries(CONFIG.JAKIM_ZONES)) {
      const distance = calculateDistance(lat, lon, data.lat, data.lon);
      if (distance < minDistance) {
        minDistance = distance;
        nearest = zone;
      }
    }

    return nearest;
  }

  // Calculate Distance (Haversine Formula)
  function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in km
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  function toRad(degrees) {
    return degrees * (Math.PI / 180);
  }

  // Handle Zone Change
  async function handleZoneChange() {
    const zone = Elements.stateSelect.value;
    if (!zone) return;

    const zoneData = CONFIG.JAKIM_ZONES[zone];
    if (!zoneData) return;

    showLoading(true);
    await loadPrayerTimes(zone, zoneData.lat, zoneData.lon);
    showLoading(false);
  }

  // Load Prayer Times
  async function loadPrayerTimes(zone, lat, lon) {
    try {
      const zoneData = CONFIG.JAKIM_ZONES[zone];
      State.currentZone = zone;
      State.currentLocation = { lat, lon };

      // Update location display
      Elements.locationName.textContent = zoneData.state;
      const optionText = Elements.stateSelect.options[Elements.stateSelect.selectedIndex]?.text || '';
      Elements.locationZone.textContent = optionText.replace(/^.*?\-\s*/, '') || zone;

      // Fetch prayer times from Aladhan API
      const today = new Date();
      const timestamp = Math.floor(today.getTime() / 1000);
      
      const response = await fetch(
        `${CONFIG.API_BASE}/timings/${timestamp}?latitude=${lat}&longitude=${lon}&method=3`
      );

      if (!response.ok) throw new Error('API request failed');

      const data = await response.json();
      
      if (data.code === 200 && data.data) {
        displayPrayerTimes(data.data);
        startCountdown();
      } else {
        throw new Error('Invalid API response');
      }

    } catch (error) {
      console.error('Error loading prayer times:', error);
      showNotification('Ralat memuat waktu solat. Sila cuba lagi.', 'error');
    }
  }

  // Display Prayer Times
  function displayPrayerTimes(data) {
    const times = data.timings;
    State.prayerTimes = {
      imsak: times.Imsak || times.Fajr,
      subuh: times.Fajr,
      syuruk: times.Sunrise,
      zohor: times.Dhuhr,
      asar: times.Asr,
      maghrib: times.Maghrib,
      isyak: times.Isha
    };

    // Update prayer cards
    const cards = {
      imsak: State.prayerTimes.imsak,
      subuh: State.prayerTimes.subuh,
      syuruk: State.prayerTimes.syuruk,
      dhuhr: State.prayerTimes.zohor,
      asr: State.prayerTimes.asar,
      maghrib: State.prayerTimes.maghrib,
      isha: State.prayerTimes.isyak
    };

    for (const [prayer, time] of Object.entries(cards)) {
      const card = document.querySelector(`[data-prayer="${prayer}"]`);
      if (card) {
        const timeElement = card.querySelector('.ws-prayer-time');
        if (timeElement) {
          timeElement.textContent = formatTime(time);
        }
      }
    }

    // Highlight current prayer
    highlightCurrentPrayer();
  }

  // Format Time (24h to 12h)
  function formatTime(time24) {
    if (!time24) return '--:--';
    const [hours, minutes] = time24.split(':');
    return `${hours}:${minutes}`;
  }

  // Highlight Current Prayer
  function highlightCurrentPrayer() {
    const now = new Date();
    const currentTime = now.getHours() * 60 + now.getMinutes();

    const prayers = [
      { name: 'imsak', time: State.prayerTimes.imsak },
      { name: 'subuh', time: State.prayerTimes.subuh },
      { name: 'syuruk', time: State.prayerTimes.syuruk },
      { name: 'dhuhr', time: State.prayerTimes.zohor },
      { name: 'asr', time: State.prayerTimes.asar },
      { name: 'maghrib', time: State.prayerTimes.maghrib },
      { name: 'isha', time: State.prayerTimes.isyak }
    ];

    // Remove all highlights
    document.querySelectorAll('.ws-prayer-card').forEach(card => {
      card.classList.remove('ws-current', 'ws-highlight');
    });

    // Find next prayer
    let nextPrayer = null;
    for (let i = 0; i < prayers.length; i++) {
      const prayer = prayers[i];
      const [hours, minutes] = prayer.time.split(':');
      const prayerTime = parseInt(hours) * 60 + parseInt(minutes);

      if (currentTime < prayerTime) {
        nextPrayer = prayer;
        break;
      }
    }

    // If no next prayer today, next is tomorrow's Imsak
    if (!nextPrayer) {
      nextPrayer = prayers[0];
    }

    State.nextPrayer = nextPrayer;

    // Highlight next prayer card
    const nextCard = document.querySelector(`[data-prayer="${nextPrayer.name}"]`);
    if (nextCard) {
      nextCard.classList.add('ws-highlight');
    }
  }

  // Start Countdown
  function startCountdown() {
    if (State.countdownInterval) {
      clearInterval(State.countdownInterval);
    }

    updateCountdown();
    State.countdownInterval = setInterval(updateCountdown, 1000);
  }

  // Update Countdown
  function updateCountdown() {
    if (!State.nextPrayer) return;

    const now = new Date();
    const [hours, minutes] = State.nextPrayer.time.split(':');
    
    let nextPrayerDate = new Date();
    nextPrayerDate.setHours(parseInt(hours), parseInt(minutes), 0, 0);

    // If prayer time has passed, set to tomorrow
    if (nextPrayerDate <= now) {
      nextPrayerDate.setDate(nextPrayerDate.getDate() + 1);
    }

    const diff = nextPrayerDate - now;
    
    const h = Math.floor(diff / 1000 / 60 / 60);
    const m = Math.floor((diff / 1000 / 60) % 60);
    const s = Math.floor((diff / 1000) % 60);

    Elements.countdown.textContent = 
      `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    
    // Update next prayer name
    const prayerNames = {
      imsak: 'Imsak',
      subuh: 'Subuh',
      syuruk: 'Syuruk',
      dhuhr: 'Zohor',
      asr: 'Asar',
      maghrib: 'Maghrib',
      isha: 'Isyak'
    };
    Elements.nextName.textContent = prayerNames[State.nextPrayer.name] || State.nextPrayer.name;
  }

  // Update Date & Time
  function updateDateTime() {
    const now = new Date();
    
    // Gregorian Date
    const options = { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    };
    Elements.dateGregorian.textContent = now.toLocaleDateString('ms-MY', options);

    // Hijri Date (approximation - for production use proper Hijri calendar API)
    const hijriDate = getHijriDate(now);
    Elements.dateHijri.textContent = hijriDate;
  }

  // Get Hijri Date (Simple approximation)
  function getHijriDate(date) {
    // This is a simplified version. For production, use proper Hijri calendar conversion
    // You can fetch from Aladhan API or use a library
    const gregDate = date.toISOString().split('T')[0];
    
    // For now, return a placeholder
    // In production, fetch from API or calculate properly
    return 'Mengira tarikh Hijrah...';
  }

  // Find Nearby Mosques
  async function findNearbyMosques() {
    if (!State.userLat || !State.userLon) {
      // Use zone coordinates if user location not available
      const zoneData = CONFIG.JAKIM_ZONES[State.currentZone];
      if (zoneData) {
        State.userLat = zoneData.lat;
        State.userLon = zoneData.lon;
      } else {
        showNotification('Sila aktifkan lokasi anda terlebih dahulu', 'warning');
        return;
      }
    }

    showLoading(true);
    Elements.mosqueSection.style.display = 'block';
    Elements.mosqueList.innerHTML = '<div class="ws-loading">Mencari masjid terdekat...</div>';

    try {
      // Using Overpass API to find mosques
      const radius = 5000; // 5km radius
      const query = `
        [out:json][timeout:25];
        (
          node["amenity"="place_of_worship"]["religion"="muslim"](around:${radius},${State.userLat},${State.userLon});
          way["amenity"="place_of_worship"]["religion"="muslim"](around:${radius},${State.userLat},${State.userLon});
        );
        out body;
        >;
        out skel qt;
      `;

      const response = await fetch(CONFIG.OVERPASS_API, {
        method: 'POST',
        body: 'data=' + encodeURIComponent(query)
      });

      if (!response.ok) throw new Error('Overpass API error');

      const data = await response.json();
      displayMosques(data.elements);

    } catch (error) {
      console.error('Error finding mosques:', error);
      Elements.mosqueList.innerHTML = '<div class="ws-loading">Ralat mencari masjid. Sila cuba lagi.</div>';
    } finally {
      showLoading(false);
    }
  }

  // Display Mosques
  function displayMosques(mosques) {
    if (!mosques || mosques.length === 0) {
      Elements.mosqueList.innerHTML = '<div class="ws-loading">Tiada masjid ditemui dalam radius 5km</div>';
      return;
    }

    // Calculate distances and sort
    const mosquesWithDistance = mosques
      .filter(m => m.lat && m.lon && m.tags && (m.tags.name || m.tags['name:ms']))
      .map(mosque => ({
        name: mosque.tags.name || mosque.tags['name:ms'] || 'Masjid',
        lat: mosque.lat,
        lon: mosque.lon,
        distance: calculateDistance(State.userLat, State.userLon, mosque.lat, mosque.lon)
      }))
      .sort((a, b) => a.distance - b.distance)
      .slice(0, 10); // Top 10 nearest

    if (mosquesWithDistance.length === 0) {
      Elements.mosqueList.innerHTML = '<div class="ws-loading">Tiada masjid ditemui</div>';
      return;
    }

    const html = mosquesWithDistance.map(mosque => `
      <div class="ws-mosque-item">
        <div class="ws-mosque-info">
          <div class="ws-mosque-name">🕌 ${mosque.name}</div>
          <div class="ws-mosque-distance">📍 ${mosque.distance.toFixed(2)} km dari lokasi anda</div>
        </div>
        <a href="https://www.google.com/maps/dir/?api=1&destination=${mosque.lat},${mosque.lon}" 
           target="_blank" 
           rel="noopener noreferrer"
           class="ws-mosque-directions">
          Arah
        </a>
      </div>
    `).join('');

    Elements.mosqueList.innerHTML = html;
  }

  // Toggle Qibla Compass
  function toggleQibla() {
    if (Elements.qiblaSection.style.display === 'none' || !Elements.qiblaSection.style.display) {
      showQibla();
    } else {
      hideQibla();
    }
  }

  // Show Qibla
  function showQibla() {
    if (!State.userLat || !State.userLon) {
      const zoneData = CONFIG.JAKIM_ZONES[State.currentZone];
      if (zoneData) {
        State.userLat = zoneData.lat;
        State.userLon = zoneData.lon;
      } else {
        showNotification('Sila aktifkan lokasi anda', 'warning');
        return;
      }
    }

    Elements.qiblaSection.style.display = 'block';
    
    // Calculate Qibla direction
    const qiblaAngle = calculateQibla(State.userLat, State.userLon);
    Elements.qiblaAngle.textContent = `${Math.round(qiblaAngle)}°`;

    // Start compass if device supports orientation
    if (window.DeviceOrientationEvent) {
      startCompass(qiblaAngle);
    } else {
      // Static display
      Elements.compass.style.transform = `rotate(${qiblaAngle}deg)`;
    }
  }

  // Hide Qibla
  function hideQibla() {
    Elements.qiblaSection.style.display = 'none';
    stopCompass();
  }

  // Calculate Qibla Direction
  function calculateQibla(lat, lon) {
    // Kaaba coordinates
    const kaabaLat = 21.4225;
    const kaabaLon = 39.8262;

    const dLon = toRad(kaabaLon - lon);
    const y = Math.sin(dLon) * Math.cos(toRad(kaabaLat));
    const x = Math.cos(toRad(lat)) * Math.sin(toRad(kaabaLat)) -
              Math.sin(toRad(lat)) * Math.cos(toRad(kaabaLat)) * Math.cos(dLon);
    
    let bearing = Math.atan2(y, x);
    bearing = (bearing * 180 / Math.PI + 360) % 360;
    
    return bearing;
  }

  // Start Compass
  function startCompass(qiblaAngle) {
    if (State.compassInterval) {
      stopCompass();
    }

    window.addEventListener('deviceorientationabsolute', handleOrientation);
    window.addEventListener('deviceorientation', handleOrientation);

    function handleOrientation(event) {
      let heading = event.alpha || event.webkitCompassHeading || 0;
      
      // Adjust for iOS
      if (event.webkitCompassHeading) {
        heading = event.webkitCompassHeading;
      } else {
        heading = 360 - heading;
      }

      const rotation = heading - qiblaAngle;
      Elements.compass.style.transform = `rotate(${-rotation}deg)`;
    }
  }

  // Stop Compass
  function stopCompass() {
    window.removeEventListener('deviceorientationabsolute', handleOrientation);
    window.removeEventListener('deviceorientation', handleOrientation);
  }

  // Download PDF
  async function downloadPDF() {
    if (!State.prayerTimes) {
      showNotification('Sila muat waktu solat terlebih dahulu', 'warning');
      return;
    }

    showLoading(true);

    try {
      // Create simple HTML for PDF
      const zoneData = CONFIG.JAKIM_ZONES[State.currentZone];
      const pdfContent = `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Waktu Solat - ${zoneData.state}</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 40px; }
            h1 { color: #249749; text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-top: 30px; }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #249749; color: white; }
            .footer { margin-top: 40px; text-align: center; font-size: 12px; color: #666; }
          </style>
        </head>
        <body>
          <h1>🕌 Waktu Solat ${zoneData.state}</h1>
          <p style="text-align:center;">${Elements.locationZone.textContent}</p>
          <p style="text-align:center;">${Elements.dateGregorian.textContent}</p>
          <table>
            <tr><th>Waktu Solat</th><th>Masa</th></tr>
            <tr><td>Imsak</td><td>${formatTime(State.prayerTimes.imsak)}</td></tr>
            <tr><td>Subuh</td><td>${formatTime(State.prayerTimes.subuh)}</td></tr>
            <tr><td>Syuruk</td><td>${formatTime(State.prayerTimes.syuruk)}</td></tr>
            <tr><td>Zohor</td><td>${formatTime(State.prayerTimes.zohor)}</td></tr>
            <tr><td>Asar</td><td>${formatTime(State.prayerTimes.asar)}</td></tr>
            <tr><td>Maghrib</td><td>${formatTime(State.prayerTimes.maghrib)}</td></tr>
            <tr><td>Isyak</td><td>${formatTime(State.prayerTimes.isyak)}</td></tr>
          </table>
          <div class="footer">
            Dijana dari www.ilmualam.com<br>
            ${new Date().toLocaleDateString('ms-MY')}
          </div>
        </body>
        </html>
      `;

      // Open print dialog
      const printWindow = window.open('', '', 'height=600,width=800');
      printWindow.document.write(pdfContent);
      printWindow.document.close();
      printWindow.focus();
      
      setTimeout(() => {
        printWindow.print();
        showLoading(false);
      }, 250);

    } catch (error) {
      console.error('PDF error:', error);
      showNotification('Ralat menjana PDF', 'error');
      showLoading(false);
    }
  }

  // Share Times
  async function shareTimes() {
    if (!State.prayerTimes) {
      showNotification('Sila muat waktu solat terlebih dahulu', 'warning');
      return;
    }

    const zoneData = CONFIG.JAKIM_ZONES[State.currentZone];
    const shareText = `🕌 Waktu Solat ${zoneData.state}\n${Elements.dateGregorian.textContent}\n\n` +
      `Imsak: ${formatTime(State.prayerTimes.imsak)}\n` +
      `Subuh: ${formatTime(State.prayerTimes.subuh)}\n` +
      `Syuruk: ${formatTime(State.prayerTimes.syuruk)}\n` +
      `Zohor: ${formatTime(State.prayerTimes.zohor)}\n` +
      `Asar: ${formatTime(State.prayerTimes.asar)}\n` +
      `Maghrib: ${formatTime(State.prayerTimes.maghrib)}\n` +
      `Isyak: ${formatTime(State.prayerTimes.isyak)}\n\n` +
      `Dapatkan waktu solat di www.ilmualam.com`;

    // Try native share API
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Waktu Solat Malaysia',
          text: shareText,
          url: window.location.href
        });
      } catch (error) {
        if (error.name !== 'AbortError') {
          fallbackShare(shareText);
        }
      }
    } else {
      fallbackShare(shareText);
    }
  }

  // Fallback Share (Copy to clipboard)
  function fallbackShare(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        showNotification('Waktu solat disalin ke clipboard!', 'success');
      }).catch(() => {
        showNotification('Tidak dapat menyalin', 'error');
      });
    } else {
      // Old method
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        showNotification('Waktu solat disalin ke clipboard!', 'success');
      } catch (error) {
        showNotification('Tidak dapat menyalin', 'error');
      }
      document.body.removeChild(textarea);
    }
  }

  // Show Loading
  function showLoading(show) {
    Elements.overlay.style.display = show ? 'flex' : 'none';
  }

  // Show Notification
  function showNotification(message, type = 'info') {
    // Simple alert for now - you can enhance this with custom notifications
    alert(message);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();