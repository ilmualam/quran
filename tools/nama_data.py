"""Curated names for /nama-bayi-islam/, written and checked by the editor. They replace any legacy row with the same
spelling and gender (tools/nama/legacy.json, the dataset of name.ilmualam.com), so a correction here always wins.

Line format: Name|Arabic|Malay meaning|source|themes
  source: n = Nabi & keluarga Nabi, s = sahabat/sahabiyah & tokoh salaf, u = nama Islam umum
  themes: c cahaya, k kekuatan, b keberkatan, i ilmu, m kemuliaan, e keindahan, a alam, h akhlak, s syurga
Whether the word is in the Quran is NOT typed here: tools/nama.py finds it in data-surah/ and records the ayah."""

LELAKI = """
Adam|آدَم|Nabi Adam a.s., manusia pertama dan bapa sekalian manusia|n|m
Idris|إِدْرِيس|Nabi Idris a.s., yang diangkat ke tempat yang tinggi (Maryam 19:57)|n|im
Nuh|نُوح|Nabi Nuh a.s., Rasul Ulul Azmi yang paling lama berdakwah|n|kh
Hud|هُود|Nabi Hud a.s., diutus kepada kaum 'Ad|n|m
Soleh|صَالِح|Yang baik dan soleh; Nabi Soleh a.s.|n|h
Ibrahim|إِبْرَاهِيم|Nabi Ibrahim a.s., Khalilullah dan bapa para nabi|n|mb
Lut|لُوط|Nabi Lut a.s., anak saudara Nabi Ibrahim|n|m
Ismail|إِسْمَاعِيل|Nabi Ismail a.s., putera Nabi Ibrahim yang sabar|n|hb
Ishak|إِسْحَاق|Nabi Ishak a.s., putera Nabi Ibrahim dan Sarah|n|b
Yaakub|يَعْقُوب|Nabi Yaakub a.s. (Israil), bapa Nabi Yusuf|n|m
Yusuf|يُوسُف|Nabi Yusuf a.s., yang dikurniakan ketampanan dan kebijaksanaan|n|ei
Ayub|أَيُّوب|Nabi Ayub a.s., lambang kesabaran ketika diuji|n|hk
Syuaib|شُعَيْب|Nabi Syuaib a.s., diutus kepada penduduk Madyan|n|m
Musa|مُوسَى|Nabi Musa a.s., Kalimullah dan Rasul Ulul Azmi|n|km
Harun|هَارُون|Nabi Harun a.s., saudara dan pembantu Nabi Musa|n|m
Zulkifli|ذُو الْكِفْل|Nabi Zulkifli a.s., yang memiliki bahagian (pahala) yang besar|n|m
Daud|دَاوُد|Nabi Daud a.s., raja dan nabi yang diberi kitab Zabur|n|km
Sulaiman|سُلَيْمَان|Nabi Sulaiman a.s., raja yang memahami bahasa haiwan|n|mi
Ilyas|إِلْيَاس|Nabi Ilyas a.s., diutus kepada Bani Israil|n|m
Ilyasa|الْيَسَع|Nabi Ilyasa' a.s., pengganti Nabi Ilyas|n|m
Yunus|يُونُس|Nabi Yunus a.s., Zun-Nun yang bertaubat dalam perut ikan|n|h
Zakaria|زَكَرِيَّا|Nabi Zakaria a.s., penjaga Maryam dan bapa Nabi Yahya|n|b
Yahya|يَحْيَى|Nabi Yahya a.s.; nama yang tiada sebelumnya (Maryam 19:7)|n|b
Isa|عِيسَى|Nabi Isa a.s., Al-Masih, Rasul Ulul Azmi|n|m
Muhammad|مُحَمَّد|Yang sangat terpuji; nama Rasulullah ﷺ|n|mb
Ahmad|أَحْمَد|Yang paling terpuji; nama Rasulullah ﷺ dalam As-Saff 61:6|n|mb
Mustafa|مُصْطَفَى|Yang terpilih; gelaran Rasulullah ﷺ|n|m
Mahmud|مَحْمُود|Yang dipuji|u|m
Hamid|حَامِد|Yang banyak memuji Allah|u|bh
Qasim|قَاسِم|Yang membahagikan; nama putera Rasulullah ﷺ|n|m
Ibrahim Khalil|إِبْرَاهِيم خَلِيل|Ibrahim sahabat setia|u|m
Abu Bakar|أَبُو بَكْر|Khalifah pertama, sahabat paling setia Rasulullah ﷺ|s|mh
Umar|عُمَر|Khalifah kedua, Al-Faruq yang adil; yang panjang umur|s|km
Uthman|عُثْمَان|Khalifah ketiga, Zun-Nurain yang pemurah|s|mh
Ali|عَلِيّ|Yang tinggi; khalifah keempat dan menantu Rasulullah ﷺ|s|mk
Hamzah|حَمْزَة|Singa Allah, bapa saudara Rasulullah ﷺ|s|k
Abbas|عَبَّاس|Singa; bapa saudara Rasulullah ﷺ|s|k
Bilal|بِلَال|Muazzin Rasulullah ﷺ; kesegaran|s|hb
Khalid|خَالِد|Yang kekal; Khalid al-Walid, Saifullah|s|k
Zaid|زَيْد|Pertambahan; satu-satunya sahabat yang namanya disebut dalam Al-Quran|s|b
Usamah|أُسَامَة|Singa; kesayangan Rasulullah ﷺ|s|k
Muaz|مُعَاذ|Yang dilindungi; sahabat yang paling tahu halal dan haram|s|i
Salman|سَلْمَان|Yang selamat; Salman al-Farisi|s|b
Ammar|عَمَّار|Yang memakmurkan; Ammar bin Yasir|s|k
Anas|أَنَس|Kemesraan; khadam Rasulullah ﷺ selama sepuluh tahun|s|h
Talhah|طَلْحَة|Nama sejenis pohon; Talhah bin Ubaidillah|s|ka
Zubair|زُبَيْر|Yang kuat; Az-Zubair bin al-Awwam, hawari Rasulullah ﷺ|s|k
Saad|سَعْد|Kebahagiaan dan tuah; Saad bin Abi Waqqas|s|b
Said|سَعِيد|Yang berbahagia|s|b
Ubaidah|عُبَيْدَة|Hamba kecil Allah; Abu Ubaidah al-Jarrah|s|h
Jaafar|جَعْفَر|Sungai kecil; Jaafar bin Abi Talib|s|a
Hasan|حَسَن|Yang baik dan elok; cucu Rasulullah ﷺ|n|eh
Husain|حُسَيْن|Yang baik (bentuk kecil Hasan); cucu Rasulullah ﷺ|n|eh
Abdullah|عَبْد اللَّه|Hamba Allah; nama yang paling disukai Allah (HR Muslim 2132)|u|b
Amru|عَمْرو|Kehidupan; Amru bin al-As|s|k
Musab|مُصْعَب|Yang teguh; Musab bin Umair, duta pertama Islam ke Madinah|s|k
Suhaib|صُهَيْب|Yang berambut keperangan; Suhaib ar-Rumi|s|m
Khabbab|خَبَّاب|Khabbab bin al-Arat, sahabat yang sabar diseksa|s|kh
Miqdad|مِقْدَاد|Al-Miqdad bin al-Aswad, penunggang kuda di Badar|s|k
Ubai|أُبَيّ|Yang enggan tunduk kepada kehinaan; Ubai bin Kaab, qari para sahabat|s|i
Huzaifah|حُذَيْفَة|Huzaifah bin al-Yaman, pemegang rahsia Rasulullah ﷺ|s|i
Jabir|جَابِر|Yang membaiki dan menghibur; Jabir bin Abdullah|s|h
Thabit|ثَابِت|Yang teguh; Thabit bin Qais, khatib Rasulullah ﷺ|s|k
Hassan|حَسَّان|Yang sangat baik; Hassan bin Thabit, penyair Rasulullah ﷺ|s|e
Usaid|أُسَيْد|Singa kecil; Usaid bin Hudhair|s|k
Nukman|نُعْمَان|Darah; kehidupan; An-Nukman bin Basyir|s|b
Qatadah|قَتَادَة|Nama sejenis pohon; Qatadah bin an-Nukman|s|a
Ikrimah|عِكْرِمَة|Merpati betina; Ikrimah bin Abi Jahal|s|k
Sufyan|سُفْيَان|Yang laju; Sufyan ath-Thauri, ulama hadis|s|i
Uqbah|عُقْبَة|Kesudahan; Uqbah bin Nafi', pembuka Afrika Utara|s|k
Uwais|أُوَيْس|Serigala kecil; Uwais al-Qarni, tabiin yang dipuji Rasulullah ﷺ|s|h
Hanzalah|حَنْظَلَة|Hanzalah, sahabat yang dimandikan malaikat|s|m
Rabiah|رَبِيعَة|Musim bunga; Rabiah bin Kaab|s|a
Baraa|بَرَاء|Yang bebas daripada kejahatan; Al-Baraa bin Azib|s|h
Kaab|كَعْب|Yang mulia kedudukannya; Kaab bin Malik|s|m
Arqam|أَرْقَم|Al-Arqam, rumahnya pusat dakwah pertama di Makkah|s|m
Dihyah|دِحْيَة|Dihyah al-Kalbi, sahabat yang tampan|s|e
Khubaib|خُبَيْب|Khubaib bin Adi, syahid yang teguh|s|k
Nuaim|نُعَيْم|Kenikmatan kecil; Nuaim bin Mas'ud|s|b
Sahl|سَهْل|Yang mudah dan lembut; Sahl bin Saad|s|h
Salim|سَالِم|Yang selamat; Salim maula Abi Huzaifah, qari Al-Quran|s|b
Safwan|صَفْوَان|Batu licin yang jernih|s|a
Tamim|تَمِيم|Yang sempurna dan kuat; Tamim ad-Dari|s|k
Urwah|عُرْوَة|Pegangan yang kukuh|s|k
Umair|عُمَيْر|Umur yang panjang (bentuk kecil Umar)|s|b
Ubadah|عُبَادَة|Ubadah bin as-Samit, ahli Badar|s|h
Imran|عِمْرَان|Kemakmuran; keluarga Maryam (Ali Imran)|n|bm
Luqman|لُقْمَان|Luqman al-Hakim, yang diberi hikmah (Luqman 31:12)|u|i
Zulqarnain|ذُو الْقَرْنَيْن|Raja soleh yang disebut dalam Al-Kahf 18:83|u|km
Tariq|طَارِق|Bintang yang terang pada malam hari (At-Tariq 86:3)|u|ca
Ziyad|زِيَاد|Pertambahan|u|b
Solahuddin|صَلَاح الدِّين|Kebaikan agama; Salahuddin al-Ayyubi|u|km
Nuruddin|نُور الدِّين|Cahaya agama|u|c
Saifuddin|سَيْف الدِّين|Pedang agama|u|k
Kamaluddin|كَمَال الدِّين|Kesempurnaan agama|u|m
Jamaluddin|جَمَال الدِّين|Keindahan agama|u|e
Syamsuddin|شَمْس الدِّين|Matahari agama|u|c
Badruddin|بَدْر الدِّين|Bulan purnama agama|u|c
Fakhruddin|فَخْر الدِّين|Kebanggaan agama|u|m
Najmuddin|نَجْم الدِّين|Bintang agama|u|c
Aiman|أَيْمَن|Yang diberkati; sebelah kanan|u|b
Aisy|عَيْش|Kehidupan|u|b
Aqil|عَقِيل|Yang berakal; Aqil bin Abi Talib|s|i
Arif|عَارِف|Yang mengenal dan berilmu|u|i
Arsyad|أَرْشَد|Yang paling lurus dan terpimpin|u|ih
Asyraf|أَشْرَف|Yang paling mulia|u|m
Azim|عَظِيم|Yang agung|u|m
Badr|بَدْر|Bulan purnama|u|ca
Bahij|بَهِيج|Yang ceria dan menyenangkan|u|e
Basyir|بَشِير|Pembawa berita gembira|u|b
Dhiya|ضِيَاء|Sinar cahaya|u|c
Fawwaz|فَوَّاز|Yang sentiasa berjaya|u|k
Fikri|فِكْرِي|Pemikiranku; yang suka berfikir|u|i
Firdaus|فِرْدَوْس|Syurga yang tertinggi|u|s
Ghazi|غَازِي|Pejuang|u|k
Habib|حَبِيب|Kekasih; yang dikasihi|u|h
Hadi|هَادِي|Pemberi petunjuk|u|i
Hafiz|حَافِظ|Penjaga; penghafal Al-Quran|u|i
Haikal|هَيْكَل|Binaan yang besar dan tersergam|u|k
Hamdan|حَمْدَان|Yang banyak memuji|u|b
Hanif|حَنِيف|Yang lurus agamanya (cenderung kepada tauhid)|u|h
Haris|حَارِث|Yang berusaha; peladang|u|k
Haziq|حَاذِق|Yang cerdik dan mahir|u|i
Hazim|حَازِم|Yang tegas dan bijak|u|k
Hilmi|حِلْمِي|Kesabaranku; yang penyantun|u|h
Hisyam|هِشَام|Yang pemurah|u|h
Imad|عِمَاد|Tiang; sandaran|u|k
Iqbal|إِقْبَال|Kejayaan; menghadap|u|b
Irfan|عِرْفَان|Pengetahuan dan pengenalan|u|i
Isyraq|إِشْرَاق|Sinar matahari terbit|u|ca
Izzat|عِزَّة|Kemuliaan dan kekuatan|u|m
Izzuddin|عِزّ الدِّين|Kemuliaan agama|u|m
Jalal|جَلَال|Keagungan|u|m
Jamal|جَمَال|Keindahan|u|e
Kamal|كَمَال|Kesempurnaan|u|m
Khairi|خَيْرِي|Kebaikanku; yang baik|u|b
Mikail|مِيكَائِيل|Malaikat Mikail|u|b
Mukhlis|مُخْلِص|Yang ikhlas|u|h
Munir|مُنِير|Yang bercahaya|u|c
Mustaqim|مُسْتَقِيم|Yang lurus|u|h
Nabil|نَبِيل|Yang mulia dan cerdik|u|m
Nafis|نَفِيس|Yang berharga|u|m
Naim|نَعِيم|Kenikmatan; nikmat syurga|u|s
Najmi|نَجْمِي|Bintangku|u|ca
Naufal|نَوْفَل|Yang pemurah|u|h
Nazmi|نَظْمِي|Susunanku; yang teratur|u|i
Rais|رَئِيس|Ketua; pemimpin|u|k
Rayyan|رَيَّان|Yang segar; nama pintu syurga untuk orang berpuasa (HR Al-Bukhari 1896)|u|s
Razin|رَزِين|Yang tenang dan berwibawa|u|h
Rifqi|رِفْقِي|Kelembutanku|u|h
Rizqi|رِزْقِي|Rezekiku|u|b
Saif|سَيْف|Pedang|u|k
Sami|سَامِي|Yang tinggi kedudukannya|u|m
Syafiq|شَفِيق|Yang penyayang|u|h
Syahmi|شَهْمِي|Yang berani dan berjiwa besar|u|k
Syakir|شَاكِر|Yang bersyukur|u|h
Syamil|شَامِل|Yang menyeluruh|u|m
Syauqi|شَوْقِي|Kerinduanku|u|h
Taufiq|تَوْفِيق|Pertolongan dan petunjuk Allah|u|b
Ubaidillah|عُبَيْد اللَّه|Hamba kecil Allah|u|b
Wafi|وَفِيّ|Yang setia dan menepati janji|u|h
Wajdi|وَجْدِي|Perasaanku yang mendalam|u|h
Yasin|يَاسِين|Nama surah Yasin|u|b
Yazid|يَزِيد|Yang bertambah|u|b
Zayyan|زَيَّان|Yang menghiasi|u|e
Zakwan|ذَكْوَان|Nama seorang sahabat Ansar (Zakwan bin Abd Qais)|s|m
Zikri|ذِكْرِي|Zikirku; ingatanku kepada Allah|u|b
Zuhair|زُهَيْر|Bunga kecil|u|ea
Qamar|قَمَر|Bulan|u|ca
Fajr|فَجْر|Fajar; waktu subuh|u|ca
Hilal|هِلَال|Anak bulan|u|ca
Syams|شَمْس|Matahari|u|ca
Najm|نَجْم|Bintang|u|ca
Raad|رَعْد|Guruh (nama surah Ar-Ra'd)|u|ka
Furqan|فُرْقَان|Pembeza antara hak dan batil; nama lain Al-Quran|u|i
Burhan|بُرْهَان|Bukti yang nyata|u|i
Ihsan|إِحْسَان|Berbuat baik; ibadah seolah-olah melihat Allah|u|h
Ikhlas|إِخْلَاص|Ketulusan niat kerana Allah|u|h
Ilham|إِلْهَام|Ilham; petunjuk ke dalam hati|u|i
Iman|إِيمَان|Keimanan|u|b
Islah|إِصْلَاح|Pembaikan|u|h
Raihan|رَيْحَان|Tumbuhan yang harum (Ar-Rahman 55:12)|u|as
Rasyid|رَاشِد|Yang lurus dan terpimpin|u|ih
Rauf|رَءُوف|Yang belas kasihan|u|h
Sabiq|سَابِق|Yang mendahului dalam kebaikan|u|k
Sadiq|صَادِق|Yang benar dan jujur|u|h
Siddiq|صِدِّيق|Yang sangat membenarkan; gelaran Abu Bakar|s|h
Faruq|فَارُوق|Pembeza hak dan batil; gelaran Umar|s|k
Muttaqin|مُتَّقِين|Orang-orang yang bertakwa|u|h
Muhsin|مُحْسِن|Yang berbuat baik|u|h
Mukmin|مُؤْمِن|Yang beriman|u|b
Muslih|مُصْلِح|Yang membuat kebaikan|u|h
Mujahid|مُجَاهِد|Yang bersungguh-sungguh di jalan Allah|u|k
Murshid|مُرْشِد|Pembimbing|u|i
Mursyid|مُرْشِد|Pembimbing|u|i
Naqib|نَقِيب|Ketua kaum|u|k
Nasir|نَاصِر|Penolong|u|k
Nizar|نِزَار|Nama moyang Rasulullah ﷺ (Nizar bin Ma'add)|n|m
Qais|قَيْس|Yang tegas; nama tokoh Arab|u|k
Rabih|رَابِح|Yang beruntung|u|b
Sajid|سَاجِد|Yang bersujud|u|h
Syahid|شَهِيد|Saksi; yang gugur di jalan Allah|u|k
Tahir|طَاهِر|Yang suci|u|h
Taqi|تَقِيّ|Yang bertakwa|u|h
Wasim|وَسِيم|Yang tampan|u|e
Yaqzan|يَقْظَان|Yang berjaga dan waspada|u|i
Zafir|ظَافِر|Yang menang|u|k
Zahid|زَاهِد|Yang zuhud|u|h
Zaki|زَكِيّ|Yang suci dan cerdik|u|ih
Zuhdi|زُهْدِي|Kezuhudanku|u|h
Fatih|فَاتِح|Pembuka; penakluk (Muhammad al-Fatih)|u|k
Faiq|فَائِق|Yang unggul|u|m
Fahim|فَهِيم|Yang faham|u|i
Fakhri|فَخْرِي|Kebanggaanku|u|m
Faris|فَارِس|Penunggang kuda yang berani|u|k
Fathi|فَتْحِي|Kemenanganku|u|k
Fauzan|فَوْزَان|Kejayaan|u|b
Ghani|غَنِيّ|Yang berkecukupan|u|b
Hakimi|حَكِيمِي|Yang bijaksana|u|i
Harith|حَارِث|Yang berusaha; peladang|u|k
Luthfi|لُطْفِي|Kelembutanku|u|h
Mahir|مَاهِر|Yang mahir|u|i
Majdi|مَجْدِي|Kemuliaanku|u|m
Marwan|مَرْوَان|Batu yang keras|u|k
Nabhan|نَبْهَان|Yang sedar dan cerdas|u|i
Naqiuddin|نَقِيّ الدِّين|Yang bersih agamanya|u|h
Qayyim|قَيِّم|Yang lurus; penjaga|u|h
Rafiq|رَفِيق|Teman; yang lemah lembut|u|h
Rasyad|رَشَاد|Petunjuk yang lurus|u|i
Riyadh|رِيَاض|Taman-taman|u|as
Syukri|شُكْرِي|Kesyukuranku|u|h
Ukasyah|عُكَّاشَة|Ukasyah bin Mihsan, sahabat yang dijanjikan syurga tanpa hisab|s|s
Wildan|وِلْدَان|Kanak-kanak syurga (Al-Insan 76:19)|u|s
Yusri|يُسْرِي|Kemudahanku|u|b
Zulfiqar|ذُو الْفَقَار|Nama pedang Ali bin Abi Talib|u|k
"""

PEREMPUAN = """
Aisyah|عَائِشَة|Yang hidup; isteri Rasulullah ﷺ dan Ummul Mukminin|n|mi
Fatimah|فَاطِمَة|Puteri Rasulullah ﷺ, penghulu wanita syurga|n|ms
Khadijah|خَدِيجَة|Isteri pertama Rasulullah ﷺ, Ummul Mukminin|n|m
Maryam|مَرْيَم|Ibu Nabi Isa a.s.; satu-satunya wanita yang namanya disebut dalam Al-Quran|n|mh
Hafsah|حَفْصَة|Puteri Umar dan isteri Rasulullah ﷺ|n|m
Zainab|زَيْنَب|Pohon yang harum; puteri Rasulullah ﷺ|n|ea
Ruqayyah|رُقَيَّة|Yang naik tinggi; puteri Rasulullah ﷺ|n|m
Ummu Kalthum|أُمّ كُلْثُوم|Puteri Rasulullah ﷺ|n|m
Sumayyah|سُمَيَّة|Yang tinggi; syahid pertama dalam Islam|s|k
Khaulah|خَوْلَة|Rusa betina; Khaulah binti al-Azwar, srikandi Islam|s|k
Nusaibah|نُسَيْبَة|Nusaibah binti Kaab, pembela Rasulullah ﷺ di Uhud|s|k
Asma|أَسْمَاء|Nama-nama; Asma' binti Abu Bakar, Zatun Nitaqain|s|m
Safiyyah|صَفِيَّة|Yang terpilih dan jernih; Ummul Mukminin|n|m
Juwairiyah|جُوَيْرِيَة|Gadis kecil; Ummul Mukminin|n|m
Maimunah|مَيْمُونَة|Yang diberkati; Ummul Mukminin|n|b
Saudah|سَوْدَة|Saudah binti Zam'ah, Ummul Mukminin|n|m
Ramlah|رَمْلَة|Sebutir pasir; Ummu Habibah, Ummul Mukminin|n|a
Hindun|هِنْد|Hindun, nama Ummu Salamah, Ummul Mukminin|n|m
Halimah|حَلِيمَة|Yang penyantun; ibu susuan Rasulullah ﷺ|n|h
Aminah|آمِنَة|Yang aman dan dipercayai; ibu Rasulullah ﷺ|n|b
Hajar|هَاجَر|Isteri Nabi Ibrahim dan ibu Nabi Ismail|n|k
Asiah|آسِيَة|Isteri Firaun yang beriman (At-Tahrim 66:11)|n|k
Balqis|بِلْقِيس|Ratu Saba' yang beriman bersama Nabi Sulaiman|u|m
Hawa|حَوَّاء|Ibu sekalian manusia, isteri Nabi Adam|n|m
Sarah|سَارَة|Yang menggembirakan; isteri Nabi Ibrahim|n|e
Rabiah|رَابِعَة|Yang keempat; Rabiah al-Adawiyah, wanita sufi|u|h
Rufaidah|رُفَيْدَة|Rufaidah al-Aslamiyah, jururawat pertama Islam|s|h
Barakah|بَرَكَة|Keberkatan; Ummu Aiman, pengasuh Rasulullah ﷺ|s|b
Lubabah|لُبَابَة|Inti yang murni; Ummul Fadhl|s|m
Syifa|شِفَاء|Penyembuhan; Asy-Syifa' binti Abdullah, guru wanita|s|i
Atikah|عَاتِكَة|Yang suci dan harum|s|e
Raihanah|رَيْحَانَة|Tumbuhan yang harum|u|ea
Zinnirah|زِنِّيرَة|Sahabiyah yang disiksa kerana Islam|s|k
Nailah|نَائِلَة|Yang memperoleh; isteri Uthman bin Affan|s|b
Khansa|خَنْسَاء|Al-Khansa', penyair sahabiyah yang tabah|s|k
Mariyah|مَارِيَة|Mariyah al-Qibtiyah, ibu Ibrahim putera Rasulullah ﷺ|n|m
Rumaisa|رُمَيْصَاء|Ummu Sulaim, sahabiyah yang dijanjikan syurga|s|s
Laila|لَيْلَى|Malam|u|a
Salma|سَلْمَى|Yang selamat|u|b
Lubna|لُبْنَى|Pohon yang harum getahnya|u|a
Suad|سُعَاد|Kebahagiaan|u|b
Habibah|حَبِيبَة|Kekasih; yang dikasihi|u|h
Jamilah|جَمِيلَة|Yang cantik|u|e
Karimah|كَرِيمَة|Yang mulia dan pemurah|u|mh
Rahimah|رَحِيمَة|Yang penyayang|u|h
Latifah|لَطِيفَة|Yang lembut|u|h
Aliyah|عَالِيَة|Yang tinggi|u|m
Amirah|أَمِيرَة|Puteri; pemimpin|u|m
Aqilah|عَاقِلَة|Yang berakal|u|i
Arifah|عَارِفَة|Yang berpengetahuan|u|i
Azizah|عَزِيزَة|Yang mulia dan dikasihi|u|m
Basyirah|بَشِيرَة|Pembawa berita gembira|u|b
Dhiya|ضِيَاء|Sinar cahaya|u|c
Farah|فَرَح|Kegembiraan|u|b
Hana|هَنَاء|Kebahagiaan|u|b
Hanan|حَنَان|Kasih sayang|u|h
Hasanah|حَسَنَة|Kebaikan|u|h
Humaira|حُمَيْرَاء|Yang kemerah-merahan; panggilan Rasulullah ﷺ kepada Aisyah|n|e
Husna|حُسْنَى|Yang terbaik|u|e
Insyirah|انْشِرَاح|Kelapangan dada (Surah Al-Insyirah)|u|b
Izzah|عِزَّة|Kemuliaan|u|m
Jannah|جَنَّة|Syurga; taman|u|s
Kauthar|كَوْثَر|Sungai di syurga; nikmat yang banyak (Al-Kauthar 108:1)|u|s
Khairunnisa|خَيْر النِّسَاء|Sebaik-baik wanita|u|m
Mardhiah|مَرْضِيَّة|Yang diredai (Al-Fajr 89:28)|u|b
Mawaddah|مَوَدَّة|Kasih sayang (Ar-Rum 30:21)|u|h
Madinah|مَدِينَة|Kota; Madinah al-Munawwarah|u|m
Nadia|نَادِيَة|Yang menyeru; embun|u|a
Najwa|نَجْوَى|Bisikan; rahsia|u|i
Nuha|نُهَى|Akal yang matang|u|i
Rahmah|رَحْمَة|Rahmat; kasih sayang|u|b
Raudhah|رَوْضَة|Taman|u|as
Sakinah|سَكِينَة|Ketenangan (Al-Fath 48:4)|u|b
Salwa|سَلْوَى|Penghibur hati; burung salwa|u|b
Tasnim|تَسْنِيم|Mata air di syurga (Al-Mutaffifin 83:27)|u|s
Ulya|عُلْيَا|Yang paling tinggi|u|m
Wafa|وَفَاء|Kesetiaan|u|h
Wardah|وَرْدَة|Bunga mawar|u|ea
Yasmin|يَاسَمِين|Bunga melur|u|ea
Yusra|يُسْرَى|Kemudahan|u|b
Zahra|زَهْرَاء|Yang berseri; gelaran Fatimah|n|ec
Zulaikha|زُلَيْخَا|Nama isteri al-Aziz dalam kisah Nabi Yusuf (menurut riwayat)|u|e
Aina|عَيْنَاء|Yang bermata cantik|u|e
Ain|عَيْن|Mata; mata air|u|ea
Alia|عَلِيَّة|Yang tinggi|u|m
Amani|أَمَانِي|Cita-cita dan harapan|u|b
Anisah|أَنِيسَة|Yang mesra|u|h
Auni|عَوْنِي|Pertolonganku|u|h
Fakhirah|فَاخِرَة|Yang megah dan berharga|u|m
Faqihah|فَقِيهَة|Yang faham agama|u|i
Hidayah|هِدَايَة|Petunjuk|u|i
Iffah|عِفَّة|Kesucian diri|u|h
Liyana|لَيَانَة|Kelembutan|u|h
Maisarah|مَيْسَرَة|Kemudahan; Maisarah, pembantu Khadijah|u|b
Masyitah|مَاشِطَة|Tukang sikat puteri Firaun yang syahid kerana iman (menurut riwayat)|u|k
Nadhirah|نَاضِرَة|Yang berseri-seri (Al-Qiyamah 75:22)|u|e
Nafisah|نَفِيسَة|Yang berharga; Sayyidah Nafisah, ulama wanita|u|m
Naqiyah|نَقِيَّة|Yang bersih dan murni|u|h
Nasuha|نَصُوحَا|Yang ikhlas (taubat nasuha, At-Tahrim 66:8)|u|h
Rifqah|رِفْقَة|Kelembutan|u|h
Syahirah|شَهِيرَة|Yang terkenal|u|m
Tahirah|طَاهِرَة|Yang suci|u|h
Umairah|عُمَيْرَة|Yang panjang umur|u|b
Wajihah|وَجِيهَة|Yang terhormat|u|m
Yumna|يُمْنَى|Yang diberkati; sebelah kanan|u|b
Zafirah|ظَافِرَة|Yang berjaya|u|k
Zahidah|زَاهِدَة|Yang zuhud|u|h
Zulfa|زُلْفَى|Kedudukan yang dekat (Sad 38:25)|u|m
Salsabila|سَلْسَبِيل|Mata air di syurga (Al-Insan 76:18)|u|s
Najmah|نَجْمَة|Bintang|u|ca
Durrah|دُرَّة|Mutiara|u|e
Lulu|لُؤْلُؤ|Mutiara|u|ea
Marjan|مَرْجَان|Batu karang merah (Ar-Rahman 55:22)|u|ea
Yaqut|يَاقُوت|Batu delima (Ar-Rahman 55:58)|u|e
Thurayya|ثُرَيَّا|Gugusan bintang Surayya|u|ca
Duha|ضُحَى|Waktu dhuha (Ad-Dhuha 93:1)|u|ca
Nada|نَدَى|Embun|u|a
Muznah|مُزْنَة|Awan hujan|u|a
Busyra|بُشْرَى|Berita gembira|u|b
Inas|إِينَاس|Kemesraan|u|h
Qanita|قَانِتَة|Yang taat (At-Tahrim 66:12)|u|h
Solehah|صَالِحَة|Yang solehah|u|h
Syakirah|شَاكِرَة|Yang bersyukur|u|h
Sabirah|صَابِرَة|Yang sabar|u|h
Mukminah|مُؤْمِنَة|Yang beriman|u|b
Muslimah|مُسْلِمَة|Wanita Islam|u|b
Muhsinah|مُحْسِنَة|Yang berbuat baik|u|h
Hafizah|حَافِظَة|Penghafal Al-Quran; penjaga|u|i
Hamidah|حَامِدَة|Yang memuji Allah|u|b
Mahmudah|مَحْمُودَة|Yang terpuji|u|m
Munirah|مُنِيرَة|Yang bercahaya|u|c
Nurul Ain|نُور الْعَيْن|Cahaya mata|u|c
Nur|نُور|Cahaya|u|c
Nurul Huda|نُور الْهُدَى|Cahaya petunjuk|u|ci
Nurul Iman|نُور الْإِيمَان|Cahaya iman|u|cb
Nurul Izzah|نُور الْعِزَّة|Cahaya kemuliaan|u|cm
Ainul Mardhiah|عَيْن الْمَرْضِيَّة|Nama bidadari dalam cerita popular (riwayatnya tidak sabit)|u|s
Qurratu Ain|قُرَّة عَيْن|Penyejuk mata (Al-Furqan 25:74)|u|b
Qamariah|قَمَرِيَّة|Seperti bulan|u|ca
Syamsiah|شَمْسِيَّة|Seperti matahari|u|ca
Badriah|بَدْرِيَّة|Seperti bulan purnama|u|ca
Sofiyyah|صَفِيَّة|Yang jernih dan terpilih|u|e
Ruqayyah|رُقَيَّة|Yang naik tinggi; puteri Rasulullah ﷺ|n|m
Firdausi|فِرْدَوْسِي|Dari syurga Firdaus|u|s
Adawiyah|عَدَوِيَّة|Dari kabilah Adi; nisbah Rabiah al-Adawiyah|u|h
"""

UNISEKS = """
Ilham|إِلْهَام|Ilham; petunjuk ke dalam hati|u|i
Iman|إِيمَان|Keimanan|u|b
Ihsan|إِحْسَان|Berbuat baik|u|h
Hidayat|هِدَايَة|Petunjuk|u|i
Firdaus|فِرْدَوْس|Syurga yang tertinggi|u|s
Nur|نُور|Cahaya|u|c
Amal|أَمَل|Harapan|u|b
Rida|رِضَا|Keredaan|u|b
Syahadah|شَهَادَة|Penyaksian; syahid|u|b
"""

# Asmaul Husna not used after "Abdul" by convention, or whose Abdul- form is unusual as a given name
ABD_SKIP = {"Al-Qabidh", "Al-Khafidh", "Al-Muzill", "Al-Mumit", "Al-Muntaqim", "Adh-Dharr", "Al-Mani'", "Al-Mu'akhkhir", "Al-Muhsi",
            "Al-Ba'ith", "Al-Mubdi'", "Al-Mu'id", "Al-Muqaddim", "Al-Muta'ali", "Al-Wali", "Al-Batin", "Al-Akhir", "Al-Awwal", "Az-Zahir",
            "Al-Jami'", "Al-Mutakabbir", "Al-Muqtadir", "Al-Muhyi", "Malikul-Mulk", "Zul-Jalali wal-Ikram", "Al-Wajid", "Ar-Raqib"}

# names reserved for Allah or with a meaning Islam forbids for people: never listed, and the name checker explains why
ALLAH_ONLY = {"allah": "Allah", "rahman": "Ar-Rahman", "ahad": "Al-Ahad", "samad": "As-Samad", "khaliq": "Al-Khaliq", "razzaq": "Ar-Razzaq",
              "quddus": "Al-Quddus", "jabbar": "Al-Jabbar", "mutakabbir": "Al-Mutakabbir", "qahhar": "Al-Qahhar", "kahhar": "Al-Qahhar",
              "ghaffar": "Al-Ghaffar", "gaffar": "Al-Ghaffar", "wahhab": "Al-Wahhab", "wahab": "Al-Wahhab", "muhaimin": "Al-Muhaimin",
              "qayyum": "Al-Qayyum", "musawwir": "Al-Musawwir", "bari": "Al-Bari'", "tabarak": "Tabaraka", "tabarakan": "Tabaraka"}

# legacy rows removed after editorial review: a bad or unsuitable meaning (Jahl = kejahilan, Qatl = pembunuhan, Kalbah = anjing
# betina, Udwan = permusuhan, Dharar = mudarat, Akhnas = a munafiq), a non-Islamic figure, a title or common word, or a made-up form
BLOCK = {"abash", "afrasyab", "afshin", "ahzab", "akhnas", "antum", "arnab", "arnabiyah", "awlad", "aulad", "bahlul", "bahram", "dharar",
         "doa", "durays", "hallaj", "harb", "harbullah", "hatar", "jahl", "jadwal", "kalbah", "kamish", "khirbaq", "khirniq", "matn",
         "matbus", "qatl", "rampah", "udwan", "ustaz", "sayidina", "raja", "siti", "mir", "agha", "ibni", "abd", "sadd", "awan",
         "dakhil", "ilal", "jaldak", "sasha", "susana", "arjuna", "anahita", "aroha", "kiran", "bayard", "lolla", "atikahum",
         "athifahtun", "asriaton", "maisaratunas", "jasminahanum", "mirnawatiyah", "insyirahah", "liyanus", "rabiatuladi",
         "julaibiiyah", "lubaybi", "nisaiyah", "abdal", "ummah", "nisa", "nisaa", "lisan", "barm", "bazt", "hamal", "kahyal",
         "barig", "baris", "ahdar", "jihat", "qaysari", "hanoum", "zarqawi", "ayuniyah", "zainiyah", "tahriyah"}

# names the hadith advise against (makruh, not haram) or that the Prophet ﷺ changed: kept out of the list, explained by the checker
MAKRUH = {"yasar": "Yasar", "aflah": "Aflah", "rabah": "Rabah", "najih": "Najih", "nafi": "Nafi'", "naafi": "Nafi'", "barrah": "Barrah"}

# feminine forms (+ah / ة) of these male adjective names, reviewed one by one: the Arabic pattern takes ة and the meaning holds
DERIVE = {"aamir", "aazim", "baasim", "bahir", "basim", "bazil", "dzakir", "fahim", "faiz", "ghalib", "hajir", "hakim", "jalil", "kazim",
          "mabruk", "mahbub", "mahfuz", "mahir", "majid", "mamduh", "maqbul", "masud", "masum", "muflih", "mukhlis", "mulhim", "munsif",
          "muqbil", "muslih", "nazim", "rabih", "raghib", "rasyid", "razin", "sabiq", "sabih", "sadiq", "said", "sajid", "salim", "samih",
          "thabit", "wafiq", "wathiq", "yasir", "makin", "nadhim", "baahir", "basit", "daim", "makruf", "bakhit", "fakhim"}
