const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Navigate to the URL containing the dynamic content
  await page.goto('https://example.com');

  // Evaluate a JavaScript expression in the browser context
  const extractedText = await page.evaluate(() => {
    // Replace with your specific selector to target the desired content
    const selector = 'your-selector-here';
    const element = document.querySelector(selector);
    return element ? element.textContent : '';
  });

  console.log(extractedText);

  await browser.close();
})();