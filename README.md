# 📖 Al-Quran Online

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/ilmualam/quran)

A comprehensive web-based Al-Quran application featuring complete Quranic text with audio recitation and multiple translations. Created to share the beauty of the Quran with Malaysians and Muslims worldwide.

## 🌟 Features

### Core Functionality
- **📚 Complete Quran**: All 114 Surahs with complete ayahs
- **🎧 Audio Recitation**: Multiple renowned reciters including:
  - Mishary Rashid Alafasy
  - Mahmoud Khalil Al-Husary
  - Muhammad Siddiq Al-Minshawi
  - Abdul Basit
- **🌍 Multiple Translations**: Support for various languages:
  - English (Saheeh International, Muhammad Asad, Pickthall, Yusuf Ali)
  - Malay (Abdullah Basmeih)
  - Indonesian
  - Urdu (Jalandhry)

### Interactive Features
- **🔍 Search**: Search across all verses of the Quran
- **🔖 Bookmarks**: Save your favorite ayahs for quick access
- **📋 Copy & Share**: Easily copy and share verses on social media
- **▶️ Audio Controls**: Play, pause, stop, previous, next with auto-play
- **🎯 Highlight**: Auto-highlight currently playing ayah
- **🔁 Repeat Mode**: Repeat individual ayah for memorization
- **🌙 Night Mode**: Eye-friendly dark theme
- **📏 Adjustable Font**: Multiple font sizes for comfortable reading
- **⌨️ Keyboard Shortcuts**: 
  - `Space` - Play/Pause
  - `←` - Previous Ayah
  - `→` - Next Ayah

### Technical Features
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **⚡ Fast Loading**: Optimized performance with caching
- **🔄 Progressive Enhancement**: Works even with slow connections
- **♿ Accessible**: WCAG compliant with semantic HTML
- **📊 Analytics Ready**: Built-in analytics tracking
- **🗺️ SEO Optimized**: With structured data and meta tags
- **💾 Offline Support**: Service worker ready for offline access

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for API access)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ilmualam/quran.git
   cd quran
   ```

2. **Open the application**
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     # Using Python
     python -m http.server 8000
     
     # Using Node.js
     npx serve
     
     # Using PHP
     php -S localhost:8000
     ```

3. **Access the application**
   - Local: Open `http://localhost:8000` in your browser
   - Online: Visit [https://ilmualam.github.io/quran/](https://ilmualam.github.io/quran/)

### Usage

1. **Select a Surah**: Choose from the dropdown menu
2. **Choose Reciter**: Select your preferred reciter
3. **Pick Translation**: Choose your preferred language
4. **Read and Listen**: Click play or on individual ayah actions
5. **Search**: Use the search box to find specific verses
6. **Customize**: Adjust font size and enable night mode as needed

## 📁 Project Structure

```
quran/
├── index.html              # Main HTML file
├── README.md               # Project documentation
├── LICENSE                 # MIT License
└── assets/
    └── js/
        ├── quran-version2.js    # Main application logic
        ├── quran-tool.js        # Utility functions
        └── sitemap.js           # Sitemap generation
```

## 🛠️ Technology Stack

- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern responsive design with CSS Grid and Flexbox
- **JavaScript (ES6+)**: Vanilla JavaScript with async/await
- **API**: [AlQuran Cloud API](https://alquran.cloud/api) for Quran data
- **Audio**: [Islamic Network CDN](https://cdn.islamic.network/) for audio recitations

## 📱 Browser Support

| Browser | Version |
|---------|---------|
| Chrome  | 90+     |
| Firefox | 88+     |
| Safari  | 14+     |
| Edge    | 90+     |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 API Reference

This project uses the [AlQuran Cloud API](https://alquran.cloud/api) which provides:
- Quran text in multiple editions
- Audio recitations
- Translations in multiple languages
- Search functionality

## 🐛 Known Issues

None at the moment. If you find any bugs, please [open an issue](https://github.com/ilmualam/quran/issues).

## 🔮 Future Enhancements

- [ ] Offline mode with service workers
- [ ] Tajweed highlighting
- [ ] Multiple bookmarks with notes
- [ ] Reading progress tracking
- [ ] Custom color themes
- [ ] Word-by-word translation
- [ ] Verse memorization tools
- [ ] Daily verse notifications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **ilmualam.com** - *Initial work* - [ilmualam](https://github.com/ilmualam)

## 🙏 Acknowledgments

- **AlQuran Cloud API** for providing comprehensive Quran data
- **Islamic Network** for audio recitations
- All the reciters whose beautiful recitations are featured
- The open-source community for inspiration and support
- Malaysian Muslim community for whom this was created

## 📞 Contact

- Website: [ilmualam.com](https://ilmualam.com)
- GitHub: [@ilmualam](https://github.com/ilmualam)

## 💝 Support

If you find this project useful, please consider:
- ⭐ Starring this repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤲 Making dua for the developers and all Muslims

---

**Made with ❤️ for Muslims worldwide | الحمد لله**
