/* Capture des screenshots EFREI a jour des 3 apps en cours d'execution.
   Ecrit dans assets/screens/ (ecrase les versions pre-EFREI). */
const { chromium } = require('playwright');
const path = require('path');
const SCR = path.join(__dirname, 'assets', 'screens');

async function shoot(page, url, file, { w = 1600, h = 900, wait = 8000, full = false, dark = false } = {}) {
  await page.setViewportSize({ width: w, height: h });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(wait);
  if (dark) {
    await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
    await page.waitForTimeout(1200);
  }
  await page.screenshot({ path: path.join(SCR, file), fullPage: full });
  console.log('  ->', file);
}

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ deviceScaleFactor: 1.25 });

  // Urban front · light + dark (1440x900 comme l'existant)
  await shoot(pg, 'http://localhost:5173', 'ude-light.png', { w: 1440, h: 900, wait: 7000 });
  await shoot(pg, 'http://localhost:5173', 'urban-dashboard-live.png', { w: 1440, h: 900, wait: 5000 });
  await shoot(pg, 'http://localhost:5173', 'ude-dark.png', { w: 1440, h: 900, wait: 5000, dark: true });

  // Urban API · Swagger (page entiere, portrait)
  await shoot(pg, 'http://localhost:8000/docs', 'ude-api.png', { w: 1425, h: 1000, wait: 4000, full: true });

  // Maintenance dashboard (1600x900)
  await shoot(pg, 'http://localhost:8501', 'maintenance-dashboard-live.png', { w: 1600, h: 900, wait: 9000 });

  // IA Pero (1600x900) · vue principale Speakeasy
  await shoot(pg, 'http://localhost:8502', 'iapero-speakeasy-live.png', { w: 1600, h: 900, wait: 11000 });
  await shoot(pg, 'http://localhost:8502', 'iapero-app-live.png', { w: 1600, h: 900, wait: 4000 });

  await b.close();
  console.log('capture done');
})().catch(e => { console.error('CAPTURE ERR', e.message); process.exit(1); });
