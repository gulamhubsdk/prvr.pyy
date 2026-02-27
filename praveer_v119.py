# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V123 HARD-STRIKE)
# 📅 STATUS: TOJI-TEXT-LOCKED | KEY-STATE-FORCED | 8-AGENTS

import os, time, random, sys, threading, base64
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 50             
SESSION_RESTART_SEC = 900          

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def v123_hard_dispatch(driver, encoded_text, delay):
    """Bypasses UI stalls by forcing a KeyUp state change after injection."""
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
                    
                    // 1. ATOMIC INJECTION
                    document.execCommand('insertText', false, msg + " " + salt);
                    
                    // 2. FORCE VALIDATION (The Fix for 'Just Typing')
                    // Firing 'input' + 'keyup' forces the UI to enable the Send button
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    box.dispatchEvent(new KeyboardEvent('keyup', { key: ' ', bubbles: true }));

                    const clickSend = () => {
                        let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => 
                            b.innerText === 'Send' || b.textContent === 'Send'
                        );
                        if (btn && !btn.disabled) {
                            btn.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
                            btn.click();
                            return true;
                        }
                        return false;
                    };

                    // 3. ATOMIC SEND
                    if (!clickSend()) {
                        // Hard Fallback to Trusted Enter
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
    while True:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(15)
            
            v123_hard_dispatch(driver, encoded_text, INTERNAL_DELAY_MS)

            cycle_start = time.time()
            while (time.time() - cycle_start) < SESSION_RESTART_SEC:
                time.sleep(30)
                try:
                    cnt = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Total: {cnt} | V123-STRIKE")
                    sys.stdout.flush()
                except: break
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    raw_text = os.environ.get("MESSAGES", "").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    encoded_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, encoded_text)
            time.sleep(10)

if __name__ == "__main__":
    main()
