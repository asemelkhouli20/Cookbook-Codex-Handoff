# One day in the kitchen

Direction: the book is organised around a day (morning, 3pm, 7pm, before the gym, after it), so the site *is* that day. The sky changes as you move through the meals. The warm painted illustrations stay untinted and read like lit windows against it.

- Colour: five skies, each a full set of tokens in `assets/styles.css`: saffron morning, clear noon blue, apricot sunset, violet dusk, indigo night. Every colour on a page comes from the current sky, and all ink/accent pairs meet WCAG AA. Recipes wear their chapter's sky, the kitchen notebook wears noon, and the footer is always night.
- Typography: Alexandria variable (100–900, hosted locally) is the only family. Hierarchy comes from extreme weight contrast. Never add letter-spacing or italics to Arabic.
- Signature motion: type rises like dough, from hairline to full weight (hero headline, chapter titles, recipe titles). Keep this the one recurring flourish.
- Floating: painted decor cutouts hover in the empty space beside content at different depths. They shift with scroll, dodge the cursor, and can be grabbed and flung. Keep them out of text and buttons, and off on phones where there's no room. Leaves drift by day and fireflies come out at dusk.
- Appearing: anything below the fold lands as it reaches the screen, one after another in reading order, never all at once off-screen. Images open from the bottom, tiles land before their calorie badge. The recipe's opening picture never animates, because it is the target of the cross-page morph.
- Homepage: a draggable sun travels an arc over an arched kitchen window; it climbs to the visitor's own hour on first load. Below it, chapters with huge titles and a staggered recipe grid. All 35 recipes stay visible: search opens a separate list and never hides the catalog.
- Recipe: picture bleeding off the page edge, servings switch, tappable ingredient checklist with progress, a sticky step picture on wide screens, and cook mode (full screen, one step at a time, timers, keeps the screen awake). The food and the current action stay fully visible (`object-fit: contain` on steps).
- Kitchen reference: sticky topic index and a fridge day slider that highlights one day across every storage table. Tables scroll inside their own area on phones.
- Direction: logical CSS properties throughout. The few physical `left` values sit under pixel-measured transforms and are marked `rtl-ok`. In cook mode left/swipe-right is forward, as in an Arabic book.
- Foundations: everything works without JavaScript (all serving columns, every step image, links for navigation), `prefers-reduced-motion` turns motion off, and printing keeps all servings and steps.
- Keep all 35 recipe choices on index.html, separate recipe URLs, existing cooking text and quantities. Use available generated artwork with original-image fallbacks.

Verification: rebuild all 37 pages; run `scripts/check.py`; check desktop and phone (down to 320px) for horizontal overflow against the device width, not `innerWidth`, which inflates with the page; exercise the sun, search, servings, checklist, cook mode, timers, the fridge slider and print.
