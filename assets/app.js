"use strict";
const mealRail = document.querySelector('.chapter-links');
if (mealRail) {
  const links = [...mealRail.querySelectorAll('a')];
  const chapters = links.map(link => document.querySelector(link.hash));
  let scheduled = false;
  const updateChapter = () => {
    const readingLine = Math.max(mealRail.offsetHeight + 40, 144);
    let current = -1;
    chapters.forEach((chapter, index) => {
      if (chapter.getBoundingClientRect().top <= readingLine) current = index;
    });
    links.forEach((link, index) => {
      if (index === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    scheduled = false;
  };
  const scheduleUpdate = () => {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(updateChapter);
    }
  };
  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', scheduleUpdate);
  window.addEventListener('pageshow', scheduleUpdate);
  document.fonts.ready.then(scheduleUpdate);
  updateChapter();
}
const printButton = document.querySelector('[data-print]');
if (printButton) printButton.addEventListener('click', async () => {
  printButton.disabled = true;
  try {
    const images = [...document.images];
    images.forEach(image => { image.loading = 'eager'; });
    await Promise.all(images.map(image => image.decode().catch(() => {})));
    window.print();
  } finally { printButton.disabled = false; }
});
