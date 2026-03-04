#!/usr/bin/env python3
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Read markdown file
with open('/tmp/dividend-pro-app/DRIP_Logic_Verification.md', 'r') as f:
    md_content = f.read()

# Convert to HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# Add CSS styling
styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        h2 {{
            color: #2980b9;
            margin-top: 25px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #16a085;
            margin-top: 20px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f8f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
            margin: 15px 0;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        strong {{
            color: #e74c3c;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        blockquote {{
            border-left: 4px solid #95a5a6;
            padding-left: 15px;
            color: #7f8c8d;
            font-style: italic;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Generate PDF
font_config = FontConfiguration()
HTML(string=styled_html).write_pdf(
    '/tmp/dividend-pro-app/DRIP_Logic_Verification.pdf',
    font_config=font_config
)

print("✅ PDF generated successfully: /tmp/dividend-pro-app/DRIP_Logic_Verification.pdf")
