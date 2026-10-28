"""The 25 prophets named in the Quran, in the order commonly taught in Malaysia. Every ayah that names a prophet is found
automatically in data-surah/ (never typed here), except where the name is also an ordinary word: Hud (also "Jews"),
Soleh ("righteous"), Yahya ("gives life"), Ilyas (Il Yasin is two words) and Muhammad (+ Ahmad), whose ayat are listed
and then checked against the text. EXPECT pins the totals, so a change in the matcher or the data fails the build."""
import json, os, re
from tahlil import bare

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_ARTICLE = "https://www.ilmualam.com/2026/03/25-nabi-dan-rasul.html"

# Story points: (text, [(surah, ayah)]) - each point cites the ayat it rests on. Key ayat are shown in full.
NABI = [
    dict(slug="nabi-adam", nama="Adam", ar="آدَم", stems=["ادم"], ms=r"Adam", gelaran="Abu al-Basyar (bapa sekalian manusia), khalifah pertama di bumi",
         kaum="Anak cucunya sendiri", tempat="Syurga, kemudian bumi", kitab="Tiada kitab yang disebut dalam Al-Quran",
         mukjizat="Diajar Allah nama segala benda, ilmu yang tidak diketahui malaikat",
         kisah=[("Allah memberitahu malaikat bahawa Dia akan menjadikan seorang khalifah di bumi.", [(2, 30)]),
                ("Adam diajar nama-nama segala benda, lalu malaikat mengakui mereka tidak mengetahuinya.", [(2, 31), (2, 32)]),
                ("Malaikat diperintah sujud hormat kepada Adam; Iblis enggan kerana sombong.", [(2, 34), (7, 12)]),
                ("Adam dan isterinya tinggal di syurga, lalu digoda syaitan sehingga memakan buah pohon larangan.", [(2, 35), (2, 36), (20, 120)]),
                ("Adam menerima kalimah daripada Allah, bertaubat dan diterima taubatnya, kemudian diturunkan ke bumi.", [(2, 37), (7, 23)])],
         pengajaran="Kesilapan boleh diampunkan dengan taubat yang ikhlas, manakala kesombongan seperti Iblis membawa kepada kebinasaan.",
         key=[(2, 31), (2, 37), (7, 23)]),
    dict(slug="nabi-idris", nama="Idris", ar="إِدْرِيس", stems=["ادريس"], ms=r"Idris",
         gelaran="Siddiq (sangat benar), diangkat ke tempat yang tinggi", kaum="Keturunan Adam sebelum Nuh", tempat="Tidak dinyatakan dalam Al-Quran",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Diangkat Allah ke kedudukan yang tinggi",
         kisah=[("Al-Quran menyifatkan Idris sebagai seorang yang sangat benar dan seorang nabi.", [(19, 56)]),
                ("Allah mengangkatnya ke tempat yang tinggi darjatnya.", [(19, 57)]),
                ("Idris disebut bersama Ismail dan Zulkifli sebagai orang-orang yang sabar.", [(21, 85), (21, 86)])],
         pengajaran="Kebenaran (sidq) dan kesabaran ialah sifat yang mengangkat darjat seseorang di sisi Allah.",
         key=[(19, 56), (19, 57), (21, 85)]),
    dict(slug="nabi-nuh", nama="Nuh", ar="نُوح", stems=["نوح", "نوحا"], ms=r"Nuh", ulul=True, surah=71,
         gelaran="Ulul Azmi, rasul pertama kepada penduduk bumi", kaum="Kaum Nuh yang menyembah berhala (Wadd, Suwa', Yaghuth, Ya'uq, Nasr)",
         tempat="Tidak dinyatakan; bahtera berlabuh di Bukit Judi", kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Bahtera yang menyelamatkan orang beriman daripada banjir besar",
         kisah=[("Nuh berdakwah kepada kaumnya selama 950 tahun.", [(29, 14)]),
                ("Kaumnya enggan dan berpegang kepada berhala Wadd, Suwa', Yaghuth, Ya'uq dan Nasr.", [(71, 23)]),
                ("Allah memerintahkannya membina bahtera dan membawa pasangan setiap haiwan serta orang beriman.", [(11, 37), (11, 40)]),
                ("Anaknya enggan menaiki bahtera dan tenggelam bersama orang yang ingkar.", [(11, 42), (11, 43)]),
                ("Air surut dan bahtera berlabuh di atas Bukit Judi.", [(11, 44)])],
         pengajaran="Istiqamah berdakwah walaupun hasilnya sedikit; hubungan darah tidak menyelamatkan tanpa iman.",
         key=[(29, 14), (11, 42), (71, 1)]),
    dict(slug="nabi-hud", nama="Hud", ar="هُود", stems=["هود", "هودا"], ms=r"Hud", surah=11,
         refs=[(7, 65), (11, 50), (11, 53), (11, 58), (11, 60), (11, 89), (26, 124)],
         gelaran="Rasul kepada kaum 'Ad", kaum="Kaum 'Ad", tempat="Al-Ahqaf (bukit-bukit pasir di selatan Semenanjung Arab)",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Diselamatkan bersama orang beriman ketika kaumnya dibinasakan",
         kisah=[("Hud diutus kepada saudaranya, kaum 'Ad, menyeru mereka menyembah Allah sahaja.", [(7, 65), (11, 50)]),
                ("Kaum 'Ad tinggal di Al-Ahqaf dan terkenal dengan binaan yang tinggi.", [(46, 21), (26, 128)]),
                ("Mereka mendustakannya dan berkata Hud tidak membawa bukti.", [(11, 53)]),
                ("Mereka dibinasakan oleh angin yang amat sejuk lagi kencang selama tujuh malam lapan hari.", [(69, 6), (69, 7)]),
                ("Hud dan orang beriman diselamatkan dengan rahmat Allah.", [(11, 58)])],
         pengajaran="Kekuatan dan kemajuan material tidak menyelamatkan kaum yang menolak kebenaran.",
         key=[(11, 50), (46, 21), (69, 7)]),
    dict(slug="nabi-soleh", nama="Soleh", ar="صَالِح", stems=["صلح", "صلحا"], ms=r"Soleh",
         refs=[(7, 73), (7, 75), (7, 77), (11, 61), (11, 62), (11, 66), (11, 89), (26, 142), (27, 45)],
         gelaran="Rasul kepada kaum Thamud", kaum="Kaum Thamud", tempat="Al-Hijr (barat laut Semenanjung Arab)",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Unta betina (naqatullah) sebagai tanda daripada Allah",
         kisah=[("Soleh diutus kepada kaum Thamud, menyeru mereka menyembah Allah sahaja.", [(7, 73), (11, 61)]),
                ("Kaum Thamud memahat gunung untuk dijadikan rumah.", [(7, 74), (15, 82)]),
                ("Allah mendatangkan unta betina sebagai tanda dan melarang mereka menyakitinya.", [(7, 73), (26, 155)]),
                ("Mereka menyembelih unta itu dan mencabar Soleh mendatangkan azab.", [(7, 77)]),
                ("Mereka dibinasakan oleh gempa dan pekikan yang dahsyat; Soleh dan orang beriman diselamatkan.", [(7, 78), (11, 66), (11, 67)])],
         pengajaran="Mukjizat tidak memberi manfaat kepada hati yang degil; amanah Allah mesti dijaga, bukan dicabar.",
         key=[(7, 73), (11, 61), (7, 78)]),
    dict(slug="nabi-ibrahim", nama="Ibrahim", ar="إِبْرَاهِيم", stems=["ابرهيم", "ابرهم"], ms=r"Ibrahim", ulul=True, surah=14,
         gelaran="Khalilullah (kekasih Allah), Abu al-Anbiya' (bapa para nabi), Ulul Azmi", kaum="Kaumnya penyembah berhala dan Raja Namrud",
         tempat="Iraq, Syam (Palestin) dan Makkah", kitab="Suhuf Ibrahim", mukjizat="Api menjadi sejuk dan selamat untuknya",
         kisah=[("Ibrahim mencari Tuhan yang sebenar dan menolak penyembahan bintang, bulan dan matahari.", [(6, 76), (6, 79)]),
                ("Beliau menghancurkan berhala kaumnya kecuali yang paling besar.", [(21, 58)]),
                ("Kaumnya mencampaknya ke dalam api, lalu Allah berfirman: “Wahai api, jadilah sejuk dan selamat bagi Ibrahim.”", [(21, 68), (21, 69)]),
                ("Beliau diuji untuk menyembelih anaknya; Allah menebusnya dengan sembelihan yang besar.", [(37, 102), (37, 107)]),
                ("Bersama Ismail, beliau meninggikan asas Kaabah dan berdoa agar amalan mereka diterima.", [(2, 127)]),
                ("Allah menjadikannya kekasih (khalil) dan memerintahkan Nabi Muhammad SAW mengikuti agamanya yang lurus.", [(4, 125), (16, 123)])],
         pengajaran="Tauhid yang tegas dan ketaatan penuh kepada perintah Allah, walaupun sangat berat.",
         key=[(21, 69), (2, 127), (4, 125)]),
    dict(slug="nabi-lut", nama="Lut", ar="لُوط", stems=["لوط", "لوطا"], ms=r"Lut",
         gelaran="Anak saudara Nabi Ibrahim yang beriman kepadanya", kaum="Kaum Lut (penduduk Sodom)", tempat="Kawasan Laut Mati",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Diselamatkan sebelum negerinya diterbalikkan",
         kisah=[("Lut beriman kepada Ibrahim dan berhijrah bersamanya.", [(29, 26)]),
                ("Beliau diutus kepada kaum yang melakukan perbuatan keji yang belum pernah dilakukan sesiapa sebelumnya.", [(7, 80), (7, 81)]),
                ("Malaikat datang sebagai tetamu dan memerintahkannya keluar pada waktu malam.", [(11, 77), (11, 81)]),
                ("Isterinya termasuk orang yang dibinasakan.", [(7, 83)]),
                ("Negeri itu diterbalikkan dan dihujani batu daripada tanah yang dibakar.", [(11, 82)])],
         pengajaran="Mencegah kemungkaran tetap wajib walaupun ditentang majoriti; iman tidak boleh diwarisi, termasuk oleh isteri seorang nabi.",
         key=[(7, 80), (11, 81), (11, 82)]),
    dict(slug="nabi-ismail", nama="Ismail", ar="إِسْمَاعِيل", stems=["اسمعيل"], ms=r"Ismail",
         gelaran="Rasul dan nabi yang benar janjinya, anak sulung Nabi Ibrahim", kaum="Penduduk Makkah", tempat="Makkah",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Ditebus dengan sembelihan yang besar",
         kisah=[("Ismail menerima perintah sembelihan dengan sabar: “Wahai ayahku, lakukanlah apa yang diperintahkan.”", [(37, 102)]),
                ("Allah menebusnya dengan sembelihan yang besar, asas ibadah korban.", [(37, 107)]),
                ("Bersama bapanya, beliau meninggikan asas Kaabah.", [(2, 127)]),
                ("Al-Quran memujinya sebagai benar janjinya, seorang rasul dan nabi yang menyuruh keluarganya solat dan berzakat.", [(19, 54), (19, 55)])],
         pengajaran="Ketaatan anak kepada ibu bapa dalam perkara yang diredai Allah, dan menepati janji.",
         key=[(19, 54), (37, 102), (2, 127)]),
    dict(slug="nabi-ishak", nama="Ishak", ar="إِسْحَاق", stems=["اسحق"], ms=r"Ishak",
         gelaran="Anak Nabi Ibrahim dan Sarah, bapa Nabi Yaakub", kaum="Keluarga Ibrahim di Syam", tempat="Syam (Palestin)",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Kelahirannya dikhabarkan malaikat ketika ibu bapanya sudah tua",
         kisah=[("Malaikat memberi khabar gembira kepada Sarah tentang kelahiran Ishak, dan selepasnya Yaakub.", [(11, 71), (11, 72)]),
                ("Allah memberi khabar gembira kepada Ibrahim tentang Ishak, seorang nabi daripada orang yang soleh.", [(37, 112), (37, 113)]),
                ("Ishak disebut dalam senarai nabi yang diberi petunjuk.", [(6, 84)])],
         pengajaran="Tiada yang mustahil bagi Allah; doa dan harapan tidak terhad oleh usia.",
         key=[(11, 71), (37, 112)]),
    dict(slug="nabi-yaakub", nama="Yaakub", ar="يَعْقُوب", stems=["يعقوب"], ms=r"Yaakub",
         gelaran="Israil, bapa kepada 12 anak termasuk Nabi Yusuf", kaum="Bani Israil (keturunannya)", tempat="Syam (Palestin), kemudian Mesir",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Penglihatannya kembali apabila baju Yusuf diletakkan ke wajahnya",
         kisah=[("Menjelang wafat, Yaakub bertanya anak-anaknya apa yang akan mereka sembah, dan mereka berikrar menyembah Allah.", [(2, 133)]),
                ("Apabila Yusuf dikatakan dibaham serigala, beliau memilih “sabar yang indah”.", [(12, 18)]),
                ("Matanya menjadi putih kerana kesedihan, namun beliau hanya mengadu kepada Allah.", [(12, 84), (12, 86)]),
                ("Penglihatannya kembali apabila baju Yusuf diletakkan ke wajahnya.", [(12, 96)])],
         pengajaran="Sabar yang indah: mengadu hanya kepada Allah dan tidak berputus asa daripada rahmat-Nya.",
         key=[(2, 133), (12, 18), (12, 86)]),
    dict(slug="nabi-yusuf", nama="Yusuf", ar="يُوسُف", stems=["يوسف"], ms=r"Yusuf", surah=12,
         gelaran="Al-Siddiq, bendahari Mesir", kaum="Penduduk Mesir", tempat="Kan'an (Palestin) dan Mesir",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Ilmu mentakbir mimpi",
         kisah=[("Yusuf bermimpi sebelas bintang, matahari dan bulan sujud kepadanya.", [(12, 4)]),
                ("Saudara-saudaranya yang dengki mencampaknya ke dalam perigi; beliau kemudian dijual sebagai hamba di Mesir.", [(12, 15), (12, 20)]),
                ("Beliau menolak godaan isteri Al-Aziz dan memilih penjara.", [(12, 23), (12, 33)]),
                ("Beliau mentakbir mimpi raja tentang tujuh tahun subur dan tujuh tahun kemarau, lalu dilantik menjaga perbendaharaan.", [(12, 47), (12, 55)]),
                ("Beliau memaafkan saudara-saudaranya dan keluarganya dihimpunkan semula di Mesir.", [(12, 92), (12, 100)])],
         pengajaran="Kesucian diri, sabar ketika dizalimi dan memaafkan apabila berkuasa. Al-Quran menyebutnya kisah yang paling baik.",
         key=[(12, 4), (12, 33), (12, 92)]),
    dict(slug="nabi-ayub", nama="Ayub", ar="أَيُّوب", stems=["ايوب"], ms=r"Ayub",
         gelaran="Contoh kesabaran", kaum="Tidak dinyatakan dalam Al-Quran", tempat="Tidak dinyatakan dalam Al-Quran",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Sembuh dengan air yang memancar apabila menghentak kakinya",
         kisah=[("Ayub ditimpa penyakit dan kesusahan, lalu berdoa: “Sesungguhnya aku ditimpa penyakit, dan Engkau Yang Maha Penyayang.”", [(21, 83)]),
                ("Allah memperkenankan doanya dan mengembalikan keluarganya, malah digandakan.", [(21, 84)]),
                ("Beliau diperintah menghentak kaki; terpancar air sejuk untuk mandi dan minum.", [(38, 41), (38, 42)]),
                ("Allah memujinya: “Sesungguhnya Kami dapati dia seorang yang sabar.”", [(38, 44)])],
         pengajaran="Sabar ketika diuji dan adab berdoa: mengadu kepada Allah tanpa merungut.",
         key=[(21, 83), (38, 44)]),
    dict(slug="nabi-syuaib", nama="Syuaib", ar="شُعَيْب", stems=["شعيب", "شعيبا"], ms=r"Syuaib",
         gelaran="Rasul kepada penduduk Madyan", kaum="Penduduk Madyan dan Ashab al-Aikah", tempat="Madyan (barat laut Semenanjung Arab)",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Diselamatkan ketika kaumnya dibinasakan",
         kisah=[("Syuaib diutus kepada saudaranya, penduduk Madyan, menyeru mereka menyembah Allah sahaja.", [(7, 85), (11, 84)]),
                ("Beliau melarang mereka mengurangkan sukatan dan timbangan serta merosakkan hak manusia.", [(11, 84), (11, 85)]),
                ("Kaumnya mempersendakan solatnya dan mengugut untuk mengusirnya.", [(11, 87), (7, 88)]),
                ("Mereka dibinasakan oleh pekikan yang dahsyat; Syuaib dan orang beriman diselamatkan.", [(11, 94)])],
         pengajaran="Iman mesti terzahir dalam muamalah: jujur dalam timbangan, sukatan dan perniagaan.",
         key=[(7, 85), (11, 84), (11, 88)]),
    dict(slug="nabi-musa", nama="Musa", ar="مُوسَى", stems=["موسي"], ms=r"Musa", ulul=True,
         gelaran="Kalimullah (yang diajak bercakap oleh Allah), Ulul Azmi", kaum="Bani Israil dan Firaun", tempat="Mesir, Madyan, Sinai",
         kitab="Taurat", mukjizat="Tongkat menjadi ular, tangan bercahaya putih, laut terbelah",
         kisah=[("Semasa bayi, ibunya diilhamkan menghanyutkannya ke sungai; beliau dibesarkan di istana Firaun.", [(28, 7), (28, 9)]),
                ("Beliau melarikan diri ke Madyan dan bekerja di sana selama beberapa tahun.", [(28, 22), (28, 27)]),
                ("Allah memanggilnya di lembah suci Tuwa dan berkata-kata dengannya secara langsung.", [(20, 11), (20, 12), (4, 164)]),
                ("Beliau diberi mukjizat tongkat yang menjadi ular dan tangan yang bercahaya, lalu diutus kepada Firaun.", [(20, 20), (20, 22), (20, 24)]),
                ("Laut terbelah untuk Bani Israil dan Firaun tenggelam bersama tenteranya.", [(26, 63), (26, 66)]),
                ("Beliau menerima Taurat; semasa ketiadaannya Bani Israil menyembah anak lembu Samiri.", [(7, 145), (20, 88)])],
         pengajaran="Berani menyampaikan kebenaran kepada pemerintah yang zalim, dengan yakin kepada pertolongan Allah.",
         key=[(4, 164), (20, 12), (26, 63)]),
    dict(slug="nabi-harun", nama="Harun", ar="هَارُون", stems=["هرون"], ms=r"Harun",
         gelaran="Saudara dan pembantu Nabi Musa", kaum="Bani Israil", tempat="Mesir dan Sinai",
         kitab="Taurat (bersama Musa)", mukjizat="Dikurniakan kefasihan untuk membantu dakwah Musa",
         kisah=[("Musa berdoa agar Harun, saudaranya yang lebih fasih, dijadikan pembantunya.", [(20, 29), (20, 30), (28, 34)]),
                ("Allah mengurniakan Harun kenabian sebagai rahmat kepada Musa.", [(19, 53)]),
                ("Harun ditinggalkan memimpin Bani Israil ketika Musa ke Bukit Tursina.", [(7, 142)]),
                ("Beliau menasihati kaumnya yang menyembah anak lembu Samiri.", [(20, 90)])],
         pengajaran="Bekerjasama dalam dakwah dan menegur dengan hikmah demi menjaga perpaduan umat.",
         key=[(19, 53), (20, 30), (20, 90)]),
    dict(slug="nabi-zulkifli", nama="Zulkifli", ar="ذُو الْكِفْل", stems=["الكفل"], ms=r"Zul-?[Kk]ifli",
         gelaran="Antara orang yang sabar dan terpilih", kaum="Tidak dinyatakan dalam Al-Quran", tempat="Tidak dinyatakan dalam Al-Quran",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Tidak diperincikan dalam Al-Quran",
         kisah=[("Zulkifli disebut bersama Ismail dan Idris sebagai orang-orang yang sabar dan dimasukkan ke dalam rahmat Allah.", [(21, 85), (21, 86)]),
                ("Beliau disebut bersama Ismail dan Alyasak sebagai orang-orang yang terbaik.", [(38, 48)])],
         pengajaran="Al-Quran tidak memperincikan kisahnya; yang diangkat ialah sifatnya: sabar dan termasuk orang yang terbaik.",
         key=[(21, 85), (38, 48)]),
    dict(slug="nabi-daud", nama="Daud", ar="دَاوُد", stems=["داود"], ms=r"Daud",
         gelaran="Khalifah di bumi, raja dan nabi", kaum="Bani Israil", tempat="Palestin",
         kitab="Zabur", mukjizat="Gunung dan burung bertasbih bersamanya; besi dilembutkan untuknya",
         kisah=[("Daud membunuh Jalut, lalu Allah memberinya kerajaan dan hikmah.", [(2, 251)]),
                ("Beliau dikurniakan kitab Zabur.", [(4, 163), (17, 55)]),
                ("Gunung-ganang dan burung bertasbih bersamanya.", [(34, 10), (21, 79)]),
                ("Besi dilembutkan untuknya bagi membuat baju besi.", [(34, 10), (34, 11)]),
                ("Allah menjadikannya khalifah dan memerintahkannya menghukum dengan adil.", [(38, 26)])],
         pengajaran="Kuasa dan kepandaian ialah amanah untuk berlaku adil dan bersyukur.",
         key=[(2, 251), (34, 10), (38, 26)]),
    dict(slug="nabi-sulaiman", nama="Sulaiman", ar="سُلَيْمَان", stems=["سليمن"], ms=r"Sulaiman",
         gelaran="Raja dan nabi, anak Nabi Daud", kaum="Bani Israil", tempat="Palestin",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Faham bahasa burung dan semut; angin dan jin tunduk kepadanya",
         kisah=[("Sulaiman mewarisi Daud dan diajar bahasa burung.", [(27, 16)]),
                ("Beliau tersenyum mendengar kata-kata seekor semut, lalu berdoa memohon dijadikan orang yang bersyukur.", [(27, 18), (27, 19)]),
                ("Angin dan jin ditundukkan untuknya dengan izin Allah.", [(34, 12), (21, 81)]),
                ("Burung hud-hud membawa berita tentang Ratu Saba' yang menyembah matahari; ratu itu akhirnya berserah diri kepada Allah.", [(27, 22), (27, 30), (27, 44)])],
         pengajaran="Nikmat yang besar diiringi syukur, bukan kesombongan.",
         key=[(27, 16), (27, 19), (27, 30)]),
    dict(slug="nabi-ilyas", nama="Ilyas", ar="إِلْيَاس", stems=["الياس", "ياسين"], ms=r"Ilyas",
         refs=[(6, 85), (37, 123), (37, 130)],
         gelaran="Rasul yang menentang penyembahan berhala Ba'l", kaum="Kaum penyembah Ba'l", tempat="Tidak dinyatakan dalam Al-Quran",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Tidak diperincikan dalam Al-Quran",
         kisah=[("Ilyas ialah salah seorang rasul.", [(37, 123)]),
                ("Beliau menegur kaumnya: “Patutkah kamu menyembah Ba'l dan meninggalkan sebaik-baik Pencipta?”", [(37, 124), (37, 125)]),
                ("Kaumnya mendustakannya, dan Allah menyebut namanya dengan kesejahteraan: “Salam sejahtera ke atas Ilyasin.”", [(37, 127), (37, 130)])],
         pengajaran="Menolak apa jua yang disembah selain Allah, walaupun sudah menjadi tradisi kaum.",
         key=[(37, 123), (37, 125), (37, 130)]),
    dict(slug="nabi-ilyasa", nama="Ilyasa'", ar="الْيَسَع", stems=["اليسع"], ms=r"Alyasak",
         gelaran="Antara orang yang terbaik (disebut Alyasak dalam terjemahan Melayu)", kaum="Tidak dinyatakan dalam Al-Quran", tempat="Tidak dinyatakan dalam Al-Quran",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Tidak diperincikan dalam Al-Quran",
         kisah=[("Ilyasa' disebut dalam senarai nabi yang dilebihkan darjatnya atas umat pada zaman mereka.", [(6, 86)]),
                ("Beliau disebut bersama Ismail dan Zulkifli sebagai orang-orang yang terbaik.", [(38, 48)])],
         pengajaran="Al-Quran tidak memperincikan kisahnya; cukup untuk kita mengimani kenabiannya dan kemuliaannya.",
         key=[(6, 86), (38, 48)]),
    dict(slug="nabi-yunus", nama="Yunus", ar="يُونُس", stems=["يونس"], ms=r"Yunus|Zun-?Nun", surah=10,
         gelaran="Zun-Nun dan Sahibul Hut (yang ditelan ikan)", kaum="Penduduk sebuah negeri yang seramai seratus ribu orang atau lebih", tempat="Tidak dinamakan dalam Al-Quran",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Selamat dalam perut ikan besar",
         kisah=[("Yunus meninggalkan kaumnya dalam keadaan marah sebelum diizinkan.", [(21, 87)]),
                ("Beliau menaiki kapal yang sarat, kalah undian dan ditelan ikan besar.", [(37, 140), (37, 141), (37, 142)]),
                ("Dalam kegelapan beliau berdoa: “La ilaha illa anta, subhanaka, inni kuntu minaz-zalimin.”", [(21, 87)]),
                ("Allah menyelamatkannya; kalau bukan kerana tasbihnya, beliau akan kekal dalam perut ikan hingga hari kiamat.", [(37, 143), (37, 144), (21, 88)]),
                ("Kaumnya beriman dan azab diangkat daripada mereka, satu-satunya kaum yang sedemikian.", [(10, 98), (37, 147), (37, 148)])],
         pengajaran="Mengakui kesilapan dan bertasbih membuka jalan keluar daripada kesempitan.",
         key=[(21, 87), (37, 139), (10, 98)]),
    dict(slug="nabi-zakaria", nama="Zakaria", ar="زَكَرِيَّا", stems=["زكريا"], ms=r"Zakaria",
         gelaran="Penjaga Maryam, bapa Nabi Yahya", kaum="Bani Israil", tempat="Baitul Maqdis",
         kitab="Tiada kitab yang disebut dalam Al-Quran", mukjizat="Dikurniakan anak ketika tua dan isterinya mandul",
         kisah=[("Zakaria menjaga Maryam dan mendapati rezeki di sisinya setiap kali masuk ke mihrab.", [(3, 37)]),
                ("Beliau berdoa memohon zuriat yang baik walaupun sudah tua.", [(3, 38), (19, 4), (21, 89)]),
                ("Allah mengkhabarkan kelahiran Yahya, dengan tanda beliau tidak bercakap selama tiga hari.", [(19, 7), (19, 10)])],
         pengajaran="Tidak berputus asa dalam berdoa; doa dengan suara yang lembut dan penuh harap.",
         key=[(3, 37), (3, 38), (21, 89)]),
    dict(slug="nabi-yahya", nama="Yahya", ar="يَحْيَى", stems=["يحيي"], ms=r"Yahya",
         refs=[(3, 39), (6, 85), (19, 7), (19, 12), (21, 90)],
         gelaran="Nama yang belum pernah diberi kepada sesiapa sebelumnya", kaum="Bani Israil", tempat="Palestin",
         kitab="Diperintah memegang Kitab (Taurat) dengan teguh", mukjizat="Diberi hikmah ketika masih kanak-kanak",
         kisah=[("Kelahiran Yahya dikhabarkan kepada Zakaria; nama ini belum pernah diberi kepada sesiapa.", [(19, 7)]),
                ("Beliau membenarkan kalimah daripada Allah (Isa), seorang pemimpin yang menjaga diri dan nabi daripada orang soleh.", [(3, 39)]),
                ("Beliau diperintah berpegang teguh kepada Kitab dan diberi hikmah semasa kanak-kanak.", [(19, 12)]),
                ("Allah mengucapkan kesejahteraan kepadanya pada hari lahir, hari wafat dan hari dibangkitkan.", [(19, 15)])],
         pengajaran="Kesolehan boleh bermula sejak kecil; berbakti kepada ibu bapa dan tidak sombong.",
         key=[(19, 7), (19, 12), (19, 15)]),
    dict(slug="nabi-isa", nama="Isa", ar="عِيسَى", stems=["عيسي"], ms=r"Isa", ulul=True,
         gelaran="Al-Masih ibnu Maryam, Ulul Azmi", kaum="Bani Israil", tempat="Palestin",
         kitab="Injil", mukjizat="Lahir tanpa bapa, bercakap semasa bayi, menyembuhkan buta dan sopak serta menghidupkan orang mati dengan izin Allah",
         kisah=[("Isa dilahirkan oleh Maryam tanpa bapa; penciptaannya seperti Adam.", [(3, 47), (3, 59)]),
                ("Beliau bercakap semasa bayi: “Sesungguhnya aku hamba Allah.”", [(19, 29), (19, 30)]),
                ("Dengan izin Allah, beliau menyembuhkan orang buta dan sopak serta menghidupkan orang mati.", [(3, 49), (5, 110)]),
                ("Beliau tidak dibunuh dan tidak disalib, tetapi diangkat Allah kepada-Nya.", [(4, 157), (4, 158)]),
                ("Beliau mengkhabarkan kedatangan seorang rasul selepasnya bernama Ahmad.", [(61, 6)])],
         pengajaran="Isa ialah hamba dan rasul Allah; mukjizatnya berlaku dengan izin Allah, bukan kerana sifat ketuhanan.",
         key=[(3, 49), (4, 157), (61, 6)]),
    dict(slug="nabi-muhammad", nama="Muhammad", ar="مُحَمَّد", stems=["محمد", "احمد"], ms=r"Muhammad|Ahmad", ulul=True, surah=47, saw=True,
         refs=[(3, 144), (33, 40), (47, 2), (48, 29), (61, 6)],
         gelaran="Khatamun Nabiyyin (penutup sekalian nabi), Ulul Azmi, rahmat bagi sekalian alam", kaum="Seluruh manusia dan jin", tempat="Makkah dan Madinah",
         kitab="Al-Quran", mukjizat="Al-Quran, peristiwa Israk dan Mikraj",
         kisah=[("Muhammad SAW ialah rasul dan penutup sekalian nabi.", [(33, 40)]),
                ("Baginda diutus sebagai rahmat bagi sekalian alam dan kepada seluruh manusia.", [(21, 107), (34, 28)]),
                ("Baginda diperjalankan pada waktu malam dari Masjidil Haram ke Masjidil Aqsa.", [(17, 1)]),
                ("Baginda dan para sahabat bersikap tegas terhadap orang kafir yang memerangi dan berkasih sayang sesama mereka.", [(48, 29)]),
                ("Kedatangannya dikhabarkan oleh Nabi Isa dengan nama Ahmad.", [(61, 6)])],
         pengajaran="Baginda ialah contoh ikutan yang terbaik (uswah hasanah) bagi sesiapa yang mengharapkan Allah dan hari akhirat (Al-Ahzab 33:21).",
         key=[(33, 40), (21, 107), (48, 29)]),
]
assert len(NABI) == 25

# occurrences, ayat: pinned so a matcher or data change is noticed. Counts are per name, not pronouns or titles.
EXPECT = {"nabi-adam": (25, 25), "nabi-idris": (2, 2), "nabi-nuh": (43, 43), "nabi-hud": (7, 7), "nabi-soleh": (9, 9), "nabi-ibrahim": (69, 63),
          "nabi-lut": (27, 27), "nabi-ismail": (12, 12), "nabi-ishak": (17, 16), "nabi-yaakub": (16, 16), "nabi-yusuf": (27, 26), "nabi-ayub": (4, 4),
          "nabi-syuaib": (11, 10), "nabi-musa": (136, 131), "nabi-harun": (20, 20), "nabi-zulkifli": (2, 2), "nabi-daud": (16, 16), "nabi-sulaiman": (17, 16),
          "nabi-ilyas": (3, 3), "nabi-ilyasa": (2, 2), "nabi-yunus": (4, 4), "nabi-zakaria": (7, 6), "nabi-yahya": (5, 5), "nabi-isa": (25, 25),
          "nabi-muhammad": (5, 5)}

ULUL_REFS = [(46, 35), (33, 7), (42, 13)]
# 18 prophets named in four consecutive ayat
ANAM = [(6, 83), (6, 84), (6, 85), (6, 86)]

PRE = ("", "و", "ف", "ب", "ل", "ك", "ي", "يا", "وي", "ول", "وب", "فل", "فب")


def _key(w):
    return bare(w).replace("ـ", "").replace("ى", "ي").replace("ء", "").replace("ؤ", "و").replace("ئ", "ي")


_Q = [json.load(open(f"{REPO}/data-surah/surah-{s}.json", encoding="utf8")) for s in range(1, 115)]
_TOK = [(s + 1, a, [_key(w) for w in v["arabic"].split()]) for s in range(114) for a, v in enumerate(_Q[s], 1)]


def ayah(s, a):
    return _Q[s - 1][a - 1]


def _count(words, stems):
    return sum(1 for w in words if any(w == p + st for p in PRE for st in stems))


def _find(n):
    if n.get("refs"):
        out = []
        for s, a in n["refs"]:
            k = _count(_TOK_IDX[(s, a)], n["stems"])
            assert k, (n["slug"], s, a, "name not found in the ayah")
            out.append((s, a, k))
        return out
    return [(s, a, k) for s, a, ws in _TOK for k in [_count(ws, n["stems"])] if k]


_TOK_IDX = {(s, a): ws for s, a, ws in _TOK}
for _n in NABI:
    _n["hits"] = _find(_n)
    _n["kali"] = sum(k for _, _, k in _n["hits"])
    _n["ayat"] = len(_n["hits"])
    _n["surahs"] = sorted({s for s, _, _ in _n["hits"]})
    assert (_n["kali"], _n["ayat"]) == EXPECT[_n["slug"]], (_n["slug"], _n["kali"], _n["ayat"])
    for _s, _a in _n["key"] + [r for _, rs in _n["kisah"] for r in rs]:
        assert 1 <= _a <= len(_Q[_s - 1]), (_n["slug"], _s, _a)
    _n["re"] = re.compile(rf"\b({_n['ms']})\b")


def title(n):
    return f"Nabi {n['nama']} {'SAW' if n.get('saw') else 'AS'}"


if __name__ == "__main__":
    for n in sorted(NABI, key=lambda n: -n["kali"]):
        print(f"{title(n):<24} {n['kali']:>4} kali  {n['ayat']:>4} ayat  {len(n['surahs']):>3} surah")
