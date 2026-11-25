/*! Al-Quran Online (The Ilmu Alam): contact form. Posts to /api/contact (worker/index.js). */
(function () {
  "use strict";
  var form = document.querySelector("[data-contact]");
  if (!form) return;
  var status = form.querySelector("[data-status]"), btn = form.querySelector("button[type=submit]");
  var LABEL = btn.textContent, MAIL = "salam@ilmualam.com";
  form.elements.t.value = String(Date.now());
  form.elements.page.value = document.referrer && document.referrer.indexOf(location.origin) === 0 ? document.referrer : "";

  var qs = new URLSearchParams(location.search);
  var topic = (qs.get("topic") || "").replace(/[^a-z]/g, "");
  if (topic && form.elements.topic.querySelector('option[value="' + topic + '"]')) form.elements.topic.value = topic;
  // Result of a native (no-JS) submit, redirected back by the worker
  if (qs.get("hantar") === "ok") done();
  else if (qs.get("hantar") === "gagal") fail(qs.get("sebab"));

  // Topic links on the page (?topic=x#borang) change the select without a reload
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href*="topic="][href$="#borang"]');
    if (!a) return;
    var t = new URL(a.href, location.href).searchParams.get("topic");
    if (t && form.elements.topic.querySelector('option[value="' + t + '"]')) form.elements.topic.value = t;
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    btn.disabled = true;
    btn.textContent = "Menghantar…";
    status.className = "cf-status";
    status.textContent = "";
    fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (j) {
        if (j.ok) {
          done();
          if (window.dataLayer) window.dataLayer.push({ event: "contact_submit", contact_topic: form.elements.topic && form.elements.topic.value });
          return;
        }
        throw new Error(j.error || "");
      })
      .catch(function (err) {
        fail(err && err.message && err.message !== "Failed to fetch" ? err.message : "");
        btn.disabled = false;
        btn.textContent = LABEL;
      });
  });

  function done() {
    form.innerHTML = '<div class="cf-done" tabindex="-1"><h2>Terima kasih, mesej anda telah dihantar</h2>' +
      "<p>Kami membalas setiap mesej yang tulen, biasanya dalam 2 hari bekerja. Semak folder spam jika belum menerima balasan.</p></div>";
    form.querySelector(".cf-done").focus();
  }

  function fail(msg) {
    status.className = "cf-status cf-status--err";
    status.textContent = (msg || "Mesej tidak dapat dihantar.") + " Anda juga boleh e-mel " + MAIL + ".";
  }
})();
