"""Malay-style Rumi (bacaan Rumi gaya Malaysia) for the most-read passages, written to be read aloud as recited (Hafs).

It replaces the English-style transliteration of data-surah/ ("Haiyul Qaiyoom", "yuheetoona") on the static pages only,
and only for surahs listed in PUBLISH. data-surah/ itself is never changed (its checksums stay pinned).

Before anything goes live it must be checked by a qualified teacher (ustaz/ustazah bertauliah):
  1. python3 tools/rumi_review.py <out.html>   -> printable review sheet (Arabic, current Rumi, proposed Rumi, note box)
  2. apply the teacher's corrections in RUMI below
  3. set REVIEWER to the teacher's name and credential, add the surah numbers to PUBLISH, rebuild.
The pages then show "Rumi disemak oleh <REVIEWER>". The build refuses PUBLISH without REVIEWER.

Convention (keep it consistent when editing):
- mad (long vowel) = double vowel: aa, ii, uu; ain = ' (na'budu); hamzah = - inside a word (qur-aan, mu-minuun), ' at the end (syaa')
- ث th · ذ z · ش sy · ص s · ض dh · ط t · ظ z · ح h · خ kh · غ gh · ق q
- written as pronounced: alif lam syamsiah (ar-rahmaan -> ar rahmaan), idgham (min rabbihim -> mir rabbihim; saddan wa -> saddaw wa),
  iqlab (min ba'di -> mim ba'di), syaddah doubled (innaka)
- each ayah ends in its waqaf form (al-hakiim, al-jannah); a comma marks a pause sign (ۚ ۖ ۗ) where readers usually stop
"""

REVIEWER = ""        # e.g. "Ustaz Ahmad bin Ali (guru al-Quran bertauliah, JAIS)"
PUBLISH = set()      # surah numbers whose Malay Rumi is live, e.g. {1, 2, 36, 112, 113, 114}

RUMI = {
    # ---- Al-Fatihah ----
    (1, 1): "Bismillaahir rahmaanir rahiim",
    (1, 2): "Alhamdu lillaahi rabbil 'aalamiin",
    (1, 3): "Ar rahmaanir rahiim",
    (1, 4): "Maaliki yaumid diin",
    (1, 5): "Iyyaaka na'budu wa iyyaaka nasta'iin",
    (1, 6): "Ihdinas siraatal mustaqiim",
    (1, 7): "Siraatal laziina an'amta 'alaihim ghairil maghdhuubi 'alaihim wa ladh dhaalliin",
    # ---- Ayat Kursi & Amanar Rasul ----
    (2, 255): ("Allaahu laa ilaaha illaa huwal hayyul qayyuum, laa ta-khuzuhuu sinatuw wa laa naum, lahuu maa fis samaawaati wa maa fil ardh, "
               "man zal lazii yasyfa'u 'indahuu illaa bi-iznih, ya'lamu maa baina aidiihim wa maa khalfahum, wa laa yuhiituuna bisyai-im min 'ilmihii "
               "illaa bimaa syaa', wasi'a kursiyyuhus samaawaati wal ardh, wa laa ya-uuduhuu hifzuhumaa, wa huwal 'aliyyul 'aziim"),
    (2, 285): ("Aamanar rasuulu bimaa unzila ilaihi mir rabbihii wal mu-minuun, kullun aamana billaahi wa malaa-ikatihii wa kutubihii wa rusulihii "
               "laa nufarriqu baina ahadim mir rusulih, wa qaaluu sami'naa wa ata'naa, ghufraanaka rabbanaa wa ilaikal masiir"),
    (2, 286): ("Laa yukallifullaahu nafsan illaa wus'ahaa, lahaa maa kasabat wa 'alaihaa maktasabat, rabbanaa laa tu-aakhiznaa in nasiinaa au akhta-naa, "
               "rabbanaa wa laa tahmil 'alainaa isran kamaa hamaltahuu 'alal laziina min qablinaa, rabbanaa wa laa tuhammilnaa maa laa taaqata lanaa bih, "
               "wa'fu 'annaa, waghfir lanaa, warhamnaa, anta maulaanaa fansurnaa 'alal qaumil kaafiriin"),
    # ---- Yasin ----
    (36, 1): "Yaa siin",
    (36, 2): "Wal qur-aanil hakiim",
    (36, 3): "Innaka laminal mursaliin",
    (36, 4): "'Alaa siraatim mustaqiim",
    (36, 5): "Tanziilal 'aziizir rahiim",
    (36, 6): "Litunzira qaumam maa unzira aabaa-uhum fahum ghaafiluun",
    (36, 7): "Laqad haqqal qaulu 'alaa aktharihim fahum laa yu-minuun",
    (36, 8): "Innaa ja'alnaa fii a'naaqihim aghlaalan fahiya ilal azqaani fahum muqmahuun",
    (36, 9): "Wa ja'alnaa mim baini aidiihim saddaw wa min khalfihim saddan fa-aghsyainaahum fahum laa yubsiruun",
    (36, 10): "Wa sawaa-un 'alaihim a-anzartahum am lam tunzirhum laa yu-minuun",
    (36, 11): "Innamaa tunziru manit taba'az zikra wa khasyiyar rahmaana bil ghaib, fabasysyirhu bimaghfiratiw wa ajrin kariim",
    (36, 12): "Innaa nahnu nuhyil mautaa wa naktubu maa qaddamuu wa aathaarahum, wa kulla syai-in ahsainaahu fii imaamim mubiin",
    (36, 13): "Wadhrib lahum mathalan ashaabal qaryati iz jaa-ahal mursaluun",
    (36, 14): "Iz arsalnaa ilaihimuth naini fakazzabuuhumaa fa'azzaznaa bithaalithin faqaaluu innaa ilaikum mursaluun",
    (36, 15): "Qaaluu maa antum illaa basyarum mithlunaa wa maa anzalar rahmaanu min syai-in in antum illaa takzibuun",
    (36, 16): "Qaaluu rabbunaa ya'lamu innaa ilaikum lamursaluun",
    (36, 17): "Wa maa 'alainaa illal balaaghul mubiin",
    (36, 18): "Qaaluu innaa tatayyarnaa bikum, la-il lam tantahuu lanarjumannakum wa layamassannakum minnaa 'azaabun aliim",
    (36, 19): "Qaaluu taa-irukum ma'akum, a-in zukkirtum, bal antum qaumum musrifuun",
    (36, 20): "Wa jaa-a min aqsal madiinati rajuluy yas'aa, qaala yaa qaumit tabi'ul mursaliin",
    (36, 21): "Ittabi'uu mal laa yas-alukum ajraw wa hum muhtaduun",
    (36, 22): "Wa maa liya laa a'budul lazii fataranii wa ilaihi turja'uun",
    (36, 23): "A-attakhizu min duunihii aalihatan iy yuridnir rahmaanu bidhurril laa tughni 'annii syafaa'atuhum syai-aw wa laa yunqizuun",
    (36, 24): "Innii izal lafii dhalaalim mubiin",
    (36, 25): "Innii aamantu birabbikum fasma'uun",
    (36, 26): "Qiilad khulil jannah, qaala yaa laita qaumii ya'lamuun",
    (36, 27): "Bimaa ghafara lii rabbii wa ja'alanii minal mukramiin",
    (36, 28): "Wa maa anzalnaa 'alaa qaumihii mim ba'dihii min jundim minas samaa-i wa maa kunnaa munziliin",
    (36, 29): "In kaanat illaa saihataw waahidatan fa-izaa hum khaamiduun",
    (36, 30): "Yaa hasratan 'alal 'ibaad, maa ya-tiihim mir rasuulin illaa kaanuu bihii yastahzi-uun",
    (36, 31): "Alam yarau kam ahlaknaa qablahum minal quruuni annahum ilaihim laa yarji'uun",
    (36, 32): "Wa in kullul lammaa jamii'ul ladainaa muhdharuun",
    (36, 33): "Wa aayatul lahumul ardhul maitatu ahyainaahaa wa akhrajnaa minhaa habban faminhu ya-kuluun",
    (36, 34): "Wa ja'alnaa fiihaa jannaatim min nakhiiliw wa a'naabiw wa fajjarnaa fiihaa minal 'uyuun",
    (36, 35): "Liya-kuluu min thamarihii wa maa 'amilathu aidiihim, afalaa yasykuruun",
    (36, 36): "Subhaanal lazii khalaqal azwaaja kullahaa mimmaa tumbitul ardhu wa min anfusihim wa mimmaa laa ya'lamuun",
    (36, 37): "Wa aayatul lahumul lailu naslakhu minhun nahaara fa-izaa hum muzlimuun",
    (36, 38): "Wasy syamsu tajrii limustaqarril lahaa, zaalika taqdiirul 'aziizil 'aliim",
    (36, 39): "Wal qamara qaddarnaahu manaazila hattaa 'aada kal 'urjuunil qadiim",
    (36, 40): "Lasy syamsu yambaghii lahaa an tudrikal qamara wa lal lailu saabiqun nahaar, wa kullun fii falakiy yasbahuun",
    (36, 41): "Wa aayatul lahum annaa hamalnaa zurriyyatahum fil fulkil masyhuun",
    (36, 42): "Wa khalaqnaa lahum mim mithlihii maa yarkabuun",
    (36, 43): "Wa in nasya' nughriqhum falaa sariikha lahum wa laa hum yunqazuun",
    (36, 44): "Illaa rahmatam minnaa wa mataa'an ilaa hiin",
    (36, 45): "Wa izaa qiila lahumut taquu maa baina aidiikum wa maa khalfakum la'allakum turhamuun",
    (36, 46): "Wa maa ta-tiihim min aayatim min aayaati rabbihim illaa kaanuu 'anhaa mu'ridhiin",
    (36, 47): ("Wa izaa qiila lahum anfiquu mimmaa razaqakumullaahu qaalal laziina kafaruu lillaziina aamanuu anut'imu mal lau yasyaa-ullaahu "
               "at'amahuu in antum illaa fii dhalaalim mubiin"),
    (36, 48): "Wa yaquuluuna mataa haazal wa'du in kuntum saadiqiin",
    (36, 49): "Maa yanzuruuna illaa saihataw waahidatan ta-khuzuhum wa hum yakhissimuun",
    (36, 50): "Falaa yastatii'uuna tausiyataw wa laa ilaa ahlihim yarji'uun",
    (36, 51): "Wa nufikha fis suuri fa-izaa hum minal ajdaathi ilaa rabbihim yansiluun",
    (36, 52): "Qaaluu yaa wailanaa mam ba'athanaa mim marqadinaa (saktah) haazaa maa wa'adar rahmaanu wa sadaqal mursaluun",
    (36, 53): "In kaanat illaa saihataw waahidatan fa-izaa hum jamii'ul ladainaa muhdharuun",
    (36, 54): "Fal yauma laa tuzlamu nafsun syai-aw wa laa tujzauna illaa maa kuntum ta'maluun",
    (36, 55): "Inna ashaabal jannatil yauma fii syughulin faakihuun",
    (36, 56): "Hum wa azwaajuhum fii zilaalin 'alal araa-iki muttaki-uun",
    (36, 57): "Lahum fiihaa faakihatuw wa lahum maa yadda'uun",
    (36, 58): "Salaamun qaulam mir rabbir rahiim",
    (36, 59): "Wamtaazul yauma ayyuhal mujrimuun",
    (36, 60): "Alam a'had ilaikum yaa banii aadama al laa ta'budusy syaitaan, innahuu lakum 'aduwwum mubiin",
    (36, 61): "Wa ani'buduunii, haazaa siraatum mustaqiim",
    (36, 62): "Wa laqad adhalla minkum jibillan kathiiraa, afalam takuunuu ta'qiluun",
    (36, 63): "Haazihii jahannamul latii kuntum tuu'aduun",
    (36, 64): "Islauhal yauma bimaa kuntum takfuruun",
    (36, 65): "Al yauma nakhtimu 'alaa afwaahihim wa tukallimunaa aidiihim wa tasyhadu arjuluhum bimaa kaanuu yaksibuun",
    (36, 66): "Wa lau nasyaa-u latamasnaa 'alaa a'yunihim fastabaqus siraata fa-annaa yubsiruun",
    (36, 67): "Wa lau nasyaa-u lamasakhnaahum 'alaa makaanatihim famastataa'uu mudhiyyaw wa laa yarji'uun",
    (36, 68): "Wa man nu'ammirhu nunakkishu fil khalq, afalaa ya'qiluun",
    (36, 69): "Wa maa 'allamnaahusy syi'ra wa maa yambaghii lah, in huwa illaa zikruw wa qur-aanum mubiin",
    (36, 70): "Liyunzira man kaana hayyaw wa yahiqqal qaulu 'alal kaafiriin",
    (36, 71): "Awalam yarau annaa khalaqnaa lahum mimmaa 'amilat aidiinaa an'aaman fahum lahaa maalikuun",
    (36, 72): "Wa zallalnaahaa lahum faminhaa rakuubuhum wa minhaa ya-kuluun",
    (36, 73): "Wa lahum fiihaa manaafi'u wa masyaarib, afalaa yasykuruun",
    (36, 74): "Wattakhazuu min duunillaahi aalihatal la'allahum yunsaruun",
    (36, 75): "Laa yastatii'uuna nasrahum wa hum lahum jundum muhdharuun",
    (36, 76): "Falaa yahzunka qauluhum, innaa na'lamu maa yusirruuna wa maa yu'linuun",
    (36, 77): "Awalam yaral insaanu annaa khalaqnaahu min nutfatin fa-izaa huwa khasiimum mubiin",
    (36, 78): "Wa dharaba lanaa mathalaw wa nasiya khalqah, qaala may yuhyil 'izaama wa hiya ramiim",
    (36, 79): "Qul yuhyiihal lazii ansya-ahaa awwala marrah, wa huwa bikulli khalqin 'aliim",
    (36, 80): "Allazii ja'ala lakum minasy syajaril akhdhari naaran fa-izaa antum minhu tuuqiduun",
    (36, 81): "Awa laisal lazii khalaqas samaawaati wal ardha biqaadirin 'alaa ay yakhluqa mithlahum, balaa wa huwal khallaaqul 'aliim",
    (36, 82): "Innamaa amruhuu izaa araada syai-an ay yaquula lahuu kun fayakuun",
    (36, 83): "Fasubhaanal lazii biyadihii malakuutu kulli syai-iw wa ilaihi turja'uun",
    # ---- 3 Qul ----
    (112, 1): "Qul huwallaahu ahad",
    (112, 2): "Allaahus samad",
    (112, 3): "Lam yalid wa lam yuulad",
    (112, 4): "Wa lam yakul lahuu kufuwan ahad",
    (113, 1): "Qul a'uuzu birabbil falaq",
    (113, 2): "Min syarri maa khalaq",
    (113, 3): "Wa min syarri ghaasiqin izaa waqab",
    (113, 4): "Wa min syarrin naffaathaati fil 'uqad",
    (113, 5): "Wa min syarri haasidin izaa hasad",
    (114, 1): "Qul a'uuzu birabbin naas",
    (114, 2): "Malikin naas",
    (114, 3): "Ilaahin naas",
    (114, 4): "Min syarril waswaasil khannaas",
    (114, 5): "Allazii yuwaswisu fii suduurin naas",
    (114, 6): "Minal jinnati wan naas",
}
COMPLETE = {1: 7, 36: 83, 112: 4, 113: 5, 114: 6}  # surahs covered in full: every ayah must be present
PARTIAL = {2: [255, 285, 286]}


def check():
    for s, n in COMPLETE.items():
        missing = [a for a in range(1, n + 1) if (s, a) not in RUMI]
        assert not missing, f"Malay Rumi: surah {s} missing ayat {missing}"
    extra = [k for k in RUMI if k[0] not in COMPLETE and k[1] not in PARTIAL.get(k[0], [])]
    assert not extra, f"Malay Rumi: unexpected refs {extra}"
    assert all(v.strip() == v and v for v in RUMI.values()), "Malay Rumi: empty or untrimmed entry"
    assert not PUBLISH or REVIEWER.strip(), "Malay Rumi: set REVIEWER (the teacher who checked it) before adding surahs to PUBLISH"
    assert PUBLISH <= set(COMPLETE) | set(PARTIAL), f"Malay Rumi: PUBLISH has surahs without data: {PUBLISH - set(COMPLETE) - set(PARTIAL)}"


check()


def rumi(s, a, fallback):
    """Malay Rumi when the surah is published, otherwise the dataset's Rumi."""
    return RUMI.get((s, a), fallback) if s in PUBLISH else fallback


def live(s):
    return s in PUBLISH


def credit():
    return f"Rumi gaya Malaysia, disemak oleh {REVIEWER}." if REVIEWER else ""
