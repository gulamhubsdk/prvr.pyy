# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V117 HEARTBEAT)
# 📅 STATUS: ANTI-TIMEOUT-ACTIVE | 50MS-TRIPLE-STRIKE | 8-AGENTS

import os, time, random, sys, threading, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 50             
SESSION_RESTART_SEC = 1800         # Increased to 30 mins
TOTAL_DURATION = 21000

def get_driver(agent_id, machine_id):
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 🛡️ RESOURCE STRIPPING
    prefs = {"profile.managed_default_content_settings.images": 2, "profile.managed_default_content_settings.stylesheets": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def god_mode_dispatch(driver, text, delay):
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        (async function godMode(msg, ms) {
            const findBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            while(window.praveer_active) {
                const box = findBox();
                if (box) {
                    box.focus();
                    for(let i=0; i<3; i++) {
                        const salt = Math.random().toString(36).substring(5);
                        document.execCommand('insertText', false, msg + " \\u200B" + salt);
                        const e = new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true});
                        box.dispatchEvent(e);
                        window.msg_count++;
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
        time.sleep(5)
        driver.add_cookie({'name': 'sessionid', 'value': cookie, 'path': '/', 'domain': '.instagram.com'})
        driver.get(f"https://www.instagram.com/direct/t/{target}/")
        time.sleep(15)
        
        print(f"🔱 [M{machine_id}-A{agent_id}] GOD-MODE ENGAGED.")
        god_mode_dispatch(driver, text, INTERNAL_DELAY_MS)
        
        # --- ❤️ HEARTBEAT MONITOR ---
        # This keeps GitHub from timing out by printing logs every 30s
        start_cycle = time.time()
        while (time.time() - start_cycle) < SESSION_RESTART_SEC:
            time.sleep(30)
            try:
                current_count = driver.execute_script("return window.msg_count;")
                print(f"💓 [M{machine_id}-A{agent_id}] Status: ACTIVE | Local Sent: {current_count}")
            except:
                break # Driver likely crashed/logged out
                
        driver.quit()
    except Exception as e:
        print(f"⚠️ Agent {agent_id} Error: {e}")

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    text = os.environ.get("MESSAGES", "SYSTEM OWNED").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, text)
            time.sleep(15)

if __name__ == "__main__":
    main()
