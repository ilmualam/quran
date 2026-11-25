// quran.ilmualam.com Worker: POST /api/contact sends the contact form by Cloudflare Email Routing; every other
// request is served from the static assets (dist/). Needs the secret CONTACT_TO (a verified Email Routing destination
// address); the sender is FROM on ilmualam.com, which has Email Routing enabled.
import { EmailMessage } from "cloudflare:email";

const FROM = "borang@ilmualam.com";
const SITE = "https://quran.ilmualam.com";
const PAGE = "/hubungi-kami/";
const TOPICS = {
  kesilapan: "Laporan kesilapan (teks, terjemahan, audio)",
  alat: "Cadangan alat baharu",
  kerjasama: "Kerjasama, masjid & sekolah",
  iklan: "Pengiklanan & tajaan",
  umum: "Soalan umum",
};
const EMAIL_RE = /^[^\s@<>"',;]+@[^\s@<>"',;]+\.[a-z]{2,}$/i;
const MIN_MS = 3000;            // humans take longer than this to fill the form
const MAX_MS = 6 * 3600 * 1000; // page left open longer than this: ask for a reload
const hits = new Map();         // best-effort per-isolate limit: 5 messages / 10 min / IP

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/contact") return env.ASSETS.fetch(request);
    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405, headers: { Allow: "POST" } });
    }
    const wantsJson = (request.headers.get("Accept") || "").includes("application/json");
    try {
      const msg = await handle(request, env);
      return reply(wantsJson, true, msg);
    } catch (err) {
      return reply(wantsJson, false, err instanceof UserError ? err.message : "Mesej tidak dapat dihantar.", err instanceof UserError ? 400 : 500);
    }
  },
};

class UserError extends Error {}

async function handle(request, env) {
  const origin = request.headers.get("Origin");
  if (origin && origin !== new URL(request.url).origin) throw new UserError("Permintaan tidak sah.");

  const ip = request.headers.get("CF-Connecting-IP") || "?";
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < 600000);
  if (recent.length >= 5) throw new UserError("Terlalu banyak mesej. Cuba lagi selepas 10 minit.");

  const f = await request.formData();
  const get = (k) => String(f.get(k) || "").trim();
  const name = get("name").replace(/\s+/g, " "), email = get("email"), message = get("message");
  const topic = TOPICS[get("topic")] ? get("topic") : "umum";
  const page = get("page").slice(0, 300);
  const started = Number(get("t")) || 0;

  // Bots: honeypot filled or submitted instantly. Pretend success so they do not retry.
  if (get("website") || (started && now - started < MIN_MS)) return "ok";
  if (!started || now - started > MAX_MS) throw new UserError("Sesi borang telah tamat. Muat semula halaman dan cuba lagi.");
  if (name.length < 2 || name.length > 100) throw new UserError("Sila masukkan nama anda (2 hingga 100 aksara).");
  if (email.length > 200 || !EMAIL_RE.test(email)) throw new UserError("Sila masukkan alamat e-mel yang sah.");
  if (message.length < 10 || message.length > 5000) throw new UserError("Mesej mesti antara 10 hingga 5,000 aksara.");
  if ((message.match(/https?:\/\//gi) || []).length > 5) throw new UserError("Mesej mengandungi terlalu banyak pautan.");
  if (!env.CONTACT_TO || !env.MAILER) throw new Error("CONTACT_TO or MAILER binding missing");

  const body = [
    `Topik: ${TOPICS[topic]}`,
    `Nama: ${name}`,
    `E-mel: ${email}`,
    `Halaman: ${page || "-"}`,
    `Negara: ${request.cf?.country || "-"}`,
    `Masa: ${new Date(now).toISOString()}`,
    "",
    message,
    "",
    "--",
    `Dihantar melalui borang ${SITE}${PAGE}. Balas e-mel ini untuk menjawab terus kepada pengirim.`,
  ].join("\r\n");

  const raw = mime({
    from: `Borang Al-Quran Online <${FROM}>`,
    to: env.CONTACT_TO,
    replyTo: `${clean(name)} <${email}>`,
    subject: `[Al-Quran Online] ${TOPICS[topic]}: ${clean(name)}`,
    body,
  });
  await env.MAILER.send(new EmailMessage(FROM, env.CONTACT_TO, raw));
  recent.push(now);
  hits.set(ip, recent);
  if (hits.size > 5000) hits.clear();
  return "ok";
}

function clean(s) {
  return s.replace(/[\r\n"<>]/g, " ").slice(0, 100);
}

function b64(s) {
  const bytes = new TextEncoder().encode(s);
  let bin = "";
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
}

function encWord(s) {
  return `=?UTF-8?B?${b64(s)}?=`;
}

function mime({ from, to, replyTo, subject, body }) {
  const id = `${crypto.randomUUID()}@ilmualam.com`;
  return [
    `From: ${from}`,
    `To: ${to}`,
    `Reply-To: ${replyTo.replace(/^([^<]+)</, (_, n) => `${encWord(n.trim())} <`)}`,
    `Subject: ${encWord(subject)}`,
    `Message-ID: <${id}>`,
    `Date: ${new Date().toUTCString()}`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "",
    b64(body).replace(/.{76}/g, "$&\r\n"),
  ].join("\r\n");
}

function reply(json, ok, msg, status = 200) {
  if (json) {
    return new Response(JSON.stringify(ok ? { ok: true } : { ok: false, error: msg }), {
      status,
      headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
    });
  }
  // Without JavaScript the form posts natively: send the visitor back to the page with the result.
  const q = ok ? "hantar=ok" : `hantar=gagal&sebab=${encodeURIComponent(msg)}`;
  return Response.redirect(`${SITE}${PAGE}?${q}#borang`, 303);
}
