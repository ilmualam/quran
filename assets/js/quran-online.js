// quran-tool.js
class QuranTool {
    constructor() {
        this.apiEndpoint = 'https://api.alquran.cloud/v1';
        this.currentSurah = 1;
        this.currentAyah = 1;
        this.audio = new Audio();
        this.isPlaying = false;
        this.autoPlay = false;
        this.language = 'my';
        
        this.init();
    }

    async init() {
        this.bindElements();
        this.bindEvents();
        await this.loadSurahList();
        await this.loadAyahs();
    }

    bindElements() {
        // Add all your DOM element bindings here
        this.surahSelect = document.getElementById('qrn-surah');
        this.playButton = document.getElementById('qrn-play');
        this.nextButton = document.getElementById('qrn-next');
        this.prevButton = document.getElementById('qrn-prev');
        this.autoplayCheckbox = document.getElementById('qrn-autoplay');
        this.contentDiv = document.getElementById('qrn-text');
        this.translationDiv = document.getElementById('qrn-translation');
    }

    bindEvents() {
        this.surahSelect.addEventListener('change', () => this.handleSurahChange());
        this.playButton.addEventListener('click', () => this.togglePlay());
        this.nextButton.addEventListener('click', () => this.nextAyah());
        this.prevButton.addEventListener('click', () => this.prevAyah());
        this.autoplayCheckbox.addEventListener('change', (e) => this.autoPlay = e.target.checked);
        
        this.audio.addEventListener('ended', () => {
            if (this.autoPlay) this.nextAyah();
        });
    }

    async loadSurahList() {
        try {
            const response = await fetch(`${this.apiEndpoint}/surah`);
            const data = await response.json();
            this.populateSurahSelect(data.data);
        } catch (error) {
            console.error('Error loading surah list:', error);
        }
    }

    populateSurahSelect(surahs) {
        this.surahSelect.innerHTML = surahs.map(surah => 
            `<option value="${surah.number}">${surah.number}. ${surah.name} - ${surah.englishName}</option>`
        ).join('');
    }

    async loadAyahs() {
        try {
            const response = await fetch(`${this.apiEndpoint}/surah/${this.currentSurah}`);
            const data = await response.json();
            this.renderAyahs(data.data);
        } catch (error) {
            console.error('Error loading ayahs:', error);
        }
    }

    renderAyahs(data) {
        // Implementation for rendering ayahs with translations
    }

    // Additional methods for audio control, navigation, etc.
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.quranTool = new QuranTool();
});