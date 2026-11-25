// SPDX-License-Identifier: MIT
// Development-only browser display test. Runtime entry remains stdlib Python.
import { createRequire } from 'node:module';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const input = path.resolve(process.argv[2]);
const output = path.resolve(process.argv[3]);
await mkdir(output, { recursive: true });
const bytes = await readFile(input);
const browser = await chromium.launch({headless:true, args:['--no-sandbox']});
try {
  const page = await browser.newPage({viewport:{width:1104,height:1104},deviceScaleFactor:1});
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.setContent(`<html><body style="margin:0;background:#18282f;display:flex;justify-content:center;padding:40px;box-sizing:border-box"><img alt="The World Today, 24 November 2026" style="display:block;width:1024px;height:1024px" src="data:image/png;base64,${bytes.toString('base64')}"></body></html>`);
  await page.locator('img').evaluate(img => img.decode());
  const dimensions = await page.locator('img').evaluate(img => ({
    naturalWidth:img.naturalWidth,naturalHeight:img.naturalHeight,
    displayWidth:img.getBoundingClientRect().width,
    displayHeight:img.getBoundingClientRect().height
  }));
  if (dimensions.naturalWidth!==1024 || dimensions.naturalHeight!==1024 || errors.length)
    throw Error(JSON.stringify({dimensions,errors}));
  await page.locator('img').screenshot({path:path.join(output,'browser-native.png')});
  await page.locator('img').evaluate(img => {img.style.width='512px';img.style.height='512px';});
  await page.locator('img').screenshot({path:path.join(output,'browser-thumbnail.png')});
  const result = {input,dimensions,errors,screenshots:['browser-native.png','browser-thumbnail.png']};
  await writeFile(path.join(output,'browser-check.json'), JSON.stringify(result,null,2));
  console.log(JSON.stringify(result));
} finally {
  await browser.close();
}
