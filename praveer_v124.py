# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V124 INFINITE-VELOCITY)
# 📅 STATUS: DOM-BLOAT-FIXED | 10-MIN-PURGE | V103-STRIKE

import os, time, random, sys, threading, base64, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ PERFORMANCE CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 50             
PURGE_INTERVAL_SEC = 600           # 🔥 Hard reset every 10 mins to kill lag
TOTAL_DURATION = 21000             

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # 🛡️ Limit RAM usage per agent to prevent slowdowns
    chrome_options.add_argument("--js-flags='--max-old-space-size=512'")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def v124_purge_dispatch(driver, encoded_text, delay):
    """Fires messages with high-priority execution."""
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        (async function fire(b64, ms) {
            const msg = decodeURIComponent(escape(atob(b64)));
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    const salt = Math.random().toString(36).substring(7);
                    document.execCommand('insertText', false, msg + " " + salt);
                    
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    box.dispatchEvent(new KeyboardEvent('keyup', { key: ' ', bubbles: true }));

                    let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => 
                        b.innerText === 'Send' || b.textContent === 'Send'
                    );

                    if (btn && !btn.disabled) {
                        btn.click();
                    } else {
                        box.dispatchEvent(new KeyboardEvent('keydown', {
                            key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
                        }));
                    }
                    window.msg_count++;
                }
                await new Promise(r => setTimeout(r, ms));
            }
        })(arguments[0], arguments[1]);
    """, encoded_text, delay)

def run_agent(agent_id, machine_id, cookie, target, encoded_text):
    start_time = time.time()
    while (time.time() - start_time) < TOTAL_DURATION:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            time.sleep(4)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(12)
            
            v124_purge_dispatch(driver, encoded_text, INTERNAL_DELAY_MS)

            # ⏳ Monitor for 10 minutes, then PURGE
            cycle_start = time.time()
            while (time.time() - cycle_start) < PURGE_INTERVAL_SEC:
                time.sleep(30)
                try:
                    cnt = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Speed: Stable | Sent: {cnt}")
                    sys.stdout.flush()
                except: break
        except: pass
        finally:
            if driver:
                driver.quit()
            print(f"🧹 [M{machine_id}-A{agent_id}] PURGING DOM & RAM. RESTARTING...")
            time.sleep(5) # Cooldown before fresh start

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    raw_text = os.environ.get("MESSAGES", "").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    encoded_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, encoded_text)
            time.sleep(8)

if __name__ == "__main__":
    main()
