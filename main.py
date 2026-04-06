import sys
import os
import requests
import webview
from src.scraper import getPage, searchq
from src.components import PageComponent, AudioGridComponent, AudioCardComponent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')

if not os.path.exists(DOWNLOADS_DIR):
    os.mkdir(DOWNLOADS_DIR)

app_window = None

class Api:
    def __init__(self):
        self.current_page = 1
        self.is_search = False

    def on_loaded(self):
        # Play the audio effect on loaded natively via Javascript!
        sound_path = os.path.join(ASSETS_DIR, 'on.mp3').replace('\\', '/')
        if os.path.exists(os.path.join(ASSETS_DIR, 'on.mp3')):
            app_window.evaluate_js(f"playSound('file:///{sound_path}')")
        
    def render_items(self, items):
        cards_html = ""
        for item in items:
            cards_html += AudioCardComponent(item)
        return AudioGridComponent(cards_html)

    def load_page(self, direction):
        if direction == -1 and self.current_page == 1:
            return None
        
        self.current_page += direction
        self.is_search = False
        try:
            items = getPage(str(self.current_page))
            return {'html': self.render_items(items), 'page': self.current_page}
        except Exception as e:
            print("Error loading page:", e)
            return None

    def search(self, query):
        if not query.strip():
            return None
        self.is_search = True
        self.current_page = 1
        try:
            items = searchq(query)
            return {'html': self.render_items(items), 'page': self.current_page}
        except Exception as e:
            print("Error searching:", e)
            return None

    def download(self, url, title):
        try:
            r = requests.get(url, stream=True)
            safe_title = title.replace('/', '_').replace('\\', '_').replace(':', '_').replace('"', '_')
            filepath = os.path.join(DOWNLOADS_DIR, f"{safe_title}.mp3")
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded: {safe_title}.mp3 to {filepath}")
            app_window.evaluate_js(f"alert('Download Successful! Saved to downloads folder.')")
        except Exception as e:
            print("Download Failed", e)
            app_window.evaluate_js("alert('Download Failed!')")
            
    def open_downloads(self):
        try:
            os.startfile(DOWNLOADS_DIR)
        except Exception as e:
            print("Could not open folder:", e)


def main():
    print("=" * 40)
    print("  MyInstants WebView App  ")
    print("=" * 40)
    print("\nFetching top trending sounds...")
    
    api = Api()
    
    # We fetch the first page from MyInstants
    items = getPage("1")
    cards_html = ""
    for item in items:
        cards_html += AudioCardComponent(item)
        
    grid_html = AudioGridComponent(cards_html)
    page_html = PageComponent("MyInstants Downloader", grid_html, 1)
    
    print("\nStarting Desktop Window...")
    
    global app_window
    app_window = webview.create_window(
        'MyInstants Downloader', 
        html=page_html, 
        js_api=api,
        width=1200, 
        height=800,
        background_color='#0f172a'
    )
    
    # Bind loaded event to play startup sound
    app_window.events.loaded += api.on_loaded
    webview.start(gui='edgechromium' if sys.platform == 'win32' else 'auto')

if __name__ == "__main__":
    main()
