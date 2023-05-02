def gen(html_text, html_template):
    return html_template.format(content=html_text)


template_forest = """<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');
    body {{
        font-family: 'Quicksand', sans-serif;
        line-height: 1.6;
        background-color: #F0F3F3;
        color: #3D3D3D;
    }}
    h1, h2, h3 {{
        font-weight: 600;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }}
    h1 {{
        font-size: 2em;
        color: #3B8E61;
    }}
    h2 {{
        font-size: 1.5em;
        color: #306152;
    }}
    h3 {{
        font-size: 1.2em;
        color: #1D5135;
    }}
    blockquote {{
        border-left: 4px solid #3B8E61;
        padding-left: 1em;
        margin: 1em 0;
        color: #606060;
        font-style: italic;
        font-size: 1.1em;
    }}
    ul, ol {{
        padding-left: 1em;
    }}
    li {{
        margin-bottom: 0.5em;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
    }}
    th, td {{
        border: 1px solid #CDCDCD;
        padding: 8px;
        text-align: left;
    }}
    th {{
        background-color: #3B8E61;
        font-weight: bold;
        color: #F0F3F3;
    }}
    tr:nth-child(even) {{
        background-color: #C2E9E2;
    }}
    tr:hover {{
        background-color: #95D0B7;
    }}
</style>
</head>
<body>
{content}
</body>
</html>"""

template_ocean = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');
    body {{
        font-family: 'Quicksand', sans-serif;
        line-height: 1.6;
        background-color: #F0F3F3;
        color: #3D3D3D;
    }}
    h1, h2, h3 {{
        font-weight: 600;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }}
    h1 {{
        font-size: 2em;
        color: #007F96;
    }}
    h2 {{
        font-size: 1.5em;
        color: #00607D;
    }}
    h3 {{
        font-size: 1.2em;
        color: #004961;
    }}
    blockquote {{
        border-left: 4px solid #007F96;
        padding-left: 1em;
        margin: 1em 0;
        color: #606060;
        font-style: italic;
        font-size: 1.1em;
    }}
    ul, ol {{
        padding-left: 1em;
    }}
    li {{
        margin-bottom: 0.5em;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
    }}
    th, td {{
        border: 1px solid #CDCDCD;
        padding: 8px;
        text-align: left;
    }}
    th {{
        background-color: #007F96;
        font-weight: bold;
        color: #F0F3F3;
    }}
    tr:nth-child(even) {{
        background-color: #B0E0E6;
    }}
    tr:hover {{
        background-color: #87CEEB;
    }}
</style>
</head>
<body>
{content}
</body>
</html>
"""
