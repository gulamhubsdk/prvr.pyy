# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V119 VORTEX-CRON)
# 📅 STATUS: 16-AGENTS-ACTIVE | RELOAD-PROOF | BUTTON-FORCE

import os, time, random, sys, threading, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ VORTEX CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 50             # 🔥 20 strikes/sec per agent
SESSION_RESTART_SEC = 600          # 10-Min Reset to prevent RAM crash (143)
TOTAL_DURATION = 21000             

def get_driver(agent_id, machine_id):
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--js-flags='--max-old-space-size=512'")
    
    # 🛡️ RESOURCE SHIELD: Block CSS/Images to stabilize UI
    prefs = {"profile.managed_default_content_settings.images": 2, "profile.managed_default_content_settings.stylesheets": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def vortex_dispatch(driver, text, delay):
    """Fires 3 unique messages, scrolls to bottom, and forces Send button."""
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        (async function vortex(msg, ms) {
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            const filler = "\\u3164\\u2060\\u034F";
            const wall = (filler + "\\n").repeat(50); 
            
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    // Force box back into view if spam pushes it away
                    box.scrollIntoView({behavior: "instant", block: "end"});
                    box.focus();
                    
                    // Triple-Strike Burst
                    for(let i=0; i<3; i++) {
                        let payload = (window.msg_count % 2 === 0) ? msg : wall;
                        const salt = Math.random().toString(36).substring(5);
                        document.execCommand('insertText', false, payload + " \\u200B" + salt);
                        box.dispatchEvent(new Event('input', { bubbles: true }));

                        // Try Button Click -> Fallback to Enter
                        let sendBtn = [...document.querySelectorAll('div[role="button"], button')].find(b => 
                            b.innerText.includes('Send') || b.querySelector('svg[aria-label*="Send"]')
                        );

                        if (sendBtn) {
                            sendBtn.click();
                        } else {
                            const e = new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true});
                            box.dispatchEvent(e);
                        }
                        window.msg_count++;
                    }
                }
                await new Promise(r => setTimeout(r, ms));
            }
        })(arguments[0], arguments[1]);
    """, text, delay)

def run_agent(agent_id, machine_id, cookie, target, text):
    start_time = time.time()
    while (time.time() - start_time) < TOTAL_DURATION:
        driver = None
        try:
            driver = get_driver(agent_id, machine_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(15)
            
            vortex_dispatch(driver, text, INTERNAL_DELAY_MS)
            
            # 💓 Heartbeat Loop
            cycle_start = time.time()
            while (time.time() - cycle_start) < SESSION_RESTART_SEC:
                time.sleep(30)
                try:
                    cnt = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Count: {cnt} | Pulse: OK")
                except: break
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(10)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    text = os.environ.get("MESSAGES", "SYSTEM OWNED").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, text)
            time.sleep(12)

if __name__ == "__main__":
    main()
