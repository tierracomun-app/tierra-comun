const C='tc-v4',F=['./','index.html','style.css','app.js','manifest.json','sw.js','data/us.json','data/resources-us.json','data/emergency/international.json','data/emergency/us.json','i18n/es.json','i18n/en.json','icons/icon.svg','data/faq.json'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(F)))});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!=C).map(x=>caches.delete(x)))).then(()=>clients.claim())));
self.addEventListener('fetch',e=>{if(e.request.method!='GET')return;e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).catch(()=>caches.match('index.html'))))});
