#!/usr/bin/env python3
"""
GSA Report HTML Converter
Converts original GSA Shot Quality Evolution HTML reports to the dark theme GSA style.

Usage:
    python convert_gsa_report.py input.html output.html
    
Or as a module:
    from convert_gsa_report import convert_gsa_report
    html_output = convert_gsa_report(html_input, title="Custom Title")
"""

import re
import sys
from typing import Optional
from bs4 import BeautifulSoup


def extract_report_data(html: str) -> dict:
    """
    Extract tabs, headers, and table data from the original GSA report HTML.
    
    Returns dict with:
        - title: str (extracted from header if possible)
        - columns: list of column header strings
        - tabs: dict mapping tab_name -> list of tables
            each table is a dict with 'title' (optional) and 'rows' (list of row tuples)
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract title from header if present
    title = "GSA Shot Quality Evolution"
    title_span = soup.select_one('h1 span.text-\\[\\#D5AA2A\\]')
    if title_span:
        title = title_span.get_text(strip=True)
    
    # Extract tab names
    tabs_ul = soup.select_one('#tabs')
    tab_names = []
    if tabs_ul:
        for link in tabs_ul.select('a'):
            tab_names.append(link.get_text(strip=True))
    
    # Extract tab contents
    tabs_data = {}
    tab_contents = soup.select('.tab-content')
    
    for i, tab_content in enumerate(tab_contents):
        tab_name = tab_names[i] if i < len(tab_names) else f"Tab {i+1}"
        tables_in_tab = []
        
        # Find all tables and optional h2 titles before them
        tables = tab_content.select('table')
        h2_titles = tab_content.select('h2')
        
        # Map h2 titles to tables (h2 appears before table)
        h2_texts = [h2.get_text(strip=True) for h2 in h2_titles]
        
        for j, table in enumerate(tables):
            table_data = {
                'title': h2_texts[j] if j < len(h2_texts) else None,
                'rows': [],
                'headers': []
            }
            
            # Extract headers
            thead = table.select_one('thead')
            if thead:
                for th in thead.select('th'):
                    header_text = th.get_text(strip=True)
                    table_data['headers'].append(header_text)
            
            # Extract rows
            tbody = table.select_one('tbody')
            if tbody:
                for tr in tbody.select('tr'):
                    row_values = []
                    for td in tr.select('td'):
                        cell_text = td.get_text(strip=True)
                        # Normalize some values
                        if cell_text == "NO SHOTS/RALLIES":
                            cell_text = "N/A"
                        row_values.append(cell_text)
                    if row_values:
                        table_data['rows'].append(tuple(row_values))
            
            tables_in_tab.append(table_data)
        
        tabs_data[tab_name] = tables_in_tab
    
    # Extract column headers from first table
    columns = []
    if tabs_data and list(tabs_data.values()):
        first_tab_tables = list(tabs_data.values())[0]
        if first_tab_tables and first_tab_tables[0]['headers']:
            columns = first_tab_tables[0]['headers']
    
    return {
        'title': title,
        'columns': columns,
        'tabs': tabs_data
    }


def generate_gsa_html(data: dict, title: Optional[str] = None, subtitle: Optional[str] = None) -> str:
    """
    Generate GSA dark theme HTML from extracted data.
    
    Args:
        data: dict from extract_report_data()
        title: optional override for report title
        subtitle: optional subtitle (e.g., player name)
    
    Returns:
        HTML string in GSA dark theme style
    """
    report_title = title or data.get('title', 'GSA Shot Quality Evolution')
    columns = data.get('columns', [])
    tabs_data = data.get('tabs', {})
    
    # Determine if this is a multi-year report (many columns) or comparison (few columns)
    num_data_cols = len(columns) - 1 if columns else 0  # subtract stat column
    
    # Extract year/period info from column headers for subtitle
    if not subtitle and columns:
        # Try to extract player name and context from headers
        sample_header = columns[1] if len(columns) > 1 else ""
        # Pattern like "TSITSIPAS 2026 HARD"
        match = re.match(r'([A-Z]+)\s+(\d{4})\s+(\w+)', sample_header)
        if match:
            player = match.group(1).title()
            surface = match.group(3).title()
            if num_data_cols > 2:
                # Multi-year
                years = []
                for col in columns[1:]:
                    year_match = re.search(r'(\d{4})', col)
                    if year_match:
                        years.append(year_match.group(1))
                if years:
                    subtitle = f"{player} – {surface} ({min(years)}-{max(years)})"
            else:
                subtitle = f"{player} – {surface} Comparison"
    
    # Generate tab buttons
    tab_ids = list(tabs_data.keys())
    colors = ['orange', 'blue', 'purple', 'green']
    
    tab_buttons = []
    for i, tab_name in enumerate(tab_ids):
        active = ' active' if i == 0 else ''
        color = colors[i % len(colors)]
        tab_id = re.sub(r'[^a-z0-9]+', '-', tab_name.lower()).strip('-')
        tab_buttons.append(f'      <button class="tab-btn{active} {color}" data-tab="{tab_id}">{tab_name}</button>')
    
    # Generate tab contents
    tab_contents = []
    for i, (tab_name, tables) in enumerate(tabs_data.items()):
        tab_id = re.sub(r'[^a-z0-9]+', '-', tab_name.lower()).strip('-')
        display = '' if i == 0 else ' style="display:none;"'
        
        sections_html = []
        for table in tables:
            # Section title if present
            section_title = ""
            if table.get('title'):
                section_title = f'<h3 class="section-title">{table["title"]}</h3>'
            
            # Generate header cells (skip first empty header for stat column)
            headers = table.get('headers', columns)
            header_cells = ''
            for h in headers[1:]:
                # Shorten header if needed
                short_h = re.sub(r'^[A-Z]+\s+', '', h)  # Remove player name prefix
                header_cells += f'<th class="th-year">{h}</th>'
            
            # Generate rows
            rows_html = []
            for row in table.get('rows', []):
                if not row:
                    continue
                stat_name = row[0]
                value_cells = ''
                for j, val in enumerate(row[1:]):
                    year_label = headers[j+1] if j+1 < len(headers) else f"Col {j+1}"
                    # Shorten label for mobile
                    short_label = re.search(r'(\d{4})', year_label)
                    short_label = short_label.group(1) if short_label else year_label
                    #value_cells += f'<td class="num" data-label="{short_label}">{val}</td>'
                    value_cells += f'<td class="num" data-label="{year_label}">{val}</td>'
                
                rows_html.append(f'''              <tr>
                <td class="col-stat" data-label="Stat">{stat_name}</td>
                {value_cells}
              </tr>''')
            
            table_html = f'''
        {section_title}
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th class="th-stat">Statistic</th>
                {header_cells}
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows_html)}
            </tbody>
          </table>
        </div>'''
            sections_html.append(table_html)
        
        tab_contents.append(f'''    <div id="{tab_id}" class="tab-content"{display}>
      <section class="section">
        {"".join(sections_html)}
      </section>
    </div>''')
    
    # Determine badges
    badges = []
    if num_data_cols > 2:
        badges.append(('<span class="pill pill-gold">' + f'{num_data_cols}-Year Analysis</span>'))
    else:
        badges.append('<span class="pill pill-gold">Performance Comparison</span>')
    #badges.append('<span class="pill">Hard Court</span>')
    badges.append('<span class="pill">GSA Analytics</span>')
    
    # Build final HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{report_title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {{
      --bg: #050816;
      --accent-gold: #D5AA2A;
      --accent-blue: #3b82f6;
      --accent-orange: #f97316;
      --accent-purple: #a855f7;
      --accent-green: #22c55e;
      --text-main: #e5e7eb;
      --text-muted: #9ca3af;
      --border-subtle: rgba(148, 163, 184, 0.3);
      --shadow-soft: 0 18px 40px rgba(15, 23, 42, 0.7);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #1e293b 0, #020617 55%);
      color: var(--text-main);
      line-height: 1.5;
      padding: 32px 16px 48px;
    }}

    @media (min-width: 768px) {{ body {{ padding: 40px 32px 64px; }} }}

    .page {{ max-width: 1400px; margin: 0 auto; }}

    .header {{ text-align: center; margin-bottom: 28px; }}

    .title-sub {{
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}

    .title-main {{
      font-size: clamp(1.8rem, 4vw, 2.6rem);
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      background: linear-gradient(135deg, #D5AA2A, #f59e0b);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}

    .title-player {{
      font-size: 1.2rem;
      color: var(--text-main);
      margin-top: 10px;
      font-weight: 500;
    }}

    .badge-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
      margin-top: 16px;
    }}

    .pill {{
      font-size: 0.75rem;
      padding: 5px 12px;
      border-radius: 999px;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      background: rgba(2,6,23,0.35);
    }}
    .pill-gold {{
      border-color: var(--accent-gold);
      color: var(--accent-gold);
      background: rgba(213, 170, 42, 0.1);
      font-weight: 600;
    }}

    .tabs-wrapper {{
      overflow-x: auto;
      margin-bottom: 20px;
      padding-bottom: 8px;
    }}

    .tabs {{
      display: flex;
      gap: 6px;
      min-width: max-content;
    }}

    .tab-btn {{
      padding: 10px 14px;
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
      background: rgba(2, 6, 23, 0.5);
      color: var(--text-muted);
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }}

    .tab-btn:hover {{ background: rgba(213, 170, 42, 0.1); border-color: var(--accent-gold); }}

    .tab-btn.active.orange {{ background: rgba(249, 115, 22, 0.15); border-color: var(--accent-orange); color: var(--accent-orange); }}
    .tab-btn.active.blue {{ background: rgba(59, 130, 246, 0.15); border-color: var(--accent-blue); color: var(--accent-blue); }}
    .tab-btn.active.purple {{ background: rgba(168, 85, 247, 0.15); border-color: var(--accent-purple); color: var(--accent-purple); }}
    .tab-btn.active.green {{ background: rgba(34, 197, 94, 0.15); border-color: var(--accent-green); color: var(--accent-green); }}

    .section {{
      padding: 20px;
      border-radius: 20px;
      background: radial-gradient(circle at top left, #111827 0, #020617 70%);
      border: 1px solid rgba(148, 163, 184, 0.4);
      box-shadow: var(--shadow-soft);
    }}

    .section-title {{
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--accent-gold);
      text-align: center;
      margin: 24px 0 16px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }}

    .section-title:first-child {{ margin-top: 0; }}

    .table-wrap {{
      overflow-x: auto;
      border-radius: 14px;
      border: 1px solid var(--border-subtle);
      background: rgba(2,6,23,0.25);
      margin-bottom: 20px;
    }}

    .table-wrap:last-child {{ margin-bottom: 0; }}

    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      min-width: 700px;
    }}

    thead th {{
      text-align: center;
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-main);
      padding: 12px 8px;
      background: linear-gradient(135deg, #D5AA2A, #b8941f);
      border-bottom: 1px solid var(--border-subtle);
      white-space: nowrap;
    }}

    thead th.th-stat {{
      text-align: left;
      border-top-left-radius: 14px;
      min-width: 200px;
      padding-left: 14px;
    }}

    thead th:last-child {{ border-top-right-radius: 14px; }}

    tbody td {{
      padding: 10px 8px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.15);
      font-size: 0.85rem;
    }}

    tbody tr:hover td {{ background: rgba(213, 170, 42, 0.06); }}

    tbody tr:last-child td {{ border-bottom: none; }}

    .col-stat {{
      font-weight: 500;
      text-align: left;
      color: var(--text-main);
      padding-left: 14px;
    }}

    .num {{
      text-align: center;
      font-variant-numeric: tabular-nums;
      font-weight: 500;
    }}

    footer {{
      margin-top: 18px;
      font-size: 0.8rem;
      color: var(--text-muted);
      text-align: right;
    }}

    /* Mobile */
    @media (max-width: 900px) {{
      body {{ padding: 18px 12px 28px; }}
      .tab-btn {{ padding: 8px 10px; font-size: 0.72rem; }}
      .section {{ padding: 14px; }}

      .table-wrap {{ overflow: visible; border: none; background: transparent; }}
      table {{ border-collapse: separate; border-spacing: 0 10px; min-width: unset; }}
      thead {{ display: none; }}
      tbody tr {{
        display: block;
        border: 1px solid rgba(148, 163, 184, 0.3);
        background: rgba(2, 6, 23, 0.5);
        border-radius: 14px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.5);
        overflow: hidden;
      }}
      tbody td {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 8px 12px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        font-size: 0.82rem;
        text-align: right !important;
      }}
      tbody td:last-child {{ border-bottom: none; }}
      tbody td::before {{
        content: attr(data-label);
        flex: 1 1 auto;
        text-align: left;
        color: var(--text-muted);
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
      }}
      tbody td.col-stat {{
        background: linear-gradient(135deg, rgba(213, 170, 42, 0.15), rgba(213, 170, 42, 0.05));
        font-weight: 600;
        text-align: left !important;
        padding: 12px;
      }}
      tbody td.col-stat::before {{ display: none; }}
    }}
  </style>
</head>

<body>
  <div class="page">
    <header class="header">
      <div class="title-sub">GSA Analytics Report</div>
      <h1 class="title-main">{report_title}</h1>
      {f'<div class="title-player">{subtitle}</div>' if subtitle else ''}
      <div class="badge-row">
        {chr(10).join(badges)}
      </div>
    </header>

    <div class="tabs-wrapper">
      <div class="tabs">
{chr(10).join(tab_buttons)}
      </div>
    </div>

{chr(10).join(tab_contents)}

    <footer>GSA owned.</footer>
  </div>

  <script>
    document.querySelectorAll('.tab-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).style.display = 'block';
      }});
    }});
  </script>
</body>
</html>
'''
    return html


def convert_gsa_report(html_input: str, title: Optional[str] = None, subtitle: Optional[str] = None) -> str:
    """
    Main conversion function. Takes original GSA report HTML and returns dark theme styled HTML.
    
    Args:
        html_input: Original HTML string
        title: Optional title override
        subtitle: Optional subtitle (e.g., player name and context)
    
    Returns:
        Converted HTML string in GSA dark theme
    """
    data = extract_report_data(html_input)
    return generate_gsa_html(data, title=title, subtitle=subtitle)


def convert_file(input_path: str, output_path: str, title: Optional[str] = None, subtitle: Optional[str] = None) -> None:
    """
    Convert an HTML file and write output to a new file.
    
    Args:
        input_path: Path to input HTML file
        output_path: Path for output HTML file
        title: Optional title override
        subtitle: Optional subtitle
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        html_input = f.read()
    
    html_output = convert_gsa_report(html_input, title=title, subtitle=subtitle)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"Converted: {input_path} -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_gsa_report.py input.html output.html [title] [subtitle]")
        print("\nExample:")
        print("  python convert_gsa_report.py report.html styled_report.html")
        print('  python convert_gsa_report.py report.html styled.html "Shot Quality" "Tsitsipas - Hard Court"')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else None
    subtitle = sys.argv[4] if len(sys.argv) > 4 else None
    
    convert_file(input_file, output_file, title=title, subtitle=subtitle)
