"""Masjid & surau finder data: one page per JAKIM zone (/cari-masjid/<slug>/). Zone codes, areas and centres are
tools/solat.py ZONES (the same 60-zone list as bukitbesi/waktu-solat v2/js/ws.js). Mosques come from OpenStreetMap via
the Overpass API (tools/masjid_fetch.py, assets/data/masjid/<ZONE>.json, © OpenStreetMap contributors, ODbL 1.0).

OSM has no JAKIM-zone boundaries, so each mosque is given to the zone of its nearest town anchor inside the same state.
Anchors are the main towns named in each zone's JAKIM area list. A 4th value caps an anchor's reach in km, for zones that
are only a summit (KDH07, PRK07, SBH06), so they don't swallow the lowland towns around them."""
import json, math, os, re
import solat as SL

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = f"{REPO}/assets/data/masjid"
LICENCE = "© OpenStreetMap contributors, ODbL 1.0 (https://www.openstreetmap.org/copyright)"

# OSM state boundaries carry ISO3166-2; WLY01 spans two federal territories
ISO = {"johor": ["MY-01"], "kedah": ["MY-02"], "kelantan": ["MY-03"], "melaka": ["MY-04"], "negeri-sembilan": ["MY-05"],
       "pahang": ["MY-06"], "pulau-pinang": ["MY-07"], "perak": ["MY-08"], "perlis": ["MY-09"], "selangor": ["MY-10"],
       "terengganu": ["MY-11"], "sabah": ["MY-12"], "sarawak": ["MY-13"], "kuala-lumpur": ["MY-14", "MY-16"], "labuan": ["MY-15"]}

# zone -> (url slug, [(town, lat, lng[, max km])])
ZONEINFO = {
    "JHR01": ("jhr01-pulau-aur-pemanggil", [("Pulau Aur", 2.450, 104.520), ("Pulau Pemanggil", 2.580, 104.320)]),
    "JHR02": ("jhr02-johor-bahru-kota-tinggi", [("Johor Bahru", 1.493, 103.741), ("Iskandar Puteri", 1.425, 103.640), ("Pasir Gudang", 1.470, 103.900),
              ("Kulai", 1.662, 103.600), ("Kota Tinggi", 1.738, 103.899), ("Mersing", 2.431, 103.836)]),
    "JHR03": ("jhr03-kluang-pontian", [("Kluang", 2.030, 103.318), ("Pontian", 1.487, 103.389)]),
    "JHR04": ("jhr04-batu-pahat-muar-segamat", [("Batu Pahat", 1.855, 102.933), ("Muar", 2.044, 102.568), ("Segamat", 2.515, 102.815),
              ("Tangkak", 2.268, 102.545), ("Gemas", 2.585, 102.612), ("Yong Peng", 2.012, 103.065)]),
    "KDH01": ("kdh01-kota-setar-kubang-pasu", [("Alor Setar", 6.121, 100.368), ("Jitra", 6.268, 100.421), ("Changlun", 6.430, 100.430), ("Pokok Sena", 6.170, 100.520)]),
    "KDH02": ("kdh02-kuala-muda-yan-pendang", [("Sungai Petani", 5.647, 100.488), ("Yan", 5.800, 100.380), ("Pendang", 5.990, 100.480), ("Gurun", 5.815, 100.475)]),
    "KDH03": ("kdh03-padang-terap-sik", [("Kuala Nerang", 6.250, 100.610), ("Sik", 5.820, 100.740)]),
    "KDH04": ("kdh04-baling", [("Baling", 5.677, 100.917), ("Kupang", 5.640, 100.850)]),
    "KDH05": ("kdh05-kulim-bandar-baharu", [("Kulim", 5.365, 100.562), ("Serdang", 5.210, 100.610), ("Bandar Baharu", 5.130, 100.500)]),
    "KDH06": ("kdh06-langkawi", [("Kuah", 6.317, 99.850), ("Padang Matsirat", 6.340, 99.730)]),
    "KDH07": ("kdh07-gunung-jerai", [("Puncak Gunung Jerai", 5.797, 100.430, 3)]),
    "KTN01": ("ktn01-kota-bharu-pasir-mas", [("Kota Bharu", 6.126, 102.238), ("Tumpat", 6.200, 102.170), ("Pasir Mas", 6.050, 102.140), ("Bachok", 6.050, 102.400),
              ("Pasir Puteh", 5.830, 102.400), ("Tanah Merah", 5.800, 102.150), ("Machang", 5.770, 102.220), ("Kuala Krai", 5.531, 102.201)]),
    "KTN02": ("ktn02-gua-musang-jeli", [("Gua Musang", 4.884, 101.968), ("Jeli", 5.700, 101.840), ("Lojing", 4.600, 101.470)]),
    "MLK01": ("mlk01-melaka", [("Bandar Melaka", 2.190, 102.250), ("Alor Gajah", 2.380, 102.210), ("Jasin", 2.310, 102.430), ("Masjid Tanah", 2.350, 102.110)]),
    "NGS01": ("ngs01-tampin-jempol", [("Tampin", 2.470, 102.233), ("Bahau", 2.810, 102.400)]),
    "NGS02": ("ngs02-kuala-pilah-jelebu-rembau", [("Kuala Pilah", 2.739, 102.249), ("Kuala Klawang", 2.940, 102.070), ("Rembau", 2.590, 102.090)]),
    "NGS03": ("ngs03-seremban-port-dickson", [("Seremban", 2.726, 101.938), ("Nilai", 2.810, 101.800), ("Port Dickson", 2.522, 101.796)]),
    "PHG01": ("phg01-pulau-tioman", [("Pulau Tioman", 2.813, 104.160)]),
    "PHG02": ("phg02-kuantan-pekan", [("Kuantan", 3.808, 103.326), ("Pekan", 3.494, 103.389), ("Muadzam Shah", 3.050, 103.080)]),
    "PHG03": ("phg03-temerloh-jerantut-maran", [("Temerloh", 3.449, 102.418), ("Jerantut", 3.940, 102.360), ("Maran", 3.590, 102.770),
              ("Bandar Bera", 3.270, 102.430), ("Chenor", 3.500, 102.610), ("Jengka", 3.780, 102.550)]),
    "PHG04": ("phg04-bentong-raub-lipis", [("Bentong", 3.522, 101.909), ("Raub", 3.793, 101.857), ("Kuala Lipis", 4.184, 102.042)]),
    "PHG05": ("phg05-janda-baik-bukit-tinggi", [("Janda Baik", 3.330, 101.860), ("Bukit Tinggi", 3.400, 101.840), ("Genting Sempah", 3.370, 101.800)]),
    "PHG06": ("phg06-cameron-highlands-genting", [("Tanah Rata", 4.471, 101.377), ("Brinchang", 4.490, 101.390), ("Ringlet", 4.410, 101.380),
              ("Genting Highlands", 3.423, 101.793), ("Bukit Fraser", 3.712, 101.740)]),
    "PHG07": ("phg07-rompin", [("Kuala Rompin", 2.800, 103.480)]),
    "PRK01": ("prk01-tapah-slim-river-tanjung-malim", [("Tapah", 4.197, 101.258), ("Bidor", 4.110, 101.290), ("Slim River", 3.830, 101.400), ("Tanjung Malim", 3.680, 101.520)]),
    "PRK02": ("prk02-ipoh-kuala-kangsar", [("Ipoh", 4.598, 101.090), ("Kuala Kangsar", 4.773, 100.937), ("Sungai Siput", 4.820, 101.070),
              ("Batu Gajah", 4.470, 101.040), ("Kampar", 4.310, 101.150)]),
    "PRK03": ("prk03-gerik-lenggong", [("Gerik", 5.428, 101.128), ("Lenggong", 5.100, 100.970), ("Pengkalan Hulu", 5.700, 100.990)]),
    "PRK04": ("prk04-temengor-belum", [("Banding (Temengor)", 5.550, 101.350)]),
    "PRK05": ("prk05-teluk-intan-lumut-sitiawan", [("Teluk Intan", 4.026, 101.021), ("Sitiawan", 4.217, 100.700), ("Lumut", 4.232, 100.630), ("Pulau Pangkor", 4.220, 100.550),
              ("Seri Iskandar", 4.360, 100.980), ("Bagan Datuk", 3.990, 100.780), ("Parit", 4.470, 100.910), ("Beruas", 4.500, 100.780), ("Kampung Gajah", 4.180, 100.940)]),
    "PRK06": ("prk06-taiping-parit-buntar", [("Taiping", 4.850, 100.741), ("Selama", 5.220, 100.690), ("Bagan Serai", 5.010, 100.540), ("Parit Buntar", 5.130, 100.490)]),
    "PRK07": ("prk07-bukit-larut", [("Bukit Larut", 4.862, 100.795, 3)]),
    "PLS01": ("pls01-perlis", [("Kangar", 6.441, 100.198), ("Arau", 6.430, 100.270), ("Kuala Perlis", 6.400, 100.130), ("Padang Besar", 6.660, 100.320)]),
    "PNG01": ("png01-pulau-pinang", [("George Town", 5.414, 100.329), ("Bayan Lepas", 5.290, 100.260), ("Balik Pulau", 5.350, 100.230), ("Butterworth", 5.399, 100.364),
              ("Bukit Mertajam", 5.360, 100.460), ("Kepala Batas", 5.520, 100.430), ("Nibong Tebal", 5.170, 100.480)]),
    "SBH01": ("sbh01-sandakan", [("Sandakan", 5.840, 118.118)]),
    "SBH02": ("sbh02-beluran-telupid", [("Beluran", 5.890, 117.550), ("Telupid", 5.630, 117.120)]),
    "SBH03": ("sbh03-lahad-datu-semporna", [("Lahad Datu", 5.032, 118.340), ("Kunak", 4.690, 118.250), ("Semporna", 4.479, 118.611)]),
    "SBH04": ("sbh04-tawau", [("Tawau", 4.245, 117.892), ("Kalabakan", 4.420, 117.480)]),
    "SBH05": ("sbh05-kudat-kota-marudu", [("Kudat", 6.883, 116.833), ("Kota Marudu", 6.490, 116.730), ("Pitas", 6.710, 117.050), ("Pulau Banggi", 7.250, 117.080)]),
    "SBH06": ("sbh06-gunung-kinabalu", [("Gunung Kinabalu", 6.075, 116.559, 4)]),
    "SBH07": ("sbh07-kota-kinabalu-tuaran-papar", [("Kota Kinabalu", 5.980, 116.074), ("Putatan", 5.890, 116.060), ("Penampang", 5.920, 116.110), ("Papar", 5.730, 115.930),
              ("Tuaran", 6.180, 116.230), ("Kota Belud", 6.350, 116.430), ("Ranau", 5.950, 116.670)]),
    "SBH08": ("sbh08-keningau-tambunan", [("Keningau", 5.339, 116.161), ("Tambunan", 5.670, 116.360), ("Nabawan", 5.060, 116.440)]),
    "SBH09": ("sbh09-beaufort-sipitang-tenom", [("Beaufort", 5.347, 115.747), ("Membakut", 5.470, 115.780), ("Kuala Penyu", 5.570, 115.600),
              ("Sipitang", 5.080, 115.550), ("Tenom", 5.120, 115.950)]),
    "SWK01": ("swk01-limbang-lawas", [("Limbang", 4.750, 115.017), ("Lawas", 4.850, 115.410)]),
    "SWK02": ("swk02-miri-marudi", [("Miri", 4.390, 113.991), ("Bekenu", 4.050, 113.850), ("Batu Niah", 3.850, 113.730), ("Marudi", 4.180, 114.320)]),
    "SWK03": ("swk03-bintulu-tatau", [("Bintulu", 3.167, 113.033), ("Tatau", 2.880, 112.850), ("Belaga", 2.700, 113.780)]),
    "SWK04": ("swk04-sibu-mukah-kapit", [("Sibu", 2.300, 111.817), ("Mukah", 2.898, 112.091), ("Dalat", 2.740, 111.930), ("Kanowit", 2.100, 112.150),
              ("Song", 2.000, 112.550), ("Kapit", 2.017, 112.933)]),
    "SWK05": ("swk05-sarikei-bintangor", [("Sarikei", 2.117, 111.517), ("Bintangor", 2.170, 111.630), ("Matu", 2.680, 111.530), ("Daro", 2.530, 111.430), ("Julau", 2.030, 111.920)]),
    "SWK06": ("swk06-sri-aman-betong", [("Sri Aman", 1.233, 111.467), ("Betong", 1.410, 111.530), ("Saratok", 1.740, 111.340), ("Lubok Antu", 1.040, 111.830)]),
    "SWK07": ("swk07-samarahan-serian", [("Kota Samarahan", 1.460, 110.490), ("Serian", 1.170, 110.570), ("Simunjan", 1.380, 110.770), ("Sebuyau", 1.520, 110.920)]),
    "SWK08": ("swk08-kuching-bau-lundu", [("Kuching", 1.553, 110.359), ("Bau", 1.420, 110.150), ("Lundu", 1.670, 109.850), ("Sematan", 1.800, 109.780)]),
    "SWK09": ("swk09-zon-khas-kampung-patarikan", [("Kampung Patarikan", 3.833, 115.500)]),
    "SGR01": ("sgr01-shah-alam-petaling-gombak", [("Shah Alam", 3.073, 101.518), ("Petaling Jaya", 3.107, 101.607), ("Subang Jaya", 3.050, 101.580), ("Puchong", 3.030, 101.620),
              ("Selayang", 3.250, 101.650), ("Gombak", 3.250, 101.700), ("Ampang", 3.150, 101.760), ("Kajang", 2.993, 101.787), ("Bangi", 2.920, 101.780),
              ("Semenyih", 2.950, 101.840), ("Cyberjaya", 2.920, 101.650), ("Sepang", 2.690, 101.750), ("Rawang", 3.320, 101.580),
              ("Batang Kali", 3.470, 101.640), ("Kuala Kubu Bharu", 3.565, 101.655)]),
    "SGR02": ("sgr02-kuala-selangor-sabak-bernam", [("Kuala Selangor", 3.338, 101.253), ("Tanjung Karang", 3.430, 101.180), ("Sekinchan", 3.500, 101.100), ("Sabak Bernam", 3.677, 100.988)]),
    "SGR03": ("sgr03-klang-kuala-langat", [("Klang", 3.044, 101.445), ("Pelabuhan Klang", 3.000, 101.390), ("Jenjarom", 2.880, 101.500), ("Banting", 2.810, 101.500)]),
    "TRG01": ("trg01-kuala-terengganu-marang", [("Kuala Terengganu", 5.330, 103.141), ("Kuala Nerus", 5.400, 103.070), ("Marang", 5.210, 103.210)]),
    "TRG02": ("trg02-besut-setiu", [("Jerteh", 5.740, 102.490), ("Kampung Raja", 5.790, 102.570), ("Permaisuri", 5.520, 102.740)]),
    "TRG03": ("trg03-hulu-terengganu", [("Kuala Berang", 5.070, 103.010)]),
    "TRG04": ("trg04-dungun-kemaman", [("Dungun", 4.758, 103.420), ("Paka", 4.640, 103.440), ("Kerteh", 4.510, 103.450), ("Chukai (Kemaman)", 4.233, 103.422)]),
    "WLY01": ("wly01-kuala-lumpur-putrajaya", [("Kuala Lumpur", 3.139, 101.687), ("Kepong", 3.210, 101.640), ("Setapak", 3.200, 101.720), ("Cheras", 3.080, 101.740),
              ("Bukit Jalil", 3.060, 101.680), ("Putrajaya", 2.926, 101.696)]),
    "WLY02": ("wly02-labuan", [("Labuan", 5.280, 115.241)]),
}
assert set(ZONEINFO) == {z[0] for z in SL.ZONES} and len(ZONEINFO) == 60
STATE_OF = {z[0]: z[1] for z in SL.ZONES}
STATE_NAME = {s[0]: s[1] for s in SL.STATES}


def km(a, b, c, d):
    p = math.pi / 180
    h = math.sin((c - a) * p / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin((d - b) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def anchors(state):
    """[(zone, town, lat, lng, cap_km or None)] for one state."""
    return [(z, a[0], a[1], a[2], a[3] if len(a) > 3 else None) for z, (_, aa) in ZONEINFO.items() if STATE_OF[z] == state for a in aa]


def nearest(state, lat, lng):
    """(zone, town, km) of the closest anchor in the state that can reach the point."""
    best = None
    for z, t, a, b, cap in anchors(state):
        d = km(lat, lng, a, b)
        if (cap is None or d <= cap) and (best is None or d < best[2]):
            best = (z, t, d)
    return best


SURAU = re.compile(r"\b(surau|musolla|musalla|musholla|musolah|mushola|madrasah|madrasatul)\b", re.I)
MASJID = re.compile(r"\b(masjid|mosque|jami|jamek)\b", re.I)


def kind(name, tags):
    if SURAU.search(name):
        return "s"
    if MASJID.search(name) or tags.get("building") == "mosque":
        return "m"
    return "t"  # tempat solat: OSM says muslim place of worship, the name doesn't say which


KIND = {"m": "Masjid", "s": "Surau", "t": "Tempat solat"}


def load(zone):
    p = f"{DATA}/{zone}.json"
    return json.load(open(p, encoding="utf8")) if os.path.exists(p) else None


def osm_url(ref):
    t = {"n": "node", "w": "way", "r": "relation"}[ref[0]]
    return f"https://www.openstreetmap.org/{t}/{ref[1:]}"


def dir_url(lat, lng):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat:.6f},{lng:.6f}"
