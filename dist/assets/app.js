/* Reformarvel Construcciones · interacción
   intro, transiciones, scroll suave, cabecera, menús, banner en movimiento, nivel de burbuja,
   rótulos, revelados, lista de oficios, proceso horizontal, petición por WhatsApp, galería,
   chispas, cursor, botones magnéticos e inclinación 3D */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const root = document.documentElement;
  const body = document.body;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  if (reduce) root.classList.add('reduce');

  /* ---------- WhatsApp ---------- */
  const NUMBER = body.dataset.waNumber;
  const pageTopic = body.dataset.topic || '';
  const waText = topic => topic
    ? `Hola, Reformarvel. Me gustaría pedir presupuesto de ${topic}. ¿Podemos hablar?`
    : 'Hola, Reformarvel. He visto vuestra web y me gustaría pedir presupuesto para una reforma. ¿Podemos hablar?';
  const waUrl = text => `https://wa.me/${NUMBER}?text=${encodeURIComponent(text)}`;
  // data-wa="tema" usa ese tema; data-wa vacío usa el servicio de la página
  $$('a[data-wa]').forEach(a => { a.href = waUrl(waText(a.dataset.wa || pageTopic.toLowerCase())); });

  /* ---------- Intro (una vez por visita) y entrada ---------- */
  const ready = () => root.classList.add('is-ready');
  const intro = $('.intro');
  if (intro && root.classList.contains('show-intro')) {
    const num = $('[data-count-intro]', intro);
    const t0 = performance.now();
    let done = false;
    const count = t => {
      const k = clamp((t - t0) / 1900, 0, 1);
      num.textContent = String(Math.round(100 * (1 - Math.pow(1 - k, 3)))).padStart(2, '0');
      if (k < 1 && !done) requestAnimationFrame(count);
    };
    requestAnimationFrame(count);
    const finish = () => {
      if (done) return; done = true;
      num.textContent = '100';
      intro.classList.add('is-open');
      try { sessionStorage.setItem('rm-intro', '1'); } catch (_) {}
      setTimeout(ready, 350);
      setTimeout(() => root.classList.remove('show-intro'), 1100);
    };
    const t = setTimeout(finish, 2250);
    intro.addEventListener('click', () => { clearTimeout(t); finish(); });
    addEventListener('keydown', () => { clearTimeout(t); finish(); }, { once: true });
  } else {
    try { sessionStorage.setItem('rm-intro', '1'); } catch (_) {}
    requestAnimationFrame(() => setTimeout(ready, root.classList.contains('veil-in') ? 300 : 60));
  }

  /* ---------- Transiciones entre páginas ---------- */
  if (root.classList.contains('veil-in')) {
    requestAnimationFrame(() => requestAnimationFrame(() => {
      root.classList.add('veil-out'); root.classList.remove('veil-in');
      setTimeout(() => root.classList.remove('veil-out'), 900);
    }));
  }
  addEventListener('pageshow', e => { if (e.persisted) root.classList.remove('is-leaving'); });
  if (!reduce) document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target || a.hasAttribute('download')) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || !/(\.html|\/)$/.test(url.pathname) || url.pathname === location.pathname) return;
    e.preventDefault();
    root.style.setProperty('--vx', e.clientX + 'px');
    root.style.setProperty('--vy', e.clientY + 'px');
    root.classList.add('is-leaving');
    try { sessionStorage.setItem('rm-nav', '1'); } catch (_) {}
    setTimeout(() => { location.href = url.href; }, 620);
  });

  /* ---------- Scroll suave con inercia ---------- */
  let lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new window.Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href*="#"]');
      if (!a) return;
      const url = new URL(a.href, location.href);
      if (url.pathname !== location.pathname || url.hash.length < 2) return;
      const target = document.getElementById(url.hash.slice(1));
      if (!target) return;
      e.preventDefault();
      closeMenus();
      lenis.scrollTo(target, { offset: -70 });
    });
  }
  const lock = on => { if (lenis) on ? lenis.stop() : lenis.start(); body.style.overflow = on ? 'hidden' : ''; };

  /* ---------- Cabecera y barra de progreso ---------- */
  const header = $('[data-header]');
  const bar = $('.progress');
  let lastY = scrollY, vel = 0;
  const onScroll = () => {
    const y = scrollY;
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : 0);
    header.classList.toggle('is-solid', y > 40);
    if (!body.classList.contains('menu-open') && !header.contains(document.activeElement)) header.classList.toggle('is-hidden', y > lastY + 4 && y > 500);
    if (y < lastY - 4) header.classList.remove('is-hidden');
    lastY = y;
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  let vy = scrollY;
  const tickVel = () => { vel += ((scrollY - vy) - vel) * .18; vy = scrollY; requestAnimationFrame(tickVel); };
  requestAnimationFrame(tickVel);

  /* ---------- Menú de servicios (escritorio) ---------- */
  const megaBtn = $('[data-mega-toggle]'), mega = $('[data-mega]');
  const previews = $$('.mega-preview img');
  const showPreview = i => previews.forEach((img, k) => img.classList.toggle('is-on', k === +i));
  showPreview(0);
  const setMega = open => { mega.classList.toggle('is-open', open); megaBtn.setAttribute('aria-expanded', open); };
  megaBtn.addEventListener('click', () => setMega(megaBtn.getAttribute('aria-expanded') !== 'true'));
  if (fine) {
    let leaveT;
    const wrap = megaBtn.parentElement;
    wrap.addEventListener('pointerenter', () => { clearTimeout(leaveT); setMega(true); });
    wrap.addEventListener('pointerleave', () => { leaveT = setTimeout(() => setMega(false), 220); });
  }
  $$('.mega-list a').forEach(a => {
    a.addEventListener('pointerenter', () => showPreview(a.dataset.preview));
    a.addEventListener('focus', () => showPreview(a.dataset.preview));
  });
  document.addEventListener('click', e => { if (!e.target.closest('.nav-services')) setMega(false); });

  /* ---------- Menú móvil ---------- */
  const burger = $('[data-burger]'), menu = $('[data-menu]');
  $$('li', menu).forEach((li, i) => li.style.setProperty('--i', i));
  const setMenu = open => {
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    body.classList.toggle('menu-open', open);
    if (open) { menu.hidden = false; requestAnimationFrame(() => menu.classList.add('is-open')); header.classList.remove('is-hidden'); }
    else { menu.classList.remove('is-open'); setTimeout(() => { if (!menu.classList.contains('is-open')) menu.hidden = true; }, 700); }
    lock(open);
  };
  function closeMenus() { setMega(false); if (burger.getAttribute('aria-expanded') === 'true') setMenu(false); }
  burger.addEventListener('click', () => setMenu(burger.getAttribute('aria-expanded') !== 'true'));
  addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenus(); closeLightbox(); } });
  addEventListener('resize', () => { if (innerWidth > 1180 && body.classList.contains('menu-open')) setMenu(false); });

  /* ---------- WhatsApp flotante ---------- */
  const float = $('.wa-float'), bubble = $('[data-wa-bubble]');
  if (pageTopic) bubble.textContent = `¿Te preparamos tu presupuesto de ${pageTopic.toLowerCase()}?`;
  setTimeout(() => float.classList.add('is-on'), root.classList.contains('show-intro') ? 3200 : 900);
  let bubbleShown = false;
  try { bubbleShown = !!sessionStorage.getItem('rm-bubble'); } catch (_) {}
  if (!bubbleShown) setTimeout(() => {
    bubble.classList.add('is-on');
    try { sessionStorage.setItem('rm-bubble', '1'); } catch (_) {}
    setTimeout(() => bubble.classList.remove('is-on'), 7000);
  }, 9000);

  /* ---------- Banner en movimiento de la portada ---------- */
  const hero = $('[data-hero]');
  if (hero) {
    const slides = $$('.slide', hero), dots = $$('.hero-dot', hero);
    const word = $('[data-now]'), tag = $('[data-now-tag]'), desc = $('[data-now-desc]'), tasks = $('[data-now-tasks]'), btnWord = $('[data-now-btn]'), btn = $('[data-hero-wa]');
    const DUR = 6500;
    let cur = 0, timer = null, paused = false;
    hero.style.setProperty('--dur', DUR + 'ms');
    const swapText = (el, txt) => { el.textContent = txt; el.classList.remove('swap'); void el.offsetWidth; el.classList.add('swap'); };
    const go = i => {
      i = (i + slides.length) % slides.length;
      if (i === cur) return;
      slides.forEach(s => s.classList.remove('is-prev'));
      slides[cur].classList.remove('is-active'); slides[cur].classList.add('is-prev');
      slides[i].classList.add('is-active');
      dots.forEach((d, k) => { d.classList.toggle('is-active', k === i); d.classList.toggle('is-done', k < i); d.setAttribute('aria-current', k === i); });
      const s = slides[i];
      swapText(word, s.dataset.topic); swapText(tag, s.dataset.tag); swapText(desc, s.dataset.desc);
      tasks.innerHTML = s.dataset.tasks.split('|').map(t => `<li>${t}</li>`).join('');
      tasks.classList.remove('swap'); void tasks.offsetWidth; tasks.classList.add('swap');
      btnWord.textContent = s.dataset.topic.toLowerCase();
      btn.href = waUrl(waText(s.dataset.topic.toLowerCase()));
      cur = i;
      schedule();
    };
    const schedule = () => { clearTimeout(timer); if (!reduce && !paused) timer = setTimeout(() => go(cur + 1), DUR); };
    const pause = on => { paused = on; hero.classList.toggle('is-paused', on); if (on) clearTimeout(timer); else schedule(); };
    dots.forEach((d, k) => d.addEventListener('click', () => go(k)));
    $('[data-next]', hero).addEventListener('click', () => go(cur + 1));
    $('[data-prev]', hero).addEventListener('click', () => go(cur - 1));
    $('.hero-nav', hero).addEventListener('pointerenter', () => pause(true));
    $('.hero-nav', hero).addEventListener('pointerleave', () => pause(false));
    hero.addEventListener('focusin', () => pause(true));
    hero.addEventListener('focusout', () => pause(false));
    document.addEventListener('visibilitychange', () => pause(document.hidden));
    // Arrastrar o deslizar para cambiar
    let sx = null;
    hero.addEventListener('pointerdown', e => { if (!e.target.closest('a,button')) sx = e.clientX; });
    hero.addEventListener('pointerup', e => { if (sx === null) return; const dx = e.clientX - sx; sx = null; if (Math.abs(dx) > 60) go(cur + (dx < 0 ? 1 : -1)); });
    hero.addEventListener('keydown', e => { if (e.key === 'ArrowRight') go(cur + 1); if (e.key === 'ArrowLeft') go(cur - 1); });
    const start = () => (root.classList.contains('show-intro') ? setTimeout(schedule, 2400) : schedule());
    start();
    dots[0].setAttribute('aria-current', true);
  }

  /* Foco de luz que sigue al ratón en las portadas */
  $$('.hero, .s-hero').forEach(h => {
    if (!fine || reduce) return;
    h.addEventListener('pointermove', e => {
      const r = h.getBoundingClientRect();
      h.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      h.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- Nivel de burbuja ---------- */
  const level = $('[data-level]');
  if (level && fine) {
    const txt = $('[data-level-txt]', level);
    let lvT;
    addEventListener('pointermove', e => {
      const k = clamp((e.clientX / innerWidth - .5) * 2, -1, 1);
      const x = k * 58;
      level.style.setProperty('--lx', x.toFixed(1) + 'px');
      const ok = Math.abs(x) < 5;
      clearTimeout(lvT);
      lvT = setTimeout(() => { level.classList.toggle('is-level', ok); txt.textContent = ok ? '¡a nivel! Así trabajamos' : 'busca el nivel'; }, 120);
    }, { passive: true });
  }

  /* ---------- Rótulos que corren con la velocidad del scroll ---------- */
  const rows = $$('[data-marquee]').map(m => {
    const track = $('.marquee-track', m);
    track.append(...[...track.children].map(n => { const c = n.cloneNode(true); c.setAttribute('aria-hidden', 'true'); if (c.tagName === 'A') c.tabIndex = -1; return c; }));
    return { track, dir: +m.dataset.marquee, x: 0, hover: false, el: m };
  });
  rows.forEach(r => { r.el.addEventListener('pointerenter', () => { r.hover = true; }); r.el.addEventListener('pointerleave', () => { r.hover = false; }); });
  if (rows.length && !reduce) {
    const run = () => {
      const boost = clamp(Math.abs(vel) * .3, 0, 16);
      rows.forEach(r => {
        const half = r.track.scrollWidth / 2;
        r.x -= ((r.hover ? .25 : .8) + boost) * r.dir;
        if (r.x <= -half) r.x += half;
        if (r.x > 0) r.x -= half;
        r.track.style.transform = `translate3d(${r.x}px,0,0) skewX(${clamp(vel * -.15, -10, 10)}deg)`;
      });
      requestAnimationFrame(run);
    };
    requestAnimationFrame(run);
  }

  /* ---------- Titulares palabra a palabra ---------- */
  $$('.split').forEach(h => {
    let i = 0;
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.append(part); return; }
          const w = document.createElement('span'); w.className = 'w';
          const inner = document.createElement('span'); inner.textContent = part; inner.style.setProperty('--i', i++);
          w.append(inner); frag.append(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    walk(h);
  });

  /* Título del servicio letra a letra (sin partir las palabras con guiones blandos) */
  $$('[data-letters]').forEach(h => {
    if (reduce || h.textContent.includes('­')) return;
    let i = 0;
    h.setAttribute('aria-label', h.textContent);
    h.innerHTML = h.textContent.split(' ').map(w => `<span class="chw" aria-hidden="true">${[...w].map(c => `<span class="ch" style="--i:${i++}">${c}</span>`).join('')}</span>`).join(' ');
  });

  /* ---------- Apariciones al hacer scroll ---------- */
  const io = new IntersectionObserver(en => en.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('is-in');
    io.unobserve(e.target);
  }), { threshold: .14, rootMargin: '0px 0px -6% 0px' });
  $$('.reveal, .reveal-img, .split, .ticks li').forEach((el, i) => {
    if (el.matches('.ticks li, .stat, .svc-row, .faq-item')) el.style.transitionDelay = ((i % 6) * 70) + 'ms';
    io.observe(el);
  });

  /* ---------- Bocadillos de las viñetas del proceso ---------- */
  const sio = new IntersectionObserver(en => en.forEach(e => { if (e.isIntersecting) { setTimeout(() => e.target.classList.add('is-on'), 350); sio.unobserve(e.target); } }), { threshold: .55 });
  $$('.chapter').forEach(c => sio.observe(c));

  /* ---------- Manifiesto que se ilumina al bajar ---------- */
  const scrub = $('[data-scrub]');
  let scrubWords = [];
  if (scrub && !reduce) {
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(p => {
          if (!p) return;
          if (/^\s+$/.test(p)) { frag.append(p); return; }
          const s = document.createElement('span'); s.className = 'sw'; s.textContent = p; frag.append(s);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1) walk(n);
    });
    walk(scrub);
    scrubWords = $$('.sw', scrub);
  }

  /* ---------- Contadores ---------- */
  $$('[data-count]').forEach(b => {
    const end = +b.dataset.count;
    if (reduce || !end) return;
    b.textContent = '0';
    new IntersectionObserver((en, o) => {
      if (!en[0].isIntersecting) return; o.disconnect();
      const t0 = performance.now();
      const tick = t => { const k = Math.min((t - t0) / 1400, 1); b.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    }, { threshold: .6 }).observe(b);
  });

  /* ---------- Lista de oficios con imagen que sigue al ratón ---------- */
  const list = $('[data-svc-list]'), fl = $('[data-svc-float]');
  if (list && fl && fine && !reduce) {
    const imgs = $$('img', fl);
    let mx = 0, my = 0, x = 0, y = 0, on = false;
    $$('.svc-row', list).forEach(row => {
      row.addEventListener('pointerenter', () => {
        imgs.forEach((im, k) => im.classList.toggle('is-on', k === +row.dataset.preview));
        on = true; fl.classList.add('is-on');
      });
    });
    list.addEventListener('pointerleave', () => { on = false; fl.classList.remove('is-on'); });
    $$('.svc-wa', list).forEach(a => {
      a.addEventListener('pointerenter', () => fl.classList.remove('is-on'));
      a.addEventListener('pointerleave', () => { if (on) fl.classList.add('is-on'); });
    });
    addEventListener('pointermove', e => { mx = e.clientX; my = e.clientY; }, { passive: true });
    const loop = () => {
      const dx = mx - x;
      x = lerp(x, mx, .14); y = lerp(y, my, .14);
      fl.style.left = x + 'px'; fl.style.top = y + 'px';
      fl.style.setProperty('--rot', clamp(dx * .05, -10, 10).toFixed(2) + 'deg');
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---------- Proceso: recorrido horizontal mientras bajas ---------- */
  const pin = $('[data-pin]');
  let pinActive = false;
  const pinTrack = pin && $('[data-pin-track]', pin), pinBar = pin && $('.pin-progress', pin);
  const sizePin = () => {
    if (!pin) return;
    pinActive = innerWidth > 900 && !reduce;
    if (!pinActive) { pin.style.height = ''; pinTrack.style.transform = ''; return; }
    pin.style.height = (pinTrack.scrollWidth - pinTrack.parentElement.clientWidth + innerHeight) + 'px';
  };
  sizePin();
  addEventListener('resize', sizePin);
  addEventListener('load', sizePin);

  /* ---------- Parallax de imágenes ---------- */
  const para = $$('[data-parallax]');
  const heroMedia = $('[data-parallax-hero]');
  const footWord = $('.footer-word');

  /* Bucle de scroll compartido */
  const frame = () => {
    const vh = innerHeight;
    if (pinActive) {
      const dist = pinTrack.scrollWidth - pinTrack.parentElement.clientWidth;
      const p = clamp((scrollY - pin.offsetTop) / (pin.offsetHeight - vh), 0, 1);
      pinTrack.style.transform = `translate3d(${(-p * dist).toFixed(1)}px,0,0)`;
      pinBar.style.setProperty('--pp', p.toFixed(4));
    }
    if (!reduce) {
      para.forEach(el => {
        const r = el.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        const k = (r.top + r.height / 2 - vh / 2) / vh;
        el.style.transform = `translate3d(0,${(k * -9).toFixed(2)}%,0)`;
      });
      if (heroMedia) heroMedia.style.transform = `translate3d(0,${(scrollY * .25).toFixed(1)}px,0)`;
      if (scrubWords.length) {
        const r = scrub.getBoundingClientRect();
        const p = clamp((vh * .85 - r.top) / (r.height + vh * .35), 0, 1);
        const n = Math.round(p * scrubWords.length);
        scrubWords.forEach((w, i) => w.classList.toggle('on', i < n));
      }
      if (footWord) {
        const left = document.documentElement.scrollHeight - (scrollY + vh);
        footWord.style.setProperty('--fw', (clamp(1 - left / 700, 0, 1) * 100).toFixed(1) + '%');
      }
    }
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  /* ---------- Petición a medida por WhatsApp ---------- */
  $$('[data-builder]').forEach(form => {
    const section = form.closest('.builder');
    const out = $('[data-preview-msg]', section), hint = $('[data-preview-hint]', section);
    const send = $('[data-builder-send]', section), copy = $('[data-builder-copy]', section), status = $('[data-builder-status]', section);
    const service = form.dataset.service;
    const val = n => (form.elements[n] && form.elements[n].value || '').trim();
    const checked = n => $$(`input[name="${n}"]:checked`, form).map(i => i.value);
    const compose = () => {
      const svc = service ? [service] : checked('svc');
      const job = checked('job'), space = checked('space')[0], when = checked('when')[0];
      const name = val('name'), zone = val('zone'), notes = val('notes');
      const any = svc.length && !service || job.length || space || when || name || zone || notes;
      if (!any) return '';
      const L = [`Hola, Reformarvel 👋`];
      L.push(svc.length ? `Me gustaría pedir presupuesto de *${svc.join(', ').toLowerCase()}*.` : 'Me gustaría pedir presupuesto para una reforma.');
      L.push('');
      if (job.length) L.push(`🔧 *Trabajo:* ${job.join(', ')}`);
      if (space) L.push(`🏠 *Inmueble:* ${space}`);
      if (when) L.push(`📅 *Plazo:* ${when}`);
      if (zone) L.push(`📍 *Zona:* ${zone}`);
      if (notes) L.push(`📝 *Detalles:* ${notes}`);
      L.push('');
      L.push(name ? `Me llamo ${name}. Si os sirve, os envío fotos por aquí.` : 'Si os sirve, os envío fotos por aquí.');
      return L.join('\n').replace(/\n{3,}/g, '\n\n');
    };
    const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
    const fmt = s => esc(s).replace(/\*([^*\n]+)\*/g, '<b>$1</b>');
    let shown = '', typeT = null;
    const render = (text, caret) => { out.innerHTML = fmt(text) + (caret ? '<span class="caret"></span>' : ''); const chat = out.parentElement; chat.scrollTop = chat.scrollHeight; };
    const update = () => {
      const msg = compose();
      const fallback = waText(service.toLowerCase());
      send.href = waUrl(msg || fallback);
      hint.hidden = !!msg;
      clearInterval(typeT);
      if (reduce || !msg) { shown = msg; render(msg, false); return; }
      let k = 0; while (k < shown.length && k < msg.length && shown[k] === msg[k]) k++;
      let pos = k;
      const step = Math.max(1, Math.ceil((msg.length - k) / 40));
      typeT = setInterval(() => {
        pos = Math.min(msg.length, pos + step);
        shown = msg.slice(0, pos);
        render(shown, pos < msg.length);
        if (pos >= msg.length) clearInterval(typeT);
      }, 16);
    };
    form.addEventListener('change', e => {
      const chip = e.target.closest('.chip');
      if (chip) { chip.classList.remove('pop'); void chip.offsetWidth; chip.classList.add('pop'); }
      $$('.chip', form).forEach(c => c.classList.toggle('is-on', $('input', c).checked));
      update();
    });
    let inT;
    form.addEventListener('input', e => { if (e.target.matches('input[type=text], input:not([type]), textarea')) { clearTimeout(inT); inT = setTimeout(update, 250); } });
    // Las opciones de radio se pueden desmarcar con un segundo toque
    $$('input[type=radio]', form).forEach(r => {
      r.addEventListener('pointerdown', () => { r.dataset.was = r.checked; });
      r.addEventListener('click', () => { if (r.dataset.was === 'true') { r.checked = false; form.dispatchEvent(new Event('change')); } });
    });
    form.addEventListener('submit', e => e.preventDefault());
    copy.addEventListener('click', async () => {
      const msg = compose() || waText(service.toLowerCase());
      try { await navigator.clipboard.writeText(msg); status.textContent = 'Mensaje copiado. Pégalo en WhatsApp al ' + '652 465 019.'; }
      catch (_) { status.textContent = 'No se ha podido copiar automáticamente. Usa el botón de WhatsApp.'; }
    });
    update();
  });

  /* ---------- Comparadores antes / después ---------- */
  $$('[data-ba]').forEach(stage => {
    const range = $('.ba-range', stage);
    const set = v => { v = clamp(v, 0, 100); stage.style.setProperty('--pos', v + '%'); range.value = Math.round(v); };
    const fromEvent = e => { const r = stage.getBoundingClientRect(); return (e.clientX - r.left) / r.width * 100; };
    let drag = false;
    stage.addEventListener('pointerdown', e => {
      drag = true; stage.classList.add('is-drag'); stage.setPointerCapture(e.pointerId); set(fromEvent(e));
      if (anim) anim = null;
    });
    stage.addEventListener('pointermove', e => { if (drag) set(fromEvent(e)); });
    const end = () => { drag = false; stage.classList.remove('is-drag'); };
    stage.addEventListener('pointerup', end);
    stage.addEventListener('pointercancel', end);
    range.addEventListener('input', () => set(+range.value));
    // Pequeño vaivén la primera vez que aparece, para enseñar que se puede arrastrar
    let anim = null;
    if (!reduce) new IntersectionObserver((en, o) => {
      if (!en[0].isIntersecting) return; o.disconnect();
      const t0 = performance.now(); anim = true;
      const tick = t => {
        if (!anim) return;
        const k = Math.min((t - t0) / 1800, 1);
        set(50 + Math.sin(k * Math.PI * 2) * 22 * (1 - k));
        if (k < 1) requestAnimationFrame(tick); else anim = null;
      };
      setTimeout(() => requestAnimationFrame(tick), 500);
    }, { threshold: .6 }).observe(stage);
  });
  $$('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
    const f = btn.dataset.filter;
    $$('[data-filter]').forEach(b => { b.classList.toggle('is-on', b === btn); b.setAttribute('aria-pressed', b === btn); });
    $$('.ba-grid .ba').forEach(ba => ba.classList.toggle('is-hidden', f !== 'todos' && ba.dataset.cat !== f));
  }));

  /* ---------- Galería con visor ---------- */
  const box = $('[data-lightbox-box]');
  const items = $$('[data-lightbox]');
  let lbI = 0, lbReturn = null;
  const lbShow = i => {
    lbI = (i + items.length) % items.length;
    const img = $('img', items[lbI]);
    const big = $('img', box);
    big.src = img.currentSrc || img.src; big.alt = img.alt;
    big.style.animation = 'none'; void big.offsetWidth; big.style.animation = '';
    $('figcaption', box).textContent = $('figcaption', items[lbI]).textContent;
  };
  function closeLightbox() { if (!box || box.hidden) return; box.hidden = true; lock(false); if (lbReturn) lbReturn.focus(); }
  if (box) {
    items.forEach((it, i) => {
      it.tabIndex = 0; it.setAttribute('role', 'button');
      const open = () => { lbReturn = it; box.hidden = false; lbShow(i); lock(true); $('.lb-close', box).focus(); };
      it.addEventListener('click', open);
      it.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
    $('.lb-close', box).addEventListener('click', closeLightbox);
    $('.lb-prev', box).addEventListener('click', () => lbShow(lbI - 1));
    $('.lb-next', box).addEventListener('click', () => lbShow(lbI + 1));
    box.addEventListener('click', e => { if (e.target === box) closeLightbox(); });
    addEventListener('keydown', e => { if (box.hidden) return; if (e.key === 'ArrowRight') lbShow(lbI + 1); if (e.key === 'ArrowLeft') lbShow(lbI - 1); });
  }

  /* ---------- Preguntas: una abierta a la vez ---------- */
  $$('.faq-item').forEach(d => d.addEventListener('toggle', () => { if (d.open) $$('.faq-item').forEach(o => { if (o !== d) o.open = false; }); }));

  if (reduce) return;

  /* ---------- Onomatopeyas de cómic al pulsar ---------- */
  const SFX = ['¡ZAS!', '¡PAM!', '¡BAM!', '¡TOC!', '¡CRAC!', '¡ZUM!', '¡CLAC!'];
  const burst = '<svg class="burst" viewBox="0 0 200 200" aria-hidden="true"><path d="M100 4l14 40 36-24-8 42 44-4-32 30 40 22-44 8 22 38-40-18-6 44-26-36-26 36-6-44-40 18 22-38-44-8 40-22-32-30 44 4-8-42 36 24z"/></svg>';
  let lastPow = 0;
  document.addEventListener('pointerdown', e => {
    if (!e.target.closest('.btn, .chip, .svc-wa, .round, .villain, .badge, .hero-dot') || performance.now() - lastPow < 250) return;
    lastPow = performance.now();
    const el = document.createElement('span');
    el.className = 'pow'; el.setAttribute('aria-hidden', 'true');
    el.innerHTML = burst + `<b>${SFX[Math.floor(Math.random() * SFX.length)]}</b>`;
    el.style.left = e.clientX + 'px'; el.style.top = e.clientY + 'px';
    body.append(el);
    const r = (Math.random() * 30 - 15).toFixed(0);
    el.animate([
      { transform: `translate(0,0) scale(.2) rotate(${r - 20}deg)`, opacity: 0 },
      { transform: `translate(14px,-40px) scale(1.05) rotate(${r}deg)`, opacity: 1, offset: .3 },
      { transform: `translate(22px,-70px) scale(.9) rotate(${+r + 6}deg)`, opacity: 0 }
    ], { duration: 820, easing: 'cubic-bezier(.2,.8,.2,1)' }).onfinish = () => el.remove();
  });

  /* ---------- Chispas de obra en la llamada final ---------- */
  $$('[data-sparks]').forEach(sec => {
    const c = $('.sparks', sec), ctx = c.getContext('2d');
    let w, h, parts = [], visible = false, running = false, pointer = null;
    const size = () => { const dpr = Math.min(devicePixelRatio || 1, 1.5); w = sec.offsetWidth; h = sec.offsetHeight; c.width = w * dpr; c.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    const make = (x, y, burst) => ({ x: x ?? Math.random() * w, y: y ?? h + 10, vx: (Math.random() - .5) * (burst ? 260 : 30), vy: -(burst ? 80 + Math.random() * 260 : 30 + Math.random() * 70), life: 0, max: burst ? .6 + Math.random() * .7 : 3 + Math.random() * 4, r: .6 + Math.random() * 1.8, hue: 8 + Math.random() * 32 });
    size();
    for (let i = 0; i < (innerWidth < 700 ? 40 : 90); i++) { const p = make(); p.y = Math.random() * h; parts.push(p); }
    addEventListener('resize', size);
    sec.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); pointer = { x: e.clientX - r.left, y: e.clientY - r.top }; });
    sec.addEventListener('pointerleave', () => { pointer = null; });
    sec.addEventListener('pointerdown', e => { const r = c.getBoundingClientRect(); for (let i = 0; i < 26; i++) parts.push(make(e.clientX - r.left, e.clientY - r.top, true)); });
    let last = performance.now();
    const loop = t => {
      const dt = Math.min((t - last) / 1000, .05); last = t;
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'lighter';
      for (let i = parts.length - 1; i >= 0; i--) {
        const p = parts[i];
        p.life += dt;
        if (pointer) { const dx = p.x - pointer.x, dy = p.y - pointer.y, d = Math.hypot(dx, dy); if (d < 120 && d > .1) { p.vx += dx / d * 300 * dt; p.vy += dy / d * 200 * dt; } }
        p.vx *= .985; p.vy += (p.max < 2 ? 220 : -6) * dt;
        p.x += p.vx * dt + Math.sin(t / 600 + i) * .2; p.y += p.vy * dt;
        const a = Math.max(0, 1 - p.life / p.max);
        if (a <= 0 || p.y < -20) { if (p.max < 2) parts.splice(i, 1); else parts[i] = make(); continue; }
        ctx.fillStyle = `hsla(${p.hue},100%,${55 + a * 20}%,${a})`;
        ctx.shadowBlur = 0;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r * (0.6 + a * .6), 0, Math.PI * 2); ctx.fill();
      }
      ctx.globalCompositeOperation = 'source-over';
      if (visible && !document.hidden) requestAnimationFrame(loop); else running = false;
    };
    new IntersectionObserver(en => { visible = en[0].isIntersecting; if (visible && !running) { running = true; last = performance.now(); requestAnimationFrame(loop); } }).observe(sec);
  });

  if (!fine) return;

  /* ---------- Cursor ---------- */
  const cursor = $('.cursor');
  root.classList.add('has-cursor');
  cursor.classList.add('is-hidden');
  const dot = $('.cursor-dot', cursor), ring = $('.cursor-ring', cursor), label = $('.cursor-label', cursor);
  let cx = innerWidth / 2, cy = innerHeight / 2, rx = cx, ry = cy;
  addEventListener('pointermove', e => { cx = e.clientX; cy = e.clientY; cursor.classList.remove('is-hidden'); }, { passive: true });
  document.addEventListener('pointerleave', () => cursor.classList.add('is-hidden'));
  const cloop = () => {
    rx = lerp(rx, cx, .2); ry = lerp(ry, cy, .2);
    dot.style.transform = `translate(${cx}px,${cy}px)`;
    ring.style.transform = `translate(${rx}px,${ry}px)`;
    requestAnimationFrame(cloop);
  };
  requestAnimationFrame(cloop);
  document.addEventListener('pointerover', e => {
    const t = e.target;
    const lab = t.closest('[data-cursor]');
    const wa = t.closest('a[href*="wa.me"]');
    const drag = t.closest('[data-hero]') && !t.closest('a,button');
    const zoom = t.closest('[data-lightbox]');
    const text = lab ? lab.dataset.cursor : zoom ? 'Abrir' : drag ? 'Arrastra' : '';
    label.textContent = text;
    cursor.classList.toggle('is-label', !!text);
    cursor.classList.toggle('is-wa', !!wa && !text);
    cursor.classList.toggle('is-link', !text && !!t.closest('a, button, label, summary, input, textarea'));
  });

  /* ---------- Botones magnéticos ---------- */
  $$('.magnetic').forEach(el => {
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      el.style.transform = `translate(${((e.clientX - r.left - r.width / 2) * .2).toFixed(1)}px,${((e.clientY - r.top - r.height / 2) * .3).toFixed(1)}px)`;
    });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  });

  /* ---------- Inclinación 3D con reflejo ---------- */
  $$('.tilt').forEach(el => {
    const glare = document.createElement('span'); glare.className = 'glare'; glare.setAttribute('aria-hidden', 'true'); el.append(glare);
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      el.classList.add('tilting');
      el.style.setProperty('--rx', ((.5 - py) * 8).toFixed(2) + 'deg');
      el.style.setProperty('--ry', ((px - .5) * 10).toFixed(2) + 'deg');
      el.style.setProperty('--gx', (px * 100).toFixed(1) + '%');
      el.style.setProperty('--gy', (py * 100).toFixed(1) + '%');
    });
    el.addEventListener('pointerleave', () => { el.classList.remove('tilting'); el.style.setProperty('--rx', '0deg'); el.style.setProperty('--ry', '0deg'); });
  });
})();
