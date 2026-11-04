"""Generate static, offline-ready Arabic cookbook pages. Run: python3 scripts/build.py."""
from pathlib import Path
from html import escape
import json
from hashlib import sha256
ROOT = Path(__file__).resolve().parents[1]
style_version = sha256((ROOT/'assets/styles.css').read_bytes()).hexdigest()[:10]
script_version = sha256((ROOT/'assets/app.js').read_bytes()).hexdigest()[:10]
book = json.loads((ROOT / 'source/book.json').read_text())
chapters = ['الفطور', 'غداء العمل', 'استراحة السابعة', 'قبل التمرين', 'عشاء ما بعد التمرين']
times = ['الصباح', '٣ عصرًا', '٧ مساءً', 'قبل النادي', 'بعد النادي']
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
def image(src, alt, cls='', prefix='', eager=False):
    return f'<img src="{prefix}{e(src)}" alt="{e(alt)}" class="{cls}{" generated-art" if "web-visuals/" in src else ""}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def icon(name='bowl'):
    paths = {
        'bowl': '<path d="M4 12h24c0 8-5 12-12 12S4 20 4 12Z"/><path d="M9 28h14M10 8c-3-3 3-3 0-6M16 8c-3-3 3-3 0-6M22 8c-3-3 3-3 0-6"/>',
        'sun': '<circle cx="16" cy="16" r="6"/><path d="M16 2v4M16 26v4M2 16h4M26 16h4M6 6l3 3M23 23l3 3M6 26l3-3M23 9l3-3"/>',
        'lunch': '<rect x="4" y="10" width="24" height="17" rx="4"/><path d="M11 10V6h10v4M4 17h24M13 17v4h6v-4"/>',
        'cup': '<path d="M5 12h17v9a7 7 0 0 1-7 7h-3a7 7 0 0 1-7-7ZM22 13h3a4 4 0 0 1 0 8h-3M9 7c-3-3 3-3 0-6M17 7c-3-3 3-3 0-6"/>',
        'leaf': '<path d="M26 4C8 3 2 14 8 23c9 6 20 0 18-19ZM7 27 22 11"/>',
        'moon': '<path d="M25 21A12 12 0 0 1 11 5a12 12 0 1 0 14 16ZM23 4v6M20 7h6"/>',
    }
    return f'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'
def page(title, body, prefix='', kind=''):
    return f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#314b3c"><title>{e(title)} — شوكة وملعقة</title><meta name="description" content="كتاب طبخ عربي مصوّر. اختر وصفتك واتبع المكوّنات والخطوات بالصور.">
<link rel="stylesheet" href="{prefix}assets/styles.css?v={style_version}"><script src="{prefix}assets/app.js?v={script_version}" defer></script></head>
<body class="{kind}"><a class="skip-link" href="#main">انتقل إلى المحتوى</a>
<header><div class="toolbar"><a class="brand" href="{prefix}index.html"><span class="brand-mark">{icon()}</span><span>شوكة وملعقة<small>أكل بيت، على مهلك</small></span></a><nav aria-label="التنقل الرئيسي"><a href="{prefix}index.html#catalog">وصفات البيت</a><a href="{prefix}kitchen.html">دفتر المطبخ</a></nav></div></header>
{body}<footer class="footer"><div class="footer-inner">{image(visual('site/footer-chef.png'), '', 'footer-chef', prefix)}<div><span class="eyebrow">من مطبخنا، بكل حب</span><strong>البيت يحلى برائحة طبخة.</strong><p>وصفة بسيطة، وقت لنفسك، ولقمة تفرّحك.</p></div><a href="{prefix}index.html#catalog">نختار طبختك الجاية <span aria-hidden="true">←</span></a></div><div class="footer-bottom">شوكة وملعقة <span>مكانك الدافئ، كل يوم.</span></div></footer></body></html>'''
# Home is exclusively a recipe directory: no recipe instructions or hidden recipe bodies.
intro = f'''<section class="welcome"><div class="welcome-copy"><span class="eyebrow"><span class="welcome-dot"></span> أهلًا وسهلًا، نوّر المطبخ</span><h1>تفضّل،<br><em>المطبخ مطبخك.</em></h1><p>خلّ يومك يهدأ شوي. نختار وصفة تحبّها،<br class="desktop-break"> ونطبخها معًا، خطوة بخطوة.</p><a class="primary-link" href="#catalog">وش نطبخ اليوم؟ <span aria-hidden="true">←</span></a><div class="welcome-footnote"><span>{icon('leaf')}</span> مكوّنات بسيطة. أكل بيت. وعلى راحتك.</div></div><div class="welcome-picture"><div class="picture-frame">{image(visual('site/home-hero.png'), 'طاهيتنا تحضّر الشوفان في مطبخ دافئ مضاء بالشمس', 'home-scene', eager=True)}</div><div class="picture-note"><span>من أول مكوّن</span><strong>إلى آخر لقمة ♡</strong></div></div><span class="welcome-edge" aria-hidden="true"></span></section>'''
body = '<main id="main" class="home-main">' + intro + '<section id="catalog"><div class="catalog-heading"><div><span class="eyebrow">دفتر وصفاتك</span><h2>لكل وقت، لقمة تحبّها.</h2></div><p>٣٥ وصفة مصوّرة، من صباحك إلى آخر اليوم.<br>اختَر وجبتك، والباقي نمشيه معًا.</p></div><nav class="chapter-links" aria-label="أوقات الوجبات">'
meal_icons = ['sun', 'lunch', 'cup', 'leaf', 'moon']
body += ''.join(f'<a href="#chapter-{k}">{icon(meal_icons[k])}<span>{c}</span><small>{recipe_count(len([r for r in book["recipes"] if r["chapter"]==k]))}</small></a>' for k,c in enumerate(chapters)) + '</nav>'
chapter_art = ['recipes/08/cover.png', 'site/work-lunch.png', 'site/evening-break.png', 'site/before-workout.png', 'site/dinner.png']
chapter_notes = ['صباح هادئ، وشيء لذيذ تبدأ به يومك.', 'خذ معك من البيت لقمة تسعدك وسط الزحمة.', 'استراحة صغيرة تستاهلها، ولقمة تردّ الروح.', 'شيء خفيف، وطاقة تكمل بها يومك.', 'انتهى يومك. حان وقت طبق دافئ وراحة.']
for k,c in enumerate(chapters):
    recipes=[r for r in book['recipes'] if r['chapter']==k]
    body += f'<section class="recipe-chapter" id="chapter-{k}"><div class="chapter-info"><span class="chapter-kicker">الفصل {ar(k+1)} <span> / </span> {times[k]}</span><h2>{c}</h2><p>{chapter_notes[k]}</p>{image(visual(chapter_art[k], recipes[0]["hero"]), "", "chapter-art")}<span class="chapter-count">{recipe_count(len(recipes))} من مطبخنا</span></div><div class="shelf">'
    for n,r in enumerate(recipes,1):
        body += f'<a class="tile" href="recipes/recipe-{r["id"]}.html"><div class="tile-art">{image(r["hero"],r["title"])}<span class="tile-open" aria-hidden="true">↖</span></div><div class="tile-copy"><span class="recipe-index">{ar(str(n).zfill(2))}</span><h3>{e(r["title"])}</h3><small>{e(ar(r["time"]))}<span>{ar(r["kcal"])} سعرة</span></small></div></a>'
    body += '</div></section>'
body += '</section><aside class="kitchen-invite"><div><span class="eyebrow">شويّة ترتيب، وراحة أكثر</span><h2>كل أسرار مطبخك، في دفتر واحد.</h2><p>تحضير الوجبات، أدواتك، وطريقة حفظ كل لقمة.</p><a href="kitchen.html">افتح دفتر المطبخ <span aria-hidden="true">←</span></a></div>'+image(visual('site/kitchen-wide.png'),'تحضير وجبات البيت','invite-art')+'</aside></main>'
(ROOT/'index.html').write_text(page('وصفات البيت',body,kind='home-page'))
labels=['بروتين','كربوهيدرات','دهون','ألياف','كالسيوم','حديد','بوتاسيوم','فيتامين ج']
for idx,r in enumerate(book['recipes']):
    body=f'<main id="main"><a class="breadcrumb" href="../index.html#chapter-{r["chapter"]}">← العودة إلى {chapters[r["chapter"]]}</a><article class="recipe" id="recipe-{r["id"]}"><div class="recipe-top"><div><span class="eyebrow">{chapters[r["chapter"]]} · {times[r["chapter"]]}</span><h1>{e(r["title"])}</h1><div class="pills"><span class="pill">{ar(r["kcal"])} سعرة للحصة</span><span class="pill">{e(ar(r["time"]))}</span></div><div class="recipe-quick-links"><a href="#ingredients">المكوّنات ↓</a><a href="#cooking">خطوات التحضير ↓</a></div><div class="nutrients">'
    body+=''.join(f'<div class="nutrient">{labels[k]}<b>{ar(n)} <small>{"غ" if k<4 else "ملغ"}</small></b></div>' for k,n in enumerate(r['nutrition']))
    body+=f'</div><p class="tools">القيم الغذائية تقديرية للحصة الواحدة.</p></div>{image(r["hero"],r["title"],"hero-art","../",True)}</div><div class="ingredients-layout"><section class="ingredients" id="ingredients"><span class="eyebrow">أولًا، نجهّز الطاولة</span><h2>مكوّناتك</h2><p class="tools">الوزن بالجرام · حدّد ما جهّزته</p><table><thead><tr><th scope="col">المكوّن</th><th scope="col">حصة</th><th scope="col">٣ حصص</th><th scope="col">٤ حصص</th></tr></thead><tbody>'
    for ingredient in r['ingredients']:
        body+=f'<tr><th scope="row"><label><input class="ingredient-check" type="checkbox">{e(ingredient["name"])}</label></th>'+''.join(f'<td>{e(ar(n))}</td>' for n in ingredient['amounts'])+'</tr>'
    body+=f'</tbody></table><p class="tools">الأدوات · {e(r["tools"])}</p></section><aside class="note"><span class="eyebrow">ورقة صغيرة من دفترنا</span><h2>طبخة اليوم، وراحة بكرة.</h2><span class="pill">{e(ar(r["batchTime"]))}</span><p>{e(ar(r["batch"]))}</p><p class="tools">احسب مدة الحفظ من التحضير الأصلي، واتبع أقصر مدة بين المكوّنات.</p><a href="../kitchen.html#storage-section">راجع دليل الثلاجة ←</a></aside></div><div class="cooking-heading" id="cooking"><div><span class="eyebrow">خطوة صغيرة، وطبق لذيذ</span><h2 class="steps-title">يلا، نطبخها معًا.</h2></div><p class="tools">خذ وقتك، واتبع الصور على راحتك.</p></div><div class="steps">'
    body+=''.join(f'<section class="step">{image(s["img"],s["text"],prefix="../")}<div class="caption"><b><span>الخطوة</span>{ar(str(k+1).zfill(2))}</b><p>{e(ar(s["text"]))}</p></div></section>' for k,s in enumerate(r['steps']))
    body+='</div><div class="recipe-actions"><button type="button" data-print>طباعة الوصفة / حفظ PDF</button><a href="../index.html#catalog">العودة لاختيار وصفة</a></div></article><nav class="recipe-pagination" aria-label="الوصفات المجاورة">'
    for adjacent,label in [(idx-1,'السابقة'),(idx+1,'التالية')]:
        if 0<=adjacent<len(book['recipes']):
            other=book['recipes'][adjacent];body+=f'<a href="recipe-{other["id"]}.html">{label}: {e(other["title"])}</a>'
    (ROOT/'recipes'/f'recipe-{r["id"]}.html').write_text(page(r['title'],body+'</nav></main>','../','recipe-page'))
# Preserve reference content on its own page, separate from recipe selection.
body=f'<main id="main"><section class="kitchen-intro">{image(visual("site/kitchen-wide.png"), "تحضير الوجبات في مطبخنا", "kitchen-scene", eager=True)}<div><span class="eyebrow">قليل من الترتيب، كثير من الراحة</span><h1>دفتر المطبخ</h1><p>دليلك للتحضير، والأدوات، وحفظ كل لقمة.</p><a href="#storage-section">إلى دليل الثلاجة ↓</a></div></section><div class="guides">' 
for g in book['guides']:
    body+=f'<article class="guide">{image(g["img"],g["title"])}<h2>{e(g["title"])}</h2><p>{e(ar(g["subtitle"]))}</p><ol>'+''.join(f'<li><b>{e(ar(h))}</b>{e(ar(b))}</li>' for h,b in g['items'])+'</ol></article>'
body+='</div><section id="storage-section"><h2>دليل الثلاجة</h2><div class="storage-notes"><p>كل الجدول يفترض التبريد المستمر عند ٤°م أو أقل. اليوم صفر يبدأ عند الطبخ أو الفتح أو التقطيع. مدة ٣–٤ أيام تنتهي عند اكتمال ٩٦ ساعة. اتبع أقصر مدة بين مكوّنات الوجبة وتعليمات العبوة.</p><p>الرموز تقدّر الطعم والقوام. الرائحة والطعم وحدهما لا يثبتان سلامة الطعام. لا تتذوّق الطعام للتحقق من سلامته.</p></div><p class="legend">🌟 جودة جيدة · 🌙 بدأت النكهة تضعف · 🌑 ضمن المدة، جودة أقل · ❌ انتهت المدة</p>'
limits={'3–4 days':'٣ إلى ٤ أيام','1–2 days':'يوم إلى يومين','3–4 days*':'٣ إلى ٤ أيام*','Package label':'حسب العبوة','About 7–14 days†':'نحو ٧ إلى ١٤ يومًا','Up to 3 days*':'حتى ٣ أيام*','Up to 7 days†':'حتى ٧ أيام','Fresh each prep':'ماء جديد لكل تحضير'}
symbols={'S':'🌟 جودة جيدة','M':'🌙 نكهة أضعف','D':'🌑 جودة أقل','X':'❌ انتهت المدة'}
for group in book['storage']:
    body+=f'<h3>{e(group["title"])}</h3><div class="storage-wrap"><table class="storage"><thead><tr><th scope="col">المكوّن وحالته</th>'+''.join(f'<th scope="col">يوم {ar(k)}</th>' for k in range(7))+'</tr></thead><tbody>'
    for row in group['rows']:
        body+=f'<tr><th scope="row">{e(row["name"])}<p class="tools">{limits[row["limit"]]} · {e(row["note"])}</p></th>'+''.join(f'<td><span title="{symbols[s]}">{symbols[s][0]}</span><span class="sr">{symbols[s][2:]}</span></td>' for s in row['seq'])+'</tr>'
    body+='</tbody></table></div>'
body+='<p>المدد المعلّمة بنجمة (*) اختيارات احتياطية للتخطيط. جمّد الحصص المتأخرة مبكرًا، وذوّبها في الثلاجة.</p><details><summary>مصادر مدد الحفظ</summary><ul>'+''.join(f'<li><a href="{e(url)}" target="_blank" rel="noopener">{e(url)}</a></li>' for url in book['sources'])+'</ul></details></section></main>'
(ROOT/'kitchen.html').write_text(page('دفتر المطبخ والحفظ',body,kind='kitchen-page'))
print('Built recipe-only catalog, 35 standalone recipe pages, and kitchen reference.')

print(f'Connected {len(used_visuals)} generated artworks; missing and withheld images retain originals.')
