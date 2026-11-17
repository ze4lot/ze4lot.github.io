/* Measure natural content heights; only pages, never sections, have a fixed size. */
window.paginateCV = function () {
  const cv = document.querySelector('main.cv');
  if (!cv || cv.dataset.paginated) return;
  const original = cv.innerHTML;
  const root = cv.querySelector(':scope > .level1');
  if (!root) return;
  const clause = cv.querySelector('.recruitment-clause');
  if (clause) clause.remove();
  const units = [];
  const masthead = document.createElement('div');
  masthead.className = 'level1 cv-masthead';
  for (const child of [...root.children]) {
    if (child.matches('.level2')) units.push(child);
    else masthead.append(child);
  }
  units.unshift(masthead);
  const experience = units.find(node => node.id === 'professional-experience');
  const entries = [...experience.querySelectorAll(':scope > .experience-entry')];
  const lastEntries = entries.filter(entry => ['AKRA Polska', 'EURA7'].includes(entry.querySelector('h3').textContent.trim()));
  const first = document.createElement('div');
  first.className = 'experience-start';
  first.append(experience.querySelector(':scope > h2'), entries[0]);
  units.splice(units.indexOf(experience), 1, first,
    ...entries.slice(1).filter(entry => !lastEntries.includes(entry)));
  // Preserve any later sections in their original reading order.
  for (const child of [...experience.children]) {
    if (!child.matches('.experience-entry')) units.push(child);
  }
  cv.replaceChildren();
  cv.dataset.paginated = 'true';
  const probe = document.createElement('div');
  probe.style.height = 'calc(var(--page-height) - 2 * var(--page-margin-y))';
  cv.append(probe);
  const pageHeight = probe.getBoundingClientRect().height;
  probe.remove();
  const newPage = () => {
    const page = document.createElement('div');
    page.className = 'cv-page';
    page.style.height = `${pageHeight}px`;
    cv.append(page);
    return page;
  };
  let page = newPage();
  for (const unit of units) {
    page.append(unit);
    if (page.scrollHeight > pageHeight + 1 && page.children.length > 1) {
      unit.remove();
      page = newPage();
      page.append(unit);
    }
  }
  if (lastEntries.length) {
    page = newPage();
    page.classList.add('cv-page-final');
    const group = document.createElement('div');
    group.className = 'early-career';
    group.append(...lastEntries);
    const reserve = document.createElement('div');
    reserve.className = 'recruitment-clause-space';
    reserve.setAttribute('aria-hidden', 'true');
    page.append(group, clause || reserve);
  }
  if (clause && !lastEntries.length) {
    page.append(clause);
  }
  // Distribute a little spare room, but never stretch sections across the page.
  for (const sheet of cv.querySelectorAll('.cv-page:not(.cv-page-final)')) {
    const styles = getComputedStyle(sheet);
    const minGap = parseFloat(styles.getPropertyValue('--section-gap-min'));
    const maxGap = parseFloat(styles.getPropertyValue('--section-gap-max'));
    const items = [...sheet.children];
    if (items.length < 2) continue;
    const used = items.reduce((sum, item) => sum + item.getBoundingClientRect().height, 0);
    const gap = Math.max(minGap, Math.min(maxGap, (pageHeight - used) / (items.length - 1)));
    sheet.style.setProperty('--section-gap', `${gap}px`);
  }
  window.addEventListener('afterprint', () => {
    cv.innerHTML = original;
    delete cv.dataset.paginated;
  }, { once: true });
};
window.addEventListener('beforeprint', window.paginateCV);
