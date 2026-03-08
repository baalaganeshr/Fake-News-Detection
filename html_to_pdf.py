from playwright.sync_api import sync_playwright
import os

html_path = os.path.abspath("Fake_News_Detection_Report.html")
pdf_path = os.path.abspath("Fake_News_Detection_Report.pdf")

print(f"Converting: {html_path}")
print(f"Output: {pdf_path}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{html_path}", wait_until="networkidle")
    page.pdf(
        path=pdf_path,
        format="A4",
        margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
        print_background=True
    )
    browser.close()

print(f"PDF created successfully! Size: {os.path.getsize(pdf_path)} bytes")
