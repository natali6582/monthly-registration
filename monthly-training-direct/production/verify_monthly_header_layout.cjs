const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require('C:/Users/Nataliek/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

async function main(input, output) {
  fs.mkdirSync(output, {recursive: false});
  const browser = await chromium.launch({headless: true, channel: 'msedge'});
  try {
    const results = [];
    for (const width of [900, 390]) {
      const page = await browser.newPage({viewport: {width, height: 1100}, locale: 'he-IL'});
      await page.setContent(fs.readFileSync(input, 'utf8'), {waitUntil: 'networkidle'});
      const info = await page.evaluate(() => {
        const img = document.querySelector('img');
        const h1 = document.querySelector('h1');
        const header = document.querySelector('td[bgcolor="#b4d2ca"]');
        const a = img.getBoundingClientRect(), b = header.getBoundingClientRect(), c = h1.getBoundingClientRect();
        return {imageLoaded: img.complete && img.naturalWidth > 0, imageWidth: a.width, imageHeight: a.height,
          centerOffset: Math.abs((a.x+a.width/2)-(b.x+b.width/2)),
          titleGap: c.y-a.bottom, font: getComputedStyle(h1).fontFamily,
          horizontalOverflow: document.documentElement.scrollWidth > innerWidth};
      });
      assert(info.imageLoaded && !info.horizontalOverflow);
      assert.equal(info.imageWidth, width === 900 ? 56 : 48);
      assert.equal(info.imageHeight, info.imageWidth);
      assert(info.centerOffset <= 1, JSON.stringify(info));
      assert(info.titleGap >= 12, JSON.stringify(info));
      assert(info.font.includes('Arial'));
      await page.locator('td[bgcolor="#b4d2ca"]').screenshot({path: path.join(output, `header-${width}.png`)});
      results.push({viewport: width, ...info});
      await page.close();
    }
    const proof = {passed: true, results};
    fs.writeFileSync(path.join(output, 'verification.json'), JSON.stringify(proof, null, 2)+'\n');
    console.log(JSON.stringify(proof));
  } finally {await browser.close();}
}
main(process.argv[2], process.argv[3]).catch(e => {console.error(e.stack); process.exitCode=1;});
