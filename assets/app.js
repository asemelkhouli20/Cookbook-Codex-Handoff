"use strict";
const root = document.documentElement;
const motion = root.classList.contains('motion');
const toArabicDigits = value => String(value).replace(/\d/g, digit => '٠١٢٣٤٥٦٧٨٩'[digit]);
const $ = (selector, scope = document) => scope.querySelector(selector);
const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
const storage = {
  get(key) { try { return sessionStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { sessionStorage.setItem(key, value); } catch {} },
};
const setSky = sky => {
  if (root.dataset.sky === sky) return;
  root.dataset.sky = sky;
  const meta = $('meta[name=theme-color]');
  const hex = { morning: '#FFD971', noon: '#A9DDF3', sunset: '#FFA472', dusk: '#BFA2F0', night: '#15193F' }[sky];
  if (meta && hex) meta.content = hex;
};
// Slide a pill-shaped thumb behind the active item. Physical pixels, since transforms ignore dir.
const placeThumb = (thumb, parent, item) => {
  if (!item) { thumb.style.setProperty('--o', 0); return; }
  const parentBox = parent.getBoundingClientRect();
  const box = item.getBoundingClientRect();
  thumb.style.setProperty('--x', `${box.left - parentBox.left}px`);
  thumb.style.setProperty('--w', `${box.width}px`);
  thumb.style.setProperty('--o', 1);
};
// Replace the picture in a box with a wipe that travels in reading direction.
const showImage = (box, src, alt, direction = 1) => {
  const token = (box.dataset.token = String(Number(box.dataset.token || 0) + 1));
  const image = new Image();
  image.src = src;
  image.alt = alt;
  const reveal = () => {
    if (box.dataset.token !== token) return;
    const previous = $$('img', box);
    box.append(image);
    const clear = () => previous.forEach(old => old.remove());
    if (!motion || !previous.length) { clear(); return; }
    image.animate({ clipPath: [direction > 0 ? 'inset(0 0 0 100%)' : 'inset(0 100% 0 0)', 'inset(0 0 0 0)'] }, { duration: 560, easing: 'cubic-bezier(.7,0,.2,1)' }).finished.then(clear, clear);
  };
  image.decode().then(reveal, reveal);
};

/* ---------- Things appear as they reach the screen ---------- */
if (motion) {
  // On wide screens step pictures stay hidden, so they simply never fire.
  const appearing = [
    ['.catalog-head h2', 'dough'], ['.catalog-head>div', 'rise'], ['.day-rail', 'rise'],
    ['.chapter-time', 'rise'], ['.chapter-title p', 'rise'], ['.chapter-art', 'open'], ['.tile', 'tile'],
    ['.kitchen-invite>div', 'rise'], ['.invite-art', 'open'],
    ['.floater:not(.hero .floater,.kitchen-intro .floater,.recipe-top .floater)', 'pop'],
    ['.nutrient', 'rise'], ['.nutrition .tools', 'rise'], ['.ingredients', 'rise'], ['.ingredients tbody tr', 'row'], ['.note', 'rise'],
    ['.cooking-heading h2', 'dough'], ['.cooking-heading p', 'rise'], ['.cooking-heading .btn', 'pop'],
    ['.step img', 'open'], ['.caption', 'rise'], ['.recipe-actions', 'rise'], ['.recipe-pagination a', 'rise'],
    ['.guide-head img', 'pop'], ['.guide h2', 'rise'], ['.guide-sub', 'rise'], ['.guide-tags span', 'pop'], ['.guide li', 'rise'],
    ['#storage-section>h2', 'dough'], ['.storage-notes p', 'rise'], ['.day-picker', 'rise'], ['.legend', 'rise'], ['#storage-section h3', 'rise'], ['.storage-wrap', 'rise'], ['.storage-foot', 'rise'],
    ['.footer-copy', 'rise'], ['.footer-chef', 'peek'],
  ];
  appearing.forEach(([selector, kind]) => $$(selector).forEach(node => { node.dataset.r = kind; }));
  // Whatever arrives together lands one after another, in reading order.
  const arrive = new IntersectionObserver(entries => {
    const arriving = entries.filter(entry => entry.isIntersecting);
    arriving.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top || b.boundingClientRect.left - a.boundingClientRect.left);
    arriving.forEach((entry, index) => {
      entry.target.style.setProperty('--d', `${Math.min(index, 8) * 70}ms`);
      entry.target.classList.add('seen');
      arrive.unobserve(entry.target);
    });
    // Already scrolled past (a deep link, or coming back): no need to replay it.
    entries.forEach(entry => {
      if (!entry.isIntersecting && entry.boundingClientRect.bottom < 0) {
        entry.target.classList.add('seen', 'instant');
        arrive.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  $$('[data-r]').forEach(node => arrive.observe(node));
}

/* ---------- Floating cutouts: depth on scroll, shy of the cursor, and they can be flung ---------- */
if (motion) {
  const floats = $$('.floater').map(element => ({ element, depth: Number(element.dataset.depth), x: 0, y: 0, vx: 0, vy: 0, held: false, moved: 0, visible: false }));
  let pointerX = -9999;
  let pointerY = -9999;
  let running = false;
  addEventListener('pointermove', event => { pointerX = event.clientX; pointerY = event.clientY; }, { passive: true });
  const animate = () => {
    const showing = floats.filter(float => float.visible);
    if (!showing.length) { running = false; return; }
    showing.forEach(float => {
      const box = float.element.getBoundingClientRect();
      const homeX = box.left + box.width / 2 - float.x;
      const homeY = box.top + box.height / 2 - float.y;
      let targetX = 0;
      let targetY = (innerHeight / 2 - homeY) * float.depth;
      if (float.held) {
        targetX = pointerX - homeX;
        targetY = pointerY - homeY;
      } else {
        const dx = homeX + targetX - pointerX;
        const dy = homeY + targetY - pointerY;
        const distance = Math.hypot(dx, dy) || 1;
        const reach = box.width * .5 + 130;
        if (distance < reach) {
          const push = (1 - distance / reach) ** 2 * 70;
          targetX += dx / distance * push;
          targetY += dy / distance * push;
        }
      }
      // A soft spring, so it overshoots and settles instead of following rigidly.
      const pull = float.held ? .22 : .05;
      float.vx = (float.vx + (targetX - float.x) * pull) * .86;
      float.vy = (float.vy + (targetY - float.y) * pull) * .86;
      float.x += float.vx;
      float.y += float.vy;
      float.element.style.translate = `${float.x.toFixed(1)}px ${float.y.toFixed(1)}px`;
      float.element.style.rotate = `${Math.max(-30, Math.min(30, float.vx * 1.5)).toFixed(1)}deg`;
    });
    requestAnimationFrame(animate);
  };
  const seen = new IntersectionObserver(entries => {
    entries.forEach(entry => { floats.find(float => float.element === entry.target).visible = entry.isIntersecting; });
    if (!running && floats.some(float => float.visible)) { running = true; requestAnimationFrame(animate); }
  }, { rootMargin: '25% 0px' });
  floats.forEach(float => {
    seen.observe(float.element);
    const picture = $('img', float.element);
    picture.addEventListener('dragstart', event => event.preventDefault());
    picture.addEventListener('pointerdown', event => {
      event.preventDefault();
      picture.setPointerCapture(event.pointerId);
      float.held = true;
      float.moved = 0;
      float.element.classList.add('dragging');
    });
    picture.addEventListener('pointermove', event => { if (float.held) float.moved += Math.abs(event.movementX) + Math.abs(event.movementY); });
    const letGo = () => {
      if (!float.held) return;
      float.held = false;
      float.element.classList.remove('dragging');
      // A plain click gets a little hop and a spin.
      if (float.moved < 6) {
        float.vy -= 22;
        float.element.animate({ rotate: ['0deg', '360deg'] }, { duration: 800, easing: 'cubic-bezier(.2,.9,.3,1)', composite: 'add' });
      }
    };
    picture.addEventListener('pointerup', letGo);
    picture.addEventListener('pointercancel', letGo);
  });
}

/* ---------- Home: the day dial ---------- */
const dial = $('[data-dial]');
let dialSky = 'morning';
if (dial) {
  const stops = $$('.stop', dial);
  const pictures = $$('.window img', dial);
  const sun = $('.sun', dial);
  const stage = $('.scene-stage', dial);
  const cta = $('[data-dial-cta]');
  const ctaLabel = $('[data-dial-cta-label]');
  const angleOf = k => 70 - k * 35;
  let current = 0;
  const select = (k, { moveSun = true, updateSky = true } = {}) => {
    current = k;
    const stop = stops[k];
    stops.forEach((other, index) => other.setAttribute('aria-pressed', String(index === k)));
    pictures.forEach((picture, index) => picture.classList.toggle('on', index === k));
    if (moveSun) sun.style.setProperty('--a', `${angleOf(k)}deg`);
    $('[data-dial-name]').textContent = stop.dataset.name;
    $('[data-dial-time]').textContent = `${stop.dataset.time}، ${stop.dataset.count}`;
    $('[data-dial-note]').textContent = stop.dataset.note;
    cta.href = `#chapter-${k}`;
    ctaLabel.textContent = stop.dataset.cta;
    dialSky = stop.dataset.sky;
    if (updateSky && window.scrollY < innerHeight * .6) setSky(dialSky);
  };
  stops.forEach((stop, k) => stop.addEventListener('click', () => select(k)));
  $$('.tick', dial).forEach(tick => tick.addEventListener('click', () => select(Number(tick.dataset.k))));
  // Drag the sun along its arc; it follows the finger and settles on the nearest meal.
  const nearest = event => {
    const box = stage.getBoundingClientRect();
    const dx = event.clientX - (box.left + box.width / 2);
    const dy = event.clientY - (box.top + box.width / 2);
    const angle = Math.max(-70, Math.min(70, Math.atan2(dx, -dy) * 180 / Math.PI));
    return { angle, k: Math.round((70 - angle) / 35) };
  };
  sun.addEventListener('pointerdown', event => {
    sun.setPointerCapture(event.pointerId);
    sun.classList.add('dragging');
  });
  sun.addEventListener('pointermove', event => {
    if (!sun.classList.contains('dragging')) return;
    const { angle, k } = nearest(event);
    sun.style.setProperty('--a', `${angle}deg`);
    if (k !== current) select(k, { moveSun: false });
  });
  const release = () => {
    if (!sun.classList.contains('dragging')) return;
    sun.classList.remove('dragging');
    select(current);
  };
  sun.addEventListener('pointerup', release);
  sun.addEventListener('pointercancel', release);
  // On load the sun climbs to the visitor's own hour, once per visit.
  const hour = new Date().getHours();
  const now = hour < 5 ? 4 : hour < 11 ? 0 : hour < 17 ? 1 : hour < 20 ? 2 : hour < 21 ? 3 : 4;
  const atTop = window.scrollY < 40 && !location.hash;
  if (motion && atTop && !storage.get('dial-played')) {
    storage.set('dial-played', '1');
    select(0);
    setTimeout(() => select(now), 900);
  } else select(now);
}

/* ---------- Home: sky follows the chapter you're reading ---------- */
const skyChapters = $$('.chapter[data-sky]');
if (skyChapters.length) {
  let scheduled = false;
  const rail = $('.day-rail');
  const railLinks = $$('a', rail);
  const thumb = $('.rail-thumb', rail);
  let active = -2;
  const followThumb = () => {
    // Labels change width while animating on phones, so track the item until they settle.
    const started = performance.now();
    const step = () => {
      placeThumb(thumb, rail, railLinks[active]);
      if (performance.now() - started < 450) requestAnimationFrame(step);
    };
    step();
  };
  const update = () => {
    scheduled = false;
    const line = innerHeight * .55;
    let current = -1;
    skyChapters.forEach((chapter, index) => { if (chapter.getBoundingClientRect().top <= line) current = index; });
    if (current === active) return;
    active = current;
    setSky(current < 0 ? dialSky : skyChapters[current].dataset.sky);
    railLinks.forEach((link, index) => {
      if (index === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    followThumb();
  };
  const schedule = () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', () => { followThumb(); schedule(); });
  addEventListener('pageshow', schedule);
  document.fonts.ready.then(followThumb);
  update();

  // A chapter's title rises the first time it arrives.
  if (motion) {
    const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('in'); reveal.unobserve(entry.target); }
    }), { rootMargin: '0px 0px -12% 0px' });
    skyChapters.forEach(chapter => reveal.observe(chapter));
  }
}

/* ---------- Home: hovering a tile flips through the recipe's steps ---------- */
if (motion && matchMedia('(hover: hover)').matches) $$('.tile').forEach(tile => {
  const frames = tile.dataset.steps.split('|');
  const art = $('.tile-art', tile);
  let wait, timer, flip, bar;
  tile.addEventListener('pointerenter', () => {
    wait = setTimeout(() => {
      let index = 0;
      flip = new Image();
      flip.className = 'flip';
      flip.alt = '';
      bar = document.createElement('span');
      bar.className = 'tile-flipbar';
      bar.innerHTML = '<i></i>';
      const show = () => {
        const next = new Image();
        const frame = index;
        next.src = frames[frame];
        next.decode().then(() => {
          if (!flip) return;
          flip.src = next.src;
          if (!flip.isConnected) art.insertBefore(flip, art.children[1]);
          if (!bar.isConnected) art.append(bar);
          bar.style.setProperty('--p', `${(frame + 1) / frames.length * 100}%`);
        }, () => {});
        index = (index + 1) % frames.length;
      };
      show();
      timer = setInterval(show, 750);
    }, 260);
  });
  tile.addEventListener('pointerleave', () => {
    clearTimeout(wait);
    clearInterval(timer);
    if (flip) flip.remove();
    if (bar) bar.remove();
    flip = bar = null;
  });
});

/* ---------- Home: find by ingredient, and surprise me ---------- */
const tiles = $$('.tile');
if (tiles.length) {
  const fold = text => text.normalize('NFC').replace(/[ً-ْ]/g, '').replace(/[أإآ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي').toLowerCase();
  const recipes = tiles.map(tile => ({
    href: tile.getAttribute('href'),
    image: $('.tile-art img', tile).getAttribute('src'),
    title: $('.tile-art img', tile).alt,
    time: $('.tile-copy p', tile).textContent,
    ingredients: tile.dataset.q,
    haystack: fold(`${$('.tile-art img', tile).alt} ${tile.dataset.q}`),
  }));

  const finder = document.createElement('dialog');
  finder.className = 'finder';
  finder.setAttribute('aria-label', 'ابحث عن وصفة');
  finder.innerHTML = `<div class="finder-bar"><input type="search" dir="auto" placeholder="وش عندك في الثلاجة؟ موز، دجاج، تونة…" aria-label="ابحث باسم وصفة أو مكوّن"><button type="button" class="icon-btn" aria-label="إغلاق">×</button></div><div class="finder-chips"></div><ul class="finder-results"></ul><p class="finder-empty" hidden>ما لقينا وصفة بهذا الاسم. جرّب مكوّنًا ثانيًا مثل الأرز أو الموز.</p>`;
  document.body.append(finder);
  const input = $('input', finder);
  const results = $('.finder-results', finder);
  const empty = $('.finder-empty', finder);
  const chips = $('.finder-chips', finder);
  ['موز', 'شوفان', 'دجاج', 'تونة', 'حمّص', 'فاصوليا', 'مكرونة', 'أرز'].forEach(word => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'chip';
    chip.textContent = word;
    chip.addEventListener('click', () => { input.value = word; render(); input.focus(); });
    chips.append(chip);
  });
  let selected = 0;
  const render = () => {
    const query = fold(input.value.trim());
    const matches = query ? recipes.filter(recipe => query.split(/\s+/).every(word => recipe.haystack.includes(word))) : [];
    selected = 0;
    results.innerHTML = '';
    matches.forEach((recipe, index) => {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = recipe.href;
      if (index === 0) link.className = 'active';
      const image = new Image();
      image.src = recipe.image;
      image.alt = '';
      image.loading = 'lazy';
      const copy = document.createElement('span');
      const name = document.createElement('strong');
      name.textContent = recipe.title.replace(' • ', ': ');
      const time = document.createElement('small');
      time.textContent = recipe.time;
      copy.append(name, time);
      link.append(image, copy);
      item.append(link);
      results.append(item);
    });
    chips.hidden = Boolean(query);
    empty.hidden = !query || matches.length > 0;
  };
  input.addEventListener('input', render);
  input.addEventListener('keydown', event => {
    const links = $$('a', results);
    if (event.key === 'Enter' && links[selected]) { event.preventDefault(); links[selected].click(); return; }
    if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return;
    event.preventDefault();
    if (!links.length) return;
    links[selected].classList.remove('active');
    selected = (selected + (event.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
    links[selected].classList.add('active');
    links[selected].scrollIntoView({ block: 'nearest' });
  });
  const closeOnBackdrop = dialog => dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  closeOnBackdrop(finder);
  $('.icon-btn', finder).addEventListener('click', () => finder.close());
  $('[data-finder]').addEventListener('click', () => { finder.showModal(); input.focus(); });
  addEventListener('keydown', event => {
    if (event.key === '/' && !finder.open && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
      event.preventDefault();
      finder.showModal();
      input.focus();
    }
  });

  const surprise = document.createElement('dialog');
  surprise.className = 'surprise';
  surprise.setAttribute('aria-label', 'وصفة مفاجأة');
  surprise.innerHTML = `<div class="surprise-reel"></div><h2 aria-live="polite"></h2><div class="surprise-actions"><a class="btn" href="#">افتح الوصفة</a><button type="button" class="btn btn-quiet" data-again>غيرها</button><button type="button" class="btn btn-quiet" data-close>إغلاق</button></div>`;
  document.body.append(surprise);
  closeOnBackdrop(surprise);
  const reel = $('.surprise-reel', surprise);
  const heading = $('h2', surprise);
  const actions = $('.surprise-actions', surprise);
  const openLink = $('a', actions);
  const pick = list => list[Math.floor(Math.random() * list.length)];
  let run = 0;
  const spin = () => {
    const thisRun = ++run;
    const winner = pick(recipes);
    const land = () => {
      if (run !== thisRun) return;
      showImage(reel, winner.image, '');
      heading.textContent = winner.title.replace(' • ', ': ');
      openLink.href = winner.href;
      actions.hidden = false;
      if (surprise.open) openLink.focus();
      if (motion) reel.animate({ transform: ['scale(.92)', 'scale(1.03)', 'scale(1)'] }, { duration: 500, easing: 'ease-out' });
    };
    actions.hidden = true;
    heading.textContent = 'خلّنا نشوف…';
    if (!motion) { land(); return; }
    // The reel starts fast and slows down, like a wheel settling on its choice.
    let delay = 70;
    const frame = () => {
      if (run !== thisRun || !surprise.open) return;
      if (delay > 380) { land(); return; }
      reel.innerHTML = '';
      const image = new Image();
      image.src = pick(recipes).image;
      image.alt = '';
      reel.append(image);
      delay *= 1.17;
      setTimeout(frame, delay);
    };
    frame();
  };
  $('[data-surprise]').addEventListener('click', () => { surprise.showModal(); spin(); });
  $('[data-again]', surprise).addEventListener('click', spin);
  $('[data-close]', surprise).addEventListener('click', () => surprise.close());
}

/* ---------- Recipe: ingredients ---------- */
const ingredients = $('.ingredients');
if (ingredients) {
  const table = $('table', ingredients);
  const buttons = $$('.servings button', ingredients);
  const servingThumb = $('.servings-thumb', ingredients);
  const setServing = (index, animate = true) => {
    table.dataset.serving = index;
    buttons.forEach((button, k) => button.setAttribute('aria-pressed', String(k === index)));
    placeThumb(servingThumb, servingThumb.parentNode, buttons[index]);
    if (animate && motion) $$('td', table).forEach((cell, k) => {
      if (cell.offsetParent) cell.animate({ opacity: [0, 1], transform: ['translateY(.7em)', 'none'] }, { duration: 380, delay: k * 12, easing: 'cubic-bezier(.2,1.3,.4,1)', fill: 'backwards' });
    });
  };
  buttons.forEach((button, index) => button.addEventListener('click', () => {
    setServing(index);
    storage.set('serving', index);
  }));
  setServing(Number(storage.get('serving')) || 0, false);
  document.fonts.ready.then(() => placeThumb(servingThumb, servingThumb.parentNode, buttons[Number(table.dataset.serving)]));
  addEventListener('resize', () => placeThumb(servingThumb, servingThumb.parentNode, buttons[Number(table.dataset.serving)]));

  const checks = $$('.ingredient-check', ingredients);
  const meter = $('.ready-meter', ingredients);
  const note = $('.ready-note', ingredients);
  const updateReady = () => {
    const done = checks.filter(check => check.checked).length;
    meter.style.setProperty('--done', done / checks.length);
    if (!done) note.textContent = `${toArabicDigits(checks.length)} مكوّنات تجهّزها.`;
    else if (done < checks.length) note.textContent = `جهّزت ${toArabicDigits(done)} من ${toArabicDigits(checks.length)}.`;
    else note.textContent = 'كل شيء جاهز. يلا نطبخ!';
  };
  checks.forEach(check => check.addEventListener('change', updateReady));
  updateReady();
  // The whole row is a target: fingers in a kitchen aren't precise.
  $$('tbody tr', table).forEach(row => row.addEventListener('click', event => {
    if (event.target.closest('label')) return;
    const check = $('input', row);
    check.checked = !check.checked;
    check.dispatchEvent(new Event('change'));
  }));
}

/* ---------- Recipe: kitchen timer ---------- */
const clockText = seconds => toArabicDigits(`${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`);
const timerWidget = (() => {
  if (!$('[data-timer]')) return null;
  const widget = document.createElement('div');
  widget.className = 'timer';
  widget.hidden = true;
  widget.setAttribute('role', 'timer');
  widget.innerHTML = '<span></span><button type="button">إيقاف</button>';
  document.body.append(widget);
  const display = $('span', widget);
  const stopButton = $('button', widget);
  let interval, endsAt;
  const stop = () => { clearInterval(interval); widget.hidden = true; widget.classList.remove('ringing'); };
  const chime = () => {
    try {
      const audio = new AudioContext();
      [0, .28, .56].forEach(offset => {
        const tone = audio.createOscillator();
        const gain = audio.createGain();
        tone.frequency.value = 880;
        gain.gain.setValueAtTime(.18, audio.currentTime + offset);
        gain.gain.exponentialRampToValueAtTime(.001, audio.currentTime + offset + .24);
        tone.connect(gain).connect(audio.destination);
        tone.start(audio.currentTime + offset);
        tone.stop(audio.currentTime + offset + .25);
      });
    } catch {}
    if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
  };
  const tick = () => {
    const left = Math.max(0, Math.round((endsAt - Date.now()) / 1000));
    display.textContent = left ? clockText(left) : 'انتهى الوقت';
    if (!left) {
      clearInterval(interval);
      widget.classList.add('ringing');
      chime();
    }
  };
  stopButton.addEventListener('click', stop);
  return {
    start(seconds) {
      stop();
      endsAt = Date.now() + seconds * 1000;
      widget.hidden = false;
      tick();
      interval = setInterval(tick, 250);
    },
    moveTo(parent) { parent.append(widget); },
  };
})();
const timerChip = seconds => {
  const chip = document.createElement('button');
  chip.type = 'button';
  chip.className = 'timer-chip';
  chip.innerHTML = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="16" cy="16" r="12"/><path d="M16 9v7l5 3"/></svg>';
  chip.append(`شغّل مؤقت ${clockText(seconds)}`);
  chip.addEventListener('click', event => { event.stopPropagation(); timerWidget.start(seconds); });
  return chip;
};

/* ---------- Recipe: one picture stays, the steps scroll past ---------- */
const stepNodes = $$('.step');
if (stepNodes.length) {
  const stepData = stepNodes.map(node => {
    const image = $('img', node);
    return { image: image.getAttribute('src'), alt: image.alt, text: $('.caption p', node).textContent, timer: Number(node.dataset.timer) || 0 };
  });
  stepNodes.forEach((node, index) => {
    if (stepData[index].timer) $('.caption p', node).after(timerChip(stepData[index].timer));
  });
  $$('.caption', document).forEach(caption => {
    const chip = $('.timer-chip', caption);
    if (!chip) return;
    const wrap = document.createElement('div');
    $('p', caption).before(wrap);
    wrap.append($('p', caption), chip);
  });

  const stage = document.createElement('div');
  stage.className = 'stage';
  stage.innerHTML = '<div class="stage-pic"></div><div class="stage-ticks"></div>';
  const stageTicks = $('.stage-ticks', stage);
  const stagePic = $('.stage-pic', stage);
  stepNodes[0].parentNode.append(stage);
  let activeStep = -1;
  const centerStep = index => stepNodes[index].scrollIntoView({ block: 'center', behavior: motion ? 'smooth' : 'auto' });
  stepData.forEach((step, index) => {
    const tick = document.createElement('button');
    tick.type = 'button';
    tick.setAttribute('aria-label', `الخطوة ${toArabicDigits(index + 1)}`);
    tick.addEventListener('click', () => centerStep(index));
    stageTicks.append(tick);
  });
  const stageTickNodes = $$('button', stageTicks);
  const activate = index => {
    if (index === activeStep) return;
    const direction = index > activeStep ? 1 : -1;
    activeStep = index;
    stepNodes.forEach((node, k) => node.classList.toggle('active', k === index));
    stageTickNodes.forEach((tick, k) => tick.classList.toggle('done', k <= index));
    showImage(stagePic, stepData[index].image, stepData[index].alt, direction);
    const next = stepData[index + 1];
    if (next) new Image().src = next.image;
  };
  const wide = matchMedia('(min-width: 960px)');
  const watch = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting && wide.matches) activate(stepNodes.indexOf(entry.target));
  }), { rootMargin: '-48% 0px -48% 0px' });
  stepNodes.forEach(node => {
    watch.observe(node);
    node.addEventListener('click', () => { if (wide.matches) centerStep(stepNodes.indexOf(node)); });
  });
  if (wide.matches) activate(0);
  wide.addEventListener('change', () => { if (wide.matches && activeStep < 0) activate(0); });

  /* ---------- Recipe: cook mode ---------- */
  const cover = $('.hero-art');
  const next = $('[data-next]');
  const cook = document.createElement('dialog');
  cook.className = 'cook';
  cook.setAttribute('aria-label', 'وضع الطبخ');
  cook.innerHTML = `<div class="cook-bar"><button type="button" class="icon-btn" data-exit aria-label="إغلاق وضع الطبخ">×</button><div class="cook-dashes" aria-hidden="true">${stepData.map(() => '<i></i>').join('')}</div><button type="button" class="cook-tool" data-panel aria-expanded="false">المكوّنات</button></div><div class="cook-body"><div class="cook-text"><span class="cook-num"></span><div aria-live="polite"><p></p></div><div class="cook-timer"></div></div><div class="cook-pic"></div><div class="cook-end" hidden><img alt=""><h2>بالعافية!</h2><div class="cook-end-actions"></div></div><div class="cook-panel" hidden><h2>مكوّناتك</h2><ul></ul></div></div><div class="cook-nav"><button type="button" class="btn btn-quiet cook-prev"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M26 16H6M14 8l-8 8 8 8"/></svg>السابقة</button><button type="button" class="btn cook-next"><span>التالية</span><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M26 16H6M14 8l-8 8 8 8"/></svg></button></div>`;
  document.body.append(cook);
  const dashes = $$('.cook-dashes i', cook);
  const numeral = $('.cook-num', cook);
  const words = $('.cook-text p', cook);
  const wordsBox = $('.cook-text', cook);
  const picture = $('.cook-pic', cook);
  const timerSlot = $('.cook-timer', cook);
  const ending = $('.cook-end', cook);
  const panel = $('.cook-panel', cook);
  const panelToggle = $('[data-panel]', cook);
  const previousButton = $('.cook-prev', cook);
  const nextButton = $('.cook-next', cook);
  const nav = $('.cook-nav', cook);
  $('img', ending).src = cover.getAttribute('src');
  const endActions = $('.cook-end-actions', ending);
  if (next) {
    const link = document.createElement('a');
    link.className = 'btn';
    link.href = next.getAttribute('href');
    link.textContent = 'الوصفة التالية';
    endActions.append(link);
  }
  const closeButton = document.createElement('button');
  closeButton.type = 'button';
  closeButton.className = 'btn btn-quiet';
  closeButton.textContent = 'رجوع للوصفة';
  closeButton.addEventListener('click', () => cook.close());
  endActions.append(closeButton);
  let position = 0;
  let wakeLock = null;
  const celebrate = () => {
    if (!motion) return;
    const colors = ['var(--pop)', 'var(--ink)', 'var(--card)', '#F2C14E', '#2E8B65'];
    for (let k = 0; k < 40; k++) {
      const bit = document.createElement('span');
      bit.className = 'bit';
      bit.style.cssText = `left:50%;top:44%;background:${colors[k % colors.length]}`;
      cook.append(bit);
      const angle = Math.random() * Math.PI * 2;
      const reach = 120 + Math.random() * Math.min(innerWidth, innerHeight) * .5;
      bit.animate([
        { transform: 'translate(0,0) rotate(0) scale(1)', opacity: 1 },
        { transform: `translate(${Math.cos(angle) * reach}px,${Math.sin(angle) * reach + 80}px) rotate(${Math.random() * 720}deg) scale(.5)`, opacity: 0 },
      ], { duration: 900 + Math.random() * 700, easing: 'cubic-bezier(.1,.7,.3,1)' }).finished.then(() => bit.remove(), () => bit.remove());
    }
  };
  const renderCook = (index, direction = 1) => {
    position = index;
    const finished = index >= stepData.length;
    dashes.forEach((dash, k) => dash.classList.toggle('done', k <= index));
    ending.hidden = !finished;
    wordsBox.hidden = picture.hidden = finished;
    nav.hidden = finished;
    if (finished) { celebrate(); return; }
    const step = stepData[index];
    numeral.textContent = toArabicDigits(String(index + 1).padStart(2, '0'));
    words.textContent = step.text;
    timerSlot.replaceChildren();
    if (step.timer) timerSlot.append(timerChip(step.timer));
    showImage(picture, step.image, step.alt, direction);
    if (motion) wordsBox.animate({ opacity: [0, 1], transform: [`translateX(${direction * -36}px)`, 'none'] }, { duration: 420, easing: 'cubic-bezier(.2,.9,.3,1)' });
    previousButton.style.visibility = index ? 'visible' : 'hidden';
    $('span', nextButton).textContent = index === stepData.length - 1 ? 'انتهيت' : 'التالية';
    const upcoming = stepData[index + 1];
    if (upcoming) new Image().src = upcoming.image;
  };
  const go = delta => {
    const target = position + delta;
    if (target < 0 || target > stepData.length) return;
    renderCook(target, delta);
  };
  nextButton.addEventListener('click', () => go(1));
  previousButton.addEventListener('click', () => go(-1));
  $('[data-exit]', cook).addEventListener('click', () => cook.close());
  // In an Arabic book the next page sits to the left, so left is forward.
  cook.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); go(1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); go(-1); }
  });
  let touchStart = null;
  cook.addEventListener('touchstart', event => { touchStart = event.touches.length === 1 ? event.touches[0] : null; }, { passive: true });
  cook.addEventListener('touchend', event => {
    if (!touchStart) return;
    const dx = event.changedTouches[0].clientX - touchStart.clientX;
    const dy = event.changedTouches[0].clientY - touchStart.clientY;
    touchStart = null;
    if (Math.abs(dx) > 56 && Math.abs(dx) > Math.abs(dy) * 1.5) go(dx > 0 ? 1 : -1);
  }, { passive: true });
  panelToggle.addEventListener('click', () => {
    const open = panel.hidden;
    if (open) {
      const serving = Number($('.ingredients table').dataset.serving) || 0;
      const list = $('ul', panel);
      list.replaceChildren(...$$('.ingredients tbody tr').map(row => {
        const item = document.createElement('li');
        const name = document.createElement('span');
        name.textContent = $('label span', row).textContent;
        const amount = document.createElement('b');
        amount.textContent = `${$$('td', row)[serving].textContent} غ`;
        item.append(name, amount);
        return item;
      }));
    }
    panel.hidden = !open;
    panelToggle.setAttribute('aria-expanded', String(open));
  });
  // Keep the screen awake while cooking, where the browser allows it.
  const holdScreen = async () => {
    try { if ('wakeLock' in navigator && cook.open) wakeLock = await navigator.wakeLock.request('screen'); } catch {}
  };
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') holdScreen(); });
  cook.addEventListener('close', () => {
    if (wakeLock) wakeLock.release().catch(() => {});
    wakeLock = null;
    root.style.overflow = '';
    if (timerWidget) timerWidget.moveTo(document.body);
  });
  $$('[data-cook]').forEach(button => button.addEventListener('click', () => {
    panel.hidden = true;
    panelToggle.setAttribute('aria-expanded', 'false');
    cook.showModal();
    root.style.overflow = 'hidden';
    if (timerWidget) timerWidget.moveTo(cook);
    renderCook(0);
    nextButton.focus();
    holdScreen();
  }));
}

/* ---------- Kitchen: guide index and fridge day picker ---------- */
const guideIndex = $('.guide-index');
if (guideIndex) {
  const links = $$('a', guideIndex);
  const targets = links.map(link => $(link.hash));
  const mark = link => {
    links.forEach(other => { if (other === link) other.setAttribute('aria-current', 'location'); else other.removeAttribute('aria-current'); });
    // Only the phone layout scrolls sideways; keep the current chip in view without moving the page.
    const navBox = guideIndex.getBoundingClientRect();
    const box = link.getBoundingClientRect();
    guideIndex.scrollBy({ left: box.left + box.width / 2 - (navBox.left + navBox.width / 2), behavior: motion ? 'smooth' : 'auto' });
  };
  const spy = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) mark(links[targets.indexOf(entry.target)]);
  }), { rootMargin: '-30% 0px -65% 0px' });
  targets.forEach(target => spy.observe(target));
}
const dayInput = $('#storage-day');
if (dayInput) {
  const section = $('#storage-section');
  const label = $('[data-day-label]');
  const summary = $('[data-day-summary]');
  const reset = $('[data-day-reset]');
  const rows = $$('.storage tbody tr');
  const showDay = day => {
    section.dataset.day = day;
    reset.hidden = false;
    label.textContent = day ? `اليوم ${toArabicDigits(day)}` : 'يوم التحضير';
    const states = rows.map(row => $$('td', row)[day].dataset.state);
    const expired = states.filter(state => state === 'X').length;
    const good = states.filter(state => state === 'S').length;
    summary.textContent = `${toArabicDigits(good)} من ${toArabicDigits(rows.length)} بجودة جيدة، و${toArabicDigits(expired)} انتهت مدتها.`;
    // On phones the tables scroll sideways: bring the chosen day out from behind the sticky first column.
    $$('.storage-wrap').forEach(wrap => {
      const cells = $$('thead th', wrap);
      const frame = wrap.getBoundingClientRect();
      const cell = cells[day + 1].getBoundingClientRect();
      const clear = frame.width - cells[0].getBoundingClientRect().width;
      wrap.scrollBy({ left: cell.left + cell.width / 2 - (frame.left + clear / 2) });
    });
  };
  dayInput.addEventListener('input', () => showDay(Number(dayInput.value)));
  reset.addEventListener('click', () => {
    delete section.dataset.day;
    reset.hidden = true;
    summary.textContent = '';
    label.textContent = 'حرّك المؤشر';
    dayInput.value = 0;
  });
}

/* ---------- Printing waits for every image ---------- */
const printButton = $('[data-print]');
if (printButton) printButton.addEventListener('click', async () => {
  printButton.disabled = true;
  try {
    const images = [...document.images];
    images.forEach(image => { image.loading = 'eager'; });
    await Promise.all(images.map(image => image.decode().catch(() => {})));
    window.print();
  } finally { printButton.disabled = false; }
});
