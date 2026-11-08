"""Malay-style Rumi (bacaan Rumi gaya Malaysia) for the most-read passages (Al-Fatihah, Al-Kahfi, Ayat Kursi, Amanar Rasul, Yasin, Al-Mulk, 3 Qul), written to be read aloud as recited (Hafs).

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
    # ---- Al-Kahfi ----
    (18, 1): "Alhamdu lillaahil lazii anzala 'alaa 'abdihil kitaaba wa lam yaj'al lahuu 'iwajaa (saktah)",
    (18, 2): "Qayyimal liyunzira ba-san syadiidam mil ladunhu wa yubasysyiral mu-miniinal laziina ya'maluunas saalihaati anna lahum ajran hasanaa",
    (18, 3): 'Maakithiina fiihi abadaa',
    (18, 4): 'Wa yunziral laziina qaalut takhazallaahu waladaa',
    (18, 5): "Maa lahum bihii min 'ilmiw wa laa li-aabaa-ihim, kaburat kalimatan takhruju min afwaahihim, iy yaquuluuna illaa kazibaa",
    (18, 6): "Fala'allaka baakhi'un nafsaka 'alaa aathaarihim il lam yu-minuu bihaazal hadiithi asafaa",
    (18, 7): "Innaa ja'alnaa maa 'alal ardhi ziinatal lahaa linabluwahum ayyuhum ahsanu 'amalaa",
    (18, 8): "Wa innaa lajaa'iluuna maa 'alaihaa sa'iidan juruzaa",
    (18, 9): "Am hasibta anna ashaabal kahfi war raqiimi kaanuu min aayaatinaa 'ajabaa",
    (18, 10): "Iz awal fityatu ilal kahfi faqaaluu rabbanaa aatinaa mil ladunka rahmataw wa hayyi' lanaa min amrinaa rasyadaa",
    (18, 11): "Fadharabnaa 'alaa aazaanihim fil kahfi siniina 'adadaa",
    (18, 12): "Thumma ba'athnaahum lina'lama ayyul hizbaini ahsaa limaa labithuu amadaa",
    (18, 13): "Nahnu naqussu 'alaika naba-ahum bil haqq, innahum fityatun aamanuu birabbihim wa zidnaahum hudaa",
    (18, 14): "Wa rabatnaa 'alaa quluubihim iz qaamuu faqaaluu rabbunaa rabbus samaawaati wal ardhi lan nad'uwa min duunihii ilaahaa, laqad qulnaa izan syatataa",
    (18, 15): "Haa-ulaa-i qaumunat takhazuu min duunihii aalihah, lau laa ya-tuuna 'alaihim bisultaanim bayyin, faman azlamu mimmanif taraa 'alallaahi kazibaa",
    (18, 16): "Wa izi'tazaltumuuhum wa maa ya'buduuna illallaaha fa-wuu ilal kahfi yansyur lakum rabbukum mir rahmatihii wa yuhayyi' lakum min amrikum mirfaqaa",
    (18, 17): "Wa tarasy syamsa izaa tala'at tazaawaru 'an kahfihim zaatal yamiini wa izaa gharabat taqridhuhum zaatasy syimaali wa hum fii fajwatim minh, zaalika min aayaatillaah, may yahdillaahu fahuwal muhtad, wa may yudhlil falan tajida lahuu waliyyam mursyidaa",
    (18, 18): "Wa tahsabuhum aiqaazaw wa hum ruquud, wa nuqallibuhum zaatal yamiini wa zaatasy syimaal, wa kalbuhum baasitun ziraa'aihi bil wasiid, lawit tala'ta 'alaihim lawallaita minhum firaaraw wa lamuli-ta minhum ru'baa",
    (18, 19): "Wa kazaalika ba'athnaahum liyatasaa-aluu bainahum, qaala qaa-ilum minhum kam labithtum, qaaluu labithnaa yauman au ba'dha yaum, qaaluu rabbukum a'lamu bimaa labithtum fab'athuu ahadakum biwariqikum haazihii ilal madiinati falyanzur ayyuhaa azkaa ta'aaman falya-tikum birizqim minhu walyatalattaf wa laa yusy'iranna bikum ahadaa",
    (18, 20): "Innahum iy yazharuu 'alaikum yarjumuukum au yu'iiduukum fii millatihim wa lan tuflihuu izan abadaa",
    (18, 21): "Wa kazaalika a'tharnaa 'alaihim liya'lamuu anna wa'dallaahi haqquw wa annas saa'ata laa raiba fiihaa iz yatanaaza'uuna bainahum amrahum, faqaalubnuu 'alaihim bunyaanaa, rabbuhum a'lamu bihim, qaalal laziina ghalabuu 'alaa amrihim lanattakhizanna 'alaihim masjidaa",
    (18, 22): "Sayaquuluuna thalaathatur raabi'uhum kalbuhum wa yaquuluuna khamsatun saadisuhum kalbuhum rajmam bil ghaib, wa yaquuluuna sab'atuw wa thaaminuhum kalbuhum, qur rabbii a'lamu bi'iddatihim maa ya'lamuhum illaa qaliil, falaa tumaari fiihim illaa miraa-an zaahiraw wa laa tastafti fiihim minhum ahadaa",
    (18, 23): "Wa laa taquulanna lisyai-in innii faa'ilun zaalika ghadaa",
    (18, 24): "Illaa ay yasyaa-allaah, wazkur rabbaka izaa nasiita wa qul 'asaa ay yahdiyani rabbii li-aqraba min haazaa rasyadaa",
    (18, 25): "Wa labithuu fii kahfihim thalaatha mi-atin siniina wazdaaduu tis'aa",
    (18, 26): "Qulillaahu a'lamu bimaa labithuu, lahuu ghaibus samaawaati wal ardh, absir bihii wa asmi', maa lahum min duunihii miw waliyyiw wa laa yusyriku fii hukmihii ahadaa",
    (18, 27): 'Watlu maa uuhiya ilaika min kitaabi rabbik, laa mubaddila likalimaatihii wa lan tajida min duunihii multahadaa',
    (18, 28): "Wasbir nafsaka ma'al laziina yad'uuna rabbahum bil ghadaati wal 'asyiyyi yuriiduuna wajhah, wa laa ta'du 'ainaaka 'anhum turiidu ziinatal hayaatid dunyaa, wa laa tuti' man aghfalnaa qalbahuu 'an zikrinaa wattaba'a hawaahu wa kaana amruhuu furutaa",
    (18, 29): "Wa qulil haqqu mir rabbikum, faman syaa-a falyu-miw wa man syaa-a falyakfur, innaa a'tadnaa lizzaalimiina naaran ahaata bihim suraadiquhaa, wa iy yastaghiithuu yughaathuu bimaa-in kalmuhli yasywil wujuuh, bi-sasy syaraabu wa saa-at murtafaqaa",
    (18, 30): "Innal laziina aamanuu wa 'amilus saalihaati innaa laa nudhii'u ajra man ahsana 'amalaa",
    (18, 31): "Ulaa-ika lahum jannaatu 'adnin tajrii min tahtihimul anhaaru yuhallauna fiihaa min asaawira min zahabiw wa yalbasuuna thiyaaban khudhram min sundusiw wa istabraqim muttaki-iina fiihaa 'alal araa-ik, ni'math thawaabu wa hasunat murtafaqaa",
    (18, 32): "Wadhrib lahum mathalar rajulaini ja'alnaa li-ahadihimaa jannataini min a'naabiw wa hafafnaahumaa binakhliw wa ja'alnaa bainahumaa zar'aa",
    (18, 33): 'Kiltal jannataini aatat ukulahaa wa lam tazlim minhu syai-aa, wa fajjarnaa khilaalahumaa naharaa',
    (18, 34): "Wa kaana lahuu thamarun faqaala lisaahibihii wa huwa yuhaawiruhuu ana aktharu minka maalaw wa a'azzu nafaraa",
    (18, 35): 'Wa dakhala jannatahuu wa huwa zaalimul linafsihii qaala maa azunnu an tabiida haazihii abadaa',
    (18, 36): "Wa maa azunnus saa'ata qaa-imataw wa la-ir rudittu ilaa rabbii la-ajidanna khairam minhaa munqalabaa",
    (18, 37): 'Qaala lahuu saahibuhuu wa huwa yuhaawiruhuu akafarta billazii khalaqaka min turaabin thumma min nutfatin thumma sawwaaka rajulaa',
    (18, 38): 'Laakinna huwallaahu rabbii wa laa usyriku birabbii ahadaa',
    (18, 39): 'Wa lau laa iz dakhalta jannataka qulta maa syaa-allaahu laa quwwata illaa billaah, in tarani ana aqalla minka maalaw wa waladaa',
    (18, 40): "Fa'asaa rabbii ay yu-tiyani khairam min jannatika wa yursila 'alaihaa husbaanam minas samaa-i fatusbiha sa'iidan zalaqaa",
    (18, 41): "Au yusbiha maa-uhaa ghauran falan tastatii'a lahuu talabaa",
    (18, 42): "Wa uhiita bithamarihii fa-asbaha yuqallibu kaffaihi 'alaa maa anfaqa fiihaa wa hiya khaawiyatun 'alaa 'uruusyihaa wa yaquulu yaa laitanii lam usyrik birabbii ahadaa",
    (18, 43): 'Wa lam takul lahuu fi-atuy yansuruunahuu min duunillaahi wa maa kaana muntasiraa',
    (18, 44): "Hunaalikal walaayatu lillaahil haqq, huwa khairun thawaabaw wa khairun 'uqbaa",
    (18, 45): "Wadhrib lahum mathalal hayaatid dunyaa kamaa-in anzalnaahu minas samaa-i fakhtalata bihii nabaatul ardhi fa-asbaha hasyiiman tazruuhur riyaah, wa kaanallaahu 'alaa kulli syai-im muqtadiraa",
    (18, 46): "Al maalu wal banuuna ziinatul hayaatid dunyaa, wal baaqiyaatus saalihaatu khairun 'inda rabbika thawaabaw wa khairun amalaa",
    (18, 47): 'Wa yauma nusayyirul jibaala wa taral ardha baarizataw wa hasyarnaahum falam nughaadir minhum ahadaa',
    (18, 48): "Wa 'uridhuu 'alaa rabbika saffal laqad ji-tumuunaa kamaa khalaqnaakum awwala marrah, bal za'amtum allan naj'ala lakum mau'idaa",
    (18, 49): "Wa wudhi'al kitaabu fataral mujrimiina musyfiqiina mimmaa fiihi wa yaquuluuna yaa wailatanaa maali haazal kitaabi laa yughaadiru saghiirataw wa laa kabiiratan illaa ahsaahaa, wa wajaduu maa 'amiluu haadhiraa, wa laa yazlimu rabbuka ahadaa",
    (18, 50): "Wa iz qulnaa lil malaa-ikatisjuduu li-aadama fasajaduu illaa ibliisa kaana minal jinni fafasaqa 'an amri rabbih, afatattakhizuunahuu wa zurriyyatahuu auliyaa-a min duunii wa hum lakum 'aduww, bi-sa lizzaalimiina badalaa",
    (18, 51): "Maa asyhattuhum khalqas samaawaati wal ardhi wa laa khalqa anfusihim wa maa kuntu muttakhizal mudhilliina 'adhudaa",
    (18, 52): "Wa yauma yaquulu naaduu syurakaa-iyal laziina za'amtum fada'auhum falam yastajiibuu lahum wa ja'alnaa bainahum maubiqaa",
    (18, 53): "Wa ra-al mujrimuunan naara fazannuu annahum muwaaqi'uuhaa wa lam yajiduu 'anhaa masrifaa",
    (18, 54): 'Wa laqad sarrafnaa fii haazal qur-aani linnaasi min kulli mathal, wa kaanal insaanu akthara syai-in jadalaa',
    (18, 55): "Wa maa mana'an naasa ay yu-minuu iz jaa-ahumul hudaa wa yastaghfiruu rabbahum illaa an ta-tiyahum sunnatul awwaliina au ya-tiyahumul 'azaabu qubulaa",
    (18, 56): 'Wa maa nursilul mursaliina illaa mubasysyiriina wa munziriin, wa yujaadilul laziina kafaruu bil baatili liyudhiduu bihil haqq, wattakhazuu aayaatii wa maa unziruu huzuwaa',
    (18, 57): "Wa man azlamu mimman zukkira bi-aayaati rabbihii fa-a'radha 'anhaa wa nasiya maa qaddamat yadaah, innaa ja'alnaa 'alaa quluubihim akinnatan ay yafqahuuhu wa fii aazaanihim waqraa, wa in tad'uhum ilal hudaa falay yahtaduu izan abadaa",
    (18, 58): "Wa rabbukal ghafuuru zur rahmah, lau yu-aakhizuhum bimaa kasabuu la'ajjala lahumul 'azaab, bal lahum mau'idul lay yajiduu min duunihii mau-ilaa",
    (18, 59): "Wa tilkal quraa ahlaknaahum lammaa zalamuu wa ja'alnaa limahlikihim mau'idaa",
    (18, 60): "Wa iz qaala muusaa lifataahu laa abrahu hattaa ablugha majma'al bahraini au amdhiya huqubaa",
    (18, 61): "Falammaa balaghaa majma'a bainihimaa nasiyaa huutahumaa fattakhaza sabiilahuu fil bahri sarabaa",
    (18, 62): 'Falammaa jaawazaa qaala lifataahu aatinaa ghadaa-anaa laqad laqiinaa min safarinaa haazaa nasabaa',
    (18, 63): "Qaala ara-aita iz awainaa ilas sakhrati fa-innii nasiitul huuta wa maa ansaaniihu illasy syaitaanu an azkurah, wattakhaza sabiilahuu fil bahri 'ajabaa",
    (18, 64): "Qaala zaalika maa kunnaa nabgh, fartaddaa 'alaa aathaarihimaa qasasaa",
    (18, 65): "Fawajadaa 'abdam min 'ibaadinaa aatainaahu rahmatam min 'indinaa wa 'allamnaahu mil ladunnaa 'ilmaa",
    (18, 66): "Qaala lahuu muusaa hal attabi'uka 'alaa an tu'allimani mimmaa 'ullimta rusydaa",
    (18, 67): "Qaala innaka lan tastatii'a ma'iya sabraa",
    (18, 68): "Wa kaifa tasbiru 'alaa maa lam tuhit bihii khubraa",
    (18, 69): "Qaala satajidunii in syaa-allaahu saabiraw wa laa a'sii laka amraa",
    (18, 70): "Qaala fa-inittaba'tanii falaa tas-alnii 'an syai-in hattaa uhditha laka minhu zikraa",
    (18, 71): 'Fantalaqaa hattaa izaa rakibaa fis safiinati kharaqahaa, qaala akharaqtahaa litughriqa ahlahaa laqad ji-ta syai-an imraa',
    (18, 72): "Qaala alam aqul innaka lan tastatii'a ma'iya sabraa",
    (18, 73): "Qaala laa tu-aakhiznii bimaa nasiitu wa laa turhiqnii min amrii 'usraa",
    (18, 74): 'Fantalaqaa hattaa izaa laqiyaa ghulaaman faqatalahuu qaala aqatalta nafsan zakiyyatam bighairi nafsil laqad ji-ta syai-an nukraa',
    (18, 75): "Qaala alam aqul laka innaka lan tastatii'a ma'iya sabraa",
    (18, 76): "Qaala in sa-altuka 'an syai-im ba'dahaa falaa tusaahibnii, qad balaghta mil ladunnii 'uzraa",
    (18, 77): "Fantalaqaa hattaa izaa atayaa ahla qaryatinis tat'amaa ahlahaa fa-abau ay yudhayyifuuhumaa fawajadaa fiihaa jidaaray yuriidu ay yanqadhdha fa-aqaamah, qaala lau syi-ta lattakhazta 'alaihi ajraa",
    (18, 78): "Qaala haazaa firaaqu bainii wa bainik, sa-unabbi-uka bita-wiili maa lam tastati' 'alaihi sabraa",
    (18, 79): "Ammas safiinatu fakaanat limasaakiina ya'maluuna fil bahri fa-arattu an a'iibahaa wa kaana waraa-ahum malikuy ya-khuzu kulla safiinatin ghasbaa",
    (18, 80): 'Wa ammal ghulaamu fakaana abawaahu mu-minaini fakhasyiinaa ay yurhiqahumaa tughyaanaw wa kufraa',
    (18, 81): 'Fa-aradnaa ay yubdilahumaa rabbuhumaa khairam minhu zakaataw wa aqraba ruhmaa',
    (18, 82): "Wa ammal jidaaru fakaana lighulaamaini yatiimaini fil madiinati wa kaana tahtahuu kanzul lahumaa wa kaana abuuhumaa saalihan fa-araada rabbuka ay yablughaa asyuddahumaa wa yastakhrijaa kanzahumaa rahmatam mir rabbik, wa maa fa'altuhuu 'an amrii, zaalika ta-wiilu maa lam tasti' 'alaihi sabraa",
    (18, 83): "Wa yas-aluunaka 'an zil qarnain, qul sa-atluu 'alaikum minhu zikraa",
    (18, 84): 'Innaa makkannaa lahuu fil ardhi wa aatainaahu min kulli syai-in sababaa',
    (18, 85): "Fa-atba'a sababaa",
    (18, 86): "Hattaa izaa balagha maghribasy syamsi wajadahaa taghrubu fii 'ainin hami-atiw wa wajada 'indahaa qaumaa, qulnaa yaa zal qarnaini immaa an tu'azziba wa immaa an tattakhiza fiihim husnaa",
    (18, 87): "Qaala ammaa man zalama fasaufa nu'azzibuhuu thumma yuraddu ilaa rabbihii fayu'azzibuhuu 'azaaban nukraa",
    (18, 88): "Wa ammaa man aamana wa 'amila saalihan falahuu jazaa-anil husnaa, wa sanaquulu lahuu min amrinaa yusraa",
    (18, 89): "Thumma atba'a sababaa",
    (18, 90): "Hattaa izaa balagha matli'asy syamsi wajadahaa tatlu'u 'alaa qaumil lam naj'al lahum min duunihaa sitraa",
    (18, 91): 'Kazaalika wa qad ahatnaa bimaa ladaihi khubraa',
    (18, 92): "Thumma atba'a sababaa",
    (18, 93): 'Hattaa izaa balagha bainas saddaini wajada min duunihimaa qaumal laa yakaaduuna yafqahuuna qaulaa',
    (18, 94): "Qaaluu yaa zal qarnaini inna ya-juuja wa ma-juuja mufsiduuna fil ardhi fahal naj'alu laka kharjan 'alaa an taj'ala bainanaa wa bainahum saddaa",
    (18, 95): "Qaala maa makkannii fiihi rabbii khairun fa-a'iinuunii biquwwatin aj'al bainakum wa bainahum radmaa",
    (18, 96): "Aatuunii zubaral hadiid, hattaa izaa saawaa bainas sadafaini qaalanfukhuu, hattaa izaa ja'alahuu naaran qaala aatuunii ufrigh 'alaihi qitraa",
    (18, 97): "Famastaa'uu ay yazharuuhu wa mastataa'uu lahuu naqbaa",
    (18, 98): "Qaala haazaa rahmatum mir rabbii, fa-izaa jaa-a wa'du rabbii ja'alahuu dakkaa', wa kaana wa'du rabbii haqqaa",
    (18, 99): "Wa taraknaa ba'dhahum yauma-iziy yamuuju fii ba'dh, wa nufikha fis suuri fajama'naahum jam'aa",
    (18, 100): "Wa 'aradhnaa jahannama yauma-izil lil kaafiriina 'ardhaa",
    (18, 101): "Allaziina kaanat a'yunuhum fii ghitaa-in 'an zikrii wa kaanuu laa yastatii'uuna sam'aa",
    (18, 102): "Afahasibal laziina kafaruu ay yattakhizuu 'ibaadii min duunii auliyaa', innaa a'tadnaa jahannama lil kaafiriina nuzulaa",
    (18, 103): "Qul hal nunabbi-ukum bil akhsariina a'maalaa",
    (18, 104): "Allaziina dhalla sa'yuhum fil hayaatid dunyaa wa hum yahsabuuna annahum yuhsinuuna sun'aa",
    (18, 105): "Ulaa-ikal laziina kafaruu bi-aayaati rabbihim wa liqaa-ihii fahabitat a'maaluhum falaa nuqiimu lahum yaumal qiyaamati waznaa",
    (18, 106): 'Zaalika jazaa-uhum jahannamu bimaa kafaruu wattakhazuu aayaatii wa rusulii huzuwaa',
    (18, 107): "Innal laziina aamanuu wa 'amilus saalihaati kaanat lahum jannaatul firdausi nuzulaa",
    (18, 108): "Khaalidiina fiihaa laa yabghuuna 'anhaa hiwalaa",
    (18, 109): 'Qul lau kaanal bahru midaadal likalimaati rabbii lanafidal bahru qabla an tanfada kalimaatu rabbii wa lau ji-naa bimithlihii madadaa',
    (18, 110): "Qul innamaa ana basyarum mithlukum yuuhaa ilayya annamaa ilaahukum ilaahuw waahid, faman kaana yarjuu liqaa-a rabbihii falya'mal 'amalan saalihaw wa laa yusyrik bi'ibaadati rabbihii ahadaa",
    # ---- Al-Mulk ----
    (67, 1): "Tabaarakal lazii biyadihil mulku wa huwa 'alaa kulli syai-in qadiir",
    (67, 2): "Allazii khalaqal mauta wal hayaata liyabluwakum ayyukum ahsanu 'amalaa, wa huwal 'aziizul ghafuur",
    (67, 3): "Allazii khalaqa sab'a samaawaatin tibaaqaa, maa taraa fii khalqir rahmaani min tafaawut, farji'il basara hal taraa min futuur",
    (67, 4): "Thummarji'il basara karrataini yanqalib ilaikal basaru khaasi-aw wa huwa hasiir",
    (67, 5): "Wa laqad zayyannas samaa-ad dunyaa bimasaabiiha wa ja'alnaahaa rujuumal lisy syayaatiin, wa a'tadnaa lahum 'azaabas sa'iir",
    (67, 6): "Wa lillaziina kafaruu birabbihim 'azaabu jahannam, wa bi-sal masiir",
    (67, 7): "Izaa ulquu fiihaa sami'uu lahaa syahiiqaw wa hiya tafuur",
    (67, 8): 'Takaadu tamayyazu minal ghaiz, kullamaa ulqiya fiihaa faujun sa-alahum khazanatuhaa alam ya-tikum naziir',
    (67, 9): 'Qaaluu balaa qad jaa-anaa naziirun fakazzabnaa wa qulnaa maa nazzalallaahu min syai-in in antum illaa fii dhalaalin kabiir',
    (67, 10): "Wa qaaluu lau kunnaa nasma'u au na'qilu maa kunnaa fii ashaabis sa'iir",
    (67, 11): "Fa'tarafuu bizambihim fasuhqal li-ashaabis sa'iir",
    (67, 12): 'Innal laziina yakhsyauna rabbahum bil ghaibi lahum maghfiratuw wa ajrun kabiir',
    (67, 13): "Wa asirruu qaulakum awijharuu bih, innahuu 'aliimum bizaatis suduur",
    (67, 14): "Alaa ya'lamu man khalaqa wa huwal latiiful khabiir",
    (67, 15): "Huwal lazii ja'ala lakumul ardha zaluulan famsyuu fii manaakibihaa wa kuluu mir rizqih, wa ilaihin nusyuur",
    (67, 16): 'A-amintum man fis samaa-i ay yakhsifa bikumul ardha fa-izaa hiya tamuur',
    (67, 17): "Am amintum man fis samaa-i ay yursila 'alaikum haasibaa, fasata'lamuuna kaifa naziir",
    (67, 18): 'Wa laqad kazzabal laziina min qablihim fakaifa kaana nakiir',
    (67, 19): 'Awalam yarau ilat tairi fauqahum saaffaatiw wa yaqbidhn, maa yumsikuhunna illar rahmaan, innahuu bikulli syai-im basiir',
    (67, 20): 'Amman haazal lazii huwa jundul lakum yansurukum min duunir rahmaan, inil kaafiruuna illaa fii ghuruur',
    (67, 21): "Amman haazal lazii yarzuqukum in amsaka rizqah, bal lajjuu fii 'utuwwiw wa nufuur",
    (67, 22): "Afamay yamsyii mukibban 'alaa wajhihii ahdaa ammay yamsyii sawiyyan 'alaa siraatim mustaqiim",
    (67, 23): "Qul huwal lazii ansya-akum wa ja'ala lakumus sam'a wal absaara wal af-idah, qaliilam maa tasykuruun",
    (67, 24): 'Qul huwal lazii zara-akum fil ardhi wa ilaihi tuhsyaruun',
    (67, 25): "Wa yaquuluuna mataa haazal wa'du in kuntum saadiqiin",
    (67, 26): "Qul innamal 'ilmu 'indallaahi wa innamaa ana naziirum mubiin",
    (67, 27): "Falammaa ra-auhu zulfatan sii-at wujuuhul laziina kafaruu wa qiila haazal lazii kuntum bihii tadda'uun",
    (67, 28): "Qul ara-aitum in ahlakaniyallaahu wa mam ma'iya au rahimanaa famay yujiirul kaafiriina min 'azaabin aliim",
    (67, 29): "Qul huwar rahmaanu aamannaa bihii wa 'alaihi tawakkalnaa, fasata'lamuuna man huwa fii dhalaalim mubiin",
    (67, 30): "Qul ara-aitum in asbaha maa-ukum ghauran famay ya-tiikum bimaa-im ma'iin",
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
COMPLETE = {1: 7, 18: 110, 36: 83, 67: 30, 112: 4, 113: 5, 114: 6}  # surahs covered in full: every ayah must be present
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
