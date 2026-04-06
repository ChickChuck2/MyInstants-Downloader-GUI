def PageComponent(title, body, page_num=1):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f172a;
            --surface: #1e293b;
            --text: #f1f5f9;
            --text-secondary: #94a3b8;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
        }}
        .menubar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--surface);
            padding: 15px 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
            flex-wrap: wrap;
            gap: 15px;
        }}
        .menu-group {{ display: flex; gap: 15px; align-items: center; }}
        input[type="text"] {{
            padding: 10px; border-radius: 6px; border: none; outline: none; background: #334155; color: white; width: 200px;
        }}
        .menu-btn {{
            background: #3b82f6; color: white; padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; transition: background 0.2s;
        }}
        .menu-btn:hover {{ background: #2563eb; }}
        .nav-btn {{ background: #475569; }}
        .nav-btn:hover {{ background: #334155; }}
        .folder-btn {{ background: #10b981; }}
        .folder-btn:hover {{ background: #059669; }}
        .page-indicator {{ font-weight: bold; padding: 0 10px; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .card {{
            background: var(--surface);
            padding: 25px 15px;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .play-button {{
            width: 90px;
            height: 90px;
            border-radius: 50%;
            border: 4px solid rgba(255, 255, 255, 0.1);
            cursor: pointer;
            outline: none;
            margin-bottom: 20px;
            box-shadow: inset 0 -4px 0 rgba(0, 0, 0, 0.4), 0 8px 15px rgba(0,0,0,0.4);
            transition: filter 0.2s, transform 0.1s;
        }}
        .play-button:hover {{
            filter: brightness(1.2);
        }}
        .play-button:active {{
            transform: scale(0.95);
            box-shadow: inset 0 2px 0 rgba(0, 0, 0, 0.4), 0 4px 10px rgba(0,0,0,0.4);
        }}
        .title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 8px;
            word-break: break-word;
            min-height: 40px;
            display: flex;
            align-items: center;
        }}
        .size {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 20px;
        }}
        .download-btn {{
            background: #3b82f6;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.95rem;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
            width: 100%;
        }}
        .download-btn:hover {{ background: #2563eb; }}
        .download-btn:active {{ background: #1d4ed8; }}
        
        #loading {{
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            padding: 20px 40px;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: bold;
            z-index: 9999;
        }}
    </style>
</head>
<body>
    <div id="loading">Loading... Please wait...</div>

    <div class="menubar">
        <div class="menu-group">
            <input type="text" id="searchInput" placeholder="Search sounds..." onkeydown="if(event.key === 'Enter') handleSearch()">
            <button class="menu-btn" onclick="handleSearch()">Search</button>
        </div>
        <div class="menu-group">
            <button class="menu-btn nav-btn" onclick="handlePage(-1)">&larr; Prev</button>
            <span id="page-indicator" class="page-indicator">Page {page_num}</span>
            <button class="menu-btn nav-btn" onclick="handlePage(1)">Next &rarr;</button>
        </div>
        <div class="menu-group">
            <button class="menu-btn folder-btn" onclick="window.pywebview.api.open_downloads()">📂 Open Downloads Folder</button>
        </div>
    </div>
    
    <div id="grid-container">
    {body}
    </div>
    
    <script>
        let currentAudio = null;

        function showLoading() {{
            document.getElementById('loading').style.display = 'block';
        }}
        
        function hideLoading() {{
            document.getElementById('loading').style.display = 'none';
        }}

        async function handleSearch() {{
            const val = document.getElementById('searchInput').value;
            showLoading();
            const data = await window.pywebview.api.search(val);
            if (data) {{
                document.getElementById('grid-container').innerHTML = data.html;
                document.getElementById('page-indicator').innerText = 'Page ' + data.page;
            }}
            hideLoading();
        }}
        
        async function handlePage(direction) {{
            showLoading();
            const data = await window.pywebview.api.load_page(direction);
            if (data) {{
                document.getElementById('grid-container').innerHTML = data.html;
                document.getElementById('page-indicator').innerText = 'Page ' + data.page;
            }}
            hideLoading();
        }}

        function playSound(url) {{
            if (currentAudio) {{
                currentAudio.pause();
                currentAudio.currentTime = 0;
            }}
            currentAudio = new Audio(url);
            currentAudio.play();
        }}
        
        async function triggerDownload(btn, url, title) {{
            btn.innerHTML = 'Downloading...';
            btn.style.background = '#64748b';
            try {{
                await window.pywebview.api.download(url, title);
            }} finally {{
                btn.innerHTML = '⬇ Download';
                btn.style.background = '#3b82f6';
            }}
        }}

        window.onload = function() {{
            hideLoading();
        }};
    </script>
</body>
</html>"""

def AudioGridComponent(children):
    return f'<div class="grid">\n{children}\n</div>'

def AudioCardComponent(item):
    title_escaped = item['title'].replace("'", "\\'").replace('"', '&quot;')
    url = item['url']
    color = item['color']
    size = item['size_kb']
    
    return f"""
    <div class="card">
        <button class="play-button" style="background-color: {color};" onclick="playSound('{url}')"></button>
        <div class="title">{item['title']}</div>
        <div class="size">{size} KB</div>
        <button class="download-btn" onclick="triggerDownload(this, '{url}', '{title_escaped}')">⬇ Download</button>
    </div>
    """
