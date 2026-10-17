"""Prayer times for Malaysia, calculated on the device with JAKIM's parameters (Subuh 20°, Isyak 18°, Asar Syafi'i,
sun altitude -0.833° for syuruk/maghrib, UTC+8) plus a small ihtiyat. assets/js/alat.js mirrors solat_day() exactly;
tools/test-alat.mjs checks the two agree. Official zone timetables: www.e-solat.gov.my."""
import math, datetime as dt

TZ = 8
FAJR, ISHA = 20.0, 18.0
KAABA = (21.4225, 39.8262)

# (slug, name, state, lat, lng, JAKIM zone): state capitals and major towns. Zone "" = no official data mapped, calculation only
CITIES = [
    ("kuala-lumpur", "Kuala Lumpur", "W.P. Kuala Lumpur, Putrajaya & Labuan", 3.139, 101.687, "WLY01"),
    ("putrajaya", "Putrajaya", "W.P. Kuala Lumpur, Putrajaya & Labuan", 2.926, 101.696, "WLY01"),
    ("labuan", "Labuan", "W.P. Kuala Lumpur, Putrajaya & Labuan", 5.280, 115.241, "WLY02"),
    ("shah-alam", "Shah Alam", "Selangor", 3.073, 101.518, "SGR01"),
    ("petaling-jaya", "Petaling Jaya", "Selangor", 3.107, 101.607, "SGR01"),
    ("klang", "Klang", "Selangor", 3.044, 101.445, "SGR03"),
    ("kuala-selangor", "Kuala Selangor", "Selangor", 3.340, 101.250, "SGR02"),
    ("sabak-bernam", "Sabak Bernam", "Selangor", 3.677, 100.988, "SGR02"),
    ("johor-bahru", "Johor Bahru", "Johor", 1.492, 103.741, "JHR02"),
    ("batu-pahat", "Batu Pahat", "Johor", 1.854, 102.933, "JHR04"),
    ("muar", "Muar", "Johor", 2.044, 102.568, "JHR04"),
    ("kluang", "Kluang", "Johor", 2.030, 103.318, "JHR03"),
    ("segamat", "Segamat", "Johor", 2.515, 102.815, "JHR04"),
    ("mersing", "Mersing", "Johor", 2.431, 103.836, "JHR02"),
    ("melaka", "Bandar Melaka", "Melaka", 2.189, 102.250, "MLK01"),
    ("seremban", "Seremban", "Negeri Sembilan", 2.726, 101.938, "NGS03"),
    ("port-dickson", "Port Dickson", "Negeri Sembilan", 2.522, 101.796, "NGS03"),
    ("kuala-pilah", "Kuala Pilah", "Negeri Sembilan", 2.739, 102.249, "NGS02"),
    ("kuantan", "Kuantan", "Pahang", 3.808, 103.326, "PHG02"),
    ("temerloh", "Temerloh", "Pahang", 3.449, 102.418, "PHG03"),
    ("bentong", "Bentong", "Pahang", 3.522, 101.909, "PHG04"),
    ("raub", "Raub", "Pahang", 3.793, 101.857, "PHG04"),
    ("kuala-lipis", "Kuala Lipis", "Pahang", 4.184, 102.042, "PHG04"),
    ("cameron-highlands", "Cameron Highlands", "Pahang", 4.471, 101.377, "PHG06"),
    ("pekan", "Pekan", "Pahang", 3.494, 103.389, "PHG02"),
    ("kuala-terengganu", "Kuala Terengganu", "Terengganu", 5.330, 103.137, "TRG01"),
    ("kemaman", "Kemaman (Chukai)", "Terengganu", 4.233, 103.422, "TRG04"),
    ("dungun", "Dungun", "Terengganu", 4.758, 103.420, "TRG04"),
    ("besut", "Besut (Kampung Raja)", "Terengganu", 5.790, 102.570, "TRG02"),
    ("kota-bharu", "Kota Bharu", "Kelantan", 6.125, 102.238, "KTN01"),
    ("kuala-krai", "Kuala Krai", "Kelantan", 5.531, 102.201, "KTN01"),
    ("gua-musang", "Gua Musang", "Kelantan", 4.884, 101.968, ""),
    ("alor-setar", "Alor Setar", "Kedah", 6.121, 100.367, "KDH01"),
    ("sungai-petani", "Sungai Petani", "Kedah", 5.647, 100.488, "KDH02"),
    ("kulim", "Kulim", "Kedah", 5.365, 100.562, "KDH05"),
    ("langkawi", "Langkawi (Kuah)", "Kedah", 6.317, 99.850, "KDH06"),
    ("baling", "Baling", "Kedah", 5.677, 100.917, "KDH04"),
    ("kangar", "Kangar", "Perlis", 6.441, 100.198, "PLS01"),
    ("george-town", "George Town", "Pulau Pinang", 5.414, 100.329, "PNG01"),
    ("butterworth", "Butterworth", "Pulau Pinang", 5.399, 100.364, "PNG01"),
    ("ipoh", "Ipoh", "Perak", 4.597, 101.090, "PRK02"),
    ("taiping", "Taiping", "Perak", 4.850, 100.741, "PRK06"),
    ("teluk-intan", "Teluk Intan", "Perak", 4.026, 101.021, "PRK05"),
    ("lumut", "Lumut", "Perak", 4.232, 100.630, "PRK05"),
    ("kuala-kangsar", "Kuala Kangsar", "Perak", 4.773, 100.937, "PRK02"),
    ("gerik", "Gerik", "Perak", 5.428, 101.128, "PRK03"),
    ("tapah", "Tapah", "Perak", 4.198, 101.261, "PRK01"),
    ("kota-kinabalu", "Kota Kinabalu", "Sabah", 5.980, 116.073, "SBH07"),
    ("sandakan", "Sandakan", "Sabah", 5.839, 118.117, "SBH01"),
    ("tawau", "Tawau", "Sabah", 4.245, 117.892, "SBH04"),
    ("lahad-datu", "Lahad Datu", "Sabah", 5.027, 118.327, "SBH03"),
    ("keningau", "Keningau", "Sabah", 5.338, 116.162, "SBH08"),
    ("kudat", "Kudat", "Sabah", 6.883, 116.847, "SBH05"),
    ("semporna", "Semporna", "Sabah", 4.479, 118.611, "SBH03"),
    ("beaufort", "Beaufort", "Sabah", 5.347, 115.746, "SBH09"),
    ("kuching", "Kuching", "Sarawak", 1.553, 110.359, "SWK08"),
    ("sibu", "Sibu", "Sarawak", 2.288, 111.831, "SWK04"),
    ("miri", "Miri", "Sarawak", 4.399, 113.991, "SWK02"),
    ("bintulu", "Bintulu", "Sarawak", 3.171, 113.041, "SWK03"),
    ("sri-aman", "Sri Aman", "Sarawak", 1.237, 111.462, "SWK06"),
    ("sarikei", "Sarikei", "Sarawak", 2.126, 111.522, "SWK05"),
    ("kapit", "Kapit", "Sarawak", 2.017, 112.933, "SWK04"),
    ("mukah", "Mukah", "Sarawak", 2.898, 112.091, "SWK04"),
    ("limbang", "Limbang", "Sarawak", 4.750, 115.000, "SWK01"),
]
NAMES = ["Imsak", "Subuh", "Syuruk", "Zohor", "Asar", "Maghrib", "Isyak"]

rad, deg = math.radians, math.degrees


def _sun(jd):
    D = jd - 2451545.0
    g = (357.529 + 0.98560028 * D) % 360
    q = (280.459 + 0.98564736 * D) % 360
    L = (q + 1.915 * math.sin(rad(g)) + 0.020 * math.sin(rad(2 * g))) % 360
    e = 23.439 - 0.00000036 * D
    ra = (deg(math.atan2(math.cos(rad(e)) * math.sin(rad(L)), math.cos(rad(L)))) / 15) % 24
    decl = deg(math.asin(math.sin(rad(e)) * math.sin(rad(L))))
    eqt = q / 15 - ra
    eqt = eqt - 24 * round(eqt / 24)
    return decl, eqt


def _jd(y, m, d):
    if m <= 2:
        y, m = y - 1, m + 12
    A = y // 100
    B = 2 - A + A // 4
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + B - 1524.5


def solat_day(y, m, d, lat, lng):
    """Minutes after local midnight for Imsak, Subuh, Syuruk, Zohor, Asar, Maghrib, Isyak."""
    jd = _jd(y, m, d) - lng / (15 * 24)

    def noon(t):
        return (12 - _sun(jd + t)[1]) % 24

    def angle_time(a, t, ccw):
        decl = _sun(jd + t)[0]
        x = (-math.sin(rad(a)) - math.sin(rad(decl)) * math.sin(rad(lat))) / (math.cos(rad(decl)) * math.cos(rad(lat)))
        T = deg(math.acos(max(-1.0, min(1.0, x)))) / 15
        return noon(t) + (-T if ccw else T)

    def asr(t):
        decl = _sun(jd + t)[0]
        a = -deg(math.atan(1 / (1 + math.tan(rad(abs(lat - decl))))))
        return angle_time(a, t, False)

    f, sr, z, a, mg, i = 5 / 24, 6 / 24, 12 / 24, 13 / 24, 18 / 24, 18 / 24
    f = angle_time(FAJR, f, True); sr = angle_time(0.833, sr, True); z = noon(z)
    a = asr(a); mg = angle_time(0.833, mg, False); i = angle_time(ISHA, i, False)
    adj = TZ - lng / 15
    f, sr, z, a, mg, i = [(x + adj) * 60 for x in (f, sr, z, a, mg, i)]
    # ihtiyat: prayer times rounded up by about 1-2 minutes, syuruk rounded down
    up = lambda x: math.ceil(x + 1)
    sub = up(f)
    return [sub - 10, sub, math.floor(sr - 1), up(z), up(a), up(mg), up(i)]


def qibla(lat, lng):
    p1, p2, dl = rad(lat), rad(KAABA[0]), rad(KAABA[1] - lng)
    return (deg(math.atan2(math.sin(dl), math.cos(p1) * math.tan(p2) - math.sin(p1) * math.cos(dl))) + 360) % 360


def hm(x):
    return f"{x // 60:02d}:{x % 60:02d}"


if __name__ == "__main__":
    for slug in ("kuala-lumpur", "kota-bharu", "kuching", "johor-bahru"):
        c = next(c for c in CITIES if c[0] == slug)
        for day in (dt.date(2026, 10, 17), dt.date(2026, 1, 1), dt.date(2026, 7, 1)):
            print(c[1], day, [hm(x) for x in solat_day(day.year, day.month, day.day, c[3], c[4])], round(qibla(c[3], c[4]), 1))
