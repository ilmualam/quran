"""Batch 1 (taharah, puasa, solat): 10 refreshed www.ilmualam.com posts. Same builder and rules as gen.py. Run from
tools/blog: python3 batch1.py (writes out/<slug>.html|json and assets/blog/<img>.webp)."""
import ibadah as I
from gen import build, card, qcard, table, write, e, Q
from cards import card as img

H = {d[0]: d for d in I.DOA_HARIAN}
W = "https://www.ilmualam.com/"
QADA = W + "2026/04/cara-solat-qada.html"
PUASA = W + "2018/01/bagaimana-cara-membayar-hutang-puasa.html"
MANDI = W + "2020/01/cara-mandi-wajib-yang-betul.html"
HAID = W + "2018/01/doa-dan-niat-mandi-besar-selesai-haid.html"
NIFAS = W + "2018/02/masa-nifas-menurut-agama-islam-yang.html"
JUNUB = W + "2018/01/bolehkah-membaca-doa-dzikir-ketika-junub.html"
SAHWI = W + "2018/02/cara-sujud-sahwi-bila-terlupa-rakaat.html"
KHUSYUK = W + "2018/01/rahsia-mendapat-nikmat-khusyuk-dalam.html"


def niat(P, title, ar, ru, mn, src="Lafaz lazim mazhab Syafi'i; niat di dalam hati ialah rukun, melafazkannya sunat", note=""):
    return card(P, title, e(ar), ru, e(mn), src, note)


def hd(P, key, note=""):
    _, t, ar, ru, mn, src = H[key]
    return card(P, t, e(ar), ru, e(mn), e(src), note)


def ul(*items, ordered=False):
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>"


def ref(t):
    return f" <em>({t})</em>"


def base(**k):
    k.setdefault("badges", ["Mazhab Syafi'i", "Dalil Al-Quran & Hadis", "Dikemas kini 2026"])
    k.setdefault("disclaimer", "Panduan umum mengikut mazhab Syafi'i, pegangan rasmi di Malaysia. Untuk kes khusus, rujuk pejabat mufti atau pejabat agama Islam negeri anda.")
    return k


POSTS = []

# 1 ---------------------------------------------------------------- mandi selepas haid
P = "ilmx-mh"
POSTS.append(("mandi-haid", base(
    ns=P, url=HAID, published="2018-01-10", pubms="10 Januari 2018",
    title="Niat Mandi Wajib Selepas Haid: Lafaz, Cara & Tanda Suci",
    desc="Niat mandi wajib selepas haid dalam tulisan Arab dan Rumi, rukun dan cara mandi yang betul, tanda suci, tempoh haid serta solat yang wajib diganti.",
    h1="Niat & Cara Mandi Wajib Selepas Haid", img=img("mandi-wajib-haid", "Panduan Taharah", "Niat Mandi Wajib Selepas Haid", "Lafaz niat, rukun, tanda suci dan solat yang wajib diganti", "الطَّهَارَةُ"),
    alt="Niat mandi wajib selepas haid dan cara mandi yang betul", refshort="Sahih Al-Bukhari & Muslim, Al-Fiqh Al-Manhaji",
    lead="Lafaz niat mandi haid, dua rukun yang menentukan sah mandi, cara memastikan sudah suci, dan solat yang wajib diganti apabila haid berhenti.",
    crumb=("Panduan", W + "search/label/Panduan"), about=["Mandi wajib", "Haid", "Taharah"],
    answer="Niat mandi wajib selepas haid: <strong>“Nawaitu raf'al hadathil akbar minal haidhi lillahi ta'ala”</strong> (sahaja aku mengangkat hadas besar daripada haid kerana Allah Taala), "
           "dihadirkan di dalam hati <strong>ketika air pertama menyentuh badan</strong>. Rukunnya hanya dua: <strong>niat</strong> dan <strong>meratakan air ke seluruh kulit dan rambut</strong>. "
           "Mandi dilakukan selepas darah benar-benar berhenti, iaitu apabila keluar cecair putih atau kapas yang dimasukkan keluar bersih.",
    sections=[
        ("niat", "Lafaz Niat Mandi Wajib Selepas Haid",
         niat(P, "Niat Mandi Haid", "نَوَيْتُ رَفْعَ الْحَدَثِ الْأَكْبَرِ مِنَ الْحَيْضِ لِلّٰهِ تَعَالَى", "Nawaitu raf'al hadathil akbar minal haidhi lillahi ta'ala.",
              "Sahaja aku mengangkat hadas besar daripada haid kerana Allah Taala.", note="Niat juga sah dengan lafaz ringkas “Nawaitu raf'al hadathil akbar lillahi ta'ala” atau “Nawaitul ghusla minal haidh”.")
         + "<p>Niat mesti hadir di hati bersama air pertama yang mengenai mana-mana bahagian badan. Jika niat dibuat selepas sebahagian badan dibasuh, bahagian yang dibasuh sebelum niat wajib dibasuh semula.</p>"),
        ("suci", "Tanda Sudah Suci daripada Haid",
         "<p>Haid dianggap berhenti apabila:</p>"
         + ul("<strong>Keluar cecair putih</strong> (al-qassah al-baidha'), atau", "<strong>Kering</strong>: kapas atau tisu yang dimasukkan sedikit ke faraj keluar bersih tanpa sebarang warna merah, coklat atau kekuningan.")
         + "<p>Aisyah RA berpesan kepada wanita yang menghantar kapas berkesan darah kepadanya: “Jangan tergesa-gesa sehingga kamu melihat al-qassah al-baidha'.”"
           + ref("riwayat Al-Bukhari secara ta'liq dalam Kitab Al-Haid; Malik dalam Al-Muwatta'") + "</p>"
         + table(["Perkara", "Mazhab Syafi'i"], [["Tempoh paling singkat", "Sehari semalam (24 jam)"], ["Tempoh biasa", "6 atau 7 hari"],
                                                  ["Tempoh paling lama", "15 hari 15 malam; darah selepas itu ialah istihadah"], ["Tempoh suci paling singkat antara dua haid", "15 hari"]])),
        ("cara", "Cara Mandi Wajib Selepas Haid (Sunnah)",
         ul("Berniat di dalam hati seperti di atas.", "Basuh kedua-dua tangan, kemudian bersihkan faraj dan kesan darah.",
            "Berwuduk seperti wuduk solat." + ref("HR Al-Bukhari, no. 248; Muslim, no. 316"),
            "Siram kepala tiga kali sambil menyelati pangkal rambut sehingga air sampai ke kulit kepala.",
            "Ratakan air ke seluruh badan bermula sebelah kanan, kemudian kiri: termasuk celah ketiak, pusat, belakang telinga, celah jari dan bawah kuku.",
            "Selepas mandi, sapukan kapas atau kain berwangi pada kesan darah untuk menghilangkan bau." + ref("HR Al-Bukhari, no. 314; Muslim, no. 332"), ordered=True)
         + f'<div class="{P}-box amber"><strong>Penghalang air:</strong> cat kuku (kutek) biasa, gam, cat dan lapisan kalis air menghalang air sampai ke kulit dan menjadikan mandi tidak sah; tanggalkan sebelum mandi. Inai tidak menghalang kerana ia warna, bukan lapisan.</div>'),
        ("solat", "Solat yang Wajib Diganti Apabila Suci",
         "<p>Dalam mazhab Syafi'i, jika haid berhenti pada waktu Asar, wanita itu wajib menunaikan <strong>Asar dan juga Zohor</strong>; jika berhenti pada waktu Isyak, wajib <strong>Isyak dan juga Maghrib</strong>, "
         "kerana kedua-dua solat itu boleh dijamak. Begitu juga jika haid datang selepas masuk waktu dan dia sempat solat tetapi belum menunaikannya, solat waktu itu wajib diqada.</p>"
         + table(["Haid berhenti pada waktu", "Solat yang wajib"], [["Subuh", "Subuh"], ["Zohor", "Zohor"], ["Asar", "Zohor dan Asar"], ["Maghrib", "Maghrib"], ["Isyak", "Maghrib dan Isyak"]])
         + f'<p>Puasa Ramadan yang tertinggal pula wajib diqada; lihat <a href="{PUASA}">cara bayar hutang puasa</a>. Solat tidak perlu diqada kerana wanita haid tidak diwajibkan solat' + ref("HR Muslim, no. 335") + ".</p>"),
        ("larangan", "Perkara yang Dilarang Sebelum Mandi",
         ul("Solat dan sujud tilawah.", "Tawaf.", "Menyentuh dan membawa mushaf, dan membaca Al-Quran dengan niat tilawah (zikir dan doa dibenarkan).", "Duduk atau beriktikaf di dalam masjid.",
            "Bersetubuh, sehingga dia mandi" + ref("Al-Baqarah 2:222") + ".",
            "Puasa <strong>boleh</strong> diteruskan walaupun belum mandi, jika darah berhenti sebelum fajar dan dia berniat pada malamnya.")
         + f'<p>Bacaan selepas mandi: ulama Syafi\'i menganjurkan doa yang sama seperti selepas wuduk.</p>' + hd(P, "selepas-wuduk")),
    ],
    faq=[("Apakah niat mandi wajib selepas haid?", "Nawaitu raf'al hadathil akbar minal haidhi lillahi ta'ala: sahaja aku mengangkat hadas besar daripada haid kerana Allah Taala, dihadirkan di hati ketika air pertama mengenai badan."),
         ("Bagaimana tahu haid sudah berhenti?", "Apabila keluar cecair putih, atau kapas yang dimasukkan sedikit ke faraj keluar bersih tanpa warna merah, coklat atau kekuningan."),
         ("Adakah perlu basuh rambut ketika mandi haid?", "Ya. Air wajib sampai ke seluruh rambut dan kulit kepala. Jika rambut diikat dan air tidak sampai ke pangkalnya, ikatan perlu dirungkai."),
         ("Jika haid berhenti waktu Asar, solat apa yang wajib?", "Asar dan Zohor, menurut mazhab Syafi'i, kerana kedua-duanya boleh dijamak."),
         ("Bolehkah berpuasa jika belum mandi haid?", "Boleh, jika darah sudah berhenti sebelum fajar dan niat puasa dibuat pada waktu malam. Mandi boleh dilakukan selepas Subuh.")],
    refs=["Al-Quran: Al-Baqarah 2:222.", "Sahih Al-Bukhari, no. 248, 314; Sahih Muslim, no. 316, 332, 335.", "Al-Muwatta' Imam Malik, Kitab At-Taharah (athar Aisyah tentang al-qassah al-baidha').",
          "Al-Fiqh Al-Manhaji 'ala Mazhab Al-Imam Asy-Syafi'i, bab haid dan mandi."],
    related=[(MANDI, "Cara Mandi Wajib yang Betul", "Rukun, langkah dan kesilapan biasa"), (NIFAS, "Masa Nifas Menurut Islam", "Tempoh, tanda suci dan niat mandi nifas"),
             (JUNUB, "Hukum Baca Doa & Zikir Ketika Junub atau Haid", "Apa yang boleh dan tidak boleh dibaca")])))

# 2 ---------------------------------------------------------------- cara mandi wajib
P = "ilmx-mw"
POSTS.append(("mandi-wajib", base(
    ns=P, url=MANDI, published="2020-01-30", pubms="30 Januari 2020",
    title="Cara Mandi Wajib yang Betul: Niat, Rukun & Langkah Sunnah",
    desc="Cara mandi wajib (junub) yang betul untuk lelaki dan wanita: lafaz niat, 2 rukun, 6 sebab wajib mandi, langkah sunnah dan kesilapan yang membatalkan mandi.",
    h1="Cara Mandi Wajib yang Betul (Lelaki & Wanita)", img=img("cara-mandi-wajib", "Panduan Taharah", "Cara Mandi Wajib yang Betul", "Niat, 2 rukun, langkah sunnah dan kesilapan biasa", "الْغُسْلُ"),
    alt="Cara mandi wajib yang betul untuk lelaki dan wanita", refshort="Sahih Al-Bukhari & Muslim, Al-Fiqh Al-Manhaji",
    lead="Enam sebab yang mewajibkan mandi, lafaz niat, dua rukun yang menentukan sahnya, langkah sunnah daripada hadis Aisyah dan Maimunah, dan kesilapan biasa.",
    crumb=("Panduan", W + "search/label/Panduan"), about=["Mandi wajib", "Mandi junub", "Taharah"],
    answer="Mandi wajib sah dengan <strong>dua rukun</strong>: <strong>niat</strong> mengangkat hadas besar ketika air pertama mengenai badan, dan <strong>meratakan air ke seluruh kulit dan rambut</strong>. "
           "Cara sunnah: basuh tangan, bersihkan kemaluan, berwuduk, siram kepala tiga kali, kemudian ratakan air ke seluruh badan bermula sebelah kanan "
           "<em>(HR Al-Bukhari, no. 248; Muslim, no. 316)</em>.",
    sections=[
        ("sebab", "6 Sebab Wajib Mandi",
         table(["Sebab", "Bagi", "Dalil / nota"], [
             ["Keluar mani (sedar atau mimpi)", "Lelaki dan wanita", "Mimpi tanpa keluar mani tidak mewajibkan mandi (HR Al-Bukhari, no. 282)"],
             ["Bersetubuh walaupun tidak keluar mani", "Lelaki dan wanita", "HR Muslim, no. 349"],
             ["Haid", "Wanita", f'<a href="{HAID}">Niat mandi haid</a>'], ["Nifas", "Wanita", f'<a href="{NIFAS}">Masa nifas</a>'],
             ["Wiladah (bersalin, termasuk tanpa darah)", "Wanita", "Termasuk keguguran"], ["Meninggal dunia", "Jenazah Muslim", "Fardu kifayah ke atas orang hidup"]])),
        ("niat", "Lafaz Niat Mandi Wajib",
         niat(P, "Niat Mandi Wajib (Umum)", "نَوَيْتُ رَفْعَ الْحَدَثِ الْأَكْبَرِ لِلّٰهِ تَعَالَى", "Nawaitu raf'al hadathil akbar lillahi ta'ala.",
              "Sahaja aku mengangkat hadas besar kerana Allah Taala.", note="Bagi junub boleh juga: “Nawaitu raf'al janabati lillahi ta'ala”. Satu mandi dengan niat mengangkat hadas besar memadai walaupun sebabnya lebih daripada satu.")),
        ("langkah", "Langkah Mandi Wajib Mengikut Sunnah",
         ul("Membaca Bismillah dan berniat di dalam hati.", "Membasuh kedua-dua tangan tiga kali.", "Membasuh kemaluan dan menghilangkan najis dengan tangan kiri.",
            "Berwuduk seperti wuduk solat (boleh menangguhkan basuhan kaki hingga akhir)." + ref("HR Al-Bukhari, no. 249 (hadis Maimunah)"),
            "Memasukkan jari ke pangkal rambut, kemudian menyiram kepala tiga kali.",
            "Meratakan air ke seluruh badan, mendahulukan sebelah kanan." + ref("HR Al-Bukhari, no. 248; Muslim, no. 316"),
            "Memastikan air sampai ke tempat yang sukar: celah ketiak, pusat, lipatan perut, belakang telinga, celah jari kaki, bawah kuku dan kulit di bawah rambut atau janggut tebal.", ordered=True)
         + "<p>Rasulullah SAW mandi dengan satu sa' air (kira-kira 3 liter) <em>(HR Al-Bukhari, no. 201)</em>: mandi yang sempurna tidak memerlukan pembaziran air.</p>"),
        ("silap", "Kesilapan yang Menjadikan Mandi Tidak Sah",
         table(["Kesilapan", "Pembetulan"], [
             ["Niat dibuat selepas sebahagian badan sudah dibasuh", "Niat bersama air pertama, atau ulang basuh bahagian yang terdahulu"],
             ["Cat kuku, gam, plaster atau lapisan kalis air pada kulit", "Tanggalkan sebelum mandi; inai dan pewarna rambut biasa tidak menghalang"],
             ["Air tidak sampai ke kulit kepala atau pangkal rambut", "Selati pangkal rambut; rungkai ikatan jika air tidak sampai"],
             ["Menyangka mandi wajib mesti tiga kali atau mesti bermula di kepala", "Wajib hanya sekali rata; tiga kali dan tertib ialah sunat"],
             ["Mandi dalam keadaan ada najis pada badan", "Hilangkan najis dahulu kerana ia boleh menghalang air"]])),
        ("khas", "Situasi Khas Ketika Mandi Wajib",
         table(["Situasi", "Hukum"], [
             ["Mandi di bawah pancuran (shower) tanpa gayung", "Sah, asalkan air rata ke seluruh badan"],
             ["Rambut wanita bersanggul atau bertocang", "Tidak wajib dirungkai jika air sampai ke pangkal rambut (HR Muslim, no. 330); wajib dirungkai jika air tidak sampai"],
             ["Junub dan haid serentak", "Satu mandi dengan niat mengangkat hadas besar memadai untuk kedua-duanya"],
             ["Mandi wajib sekali gus mandi sunat Jumaat", "Sah dengan menggabungkan kedua-dua niat; mendapat pahala kedua-duanya menurut mazhab Syafi'i"],
             ["Berkumur dan memasukkan air ke hidung", "Sunat dalam mazhab Syafi'i, bukan rukun"],
             ["Terlupa sebahagian kecil anggota tidak terkena air", "Basuh bahagian itu sahaja dengan niat; tidak perlu mengulang mandi"],
             ["Luka berbalut (jabirah)", "Basuh bahagian yang sihat, sapu air di atas balutan, dan bertayammum"]])),
        ("sunat", "Mandi Wajib dan Mandi Sunat: Bezanya",
         "<p>Selain mandi wajib, Islam menganjurkan beberapa mandi sunat dengan niat tersendiri. Cara mandinya sama; yang berbeza hanyalah niat dan hukumnya.</p>"
         + table(["Mandi sunat", "Bila"], [["Mandi Jumaat", "Sebelum solat Jumaat (HR Al-Bukhari, no. 877)"], ["Mandi dua hari raya", "Pagi Aidilfitri dan Aidiladha"],
                                           ["Mandi ihram", "Sebelum berniat ihram haji atau umrah"], ["Mandi selepas memandikan jenazah", "Bagi orang yang memandikan"],
                                           ["Mandi orang yang baru memeluk Islam", "Jika tidak berjunub sebelumnya"], ["Mandi solat gerhana dan istisqa'", "Sebelum solat tersebut"]])
         + "<p>Perbezaan utama: mandi wajib mengangkat hadas besar dan menjadi syarat sah solat; mandi sunat tidak mengangkat hadas dan tidak memadai untuk solat jika seseorang berjunub, kecuali niat mengangkat hadas besar dibuat.</p>"),
        ("larangan", "Larangan Ketika Dalam Junub",
         ul("Solat, sujud tilawah dan sujud syukur.", "Tawaf.", "Menyentuh dan membawa mushaf.", "Membaca Al-Quran dengan niat tilawah; zikir dan doa dibenarkan "
            + f'(<a href="{JUNUB}">huraian</a>).', "Duduk atau beriktikaf di dalam masjid.")
         + "<p>Sunat menyegerakan mandi. Jika hendak tidur, makan atau mengulangi persetubuhan sebelum mandi, sunat berwuduk terlebih dahulu" + ref("HR Al-Bukhari, no. 288; Muslim, no. 305") + ".</p>"),
    ],
    faq=[("Apakah rukun mandi wajib?", "Dua: niat mengangkat hadas besar dan meratakan air ke seluruh kulit serta rambut. Langkah lain seperti wuduk dan tiga kali siraman ialah sunat."),
         ("Apakah niat mandi wajib?", "Nawaitu raf'al hadathil akbar lillahi ta'ala: sahaja aku mengangkat hadas besar kerana Allah Taala, dihadirkan di hati ketika air pertama mengenai badan."),
         ("Perlukah berwuduk lagi selepas mandi wajib untuk solat?", "Tidak, jika tidak berlaku perkara yang membatalkan wuduk selepas mandi. Mandi wajib sudah mengangkat hadas kecil juga."),
         ("Adakah mimpi basah tanpa air mani perlu mandi?", "Tidak. Nabi SAW bersabda mandi wajib apabila melihat air (mani) (HR Al-Bukhari 282)."),
         ("Adakah cat kuku membatalkan mandi wajib?", "Cat kuku yang membentuk lapisan menghalang air sampai ke kuku, jadi mandi tidak sah selagi ia tidak ditanggalkan. Inai tidak menghalang.")],
    refs=["Sahih Al-Bukhari, no. 201, 248, 249, 282, 288.", "Sahih Muslim, no. 305, 316, 349.", "Al-Fiqh Al-Manhaji 'ala Mazhab Al-Imam Asy-Syafi'i, bab mandi."],
    related=[(HAID, "Niat Mandi Wajib Selepas Haid", "Tanda suci dan solat yang wajib diganti"), (JUNUB, "Hukum Baca Doa & Zikir Ketika Junub", "Apa yang boleh dibaca sebelum mandi"),
             (Q + "belajar-solat/", "Cara Solat Lengkap", "Panduan solat langkah demi langkah")])))

# 3 ---------------------------------------------------------------- nifas
P = "ilmx-nf"
POSTS.append(("masa-nifas", base(
    ns=P, url=NIFAS, published="2019-12-19", pubms="19 Disember 2019",
    title="Masa Nifas dalam Islam: Tempoh 40 & 60 Hari, Tanda Suci & Niat",
    desc="Tempoh nifas mazhab Syafi'i (biasa 40 hari, maksimum 60 hari), suci sebelum 40 hari, nifas selepas keguguran dan caesarean, larangan dan niat mandi nifas.",
    h1="Masa Nifas Menurut Islam (Mazhab Syafi'i)", img=img("masa-nifas", "Panduan Wanita", "Masa Nifas dalam Islam", "Tempoh 40 & 60 hari, tanda suci dan niat mandi nifas", "النِّفَاسُ"),
    alt="Masa nifas menurut Islam: tempoh, tanda suci dan niat mandi", refshort="Sunan Abu Daud & At-Tirmizi, Al-Fiqh Al-Manhaji",
    lead="Tempoh nifas yang sebenar menurut fiqh, apa berlaku jika darah berhenti awal atau melebihi 60 hari, nifas selepas keguguran dan pembedahan, serta niat mandi nifas.",
    crumb=("Panduan", W + "search/label/Panduan"), about=["Nifas", "Wanita bersalin", "Taharah"],
    answer="Nifas ialah darah yang keluar selepas bersalin. Dalam mazhab Syafi'i, tempohnya <strong>paling singkat sekejap</strong>, <strong>biasanya 40 hari</strong> dan <strong>paling lama 60 hari</strong>. "
           "Jika darah berhenti sebelum 40 hari, wanita itu <strong>sudah suci</strong>: wajib mandi dan solat walaupun belum cukup 40 hari. Darah yang berterusan selepas 60 hari dikira istihadah.",
    sections=[
        ("tempoh", "Tempoh Nifas Menurut Mazhab Syafi'i",
         table(["Perkara", "Hukum"], [["Paling singkat", "Sekejap (setitis darah pun dikira nifas)"], ["Kebiasaan", "40 hari"], ["Paling lama", "60 hari"],
                                     ["Darah berhenti sebelum 40 hari", "Suci; mandi dan terus solat"], ["Darah melebihi 60 hari", "Istihadah; rujuk ustazah atau pejabat agama untuk menentukan baki"]])
         + "<p>Ummu Salamah RA berkata wanita nifas pada zaman Rasulullah SAW berehat selama empat puluh hari" + ref("HR Abu Daud, no. 311; At-Tirmizi, no. 139") + ". "
           "Hadis ini menerangkan kebiasaan, bukan tempoh wajib; sebab itu suci sebelum 40 hari diterima apabila darah benar-benar berhenti.</p>"),
        ("suci", "Tanda Suci dan Darah yang Berhenti Kemudian Keluar Semula",
         ul("Tanda suci sama seperti haid: keluar cecair putih, atau kapas yang dimasukkan keluar bersih.",
            "Jika darah berhenti kurang daripada 15 hari kemudian keluar semula dalam tempoh 60 hari, darah itu masih nifas dan tempoh berhenti juga dikira nifas menurut pendapat yang muktamad; solat yang dilakukan dalam tempoh itu tidak perlu diganti.",
            "Jika darah keluar semula selepas suci 15 hari atau lebih, ia dikira haid.")),
        ("khas", "Keguguran, Pembedahan Caesarean & Wiladah",
         table(["Keadaan", "Hukum"], [
             ["Keguguran janin yang sudah berbentuk ketulan darah ('alaqah) atau daging (mudghah)", "Darah selepasnya ialah nifas; wajib mandi wiladah"],
             ["Bersalin secara caesarean, darah keluar dari faraj", "Nifas"],
             ["Bersalin tanpa darah (jarang berlaku)", "Tiada nifas, tetapi tetap wajib mandi wiladah"]])
         + "<p>Penentuan sama ada janin sudah berbentuk dirujuk kepada doktor atau bidan.</p>"),
        ("kira", "Kalkulator Tarikh 40 & 60 Hari Nifas",
         '<div class="ilmx-nf-calc"><h3>📅 Kira tarikh nifas</h3><div class="ilmx-nf-grid"><div><label for="ilmx-nf-d">Tarikh bersalin</label><input id="ilmx-nf-d" type="date"></div></div>'
         '<div class="ilmx-nf-out" id="ilmx-nf-o" aria-live="polite">Pilih tarikh bersalin.</div>'
         '<p style="font-size:.82rem;color:#5b6b60;margin:.6rem 0 0">Hari bersalin dikira hari pertama. Jika darah berhenti lebih awal, anda sudah suci pada hari itu; tarikh 60 hari ialah had maksimum nifas.</p></div>'),
        ("istihadah", "Jika Darah Melebihi 60 Hari (Istihadah)",
         "<p>Darah yang berterusan selepas 60 hari ialah <strong>istihadah</strong>, iaitu darah penyakit yang tidak menghalang solat dan puasa. Wanita yang beristihadah:</p>"
         + ul("Membasuh darah dan memakai pelapik pada setiap kali hendak solat fardu.", "Berwuduk selepas masuk waktu, bagi setiap solat fardu.",
              "Segera solat selepas berwuduk; boleh menunaikan solat sunat bersama fardu itu.", "Berpuasa, membaca Al-Quran dan bersama suami seperti biasa.")
         + "<p>Fatimah binti Abi Hubaisy RA pernah bertanya tentang darah yang tidak berhenti, lalu Nabi SAW menjelaskan ia darah urat, bukan haid, dan menyuruhnya solat" + ref("HR Al-Bukhari, no. 228; Muslim, no. 333") + ".</p>"),
        ("larangan", "Larangan Semasa Nifas",
         ul("Solat (tidak perlu diqada).", "Puasa (wajib diqada" + f' — <a href="{PUASA}">cara qada dan fidyah</a>).',
            "Tawaf.", "Menyentuh mushaf dan membaca Al-Quran dengan niat tilawah.", "Duduk di dalam masjid.",
            "Bersetubuh sehingga mandi" + ref("Al-Baqarah 2:222") + ". Bermesra selain itu dibenarkan.")
         + "<p>Zikir, selawat dan doa dibenarkan sepanjang tempoh nifas, malah amat digalakkan.</p>"),
        ("niat", "Niat Mandi Nifas & Wiladah",
         niat(P, "Niat Mandi Nifas", "نَوَيْتُ رَفْعَ الْحَدَثِ الْأَكْبَرِ مِنَ النِّفَاسِ لِلّٰهِ تَعَالَى", "Nawaitu raf'al hadathil akbar minan-nifasi lillahi ta'ala.",
              "Sahaja aku mengangkat hadas besar daripada nifas kerana Allah Taala.", note="Bagi bersalin tanpa darah: “Nawaitu raf'al hadathil akbar minal wiladati lillahi ta'ala”.")
         + f'<p>Cara mandinya sama seperti mandi wajib biasa; lihat <a href="{MANDI}">langkah mandi wajib yang betul</a>.</p>'),
    ],
    faq=[("Berapa lama tempoh nifas?", "Dalam mazhab Syafi'i: paling singkat sekejap, biasanya 40 hari dan paling lama 60 hari."),
         ("Bolehkah solat jika nifas berhenti sebelum 40 hari?", "Wajib. Apabila darah benar-benar berhenti, mandi dan terus solat, walaupun belum cukup 40 hari."),
         ("Adakah keguguran mewajibkan mandi nifas?", "Ya, jika janin sudah berbentuk ketulan darah atau daging. Darah selepasnya ialah nifas dan wajib mandi apabila berhenti."),
         ("Adakah ibu yang bersalin caesarean mengalami nifas?", "Ya, jika darah keluar dari faraj selepas bersalin. Jika tiada darah langsung, dia tetap wajib mandi wiladah."),
         ("Bolehkah suami isteri bersama sebelum 40 hari?", "Boleh selepas nifas berhenti dan isteri sudah mandi, walaupun belum cukup 40 hari, dengan mengambil kira nasihat doktor tentang kesihatan.")],
    refs=["Al-Quran: Al-Baqarah 2:222.", "Sunan Abu Daud, no. 311; Sunan At-Tirmizi, no. 139.", "Al-Fiqh Al-Manhaji 'ala Mazhab Al-Imam Asy-Syafi'i, bab haid dan nifas."],
    related=[(HAID, "Niat Mandi Wajib Selepas Haid", "Tanda suci dan solat yang wajib diganti"), (PUASA, "Cara Bayar Hutang Puasa", "Qada, fidyah dan kalkulator"),
             (Q + "nama-bayi-islam/", "Nama Bayi Islam", "Penjana nama dengan maksud dan ayat Al-Quran")],
    js="var d=document.getElementById('ilmx-nf-d'),o=document.getElementById('ilmx-nf-o');function f(n){var x=new Date(d.value+'T00:00:00');x.setDate(x.getDate()+n-1);return x.toLocaleDateString('ms-MY',{weekday:'long',day:'numeric',month:'long',year:'numeric'})}"
       "d.addEventListener('input',function(){if(!d.value){o.textContent='Pilih tarikh bersalin.';return}o.innerHTML='Hari ke-40: <strong>'+f(40)+'</strong><br>Had maksimum (hari ke-60): <strong>'+f(60)+'</strong>'});"
       "var t=new Date();t.setDate(t.getDate()-10);d.value=t.toISOString().slice(0,10);d.dispatchEvent(new Event('input'));")))

# 4 ---------------------------------------------------------------- perkara membatalkan puasa
P = "ilmx-bp"
POSTS.append(("batal-puasa", base(
    ns=P, url=W + "2020/04/perkara-yang-membatalkan-puasa-ramadhan.html", published="2020-04-25", pubms="25 April 2020",
    title="Perkara yang Membatalkan Puasa: Senarai, Kaffarah & Yang Tidak Batal",
    desc="Perkara yang membatalkan puasa menurut mazhab Syafi'i, kaffarah bersetubuh siang Ramadan, perkara yang tidak membatalkan puasa dan niat puasa Ramadan.",
    h1="Perkara yang Membatalkan Puasa (Mazhab Syafi'i)", img=img("perkara-membatalkan-puasa", "Panduan Puasa", "Perkara yang Membatalkan Puasa", "Senarai, kaffarah dan perkara yang tidak membatalkan puasa", "الصِّيَامُ"),
    alt="Perkara yang membatalkan puasa dan yang tidak membatalkan puasa", refshort="Sahih Al-Bukhari & Muslim, Sunan Abu Daud, Al-Fiqh Al-Manhaji",
    lead="Senarai lengkap perkara yang membatalkan puasa, bezanya dengan yang hanya mengurangkan pahala, kaffarah, dan perkara yang ramai sangka membatalkan puasa padahal tidak.",
    crumb=("Puasa", W + "search/label/Puasa"), about=["Puasa Ramadan", "Perkara membatalkan puasa"],
    answer="Puasa batal dengan: <strong>memasukkan sesuatu ke rongga badan dengan sengaja</strong> (makan, minum dan seumpamanya), <strong>muntah dengan sengaja</strong>, <strong>bersetubuh</strong>, "
           "<strong>mengeluarkan mani dengan sengaja</strong>, <strong>haid atau nifas</strong>, <strong>gila</strong> dan <strong>murtad</strong>. Makan atau minum kerana <strong>terlupa tidak membatalkan</strong> puasa "
           "<em>(HR Al-Bukhari, no. 1933; Muslim, no. 1155)</em>.",
    sections=[
        ("senarai", "Senarai Perkara yang Membatalkan Puasa",
         table(["Perkara", "Akibat", "Dalil / nota"], [
             ["Makan, minum atau memasukkan sesuatu ke rongga terbuka (mulut, hidung, telinga, dubur, qubul) dengan sengaja", "Batal; wajib qada", "Al-Baqarah 2:187"],
             ["Muntah dengan sengaja", "Batal; wajib qada", "Muntah tidak sengaja tidak membatalkan (HR Abu Daud, no. 2380; At-Tirmizi, no. 720)"],
             ["Bersetubuh pada siang hari Ramadan", "Batal; wajib qada dan kaffarah", "HR Al-Bukhari, no. 1936; Muslim, no. 1111"],
             ["Mengeluarkan mani dengan sengaja (onani, bercumbu)", "Batal; wajib qada", "Mimpi basah tidak membatalkan"],
             ["Haid atau nifas walaupun sesaat sebelum Maghrib", "Batal; wajib qada", "HR Muslim, no. 335"],
             ["Gila walaupun seketika", "Batal", ""], ["Murtad", "Batal", ""]])),
        ("kaffarah", "Kaffarah Bersetubuh pada Siang Ramadan",
         "<p>Seorang lelaki datang kepada Nabi SAW mengaku telah bersetubuh dengan isterinya pada siang Ramadan. Baginda memerintahkan kaffarah mengikut susunan" + ref("HR Al-Bukhari, no. 1936; Muslim, no. 1111") + ":</p>"
         + ul("Membebaskan seorang hamba (tiada pada zaman ini);", "Jika tidak mampu, berpuasa <strong>dua bulan berturut-turut</strong>;", "Jika tidak mampu, memberi makan <strong>60 orang miskin</strong>, seorang secupak.", ordered=True)
         + "<p>Dalam mazhab Syafi'i, kaffarah wajib ke atas suami sahaja, dan bagi setiap hari yang dilanggar ada kaffarah tersendiri. Kedua-duanya tetap wajib mengqada puasa hari itu.</p>"),
        ("tidak", "Perkara yang Tidak Membatalkan Puasa",
         table(["Perkara", "Nota"], [
             ["Makan atau minum kerana terlupa", "Teruskan puasa (HR Al-Bukhari, no. 1933; Muslim, no. 1155)"],
             ["Mimpi basah", "Tidak sengaja"], ["Menelan air liur sendiri yang bersih", ""],
             ["Bersugi atau memberus gigi", "Makruh selepas gelincir matahari dalam mazhab Syafi'i; jangan telan ubat gigi"],
             ["Mandi, berenang tanpa air masuk ke rongga, merasa makanan di hujung lidah lalu diludah", "Hati-hati supaya tiada yang tertelan"],
             ["Ujian darah dan beberapa prosedur perubatan", "Muzakarah Jawatankuasa Fatwa Kebangsaan telah memutuskan beberapa prosedur tidak membatalkan puasa; semak senarai terkini di laman JAKIM sebelum rawatan"]])),
        ("pahala", "Perkara yang Merosakkan Pahala Puasa",
         "<p>Puasa tetap sah tetapi pahalanya terjejas dengan perbuatan seperti mengumpat, berbohong dan bercakap kotor. Nabi SAW bersabda: “Sesiapa yang tidak meninggalkan kata-kata dusta dan perbuatannya, "
         "maka Allah tidak berhajat kepada dia meninggalkan makan dan minumnya”" + ref("HR Al-Bukhari, no. 1903") + ".</p>"),
        ("sunnah", "Sunnah dan Perkara Makruh Ketika Berpuasa",
         table(["Sunnah", "Dalil"], [["Bersahur, walaupun seteguk air", "“Bersahurlah, kerana pada sahur itu ada keberkatan” (HR Al-Bukhari, no. 1923; Muslim, no. 1095)"],
                                     ["Melewatkan sahur hingga hampir imsak", "Jarak sahur Nabi SAW dengan solat Subuh sekadar bacaan 50 ayat (HR Al-Bukhari, no. 1921)"],
                                     ["Menyegerakan berbuka sebaik masuk Maghrib", "“Manusia sentiasa dalam kebaikan selama mereka menyegerakan berbuka” (HR Al-Bukhari, no. 1957)"],
                                     ["Berbuka dengan kurma atau air", "HR Abu Daud, no. 2356; At-Tirmizi, no. 696"],
                                     ["Memperbanyakkan bacaan Al-Quran, sedekah dan doa", "Doa orang berpuasa tidak ditolak (HR At-Tirmizi, no. 3598)"]])
         + "<p><strong>Makruh</strong> (tidak membatalkan, tetapi elok dielakkan): berkumur dan memasukkan air ke hidung secara berlebihan, merasa makanan tanpa keperluan, bersugi selepas gelincir matahari "
           "(mazhab Syafi'i), dan bercumbu bagi orang yang bimbang tidak dapat mengawal diri.</p>"
         + card(P, "Doa Berbuka Puasa", "ذَهَبَ الظَّمَأُ وَابْتَلَّتِ الْعُرُوقُ وَثَبَتَ الْأَجْرُ إِنْ شَاءَ اللّٰهُ", "Zahabaz-zama'u wabtallatil-'uruqu wa thabatal-ajru in sya Allah.",
                "Telah hilang dahaga, telah basah urat-urat, dan telah tetap pahala, insya-Allah.", "HR Abu Daud, no. 2357 (hasan)",
                "Dibaca selepas berbuka. Lafaz popular “Allahumma laka sumtu…” diriwayatkan secara mursal (HR Abu Daud, no. 2358) dan boleh dibaca sebagai doa umum.")),
        ("niat", "Niat Puasa Ramadan",
         niat(P, "Niat Puasa Ramadan", "نَوَيْتُ صَوْمَ غَدٍ عَنْ أَدَاءِ فَرْضِ شَهْرِ رَمَضَانَ هٰذِهِ السَّنَةِ لِلّٰهِ تَعَالَى",
              "Nawaitu sauma ghadin 'an ada'i fardhi syahri Ramadhana hazihis-sanati lillahi ta'ala.",
              "Sahaja aku berpuasa esok hari bagi menunaikan fardu bulan Ramadan tahun ini kerana Allah Taala.",
              note="Niat wajib dibuat setiap malam sebelum fajar (HR Abu Daud, no. 2454). Mazhab Syafi'i membolehkan bertaklid kepada Maliki dengan niat sebulan pada malam pertama sebagai langkah berjaga-jaga jika terlupa.")
         + f'<p>Semak waktu imsak dan berbuka bagi zon anda di <a href="{Q}waktu-berbuka-puasa/">Waktu Berbuka Puasa & Imsak</a>.</p>'),
    ],
    faq=[("Adakah terlupa makan ketika puasa membatalkan puasa?", "Tidak. Teruskan puasa; Allah yang memberinya makan dan minum (HR Al-Bukhari 1933; Muslim 1155)."),
         ("Adakah muntah membatalkan puasa?", "Muntah dengan sengaja membatalkan dan wajib qada. Muntah yang tidak disengajakan tidak membatalkan (HR Abu Daud 2380)."),
         ("Apakah kaffarah bersetubuh siang Ramadan?", "Puasa dua bulan berturut-turut; jika tidak mampu, memberi makan 60 orang miskin. Wajib juga qada puasa hari itu (HR Al-Bukhari 1936)."),
         ("Adakah memberus gigi membatalkan puasa?", "Tidak, jika tiada yang tertelan. Dalam mazhab Syafi'i, bersugi selepas gelincir matahari makruh."),
         ("Adakah suntikan membatalkan puasa?", "Muzakarah Jawatankuasa Fatwa Kebangsaan memutuskan beberapa jenis suntikan dan prosedur perubatan tidak membatalkan puasa. Semak senarai terkini JAKIM untuk prosedur tertentu.")],
    refs=["Al-Quran: Al-Baqarah 2:187.", "Sahih Al-Bukhari, no. 1903, 1933, 1936; Sahih Muslim, no. 335, 1111, 1155.", "Sunan Abu Daud, no. 2380, 2454; Sunan At-Tirmizi, no. 720.",
          "Keputusan Muzakarah Jawatankuasa Fatwa Majlis Kebangsaan Bagi Hal Ehwal Ugama Islam Malaysia berkaitan puasa dan perubatan.", "Al-Fiqh Al-Manhaji, bab puasa."],
    related=[(PUASA, "Cara Bayar Hutang Puasa Bertahun-tahun", "Qada, fidyah dan kalkulator"), (Q + "waktu-berbuka-puasa/", "Waktu Berbuka Puasa & Imsak", "Jadual rasmi JAKIM ikut zon"),
             (Q + "zakat-fitrah/", "Zakat Fitrah", "Kadar semua negeri dan kalkulator keluarga")])))

# 5 ---------------------------------------------------------------- doa & zikir ketika junub
P = "ilmx-jb"
POSTS.append(("zikir-junub", base(
    ns=P, url=JUNUB, published="2018-01-19", pubms="19 Januari 2018",
    title="Hukum Baca Doa, Zikir & Al-Quran Ketika Junub dan Haid",
    desc="Bolehkah membaca doa, zikir, Ayat Kursi dan Al-Quran ketika junub atau haid? Hukum mazhab Syafi'i, menyentuh mushaf dan telefon, dan senarai boleh/tidak.",
    h1="Hukum Baca Doa, Zikir & Al-Quran Ketika Junub atau Haid", img=img("zikir-ketika-junub", "Hukum Ibadah", "Baca Doa & Zikir Ketika Junub atau Haid", "Apa yang boleh, apa yang tidak, dan dalilnya", "الذِّكْرُ"),
    alt="Hukum membaca doa, zikir dan Al-Quran ketika junub atau haid", refshort="Sahih Muslim, Sunan Abu Daud, Al-Majmu' An-Nawawi",
    lead="Panduan jelas tentang apa yang boleh dibaca ketika dalam hadas besar: zikir, doa, ayat Al-Quran dengan niat doa, mendengar, menyentuh mushaf dan aplikasi Al-Quran.",
    crumb=("Hukum", W + "search/label/Hukum"), about=["Junub", "Haid", "Zikir", "Membaca Al-Quran"],
    answer="Orang yang junub, haid atau nifas <strong>boleh berzikir, berselawat dan berdoa</strong>: Rasulullah SAW berzikir kepada Allah dalam semua keadaannya <em>(HR Muslim, no. 373)</em>. "
           "Dalam mazhab Syafi'i, yang dilarang ialah <strong>membaca Al-Quran dengan niat tilawah</strong> dan <strong>menyentuh mushaf</strong>. Ayat Al-Quran yang dibaca dengan <strong>niat zikir atau doa</strong>, "
           "seperti Ayat Kursi sebagai pendinding atau doa Rabbana, dibenarkan.",
    sections=[
        ("ringkas", "Boleh dan Tidak Boleh: Ringkasan",
         table(["Perbuatan", "Junub / haid / nifas"], [
             ["Zikir, tasbih, tahlil, istighfar, selawat", "✅ Boleh"], ["Berdoa, termasuk doa daripada Al-Quran dengan niat doa", "✅ Boleh"],
             ["Membaca Ayat Kursi atau 3 Qul dengan niat zikir atau pendinding", "✅ Boleh"], ["Mendengar bacaan Al-Quran", "✅ Boleh"],
             ["Membaca di dalam hati atau melihat mushaf tanpa melafazkan", "✅ Boleh"],
             ["Membaca Al-Quran dengan niat tilawah", "❌ Tidak boleh (mazhab Syafi'i)"], ["Menyentuh atau membawa mushaf", "❌ Tidak boleh"],
             ["Duduk di dalam masjid", "❌ Tidak boleh"]])),
        ("dalil", "Dalil dan Penjelasan",
         ul("Aisyah RA berkata: “Nabi SAW berzikir kepada Allah dalam semua keadaannya.”" + ref("HR Muslim, no. 373"),
            "Ali RA berkata tiada yang menghalang Rasulullah SAW daripada membaca Al-Quran kecuali junub." + ref("HR Abu Daud, no. 229; dinilai hasan oleh sebahagian ulama"),
            "Hadis “Wanita haid dan orang junub tidak boleh membaca apa-apa daripada Al-Quran” (HR At-Tirmizi, no. 131) dinilai <strong>dhaif</strong>; mazhab Syafi'i berpegang kepada larangan berdasarkan riwayat Ali dan amalan sahabat.",
            "Larangan menyentuh mushaf berdasarkan surat Nabi SAW kepada penduduk Yaman: “Tidak menyentuh Al-Quran kecuali orang yang suci”." + ref("riwayat Malik dalam Al-Muwatta' dan An-Nasa'i"))
         + f'<div class="{P}-box amber"><strong>Kunci: niat.</strong> Lafaz yang sama boleh menjadi tilawah atau zikir bergantung pada niat. Contohnya membaca “Rabbana atina fid-dunya hasanah…” dengan niat berdoa dibenarkan ketika haid.</div>'),
        ("telefon", "Menyentuh Telefon dan Aplikasi Al-Quran",
         "<p>Ramai pejabat mufti berpendapat telefon atau tablet yang memaparkan ayat Al-Quran <strong>tidak mengambil hukum mushaf</strong> kerana teks itu hanya paparan elektronik, maka boleh disentuh tanpa wuduk. "
         "Namun hukum <strong>membaca</strong> dengan niat tilawah tetap sama: tidak dibenarkan ketika junub atau haid dalam mazhab Syafi'i. Menghormati ayat tetap dituntut.</p>"),
        ("guru", "Bagaimana dengan Guru dan Pelajar Al-Quran yang Haid?",
         "<p>Mazhab Maliki membenarkan wanita haid membaca Al-Quran kerana tempoh haid panjang dan ada keperluan, berbeza dengan junub yang boleh segera diangkat dengan mandi. "
         "Sebahagian institusi tahfiz dan pejabat mufti membenarkan guru dan pelajar perempuan yang haid bertaklid kepada pendapat ini <strong>bagi tujuan mengajar dan menjaga hafazan</strong>. "
         "Bagi selain keperluan itu, ikut pegangan mazhab Syafi'i.</p>"),
        ("amalan", "Amalan yang Dianjurkan Ketika Haid",
         ul("Zikir pagi dan petang, dan tasbih 33·33·33 selepas waktu solat.", "Selawat dan istighfar.", "Mendengar bacaan Al-Quran dan tafsir.", "Berdoa dengan doa-doa Al-Quran dengan niat doa.")
         + f'<p>Gunakan <a href="{Q}zikir-pagi-petang/">Zikir Pagi & Petang dengan kaunter</a> dan <a href="{Q}tasbih-digital/">Tasbih Digital</a>.</p>'),
    ],
    faq=[("Bolehkah membaca Ayat Kursi ketika haid?", "Boleh dengan niat zikir atau pendinding diri, bukan niat tilawah, menurut mazhab Syafi'i."),
         ("Bolehkah orang junub berzikir dan berdoa?", "Boleh. Nabi SAW berzikir dalam semua keadaannya (HR Muslim 373)."),
         ("Bolehkah menyentuh telefon yang ada aplikasi Al-Quran ketika haid?", "Ramai mufti membolehkannya kerana telefon tidak mengambil hukum mushaf. Membaca Al-Quran dengan niat tilawah tetap tidak dibenarkan."),
         ("Bolehkah mendengar Al-Quran ketika junub?", "Boleh. Larangan hanya pada membaca dengan lisan dan menyentuh mushaf."),
         ("Bolehkah wanita haid membaca Yasin pada malam Jumaat?", "Dalam mazhab Syafi'i tidak dengan niat tilawah. Dia boleh mendengar bacaan Yasin, berzikir dan berdoa.")],
    refs=["Sahih Muslim, no. 373.", "Sunan Abu Daud, no. 229; Sunan At-Tirmizi, no. 131 (dhaif).", "Al-Muwatta' Imam Malik (surat 'Amr bin Hazm); Sunan An-Nasa'i.",
          "Imam An-Nawawi, Al-Majmu' Syarh Al-Muhadzdzab, bab apa yang haram bagi orang junub."],
    related=[(MANDI, "Cara Mandi Wajib yang Betul", "Niat, rukun dan langkah sunnah"), (Q + "ayat-kursi/", "Ayat Kursi: Bacaan & Kelebihan", "Arab, Rumi dan maksud dengan audio"),
             (Q + "zikir-pagi-petang/", "Zikir Pagi & Petang", "Dengan kaunter dan rujukan hadis")])))

# 6 ---------------------------------------------------------------- sujud sahwi
P = "ilmx-ss"
POSTS.append(("sujud-sahwi", base(
    ns=P, url=SAHWI, published="2018-02-01", pubms="1 Februari 2018",
    title="Cara Sujud Sahwi: Sebab, Bacaan & Bila Dilakukan (Mazhab Syafi'i)",
    desc="Cara sujud sahwi yang betul menurut mazhab Syafi'i: empat sebab, bacaan, sebelum salam, terlupa tahiyat awal atau qunut, ragu bilangan rakaat dan makmum.",
    h1="Cara Sujud Sahwi yang Betul", img=img("sujud-sahwi", "Panduan Solat", "Cara Sujud Sahwi", "Sebab, bacaan dan bila dilakukan mengikut mazhab Syafi'i", "سُجُودُ السَّهْوِ"),
    alt="Cara sujud sahwi: sebab, bacaan dan bila dilakukan", refshort="Sahih Al-Bukhari & Muslim, Al-Fiqh Al-Manhaji",
    lead="Bila sujud sahwi disunatkan, cara melakukannya sebelum salam, bacaannya, dan apa yang perlu dibuat jika ragu bilangan rakaat atau terlupa qunut.",
    crumb=("Panduan", W + "search/label/Panduan"), about=["Sujud sahwi", "Cara solat"],
    answer="Sujud sahwi ialah <strong>dua kali sujud</strong> (dengan duduk antara dua sujud) yang dilakukan <strong>selepas tahiyat akhir dan sebelum salam</strong> kerana kelupaan dalam solat. "
           "Dalam mazhab Syafi'i hukumnya <strong>sunat</strong>, dan sebabnya empat: tertinggal sunat ab'adh (seperti tahiyat awal atau qunut), ragu bilangan rakaat, terlebih perbuatan kerana lupa, "
           "dan memindahkan bacaan rukun ke tempat yang salah. Dalilnya: Nabi SAW terlupa tahiyat awal lalu sujud dua kali sebelum salam <em>(HR Al-Bukhari, no. 829; Muslim, no. 570)</em>.",
    sections=[
        ("sebab", "4 Sebab Sujud Sahwi",
         table(["Sebab", "Contoh"], [
             ["Tertinggal sunat ab'adh", "Terlupa tahiyat awal, terlupa qunut Subuh, terlupa selawat dalam tahiyat awal"],
             ["Ragu bilangan rakaat", "Tidak pasti sudah 3 atau 4 rakaat: ambil yang sedikit (3), tambah satu rakaat, kemudian sujud sahwi (HR Muslim, no. 571)"],
             ["Terlebih perbuatan kerana lupa", "Terbangun ke rakaat kelima, tersujud tiga kali, terduduk tahiyat pada rakaat pertama"],
             ["Memindahkan bacaan ke tempat lain", "Terbaca Al-Fatihah ketika duduk tahiyat, atau tasyahhud ketika berdiri"]])
         + "<p>Tertinggal <strong>rukun</strong> (seperti rukuk atau sujud) tidak cukup dengan sujud sahwi: rukun itu mesti dilakukan, kemudian sujud sahwi. Tertinggal <strong>sunat hai'ah</strong> "
           "(seperti doa iftitah atau surah selepas Al-Fatihah) tidak disunatkan sujud sahwi.</p>"),
        ("cara", "Cara Sujud Sahwi Langkah demi Langkah",
         ul("Selesaikan tahiyat akhir hingga selawat seperti biasa.", "Berniat sujud sahwi di dalam hati (bagi imam dan orang yang solat sendirian).",
            "Bertakbir dan sujud, kemudian duduk antara dua sujud, kemudian sujud kali kedua.", "Bangkit duduk tahiyat (tanpa mengulang tasyahhud), kemudian memberi salam.", ordered=True)
         + card(P, "Bacaan dalam Sujud Sahwi", "سُبْحَانَ مَنْ لَا يَنَامُ وَلَا يَسْهُو", "Subhana man la yanamu wa la yashu.",
                "Maha Suci Tuhan yang tidak tidur dan tidak lupa.", "Dianjurkan oleh sebahagian ulama Syafi'i; tiada hadis khusus",
                "Boleh juga membaca tasbih sujud biasa “Subhana rabbiyal a'la”. Kedua-duanya sah.")),
        ("makmum", "Sujud Sahwi Bagi Makmum",
         ul("Jika <strong>imam</strong> sujud sahwi, makmum wajib mengikutnya walaupun makmum tidak menyedari kelupaan imam.",
            "Jika <strong>makmum</strong> lupa ketika mengikut imam, imam menanggungnya; makmum tidak sujud sahwi sendiri.",
            "Makmum <strong>masbuq</strong> mengikut sujud sahwi imam, kemudian mengulanginya pada akhir solatnya sendiri menurut pendapat yang muktamad dalam mazhab Syafi'i.",
            "Jika imam terlupa sesuatu, makmum lelaki menegur dengan “Subhanallah” dan makmum perempuan dengan menepuk tangan" + ref("HR Al-Bukhari, no. 1203; Muslim, no. 422") + ".")),
        ("lupa", "Terlupa Sujud Sahwi Sehingga Salam",
         "<p>Jika teringat sejurus selepas salam dan jaraknya masih pendek, sunat kembali sujud sahwi kemudian memberi salam semula. Jika sudah lama atau sudah berbual panjang, tidak perlu; solatnya tetap sah "
         "kerana sujud sahwi hukumnya sunat.</p>"
         + f'<p>Pelajari bacaan <a href="{Q}doa-qunut/">doa qunut</a> dan <a href="{Q}tahiyat-akhir/">tahiyat awal & akhir</a> supaya kelupaan dapat dikurangkan, dan semak <a href="{Q}belajar-solat/">cara solat langkah demi langkah</a>.</p>'),
    ],
    faq=[("Bilakah sujud sahwi dilakukan?", "Dalam mazhab Syafi'i, selepas tahiyat akhir dan sebelum salam (HR Al-Bukhari 829; Muslim 570)."),
         ("Apakah bacaan sujud sahwi?", "Sebahagian ulama Syafi'i menganjurkan “Subhana man la yanamu wa la yashu”. Boleh juga membaca tasbih sujud biasa."),
         ("Terlupa qunut Subuh, perlu sujud sahwi?", "Ya, sunat sujud sahwi kerana qunut ialah sunat ab'adh."),
         ("Ragu sudah 3 atau 4 rakaat, apa perlu dibuat?", "Ambil bilangan yang sedikit (3), sempurnakan rakaat keempat, kemudian sujud sahwi sebelum salam (HR Muslim 571)."),
         ("Adakah solat batal jika tidak sujud sahwi?", "Tidak. Sujud sahwi hukumnya sunat dalam mazhab Syafi'i.")],
    refs=["Sahih Al-Bukhari, no. 829, 1203; Sahih Muslim, no. 422, 570, 571.", "Al-Fiqh Al-Manhaji 'ala Mazhab Al-Imam Asy-Syafi'i, bab sujud sahwi."],
    related=[(Q + "doa-qunut/", "Doa Qunut Subuh", "Bacaan, cara dan hukum jika tertinggal"), (QADA, "Cara Solat Qada", "Ganti solat yang tertinggal dengan kalkulator"),
             (Q + "belajar-solat/", "Cara Solat Lengkap", "Panduan langkah demi langkah dengan bacaan")])))

# 7 ---------------------------------------------------------------- solat gerhana
P = "ilmx-gr"
POSTS.append(("solat-gerhana", base(
    ns=P, url=W + "2018/01/allahuakhbar-inilah-sebab-rasulullah.html", published="2018-01-31", pubms="31 Januari 2018",
    title="Solat Sunat Gerhana: Cara, Niat & Amalan Ketika Gerhana",
    desc="Cara solat sunat gerhana matahari dan bulan: dua rakaat dengan dua rukuk setiap rakaat, lafaz niat, khutbah, amalan ketika gerhana dan mitos yang tiada asas.",
    h1="Solat Sunat Gerhana: Cara, Niat & Amalan", img=img("solat-gerhana", "Solat Sunat", "Solat Sunat Gerhana", "Cara dua rukuk setiap rakaat, niat dan amalan ketika gerhana", "صَلَاةُ الْكُسُوفِ"),
    alt="Cara solat sunat gerhana matahari dan bulan", refshort="Sahih Al-Bukhari & Muslim",
    lead="Kenapa Rasulullah SAW keluar dalam keadaan cemas ketika gerhana, cara solat gerhana yang unik dengan dua rukuk setiap rakaat, dan amalan yang Baginda perintahkan.",
    crumb=("Ibadah", W + "search/label/Ibadah"), about=["Solat gerhana", "Gerhana matahari", "Gerhana bulan"],
    answer="Solat gerhana ialah <strong>sunat muakkad</strong>, dua rakaat dengan <strong>dua kali berdiri, dua kali membaca Al-Fatihah dan surah, serta dua kali rukuk dalam setiap rakaat</strong>, "
           "kemudian dua sujud seperti biasa <em>(HR Al-Bukhari, no. 1044; Muslim, no. 901)</em>. Ia dilakukan dari mula gerhana hingga selesai, sunat berjemaah di masjid dan diikuti khutbah. "
           "Nabi SAW memerintahkan solat, doa, takbir dan sedekah ketika gerhana.",
    sections=[
        ("sebab", "Kenapa Rasulullah SAW Cemas Ketika Gerhana",
         "<p>Ketika berlaku gerhana matahari, Nabi SAW bangun dalam keadaan cemas, bimbang ia tanda Kiamat, lalu terus ke masjid dan solat dengan berdiri, rukuk dan sujud yang sangat panjang" + ref("HR Al-Bukhari, no. 1059; Muslim, no. 912") + ".</p>"
         "<p>Gerhana berlaku pada hari wafat putera Baginda, Ibrahim, dan orang ramai menyangka ia kerana kematian itu. Baginda menolak sangkaan tersebut: “Matahari dan bulan ialah dua tanda daripada tanda-tanda (kebesaran) Allah. "
         "Ia tidak gerhana kerana kematian atau kelahiran seseorang. Apabila kamu melihatnya, berdoalah kepada Allah dan solatlah sehingga ia hilang.”" + ref("HR Al-Bukhari, no. 1043; Muslim, no. 915") + "</p>"),
        ("cara", "Cara Solat Sunat Gerhana",
         ul("Seruan “As-solatu jami'ah” (tanpa azan dan iqamah)." + ref("HR Al-Bukhari, no. 1045"), "Niat dan takbiratul ihram, doa iftitah.",
            "<strong>Berdiri pertama:</strong> Al-Fatihah dan surah panjang (seperti Al-Baqarah atau sekadar mampu).", "<strong>Rukuk pertama</strong> yang panjang, kemudian bangkit (iktidal).",
            "<strong>Berdiri kedua:</strong> Al-Fatihah dan surah yang lebih pendek daripada yang pertama.", "<strong>Rukuk kedua</strong>, kemudian iktidal, kemudian dua sujud seperti biasa.",
            "Rakaat kedua sama seperti rakaat pertama (dua berdiri dan dua rukuk), tetapi lebih pendek.", "Tahiyat akhir dan salam, kemudian imam berkhutbah dua khutbah menurut mazhab Syafi'i.", ordered=True)
         + table(["", "Gerhana matahari (kusuf)", "Gerhana bulan (khusuf)"], [["Bacaan", "Perlahan (sir)", "Kuat (jahar)"], ["Waktu", "Dari mula gerhana hingga matahari terang semula", "Dari mula gerhana hingga bulan terang semula"],
                                                                             ["Jika gerhana selesai ketika solat", "Sempurnakan solat dengan ringkas", "Sempurnakan solat dengan ringkas"]])
         + "<p>Bentuk minimum yang sah ialah dua rakaat seperti solat sunat biasa; bentuk dua rukuk setiap rakaat ialah yang lebih sempurna.</p>"),
        ("niat", "Lafaz Niat Solat Gerhana",
         niat(P, "Niat Solat Gerhana Matahari", "أُصَلِّي سُنَّةَ كُسُوفِ الشَّمْسِ رَكْعَتَيْنِ لِلّٰهِ تَعَالَى", "Usolli sunnata kusufisy-syamsi rak'ataini lillahi ta'ala.",
              "Sahaja aku solat sunat gerhana matahari dua rakaat kerana Allah Taala.", note="Tambah “imaman” (sebagai imam) atau “ma'muman” (sebagai makmum) sebelum “lillahi ta'ala” ketika berjemaah.")
         + niat(P, "Niat Solat Gerhana Bulan", "أُصَلِّي سُنَّةَ خُسُوفِ الْقَمَرِ رَكْعَتَيْنِ لِلّٰهِ تَعَالَى", "Usolli sunnata khusufil-qamari rak'ataini lillahi ta'ala.",
                "Sahaja aku solat sunat gerhana bulan dua rakaat kerana Allah Taala.")),
        ("amalan", "Amalan Ketika Gerhana",
         ul("Solat gerhana.", "Berdoa dan beristighfar.", "Bertakbir.", "Bersedekah." + ref("HR Al-Bukhari, no. 1044: “berdoalah kepada Allah, bertakbirlah, solatlah dan bersedekahlah”"),
            "Membebaskan hamba (pada zaman itu) dan mengingati azab kubur, sebagaimana khutbah Nabi SAW ketika gerhana.")
         + "<p>Tarikh dan waktu gerhana yang kelihatan di Malaysia diumumkan oleh JAKIM dan Planetarium Negara; masjid lazimnya mengumumkan solat gerhana berjemaah.</p>"),
        ("sendiri", "Jika Tidak Dapat Berjemaah",
         "<p>Solat gerhana sah dilakukan seorang diri di rumah, oleh lelaki dan wanita, dengan cara yang sama. Wanita boleh hadir berjemaah di masjid; Asma' binti Abi Bakr RA solat gerhana bersama orang ramai pada zaman Nabi SAW"
         + ref("HR Al-Bukhari, no. 1053") + ". Jika gerhana berlaku pada waktu yang dilarang solat, solat gerhana tetap dibenarkan dalam mazhab Syafi'i kerana ia mempunyai sebab.</p>"
         "<p>Jika gerhana sudah hampir selesai, solat dua rakaat secara ringkas dan perbanyakkan doa dan istighfar hingga ia berakhir.</p>"),
        ("sains", "Gerhana: Sains dan Iman",
         "<p>Gerhana matahari berlaku apabila bulan berada di antara matahari dan bumi; gerhana bulan pula apabila bumi berada di antara matahari dan bulan. Kerana ia mengikut peredaran yang tetap, "
         "ahli falak dapat meramalkan tarikh dan waktunya bertahun-tahun lebih awal. Al-Quran menyebut matahari dan bulan beredar mengikut perhitungan" + ref("Ar-Rahman 55:5") + ".</p>"
         "<p>Memahami sebab saintifik tidak bercanggah dengan sunnah solat gerhana. Nabi SAW mengajar bahawa gerhana ialah tanda kebesaran Allah untuk menginsafkan manusia, "
         "bukan petanda kematian atau nasib seseorang. Jangan melihat gerhana matahari dengan mata kasar; gunakan penapis suria yang diluluskan.</p>"),
        ("mitos", "Mitos Gerhana yang Tiada Asas",
         table(["Kepercayaan", "Hakikat"], [["Gerhana kerana kematian atau kelahiran orang besar", "Dinafikan sendiri oleh Nabi SAW (HR Al-Bukhari, no. 1043)"],
                                            ["Wanita hamil mesti berkurung atau anak akan cacat", "Tiada asas dalam syarak"], ["Gerhana membawa sial atau bala tertentu", "Gerhana ialah tanda kebesaran Allah untuk mengingatkan manusia, bukan petanda sial"]])),
    ],
    faq=[("Berapa rakaat solat gerhana?", "Dua rakaat, dan setiap rakaat mempunyai dua kali berdiri dengan bacaan Al-Fatihah serta surah, dan dua kali rukuk, diikuti dua sujud (HR Al-Bukhari 1044; Muslim 901)."),
         ("Apakah hukum solat gerhana?", "Sunat muakkad bagi lelaki dan wanita, sunat berjemaah di masjid."),
         ("Bilakah waktu solat gerhana?", "Dari mula gerhana kelihatan hingga ia selesai. Tiada solat gerhana jika gerhana sudah berakhir."),
         ("Adakah bacaan solat gerhana kuat atau perlahan?", "Dalam mazhab Syafi'i, perlahan bagi gerhana matahari dan kuat bagi gerhana bulan."),
         ("Apakah amalan lain ketika gerhana?", "Berdoa, bertakbir, beristighfar dan bersedekah, sebagaimana perintah Nabi SAW (HR Al-Bukhari 1044).")],
    refs=["Sahih Al-Bukhari, no. 1043, 1044, 1045, 1059.", "Sahih Muslim, no. 901, 912, 915.", "Al-Fiqh Al-Manhaji 'ala Mazhab Al-Imam Asy-Syafi'i, bab solat gerhana."],
    related=[(Q + "solat-sunat/", "Solat Sunat: Cara & Niat", "Taubat, dhuha, hajat, jenazah, witir dan lain-lain"), (Q + "kalendar-hijrah/", "Kalendar Hijrah", "Tarikh Hijrah rasmi JAKIM dan hari kebesaran Islam"),
             (SAHWI, "Cara Sujud Sahwi", "Jika terlupa dalam solat")])))

# 8 ---------------------------------------------------------------- makmum batal / lalu depan orang solat
P = "ilmx-mb"
POSTS.append(("makmum-batal", base(
    ns=P, url=W + "2018/01/makmum-batal-lewat-depan-makmum-lainnya.html", published="2018-01-19", pubms="19 Januari 2018",
    title="Makmum Batal Wuduk: Cara Keluar Saf & Hukum Lalu Depan Orang Solat",
    desc="Apa perlu dibuat jika wuduk batal ketika solat berjemaah, bolehkah lalu di depan makmum lain, hukum lalu di depan orang solat, sutrah dan jika imam batal.",
    h1="Makmum Batal Wuduk & Hukum Lalu di Depan Orang Solat", img=img("makmum-batal-wuduk", "Panduan Solat", "Makmum Batal Wuduk Ketika Berjemaah", "Cara keluar saf, sutrah dan hukum lalu di depan orang solat", "السُّتْرَةُ"),
    alt="Makmum batal wuduk ketika solat berjemaah dan hukum lalu di depan orang solat", refshort="Sahih Al-Bukhari & Muslim",
    lead="Langkah yang betul apabila wuduk terbatal di tengah saf, bila lalu di depan orang solat dibenarkan, apa itu sutrah, dan apa berlaku jika imam pula yang batal.",
    crumb=("Hukum", W + "search/label/Hukum"), about=["Solat berjemaah", "Sutrah", "Batal wuduk"],
    answer="Makmum yang batal wuduk <strong>wajib keluar daripada solat</strong> dan <strong>boleh melintas di hadapan makmum lain</strong> untuk keluar, kerana sutrah imam ialah sutrah bagi makmum: "
           "Ibn Abbas RA pernah melalui hadapan saf ketika Nabi SAW mengimami solat dan tiada yang membantahnya <em>(HR Al-Bukhari, no. 76)</em>. Yang dilarang keras ialah lalu di hadapan "
           "<strong>orang yang solat sendirian</strong> di antara dia dan sutrahnya <em>(HR Al-Bukhari, no. 510; Muslim, no. 507)</em>.",
    sections=[
        ("langkah", "Langkah Jika Wuduk Batal Ketika Berjemaah",
         ul("Hentikan solat (tidak perlu memberi salam).", "Keluar dengan tenang ke arah yang paling mudah, ke tepi atau ke belakang; melalui hadapan makmum lain dibenarkan.",
            "Ambil wuduk semula.", "Sertai semula jemaah sebagai makmum masbuq dan sempurnakan rakaat yang tertinggal selepas imam memberi salam.", ordered=True)
         + f'<div class="{P}-box amber">Jangan meneruskan solat dalam keadaan tidak berwuduk kerana malu; solat itu tidak sah dan berdosa. Keluar saf kerana batal wuduk ialah perkara biasa dan dibenarkan.</div>'),
        ("lalu", "Hukum Lalu di Depan Orang Solat",
         "<p>Nabi SAW bersabda: “Jika orang yang lalu di hadapan orang yang sedang solat mengetahui (dosa) yang ditanggungnya, nescaya dia berdiri menunggu empat puluh lebih baik baginya daripada lalu di hadapannya.”"
         + ref("HR Al-Bukhari, no. 510; Muslim, no. 507") + "</p>"
         + table(["Keadaan", "Hukum (mazhab Syafi'i)"], [
             ["Lalu di hadapan orang solat sendirian yang menghadap sutrah, di antara dia dan sutrahnya", "Haram"],
             ["Orang solat tanpa sutrah, atau sutrahnya terlalu jauh", "Tidak haram, tetapi makruh; orang yang solat itu yang cuai"],
             ["Melalui hadapan saf makmum dalam solat berjemaah", "Dibenarkan, terutama kerana keperluan (HR Al-Bukhari, no. 76)"],
             ["Kawasan yang sangat sesak seperti Masjidil Haram ketika musim haji", "Diberi kelonggaran oleh ramai ulama kerana sukar dielakkan"]])),
        ("sutrah", "Apa Itu Sutrah",
         "<p>Sutrah ialah penghadang di hadapan orang yang solat, seperti dinding, tiang, beg atau sejadah yang dibentangkan. Nabi SAW bersabda ia setinggi kayu di belakang pelana unta" + ref("HR Muslim, no. 499") + ", "
         "lebih kurang dua pertiga hasta. Dalam mazhab Syafi'i, jaraknya tidak lebih daripada tiga hasta (lebih kurang 1.5 meter) dari tempat berdiri.</p>"
         "<p>Orang yang solat dianjurkan menahan orang yang hendak lalu di antara dia dan sutrahnya dengan isyarat tangan" + ref("HR Al-Bukhari, no. 509; Muslim, no. 505") + ".</p>"),
        ("imam", "Jika Imam Batal Wuduk",
         "<p>Imam yang batal wuduk keluar daripada solat dan sunat menarik seorang makmum di belakangnya untuk menggantikannya (istikhlaf), dan solat diteruskan. "
         "Umar RA melakukannya ketika beliau ditikam dalam solat Subuh, lalu Abdul Rahman bin Auf menyempurnakan solat bersama jemaah" + ref("HR Al-Bukhari, no. 3700") + ". "
         "Jika imam tidak menunjuk pengganti, makmum boleh mendahulukan seseorang, atau menyempurnakan solat masing-masing.</p>"),
    ],
    faq=[("Bolehkah makmum yang batal wuduk lalu di depan makmum lain?", "Boleh. Sutrah imam ialah sutrah bagi makmum, dan Ibn Abbas pernah melalui hadapan saf tanpa dibantah (HR Al-Bukhari 76)."),
         ("Perlukah memberi salam jika wuduk batal ketika solat?", "Tidak. Solat sudah terbatal; terus keluar, berwuduk dan sertai semula jemaah."),
         ("Apakah hukum lalu di depan orang solat?", "Haram jika dia solat sendirian menghadap sutrah dan anda lalu di antara dia dan sutrahnya (HR Al-Bukhari 510; Muslim 507)."),
         ("Apakah yang boleh dijadikan sutrah?", "Dinding, tiang, beg atau objek setinggi kira-kira dua pertiga hasta, atau sejadah yang dibentangkan, tidak lebih tiga hasta dari tempat berdiri."),
         ("Apa berlaku jika imam batal wuduk?", "Imam keluar dan sunat menunjuk makmum di belakangnya untuk meneruskan solat (istikhlaf), seperti yang berlaku pada Umar RA (HR Al-Bukhari 3700).")],
    refs=["Sahih Al-Bukhari, no. 76, 509, 510, 3700.", "Sahih Muslim, no. 499, 505, 507.", "Al-Fiqh Al-Manhaji 'ala Mazhab Al-Imam Asy-Syafi'i, bab sutrah dan solat berjemaah."],
    related=[(Q + "belajar-solat/", "Cara Solat Lengkap", "Rukun, bacaan dan perkara membatalkan solat"), (SAHWI, "Cara Sujud Sahwi", "Jika terlupa dalam solat"),
             (Q + "cari-masjid/", "Cari Masjid & Surau", "Masjid terdekat dengan waktu solat hari ini")])))

# 9 ---------------------------------------------------------------- isteri kejut suami subuh
P = "ilmx-ks"
POSTS.append(("kejut-subuh", base(
    ns=P, url=W + "2020/03/hukum-isteri-kejutkan-suami-solat-subuh.html", published="2020-03-01", pubms="1 Mac 2020",
    title="Hukum Isteri Kejutkan Suami untuk Solat Subuh (Dalil & Adab)",
    desc="Hukum isteri mengejutkan suami untuk solat Subuh dan sebaliknya, hadis merenjis air, dosa terlepas Subuh kerana tertidur, adab mengejutkan dan tip bangun Subuh.",
    h1="Hukum Isteri Kejutkan Suami untuk Solat Subuh", img=img("kejut-solat-subuh", "Rumah Tangga", "Isteri Kejutkan Suami untuk Solat Subuh", "Dalil, adab mengejutkan dan hukum terlepas Subuh kerana tertidur", "صَلَاةُ الْفَجْرِ"),
    alt="Hukum isteri mengejutkan suami untuk solat Subuh", refshort="Sahih Al-Bukhari & Muslim, Sunan Abu Daud",
    lead="Saling mengejutkan untuk solat ialah tanda rumah tangga yang dirahmati. Dalil, hukum orang yang tertidur, dan cara mengejutkan yang beradab.",
    crumb=("Hukum", W + "search/label/Hukum"), about=["Solat Subuh", "Suami isteri"],
    answer="Isteri mengejutkan suami (dan suami mengejutkan isteri) untuk solat ialah <strong>amalan yang dipuji</strong>. Nabi SAW mendoakan rahmat bagi suami yang bangun solat malam lalu mengejutkan isterinya, "
           "dan bagi isteri yang bangun lalu mengejutkan suaminya, hingga merenjis air ke mukanya jika enggan <em>(HR Abu Daud, no. 1308; hasan)</em>. Untuk solat fardu, mengejutkan termasuk "
           "<strong>menyuruh kepada kebaikan</strong> yang sangat dituntut.",
    sections=[
        ("dalil", "Dalil Saling Mengejutkan untuk Solat",
         ul("“Allah merahmati lelaki yang bangun malam lalu solat dan mengejutkan isterinya; jika isterinya enggan, dia merenjis air ke mukanya. Allah merahmati wanita yang bangun malam lalu solat dan mengejutkan suaminya; "
            "jika suaminya enggan, dia merenjis air ke mukanya.”" + ref("HR Abu Daud, no. 1308; An-Nasa'i, no. 1610"),
            "Aisyah RA berkata Nabi SAW solat malam ketika dia tidur, dan apabila Baginda hendak berwitir, Baginda mengejutkannya lalu dia pun berwitir." + ref("HR Al-Bukhari, no. 512"),
            "“Dan perintahkanlah keluargamu mendirikan solat dan bersabarlah dalam mengerjakannya.”" + ref("Taha 20:132"))),
        ("hukum", "Hukum Orang yang Tertidur Hingga Terlepas Subuh",
         "<p>Nabi SAW bersabda: “Tiada kecuaian dalam tidur; kecuaian hanyalah pada orang yang tidak solat sehingga masuk waktu solat yang lain”" + ref("HR Muslim, no. 681") + ". "
         "Orang yang tertidur tanpa sengaja tidak berdosa, tetapi wajib solat sebaik sahaja bangun" + ref("HR Al-Bukhari, no. 597; Muslim, no. 684") + ".</p>"
         + table(["Keadaan", "Hukum"], [["Tidur sebelum masuk waktu Subuh dan sudah berusaha bangun (alarm, minta dikejutkan)", "Tidak berdosa; solat sebaik bangun"],
                                       ["Tidur selepas masuk waktu tanpa yakin akan bangun sebelum habis waktu", "Berdosa menurut ulama"],
                                       ["Sengaja tidak bangun walaupun dikejutkan", "Berdosa; wajib qada segera"]])
         + f'<p>Solat yang tertinggal wajib diganti: lihat <a href="{QADA}">cara solat qada</a>.</p>'),
        ("adab", "Adab Mengejutkan Pasangan",
         ul("Mulakan dengan lembut: sentuhan, panggilan nama yang baik, atau ucapan salam.", "Ulang beberapa kali dengan sabar; ada orang yang tidur sangat lena.",
            "Renjisan air yang sedikit dibenarkan dalam hadis jika pasangan sukar bangun, bukan untuk menyakitkan atau memalukan.",
            "Jangan memarahi atau menyindir; tujuan ialah solat, bukan menang dalam pertengkaran.", "Bersepakat lebih awal: pasangan memberi izin dan menyatakan cara dia mahu dikejutkan.")),
        ("tip", "Tip Supaya Mudah Bangun Subuh",
         ul("Tidur awal dan elakkan bersembang atau bermain telefon lewat malam selepas Isyak.", "Berwuduk dan membaca doa sebelum tidur.",
            "Pasang dua alarm: satu di sisi katil dan satu jauh dari katil.", "Minta pasangan atau ahli keluarga mengejutkan, dan berjanji saling mengejutkan.")
         + f'<p>Semak waktu Subuh zon anda di <a href="{Q}waktu-solat/">Waktu Solat Hari Ini</a> dan amalkan <a href="{Q}doa-sebelum-tidur/">doa sebelum tidur</a>.</p>'),
    ],
    faq=[("Apakah hukum isteri mengejutkan suami untuk solat Subuh?", "Sangat digalakkan. Ia termasuk menyuruh kepada kebaikan dan didoakan rahmat oleh Nabi SAW (HR Abu Daud 1308)."),
         ("Bolehkah merenjis air untuk mengejutkan suami?", "Boleh dengan cara yang lembut dan sedikit, sebagaimana disebut dalam hadis Abu Daud 1308."),
         ("Adakah berdosa jika tertidur hingga terlepas Subuh?", "Tidak berdosa jika tertidur tanpa sengaja selepas berusaha bangun (HR Muslim 681), tetapi wajib solat sebaik sahaja bangun."),
         ("Bagaimana jika suami selalu enggan bangun?", "Nasihat dengan baik pada waktu yang sesuai, bantu dengan rutin tidur yang lebih awal, dan jika berterusan, dapatkan bantuan kaunseling keluarga di pejabat agama.")],
    refs=["Al-Quran: Taha 20:132.", "Sahih Al-Bukhari, no. 512, 597; Sahih Muslim, no. 681, 684.", "Sunan Abu Daud, no. 1308; Sunan An-Nasa'i, no. 1610."],
    related=[(QADA, "Cara Solat Qada", "Ganti solat yang tertinggal"), (Q + "waktu-solat/", "Waktu Solat Hari Ini", "Jadual rasmi JAKIM untuk semua zon"),
             (Q + "doa-sebelum-tidur/", "Doa & Zikir Sebelum Tidur", "Amalan sunnah sebelum tidur")])))

# 10 ---------------------------------------------------------------- khusyuk dalam solat
P = "ilmx-kh"
POSTS.append(("khusyuk-solat", base(
    ns=P, url=KHUSYUK, published="2018-01-17", pubms="17 Januari 2018",
    title="Cara Khusyuk dalam Solat: 10 Langkah daripada Al-Quran & Sunnah",
    desc="Cara khusyuk dalam solat: maksud dan hukum khusyuk, 10 langkah praktikal daripada Al-Quran dan hadis, gangguan Khinzab dan perkara yang menghilangkan khusyuk.",
    h1="Cara Khusyuk dalam Solat", img="khusyuk-solat-ilustrasi.webp",
    alt="Cara mendapat khusyuk dalam solat", refshort="Al-Quran, Sahih Al-Bukhari & Muslim",
    lead="Khusyuk ialah ruh solat. Maksudnya, hukumnya menurut fiqh, dan sepuluh langkah praktikal yang diajar Al-Quran dan Sunnah untuk mencapainya.",
    crumb=("Ibadah", W + "search/label/Ibadah"), about=["Khusyuk", "Solat"],
    answer="Khusyuk ialah <strong>hati yang hadir dan tenang serta anggota yang tenteram</strong> di hadapan Allah. Allah memuji orang beriman yang khusyuk dalam solat <em>(Al-Mu'minun 23:1–2)</em>. "
           "Langkah utama: <strong>bersedia awal, faham bacaan, tuma'ninah, pandang tempat sujud, dan berlindung daripada gangguan syaitan</strong>. Dalam mazhab Syafi'i, khusyuk bukan syarat sah solat, "
           "tetapi pahala solat bergantung pada kadar khusyuk.",
    sections=[
        ("ayat", "Khusyuk dalam Al-Quran", qcard(P, "Al-Mu'minun 23:1–2", 23, 1, 2, "Surah Al-Mu'minun, ayat 1–2")),
        ("maksud", "Maksud dan Hukum Khusyuk",
         "<p>Khusyuk mempunyai dua bahagian: <strong>khusyuk hati</strong> (menyedari kebesaran Allah dan memahami apa yang dibaca) dan <strong>khusyuk anggota</strong> (tenang, tidak bermain-main dan tidak menoleh). "
         "Tahap tertingginya ialah ihsan: “Engkau menyembah Allah seolah-olah engkau melihat-Nya; jika engkau tidak melihat-Nya, Dia melihatmu”" + ref("HR Al-Bukhari, no. 50; Muslim, no. 8") + ".</p>"
         "<p>Menurut jumhur ulama termasuk mazhab Syafi'i, khusyuk ialah sunat yang sangat dituntut; solat tetap sah tanpanya. Yang wajib ialah <strong>tuma'ninah</strong> (berhenti seketika dalam setiap rukun), "
         "kerana Nabi SAW menyuruh seorang lelaki mengulangi solat yang dilakukan tergesa-gesa" + ref("HR Al-Bukhari, no. 757; Muslim, no. 397") + ".</p>"),
        ("langkah", "10 Langkah untuk Khusyuk",
         ul("<strong>Sempurnakan wuduk.</strong> Sesiapa berwuduk dengan sempurna lalu solat dua rakaat dengan hati yang hadir, diampunkan dosanya yang lalu." + ref("HR Al-Bukhari, no. 159; Muslim, no. 226"),
            "<strong>Datang awal</strong> dan tunaikan solat sunat qabliyah supaya hati sudah tenang sebelum fardu.",
            "<strong>Selesaikan hajat dahulu.</strong> Jangan solat ketika makanan sudah terhidang atau menahan buang air." + ref("HR Muslim, no. 560"),
            "<strong>Hadirkan niat</strong>: ingat bahawa ini mungkin solat terakhir. “Apabila kamu berdiri solat, solatlah seperti solat orang yang hendak berpisah.”" + ref("HR Ibn Majah, no. 4171; hasan"),
            "<strong>Fahami bacaan.</strong> Pelajari maksud Al-Fatihah, tasbih rukuk dan sujud serta tahiyat; hati mengikut apa yang difahami.",
            "<strong>Tuma'ninah</strong> dalam setiap rukun; jangan tergesa-gesa.",
            "<strong>Pandang tempat sujud</strong> dan jangan menoleh. Menoleh ialah curian syaitan daripada solat seseorang." + ref("HR Al-Bukhari, no. 751"),
            "<strong>Berlindung daripada was-was.</strong> Syaitan yang mengganggu solat bernama Khinzab; apabila terasa gangguan, berlindunglah kepada Allah dan hembus ke kiri tiga kali." + ref("HR Muslim, no. 2203"),
            "<strong>Kurangkan gangguan:</strong> telefon senyap, sejadah tanpa corak yang menarik perhatian, tempat yang tenang.",
            "<strong>Perbanyakkan doa</strong> dalam sujud kerana itulah keadaan paling dekat seorang hamba dengan Tuhannya." + ref("HR Muslim, no. 482"), ordered=True)),
        ("hilang", "Perkara yang Menghilangkan Khusyuk",
         table(["Perkara", "Pembetulan"], [["Solat di hujung waktu dalam keadaan tergesa-gesa", "Solat awal waktu; semak waktu solat zon anda"],
                                          ["Memikirkan urusan kerja dan telefon", "Selesaikan atau catat urusan sebelum takbir; telefon senyap"],
                                          ["Bacaan yang tidak difahami", "Belajar maksud bacaan solat satu demi satu"], ["Pergerakan berlebihan dan membetulkan pakaian", "Bersiap sebelum takbir; tenangkan anggota"],
                                          ["Lapar atau menahan hajat", "Makan atau ke tandas dahulu jika waktu masih luas (HR Muslim, no. 560)"]])
         + f'<p>Pelajari bacaan dan maksudnya dengan <a href="{Q}belajar-solat/">Cara Solat Lengkap</a>, dan semak <a href="{Q}waktu-solat/">waktu solat hari ini</a>.</p>'),
    ],
    faq=[("Apakah maksud khusyuk dalam solat?", "Hati yang hadir dan tenang menyedari kebesaran Allah, serta anggota yang tenteram tanpa pergerakan sia-sia."),
         ("Adakah solat tidak sah jika tidak khusyuk?", "Sah menurut mazhab Syafi'i dan jumhur ulama, tetapi pahala bergantung pada kadar khusyuk. Tuma'ninah pula wajib."),
         ("Apakah doa ketika diganggu was-was dalam solat?", "Berlindung kepada Allah (a'uzubillahi minasy-syaitanir-rajim) dan menghembus ke kiri tiga kali, sebagaimana diajar Nabi SAW kepada Uthman bin Abi Al-'As (HR Muslim 2203)."),
         ("Bagaimana cara cepat khusyuk?", "Mulakan dengan memahami maksud Al-Fatihah dan bacaan rukuk serta sujud, solat awal waktu, dan tuma'ninah dalam setiap rukun.")],
    refs=["Al-Quran: Al-Mu'minun 23:1–2.", "Sahih Al-Bukhari, no. 50, 159, 751, 757.", "Sahih Muslim, no. 8, 226, 397, 482, 560, 2203.", "Sunan Ibn Majah, no. 4171."],
    related=[(Q + "belajar-solat/", "Cara Solat Lengkap", "Bacaan dan maksud setiap langkah solat"), (SAHWI, "Cara Sujud Sahwi", "Jika terlupa dalam solat"),
             (QADA, "Cara Solat Qada", "Ganti solat yang tertinggal")])))

if __name__ == "__main__":
    write(POSTS)
