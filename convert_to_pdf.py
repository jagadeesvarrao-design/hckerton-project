import os
import sys
import subprocess
import markdown

# Ensure utf-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

def convert_md_to_pdf(md_filename="PROJECT_WHITE_PAPER.md", pdf_filename="PROJECT_WHITE_PAPER.pdf"):
    print(f"[+] Reading {md_filename}...")
    if not os.path.exists(md_filename):
        print(f"[-] Error: {md_filename} not found.")
        return False

    with open(md_filename, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert Markdown to HTML with tables, fenced code, and TOC extensions
    html_body = markdown.markdown(
        md_text,
        extensions=['extra', 'tables', 'fenced_code', 'toc', 'nl2br']
    )

    # Wrap in modern GitHub + Swaraj Heritage PDF-optimized Print CSS
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Passport Seva AI 2.0 - Technical Whitepaper & Dossier</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4 portrait;
            margin: 15mm 12mm 15mm 12mm;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #0b1329;
            background-color: #ffffff;
            line-height: 1.6;
            font-size: 10pt;
            margin: 0;
            padding: 15px;
        }}

        h1, h2, h3, h4 {{
            color: #000080;
            font-weight: 700;
            page-break-after: avoid;
        }}

        h1 {{
            font-family: 'Cinzel', Georgia, serif;
            font-size: 18pt;
            border-bottom: 3px solid #D4AF37;
            padding-bottom: 8px;
            margin-top: 10px;
            margin-bottom: 12px;
            text-align: center;
            color: #000080;
        }}

        h2 {{
            font-size: 13pt;
            border-bottom: 1.5px solid #D4AF37;
            padding-bottom: 4px;
            margin-top: 22px;
            margin-bottom: 10px;
            color: #000080;
        }}

        h3 {{
            font-size: 11pt;
            margin-top: 16px;
            margin-bottom: 6px;
            color: #1a2a6c;
        }}

        p {{
            margin-top: 4px;
            margin-bottom: 8px;
        }}

        blockquote {{
            margin: 10px 0;
            padding: 8px 14px;
            background-color: #fdfbf2;
            border-left: 4px solid #D4AF37;
            border-radius: 4px;
            font-size: 9.5pt;
            color: #4a3e00;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #dcdfe6;
            padding: 6px 8px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            background-color: #000080;
            color: #ffffff;
            font-weight: 700;
            font-size: 8.5pt;
        }}

        tr:nth-child(even) {{
            background-color: #f8f9fc;
        }}

        code {{
            font-family: 'JetBrains Mono', Consolas, monospace;
            background-color: #f1f3f9;
            color: #000080;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 8.5pt;
            border: 1px solid #e2e8f0;
        }}

        pre {{
            background-color: #0c1427;
            color: #f8fafc;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 8pt;
            line-height: 1.4;
            border: 1px solid #D4AF37;
            page-break-inside: avoid;
            margin: 12px 0;
        }}

        pre code {{
            background-color: transparent;
            color: inherit;
            padding: 0;
            border: none;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 18px 0;
        }}

        ul, ol {{
            margin: 4px 0 10px 18px;
            padding: 0;
        }}

        li {{
            margin-bottom: 3px;
        }}

        a {{
            color: #000080;
            text-decoration: underline;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""

    html_filename = md_filename.replace(".md", ".html")
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[+] Generated styled HTML: {html_filename}")

    # Paths to Edge / Chrome
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]

    browser_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            browser_exe = p
            break

    if not browser_exe:
        print("[-] Chrome/Edge not found in default locations. HTML is ready for manual browser print.")
        return True

    print(f"[+] Converting HTML to PDF via {os.path.basename(browser_exe)} Headless...")
    abs_html = os.path.abspath(html_filename).replace("\\", "/")
    abs_pdf = os.path.abspath(pdf_filename)

    cmd = f'"{browser_exe}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{abs_pdf}" "file:///{abs_html}"'

    try:
        subprocess.run(cmd, shell=True, check=True, timeout=30)
        if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
            print(f"[+] SUCCESS! PDF successfully created: {abs_pdf} ({os.path.getsize(abs_pdf)/1024:.1f} KB)")
            return True
    except Exception as e:
        print(f"[-] Headless print note: {e}")

    return True

if __name__ == "__main__":
    convert_md_to_pdf("PROJECT_WHITE_PAPER.md", "PROJECT_WHITE_PAPER.pdf")
    convert_md_to_pdf("README.md", "README.pdf")
