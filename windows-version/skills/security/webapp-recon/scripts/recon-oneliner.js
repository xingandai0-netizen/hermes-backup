// Web App Recon - Browser Console Script
// Usage: paste into browser_console via Hermes browser tool
// Returns JSON with all recon data in one call

(function(){
  const r = {
    // Phase 1: Tech Stack
    tech: {
      url: location.href,
      host: location.host,
      vue2: !!(document.querySelector('#app')?.__vue__),
      vue3: !!(document.querySelector('#app')?.__vue_app__),
      react: !!window.__REACT_DEVTOOLS_GLOBAL_HOOK__,
      angular: !!window.ng || !!document.querySelector('[ng-version]'),
      jquery: typeof jQuery !== 'undefined' ? jQuery.fn.jquery : 'none',
      vite: !!document.querySelector('script[type="module"]'),
      app_version: window.__APP_VERSION__ || 'not exposed',
    },

    // Phase 2: Scripts (bundle URLs for further analysis)
    scripts: [...document.querySelectorAll('script[src]')].map(s => s.src),
    inline_scripts: document.querySelectorAll('script:not([src])').length,

    // Phase 3: Links (CSS, icons, preloads)
    links: [...document.querySelectorAll('link[href]')].map(l => ({
      rel: l.rel, href: l.href
    })).slice(0, 20),

    // Phase 4: Inputs and Forms (registration/login surface)
    inputs: [...document.querySelectorAll('input')].map(i => ({
      type: i.type, name: i.name, id: i.id, placeholder: i.placeholder
    })),
    forms: [...document.querySelectorAll('form')].map(f => ({
      action: f.action, method: f.method
    })),

    // Phase 5: iframes (potential clickjack targets)
    iframes: [...document.querySelectorAll('iframe')].map(f => f.src),

    // Phase 6: Config objects (lib, config, etc.)
    config: typeof lib !== 'undefined' ? {
      theme: lib.theme, title: lib.title,
      captchaId: lib.captchaId, device: lib.device,
      web_type: lib.WEB_TYPE__, is_app: lib.IsApp,
    } : 'lib not found',

    // Phase 7: Page structure
    div_ids: [...document.querySelectorAll('div[id]')].map(d => d.id).slice(0, 30),
    a_tags: [...document.querySelectorAll('a[href]')].map(a => ({
      text: a.innerText.trim().substring(0, 50), href: a.href
    })).slice(0, 15),

    // Phase 8: Body text preview
    body_preview: document.body.innerText.substring(0, 500),
  };

  return JSON.stringify(r, null, 2);
})();
