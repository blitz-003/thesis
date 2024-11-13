const puppeteer = require("puppeteer");

async function getComputedFontSizes(url) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle2" });

  const fontSizes = await page.evaluate(() => {
    const elements = document.querySelectorAll("*");
    const fontSizes = {};

    elements.forEach((element) => {
      const style = window.getComputedStyle(element);
      const fontSize = style.fontSize;
      const tagName = element.tagName.toLowerCase(); // Corrected variable name
      // ^^^^ Corrected variable name

      if (!fontSizes[tagName]) {
        fontSizes[tagName] = new Set();
      }

      fontSizes[tagName].add(fontSize);
    });

    // Convert sets to arrays for JSON serialization
    for (let tag in fontSizes) {
      fontSizes[tag] = Array.from(fontSizes[tag]);
    }

    return fontSizes;
  });

  await browser.close();
  return fontSizes;
}

// Run the function if this script is executed directly
if (require.main === module) {
  const url = process.argv[2];
  getComputedFontSizes(url)
    .then((fontSizes) => {
      console.log(JSON.stringify(fontSizes, null, 2));
    })
    .catch((err) => {
      console.error("Error:", err);
    });
}
