# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V115 TRIPLE-ANCHOR)
# 📅 STATUS: 3-MSG-BURST | 8-AGENTS-TOTAL | ANTI-RELOAD

import os, time, random, sys, threading, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ SPEED CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 150            # Delay between Triple-Taps
SESSION_RESTART_SEC = 900          
TOTAL_DURATION = 21000

BROWSER_LAUNCH_LOCK = threading.Lock()

def get_driver(agent_id, machine_id):
    with BROWSER_LAUNCH_LOCK:
        time.sleep(agent_id * 5) # Staggered entry for account safety
        chrome_options = Options()
        chrome_options.page_load_strategy = 'eager'
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # 🛡️ STABILITY: Block images/CSS to stop the flickering
        prefs = {"profile.managed_default_content_settings.images": 2, "profile.managed_default_content_settings.stylesheets": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
        return driver

def triple_anchor_dispatch(driver, text, delay):
    """Fires 3 unique messages and locks onto the box during reloads."""
    driver.execute_script("""
        window.praveer_active = true;
        (async function blitz(msg, ms) {
            const findBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            while(window.praveer_active) {
                const box = findBox();
                if (box) {
                    box.focus();
                    // Triple-Strike Loop
                    for(let i=0; i<3; i++) {
                        const salt = Math.random().toString(36).substring(7);
                        document.execCommand('insertText', false, msg + " \\u200B" + salt);
                        const e = new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true});
                        box.dispatchEvent(e);
                    }
                }
                await new Promise(r => setTimeout(r, ms));
            }
        })(arguments[0], arguments[1]);
    """, text, delay)

def run_agent(agent_id, machine_id, cookie, target, text):
    try:
        driver = get_driver(agent_id, machine_id)
        driver.get("https://www.instagram.com/")
        time.sleep(4)
        driver.add_cookie({'name': 'sessionid', 'value': cookie, 'path': '/', 'domain': '.instagram.com'})
        driver.get(f"https://www.instagram.com/direct/t/{target}/")
        
        # Handshake wait
        time.sleep(15)
        print(f"🔥 [M{machine_id}-A{agent_id}] Triple-Anchor Active.")
        triple_anchor_dispatch(driver, text, INTERNAL_DELAY_MS)
        
        time.sleep(SESSION_RESTART_SEC)
        driver.quit()
    except Exception as e:
        print(f"⚠️ Error: {e}")

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    text = os.environ.get("MESSAGES", "V115 OWNED").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, text)
            time.sleep(10)

if __name__ == "__main__":
    main()
