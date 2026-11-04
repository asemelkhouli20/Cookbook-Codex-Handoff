"""Generate static, offline-ready Arabic cookbook pages. Run: python3 scripts/build.py."""
from pathlib import Path
from html import escape
import json
import re
from hashlib import sha256
ROOT = Path(__file__).resolve().parents[1]
style_version = sha256((ROOT/'assets/styles.css').read_bytes()).hexdigest()[:10]
script_version = sha256((ROOT/'assets/app.js').read_bytes()).hexdigest()[:10]
book = json.loads((ROOT / 'source/book.json').read_text())
chapters = ['الفطور', 'غداء العمل', 'استراحة السابعة', 'قبل التمرين', 'عشاء ما بعد التمرين']
short_names = ['الفطور', 'الغداء', 'الاستراحة', 'قبل التمرين', 'العشاء']
times = ['الصباح', '٣ عصرًا', '٧ مساءً', 'قبل النادي', 'بعد النادي']
# The book follows one day, so each chapter wears the sky of its hour (see DESIGN.md).
SKIES = ['morning', 'noon', 'sunset', 'dusk', 'night']
SKY_HEX = {'morning': '#FFD971', 'noon': '#A9DDF3', 'sunset': '#FFA472', 'dusk': '#BFA2F0', 'night': '#15193F'}
meal_icons = ['sun', 'lunch', 'cup', 'leaf', 'moon']
chapter_notes = ['صباح هادئ، وشيء لذيذ تبدأ به يومك.', 'خذ معك من البيت لقمة تسعدك وسط الزحمة.', 'استراحة صغيرة تستاهلها، ولقمة تردّ الروح.', 'شيء خفيف، وطاقة تكمل بها يومك.', 'انتهى يومك. حان وقت طبق دافئ وراحة.']
chapter_art = ['recipes/08/cover.png', 'site/work-lunch.png', 'site/evening-break.png', 'site/before-workout.png', 'site/dinner.png']
# site/breakfast.png is withheld, so the opening scene stands in for morning on the dial.
dial_art = ['site/home-hero.png', 'site/work-lunch.png', 'site/evening-break.png', 'site/before-workout.png', 'site/dinner.png']
# Missing or flagged artwork keeps its original illustration until a replacement is ready.
WITHHELD = {'site/breakfast.png', 'recipes/11/step-03.png', 'recipes/27/step-05.png'}
used_visuals = set()
def visual(relative, fallback=''):
    candidate = 'assets/web-visuals/' + str(Path(relative).with_suffix('.webp'))
    if relative not in WITHHELD and (ROOT/candidate).is_file():
        used_visuals.add(relative)
        return candidate
    return fallback
for recipe in book['recipes']:
    recipe['hero'] = visual(f'recipes/{recipe["id"]:02d}/cover.png', recipe['hero'])
    for number, step in enumerate(recipe['steps'], 1):
        step['img'] = visual(f'recipes/{recipe["id"]:02d}/step-{number:02d}.png', step['img'])
for number, guide in enumerate(book['guides'], 1):
    guide['img'] = visual(f'guides/guide-{number:02d}.png', guide['img'])
def e(value): return escape(str(value), quote=True)
def ar(value): return str(value).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
def recipe_count(count):
    if count == 1: return 'وصفة واحدة'
    if count == 2: return 'وصفتان'
    return f'{ar(count)} {"وصفات" if count <= 10 else "وصفة"}'
def image(src, alt, cls='', prefix='', eager=False, attrs=''):
    return f'<img src="{prefix}{e(src)}" alt="{e(alt)}" class="{cls}{" generated-art" if "web-visuals/" in src else ""}" loading="{"eager" if eager else "lazy"}" decoding="async"{attrs}>'
def icon(name='bowl'):
    paths = {
        'bowl': '<path d="M4 12h24c0 8-5 12-12 12S4 20 4 12Z"/><path d="M9 28h14M10 8c-3-3 3-3 0-6M16 8c-3-3 3-3 0-6M22 8c-3-3 3-3 0-6"/>',
        'sun': '<circle cx="16" cy="16" r="6"/><path d="M16 2v4M16 26v4M2 16h4M26 16h4M6 6l3 3M23 23l3 3M6 26l3-3M23 9l3-3"/>',
        'lunch': '<rect x="4" y="10" width="24" height="17" rx="4"/><path d="M11 10V6h10v4M4 17h24M13 17v4h6v-4"/>',
        'cup': '<path d="M5 12h17v9a7 7 0 0 1-7 7h-3a7 7 0 0 1-7-7ZM22 13h3a4 4 0 0 1 0 8h-3M9 7c-3-3 3-3 0-6M17 7c-3-3 3-3 0-6"/>',
        'leaf': '<path d="M26 4C8 3 2 14 8 23c9 6 20 0 18-19ZM7 27 22 11"/>',
        'moon': '<path d="M25 21A12 12 0 0 1 11 5a12 12 0 1 0 14 16ZM23 4v6M20 7h6"/>',
        'search': '<circle cx="14" cy="14" r="9"/><path d="m21 21 7 7"/>',
        'dice': '<rect x="5" y="5" width="22" height="22" rx="5"/><path d="M11 11h.01M21 11h.01M16 16h.01M11 21h.01M21 21h.01" stroke-width="3"/>',
        'pot': '<path d="M6 13h20v11a4 4 0 0 1-4 4H10a4 4 0 0 1-4-4ZM2 13h28M13 9h6"/>',
        'clock': '<circle cx="16" cy="16" r="12"/><path d="M16 9v7l5 3"/>',
        'back': '<path d="M26 16H6M14 8l-8 8 8 8"/>',
    }
    return f'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'
def arrow(): return f'<span class="arrow">{icon("back")}</span>'
def title_parts(title):
    """Recipes titled 'base • flavour' read best with the flavour as the name."""
    base, _, flavour = title.partition(' • ')
    return (base, flavour) if flavour else ('', title)
def step_timer(text):
    """Seconds for a kitchen timer when a step names minutes; ranges start at the low end. Fridge hours get none."""
    match = re.search(r'(\d+)(?:[–-]\d+)?\s*(?:دقيقة|دقائق)', text)
    if match: return int(match.group(1)) * 60
    if 'دقيقتين' in text: return 120
    if re.search(r'(?<!\S)دقيقة', text): return 60
    return 0
def page(title, body, prefix='', kind='', sky='morning', current=''):
    links = [('catalog', f'{prefix}index.html#catalog', 'وصفات البيت'), ('kitchen', f'{prefix}kitchen.html', 'دفتر المطبخ')]
    nav = ''.join(f'<a href="{href}"{" aria-current=\"page\"" if key == current else ""}>{label}</a>' for key, href, label in links)
    return f'''<!doctype html>
<html lang="ar" dir="rtl" data-sky="{sky}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.classList.add('js');if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('motion')</script>
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="{SKY_HEX[sky]}"><title>{e(title)} — شوكة وملعقة</title><meta name="description" content="كتاب طبخ عربي مصوّر. اختر وصفتك واتبع المكوّنات والخطوات بالصور.">
<link rel="preload" href="{prefix}assets/fonts/alexandria-variable.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{prefix}assets/styles.css?v={style_version}"><script src="{prefix}assets/app.js?v={script_version}" defer></script></head>
<body class="{kind}"><a class="skip-link" href="#main">انتقل إلى المحتوى</a>
<header class="site-head"><a class="brand" href="{prefix}index.html"><span class="brand-mark">{icon()}</span><span>شوكة وملعقة<small>أكل بيت، على مهلك</small></span></a><nav aria-label="التنقل الرئيسي">{nav}</nav></header>
{body}<footer class="footer"><div class="footer-inner"><div class="footer-copy"><strong>البيت يحلى برائحة طبخة.</strong><p>وصفة بسيطة، وقت لنفسك، ولقمة تفرّحك.</p><a class="btn btn-footer" href="{prefix}index.html#catalog">نختار طبختك الجاية {arrow()}</a></div>{image(visual('site/footer-chef.png'), '', 'footer-chef', prefix)}</div><div class="footer-bottom">شوكة وملعقة <span>مكانك الدافئ، كل يوم.</span></div></footer></body></html>'''
# Home is exclusively a recipe directory: no recipe instructions or hidden recipe bodies.
counts = [len([r for r in book['recipes'] if r['chapter'] == k]) for k in range(len(chapters))]
window_art = ''.join(image(visual(dial_art[k], ''), 'طاهيتنا تحضّر الشوفان في مطبخ دافئ مضاء بالشمس' if k == 0 else '', 'on' if k == 0 else '', eager=k == 0, attrs=' style="object-position:18% center"' if k == 0 else '') for k in range(5))
ticks = ''.join(f'<span class="tick" data-k="{k}" style="--a:{70 - k * 35}deg"></span>' for k in range(5))
stops = ''.join(f'<button type="button" class="stop" data-k="{k}" data-sky="{SKIES[k]}" data-hex="{SKY_HEX[SKIES[k]]}" data-name="{chapters[k]}" data-time="{times[k]}" data-note="{e(chapter_notes[k])}" data-count="{recipe_count(counts[k])}" data-cta="{"وصفة" if counts[k] == 1 else "وصفات"} {short_names[k]}" aria-pressed="{"true" if k == 0 else "false"}">{icon(meal_icons[k])}<span class="stop-label">{short_names[k]}</span></button>' for k in range(5))
intro = f'''<section class="hero"><div class="hero-copy"><h1><span class="thin">تفضّل،</span><span class="heavy">المطبخ مطبخك.</span></h1><p>خلّ يومك يهدأ شوي. نختار وصفة تحبّها، ونطبخها معًا، خطوة بخطوة.</p><a class="btn" href="#catalog" data-dial-cta><span data-dial-cta-label>وش نطبخ اليوم؟</span> {arrow()}</a><p class="hero-foot">{icon('leaf')} مكوّنات بسيطة. أكل بيت. وعلى راحتك.</p></div><div class="scene" data-dial><div class="scene-stage"><div class="orbit" aria-hidden="true"><span class="orbit-track"></span>{ticks}<span class="sun js-only" style="--a:70deg"><svg class="sun-disc" viewBox="0 0 64 64" aria-hidden="true"><g class="sun-rays" stroke="currentColor" stroke-width="4" stroke-linecap="round"><path d="M32 3v7M32 54v7M3 32h7M54 32h7M11.5 11.5l5 5M47.5 47.5l5 5M11.5 52.5l5-5M47.5 16.5l5-5"/></g><circle cx="32" cy="32" r="15" fill="currentColor"/></svg><svg class="moon-disc" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M47 42A22 22 0 0 1 23 13a22 22 0 1 0 24 29Z"/></svg></span></div><div class="window">{window_art}</div><div class="dial-caption" aria-live="polite"><strong data-dial-name>{chapters[0]}</strong><span data-dial-time>{times[0]}، {recipe_count(counts[0])}</span><p data-dial-note>{chapter_notes[0]}</p></div></div><div class="dial-stops js-only" role="group" aria-label="اختر وقت الوجبة">{stops}</div></div></section>'''
stars = '<span class="stars"></span><span class="stars stars-b"></span>'
clouds = ''.join(f'<svg class="cloud cloud-{n}" viewBox="0 0 200 80" aria-hidden="true"><path fill="currentColor" d="M42 72a26 26 0 0 1-4-52 38 38 0 0 1 70-10 30 30 0 0 1 48 16 24 24 0 0 1 4 46Z"/></svg>' for n in range(1, 4))
body = f'<div class="sky-decor" aria-hidden="true">{stars}{clouds}</div><main id="main" class="home-main">' + intro + f'<section id="catalog"><div class="catalog-head"><h2>لكل وقت، لقمة تحبّها.</h2><div><p>٣٥ وصفة مصوّرة، من صباحك إلى آخر اليوم. اختَر وجبتك، والباقي نمشيه معًا.</p><div class="catalog-tools js-only"><button type="button" class="btn btn-quiet" data-finder>{icon("search")}ابحث باسم مكوّن</button><button type="button" class="btn btn-quiet" data-surprise>{icon("dice")}فاجئني بوصفة</button></div></div></div><nav class="day-rail" aria-label="أوقات الوجبات"><span class="rail-thumb" aria-hidden="true"></span>'
body += ''.join(f'<a href="#chapter-{k}">{icon(meal_icons[k])}<span class="rail-label">{short_names[k]}</span></a>' for k in range(5)) + '</nav>'
for k, c in enumerate(chapters):
    recipes = [r for r in book['recipes'] if r['chapter'] == k]
    few = ' chapter-few' if len(recipes) <= 2 else ''
    body += f'<section class="chapter{few}" id="chapter-{k}" data-sky="{SKIES[k]}"><div class="chapter-head"><div class="chapter-title"><span class="chapter-time">{times[k]}</span><h2>{c}</h2><p>{chapter_notes[k]} <b>{recipe_count(len(recipes))} من مطبخنا.</b></p></div>{image(visual(chapter_art[k], recipes[0]["hero"]), "", "chapter-art")}</div><div class="shelf" data-count="{len(recipes)}">'
    for r in recipes:
        base, name = title_parts(r['title'])
        search = ' '.join(i['name'] for i in r['ingredients'])
        step_images = '|'.join(s['img'] for s in r['steps'])
        kicker = f'<small>{e(base)}</small>' if base else ''
        body += f'<a class="tile" href="recipes/recipe-{r["id"]}.html" data-q="{e(search)}" data-steps="{e(step_images)}"><div class="tile-art">{image(r["hero"], r["title"], attrs=f" style=\"view-transition-name:r{r["id"]}\"")}<span class="tile-kcal"><b>{ar(r["kcal"])}</b>سعرة</span></div><div class="tile-copy"><h3>{kicker}{e(name)}</h3><p>{e(ar(r["time"]))}</p></div></a>'
    body += '</div></section>'
body += '</section><aside class="kitchen-invite"><div><h2>كل أسرار مطبخك، في دفتر واحد.</h2><p>تحضير الوجبات، أدواتك، وطريقة حفظ كل لقمة.</p><a class="btn" href="kitchen.html">افتح دفتر المطبخ ' + arrow() + '</a></div>' + image(visual('site/kitchen-wide.png'), 'تحضير وجبات البيت', 'invite-art') + '</aside></main>'
(ROOT/'index.html').write_text(page('وصفات البيت', body, kind='home-page', current='catalog'))
labels = ['بروتين', 'كربوهيدرات', 'دهون', 'ألياف', 'كالسيوم', 'حديد', 'بوتاسيوم', 'فيتامين ج']
serving_labels = ['حصة', '٣ حصص', '٤ حصص']
for idx, r in enumerate(book['recipes']):
    base, name = title_parts(r['title'])
    kicker = f'<small>{e(base)}</small>' if base else ''
    body = f'<main id="main" class="recipe-main"><a class="breadcrumb" href="../index.html#chapter-{r["chapter"]}">{icon("back")}العودة إلى {chapters[r["chapter"]]}</a><article class="recipe" id="recipe-{r["id"]}"><div class="recipe-top"><div class="recipe-intro"><span class="recipe-when">{chapters[r["chapter"]]}، {times[r["chapter"]]}</span><h1>{kicker}{e(name)}</h1><p class="recipe-time">{icon("clock")}{e(ar(r["time"]))}</p><div class="recipe-quick-links"><button type="button" class="btn js-only" data-cook>{icon("pot")}ابدأ وضع الطبخ</button><a class="btn btn-quiet" href="#ingredients">المكوّنات</a><a class="btn btn-quiet" href="#cooking">الخطوات</a></div></div><div class="hero-frame">{image(r["hero"], r["title"], "hero-art", "../", True, attrs=f" style=\"view-transition-name:r{r["id"]}\"")}<span class="kcal-badge"><b>{ar(r["kcal"])}</b>سعرة للحصة</span></div></div><section class="nutrition" aria-label="القيم الغذائية للحصة الواحدة"><div class="nutrients">'
    body += ''.join(f'<div class="nutrient{" macro" if k < 4 else ""}">{labels[k]}<b>{ar(n)} <small>{"غ" if k < 4 else "ملغ"}</small></b></div>' for k, n in enumerate(r['nutrition']))
    body += f'</div><p class="tools">القيم الغذائية تقديرية للحصة الواحدة.</p></section><div class="prep"><section class="ingredients" id="ingredients"><div class="ingredients-head"><div><h2>مكوّناتك</h2><p class="tools">الوزن بالجرام. حدّد ما جهّزته.</p></div><div class="servings js-only" role="group" aria-label="عدد الحصص"><span class="servings-thumb" aria-hidden="true"></span>' + ''.join(f'<button type="button" data-serving="{k}" aria-pressed="{"true" if k == 0 else "false"}">{label}</button>' for k, label in enumerate(serving_labels)) + '</div></div><div class="ready-meter js-only" aria-hidden="true"><span></span></div><p class="ready-note js-only" aria-live="polite"></p><table><thead><tr><th scope="col">المكوّن</th>' + ''.join(f'<th scope="col">{label}</th>' for label in serving_labels) + '</tr></thead><tbody>'
    for ingredient in r['ingredients']:
        body += f'<tr><th scope="row"><label><input class="ingredient-check" type="checkbox"><span>{e(ingredient["name"])}</span></label></th>' + ''.join(f'<td>{e(ar(n))}</td>' for n in ingredient['amounts']) + '</tr>'
    body += f'</tbody></table><p class="tools">الأدوات: {e(ar(r["tools"]))}</p></section><aside class="note"><h2>طبخة اليوم، وراحة بكرة.</h2><span class="pill">{icon("clock")}{e(ar(r["batchTime"]))}</span><p>{e(ar(r["batch"]))}</p><p class="tools">احسب مدة الحفظ من التحضير الأصلي، واتبع أقصر مدة بين المكوّنات.</p><a href="../kitchen.html#storage-section">راجع دليل الثلاجة</a></aside></div><div class="cooking-heading" id="cooking"><h2>يلا، نطبخها معًا.</h2><p>خذ وقتك، واتبع الصور على راحتك.</p><button type="button" class="btn js-only" data-cook>{icon("pot")}ابدأ وضع الطبخ</button></div><div class="steps">'
    for k, s in enumerate(r['steps']):
        timer = step_timer(s['text'])
        timer_attr = f' data-timer="{timer}"' if timer else ''
        body += f'<section class="step"{timer_attr}>{image(s["img"], s["text"], prefix="../")}<div class="caption"><b><span class="sr">الخطوة </span>{ar(str(k + 1).zfill(2))}</b><p>{e(ar(s["text"]))}</p></div></section>'
    body += f'</div><div class="recipe-actions"><button type="button" class="btn btn-quiet" data-print>طباعة الوصفة / حفظ PDF</button><a href="../index.html#catalog">العودة لاختيار وصفة</a></div></article><nav class="recipe-pagination" aria-label="الوصفات المجاورة">'
    for adjacent, label, rel in [(idx - 1, 'السابقة', 'prev'), (idx + 1, 'التالية', 'next')]:
        if 0 <= adjacent < len(book['recipes']):
            other = book['recipes'][adjacent]
            body += f'<a class="page-{rel}" href="recipe-{other["id"]}.html"{" data-next" if rel == "next" else ""}>{image(other["hero"], "", prefix="../")}<span><small>{label}</small>{e(other["title"].replace(" • ", ": "))}</span></a>'
    (ROOT/'recipes'/f'recipe-{r["id"]}.html').write_text(page(r['title'], body + '</nav></main>', '../', 'recipe-page', SKIES[r['chapter']]))
# Preserve reference content on its own page, separate from recipe selection.
index_links = ''.join(f'<a href="#guide-{g["id"]}">{e(g["title"])}</a>' for g in book['guides']) + '<a href="#storage-section">دليل الثلاجة</a>'
body = f'<main id="main" class="kitchen-main"><section class="kitchen-intro"><div><h1>دفتر المطبخ</h1><p>دليلك للتحضير، والأدوات، وحفظ كل لقمة.</p><a class="btn" href="#storage-section">إلى دليل الثلاجة {arrow()}</a></div>{image(visual("site/kitchen-wide.png"), "تحضير الوجبات في مطبخنا", "kitchen-scene", eager=True)}</section><div class="guide-layout"><nav class="guide-index" aria-label="مواضيع الدفتر">{index_links}</nav><div class="guides">'
for g in book['guides']:
    subtitle = g['subtitle']
    tags = ''.join(f'<span>{e(ar(part))}</span>' for part in subtitle.split(' • ')) if ' • ' in subtitle else ''
    summary = f'<div class="guide-tags">{tags}</div>' if tags else f'<p class="guide-sub">{e(ar(subtitle))}</p>'
    body += f'<article class="guide" id="guide-{g["id"]}"><div class="guide-head">{image(g["img"], g["title"])}<div><h2>{e(g["title"])}</h2>{summary}</div></div><ol>' + ''.join(f'<li><b>{e(ar(h))}</b>{e(ar(b))}</li>' for h, b in g['items']) + '</ol></article>'
body += '</div></div><section id="storage-section"><h2>دليل الثلاجة</h2><div class="storage-notes"><p>كل الجدول يفترض التبريد المستمر عند ٤°م أو أقل. اليوم صفر يبدأ عند الطبخ أو الفتح أو التقطيع. مدة ٣–٤ أيام تنتهي عند اكتمال ٩٦ ساعة. اتبع أقصر مدة بين مكوّنات الوجبة وتعليمات العبوة.</p><p>الرموز تقدّر الطعم والقوام. الرائحة والطعم وحدهما لا يثبتان سلامة الطعام. لا تتذوّق الطعام للتحقق من سلامته.</p></div>'
body += '<div class="day-picker js-only"><label for="storage-day">كم يوم مرّ على التحضير؟ <b data-day-label>حرّك المؤشر</b></label><input id="storage-day" type="range" min="0" max="6" step="1" value="0"><div class="day-ticks" aria-hidden="true">' + ''.join(f'<span>{ar(k)}</span>' for k in range(7)) + '</div><p class="day-summary" aria-live="polite" data-day-summary></p><button type="button" class="btn btn-quiet" data-day-reset hidden>عرض كل الأيام</button></div>'
marks = {'S': '●', 'M': '◐', 'D': '○', 'X': '✕'}
symbols = {'S': 'جودة جيدة', 'M': 'نكهة أضعف', 'D': 'جودة أقل', 'X': 'انتهت المدة'}
body += '<p class="legend">' + ''.join(f'<span class="mark mark-{key}">{marks[key]}</span>{text} ' for key, text in [('S', 'جودة جيدة'), ('M', 'بدأت النكهة تضعف'), ('D', 'ضمن المدة، جودة أقل'), ('X', 'انتهت المدة')]) + '</p>'
limits = {'3–4 days': '٣ إلى ٤ أيام', '1–2 days': 'يوم إلى يومين', '3–4 days*': '٣ إلى ٤ أيام*', 'Package label': 'حسب العبوة', 'About 7–14 days†': 'نحو ٧ إلى ١٤ يومًا', 'Up to 3 days*': 'حتى ٣ أيام*', 'Up to 7 days†': 'حتى ٧ أيام', 'Fresh each prep': 'ماء جديد لكل تحضير'}
for group in book['storage']:
    body += f'<h3>{e(group["title"])}</h3><div class="storage-wrap" tabindex="0" role="region" aria-label="{e(group["title"])}"><table class="storage"><thead><tr><th scope="col">المكوّن وحالته</th>' + ''.join(f'<th scope="col">يوم {ar(k)}</th>' for k in range(7)) + '</tr></thead><tbody>'
    for row in group['rows']:
        body += f'<tr><th scope="row">{e(row["name"])}<p class="tools">{limits[row["limit"]]}. {e(row["note"])}</p></th>' + ''.join(f'<td class="cell-{s}" data-state="{s}"><span title="{symbols[s]}" aria-hidden="true">{marks[s]}</span><span class="sr">{symbols[s]}</span></td>' for s in row['seq']) + '</tr>'
    body += '</tbody></table></div>'
body += '<p class="storage-foot">المدد المعلّمة بنجمة (*) اختيارات احتياطية للتخطيط. جمّد الحصص المتأخرة مبكرًا، وذوّبها في الثلاجة.</p><details><summary>مصادر مدد الحفظ</summary><ul>' + ''.join(f'<li><a href="{e(url)}" target="_blank" rel="noopener">{e(url)}</a></li>' for url in book['sources']) + '</ul></details></section></main>'
(ROOT/'kitchen.html').write_text(page('دفتر المطبخ والحفظ', body, kind='kitchen-page', sky='noon', current='kitchen'))
print('Built recipe-only catalog, 35 standalone recipe pages, and kitchen reference.')

print(f'Connected {len(used_visuals)} generated artworks; missing and withheld images retain originals.')
