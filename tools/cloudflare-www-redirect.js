// Cloudflare Worker for www.quran.ilmualam.com: a permanent redirect to the same path on quran.ilmualam.com.
// Paste into Workers & Pages > Create > Worker, then add www.quran.ilmualam.com under Settings > Domains & Routes > Custom domain.
// A Worker custom domain gets its own certificate, which the free Universal SSL (apex + one level) does not give this name.
export default {
  fetch(request) {
    const url = new URL(request.url);
    return Response.redirect(`https://quran.ilmualam.com${url.pathname}${url.search}`, 301);
  },
};
