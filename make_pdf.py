"""
Enhance the HTML report with embedded images and print-friendly CSS,
then convert to PDF using Playwright.
"""
import base64, os, re
from playwright.sync_api import sync_playwright

WORKSPACE = r"c:\Users\baala\OneDrive\Desktop\New folder (4)\Fake-News-Detection-System"
HTML_FILE = os.path.join(WORKSPACE, "Fake_News_Detection_Report_40p.html")
PDF_FILE  = os.path.join(WORKSPACE, "Fake_News_Detection_Report_40p.pdf")

# ── Read the HTML ─────────────────────────────────────────────
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ── Embed report images as base64 into the HTML ──────────────
images_to_embed = {
    "report_images/1.png":            "Figure 8.3: Web Application — Home Page",
    "report_images/2.png":            "Figure 8.4: Web Application — Real News Prediction",
    "report_images/output 1.png":     "Figure 8.5: Web Application — Fake News Prediction",
    "report_images/output 2.png":     "Figure 8.6: Web Application — Additional Test Output",
    "report_images/dataset_distribution.png": "Figure 5.1: Dataset Distribution",
    "report_images/confusion_matrix.png":     "Figure 8.1: Confusion Matrix",
    "report_images/model_comparison.png":     "Figure 8.2: Model Comparison",
    "report_images/fake_data_distribution.png": "Figure 5.3: Fake Data Distribution",
}

# Build an image gallery HTML block
img_html_blocks = []
for img_path, caption in images_to_embed.items():
    full_path = os.path.join(WORKSPACE, img_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as imgf:
            b64 = base64.b64encode(imgf.read()).decode()
        img_html_blocks.append(f"""
<div style="text-align:center; margin: 15px 0; page-break-inside: avoid;">
    <img src="data:image/png;base64,{b64}" style="max-width:90%; border:1px solid #ccc; border-radius:4px;" />
    <p style="font-style:italic; font-size:0.9em; margin-top:5px;">{caption}</p>
</div>""")
        print(f"  Embedded: {img_path}")
    else:
        print(f"  Missing: {img_path}")

# Insert images before the "Chapter 9" section (after results chapter)
img_insert = "\n".join(img_html_blocks)
# Find a good place to insert — right before "Chapter 9: Conclusion"
insert_marker = "<h1>Chapter 9: Conclusion and Future Work</h1>"
if insert_marker in html:
    extra_section = f"""
<div style="page-break-before: always;">
<h2>All Output Screenshots and Visualizations</h2>
<p>The following figures present the web application interface, dataset visualizations, confusion matrix, and model comparison chart generated during the project:</p>
{img_insert}
</div>
"""
    html = html.replace(insert_marker, extra_section + insert_marker)
    print("  Inserted image gallery before Chapter 9")
else:
    # Fallback: append before closing body
    html = html.replace("</body>", img_insert + "\n</body>")
    print("  Appended images at end of document")

# ── Add print-friendly CSS ────────────────────────────────────
print_css = """
<style>
@media print {
    body { font-size: 10.5pt !important; line-height: 1.45 !important; }
    .jp-Cell { page-break-inside: avoid; }
    .jp-MarkdownOutput { page-break-inside: auto; }
    pre { page-break-inside: avoid; white-space: pre-wrap; word-wrap: break-word; font-size: 7.5pt !important; line-height: 1.2 !important; padding: 4px !important; margin: 4px 0 !important; }
    h1 { page-break-before: always; font-size: 16pt !important; margin-top: 8px !important; }
    h2 { font-size: 13pt !important; margin-top: 6px !important; }
    h3 { font-size: 11.5pt !important; margin-top: 4px !important; }
    table { page-break-inside: avoid; font-size: 9pt; }
    img { max-width: 85% !important; page-break-inside: avoid; }
    code { font-size: 7.5pt !important; }
    p { margin: 4px 0 !important; }
    ul, ol { margin: 4px 0 !important; padding-left: 20px !important; }
    li { margin: 1px 0 !important; }
    .jp-OutputArea-output { margin: 0 !important; padding: 2px !important; }
    .jp-Cell-inputWrapper { margin: 2px 0 !important; }
}
@page {
    size: A4;
    margin: 18mm 14mm 18mm 14mm;
}
body {
    max-width: 900px;
    margin: 0 auto;
    padding: 15px;
    font-size: 10.5pt;
    line-height: 1.45;
}
/* Compact code blocks */
.jp-InputArea-editor { font-size: 8px !important; line-height: 1.2 !important; }
.highlight pre { font-size: 8px !important; line-height: 1.2 !important; padding: 4px !important; }
.jp-RenderedHTMLCommon pre { font-size: 8px !important; line-height: 1.2 !important; }
.jp-OutputArea-output pre { font-size: 8px !important; line-height: 1.2 !important; }
.jp-Cell-inputWrapper { margin-bottom: 2px !important; }
.jp-Cell-outputWrapper { margin-bottom: 2px !important; }
</style>
"""
html = html.replace("</head>", print_css + "\n</head>")
print("  Added print-friendly CSS")

# ── Write enhanced HTML ───────────────────────────────────────
enhanced_html = os.path.join(WORKSPACE, "Fake_News_Detection_Report_40p_final.html")
with open(enhanced_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"  Enhanced HTML: {os.path.getsize(enhanced_html):,} bytes")

# ── Convert to PDF via Playwright ─────────────────────────────
print("\nConverting to PDF...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{enhanced_html}", wait_until="networkidle", timeout=60000)
    # Wait for MathJax / KaTeX rendering if any
    page.wait_for_timeout(3000)
    page.pdf(
        path=PDF_FILE,
        format="A4",
        margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
        print_background=True,
        display_header_footer=True,
        header_template='<div style="font-size:8px; width:100%; text-align:center; color:#888;">Fake News Detection Using Machine Learning — Project Report</div>',
        footer_template='<div style="font-size:8px; width:100%; text-align:center; color:#888;">Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
    )
    browser.close()

size = os.path.getsize(PDF_FILE)
print(f"\nPDF created: {PDF_FILE}")
print(f"Size: {size:,} bytes ({size/1024:.0f} KB)")
print("Done!")
