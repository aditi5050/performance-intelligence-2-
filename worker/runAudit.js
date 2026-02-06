import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

async function runLighthouse(url) {

  const chrome = await chromeLauncher.launch({
    chromeFlags: ['--headless']
  });

  const options = {
    logLevel: 'info',
    output: 'json',
    onlyCategories: ['performance'],
    port: chrome.port
  };

  const runnerResult = await lighthouse(url, options);

  const audits = runnerResult.lhr.audits;

  const result = {
    performance_score: runnerResult.lhr.categories.performance.score * 100,
    lcp: audits['largest-contentful-paint'].numericValue,
    cls: audits['cumulative-layout-shift'].numericValue,
    tbt: audits['total-blocking-time'].numericValue
  };

  console.log("RESULT:");
  console.log(result);

  await chrome.kill();
}

const url = process.argv[2];

if (!url) {
  console.log("Usage: node runAudit.js https://example.com");
  process.exit();
}

runLighthouse(url);
