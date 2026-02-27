# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V120 TURBO-RAW)
# 📅 STATUS: 50MS-VELOCITY | 16-AGENTS | V103-FEEL

import os, time, random, sys, threading, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ TURBO CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 50             # 🔥 20 strikes/sec per agent
SESSION_RESTART_SEC = 600          # 10-Min Reset to flush RAM
TOTAL_DURATION = 21000             

def get_driver(agent_id, machine_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--js-flags='--max-old-space-size=512'")
    
    # We keep standard loading to avoid the 'typing but not sending' lag
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def turbo_dispatch(driver, text, delay):
    """Fires 3 unique messages per 50ms strike with zero-wait logic."""
    driver.execute_script("""
        window.praveer_active = true;
        (async function turbo(msg, ms) {
            const findBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            while(window.praveer_active) {
                const box = findBox();
                if (box) {
                    box.focus();
                    for(let i=0; i<3; i++) {
                        const salt = Math.random().toString(36).substring(7);
                        document.execCommand('insertText', false, msg + " " + salt);
                        
                        // Simultaneous Enter + Click for V103 RAW feel
                        const e = new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true});
                        box.dispatchEvent(e);
                        
                        let btn = [...document.querySelectorAll('div[role="button"]')].find(b => b.innerText.includes('Send'));
                        if(btn) btn.click();
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
        time.sleep(3) 
        driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
        driver.get(f"https://www.instagram.com/direct/t/{target}/")
        
        # ⚡ RAW AUTO-START: Detects the box and launches immediately
        timeout = time.time() + 45
        while time.time() < timeout:
            if driver.execute_script("return document.querySelector('div[role=\"textbox\"], textarea') !== null"):
                print(f"🔥 [M{machine_id}-A{agent_id}] TARGET LOCKED. FIRING.")
                turbo_dispatch(driver, text, INTERNAL_DELAY_MS)
                break
            time.sleep(1)
            
        time.sleep(SESSION_RESTART_SEC)
        driver.quit()
    except: pass

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    text = os.environ.get("MESSAGES", "V120").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, text)
            time.sleep(8) 

if __name__ == "__main__":
    main()
