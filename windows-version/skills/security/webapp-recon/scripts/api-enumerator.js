// API Endpoint Enumerator - Browser Console Script
// Fetches all JS bundles and extracts API paths
// Usage: run in browser_console on the target page

(function(){
  const jsUrls = [...document.querySelectorAll('script[src]')]
    .map(s => s.src)
    .filter(s => s.includes(location.host));

  return Promise.all(jsUrls.map(url =>
    fetch(url).then(r => r.text()).then(t => {
      const apis = t.match(/["'](api\/[^"']+)["']/gi) || [];
      const clean = [...new Set(apis.map(p => p.replace(/["']/g, '')))];
      return {bundle: url.split('/').pop(), count: clean.length, apis: clean};
    }).catch(e => ({bundle: url.split('/').pop(), error: e.message}))
  )).then(results => {
    const allApis = results.flatMap(r => r.apis || []);
    const unique = [...new Set(allApis)].sort();
    const byCategory = {
      auth: unique.filter(a => /login|reg|user|auth|session|verify|sms|captcha/i.test(a)),
      financial: unique.filter(a => /pay|deposit|withdraw|transfer|wallet|balance|order|money/i.test(a)),
      game: unique.filter(a => /game|play|match|bet|lottery|sport|fish|card/i.test(a)),
      promo: unique.filter(a => /act|promo|bonus|sign|reward|hongbao|vip|rotary/i.test(a)),
      admin: unique.filter(a => /admin|manage|config|setting|system/i.test(a)),
      other: unique.filter(a => !/login|reg|user|auth|session|verify|sms|captcha|pay|deposit|withdraw|transfer|wallet|balance|order|money|game|play|match|bet|lottery|sport|fish|card|act|promo|bonus|sign|reward|hongbao|vip|rotary|admin|manage|config|setting|system/i.test(a)),
    };
    return JSON.stringify({
      total_bundles: jsUrls.length,
      total_unique_apis: unique.length,
      all_apis: unique,
      by_category: byCategory,
    }, null, 2);
  });
})();
