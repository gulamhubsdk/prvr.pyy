# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (BLITZ-VELOCITY V106)
# 📅 STATUS: FAST-DISPATCH-ACTIVE | 4-AGENTS PER MACHINE | AGENT-1-VANGUARD

import os, time, re, random, datetime, threading, sys, gc, tempfile, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- ⚡ BLITZ CONFIGURATION ---
THREADS = 4                        
TOTAL_DURATION = 21600             
# 🔥 BLITZ SPEED: 0.05 is the absolute floor for browser stability
BURST_SPEED = (0.05, 0.2)           
SESSION_RESTART_SEC = 240          # Longer sessions to maintain the "Blitz" rhythm

GLOBAL_SENT = 0
COUNTER_LOCK = threading.Lock()
BROWSER_LAUNCH_LOCK = threading.Lock()

def get_blitz_payload(custom_text):
    """Generates a high-speed payload with a tiny uniqueness-bit."""
    u_id = random.randint(1000, 9999)
    # \u200B = Zero Width Space (keeps message unique for bypass)
    return f"{custom_text} \u200B{u_id}"

def get_driver(agent_id, machine_id):
    with BROWSER_LAUNCH_LOCK:
        # 🚀 AGENT 1 VANGUARD: 0s delay. Others follow at 3s intervals.
        launch_delay = 0 if int(agent_id) == 1 else (int(agent_id) * 3) + (int(machine_id) * 5)
        time.sleep(launch_delay)
        
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        mobile_emulation = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 1{random.randint(5,7)}_0 like Mac OS X) AppleWebKit/605.1.15"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        temp_dir = os.path.join(tempfile.gettempdir(), f"pv_blitz_{machine_id}_{agent_id}")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        driver = webdriver.Chrome(options=chrome_options)
        stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="iPhone", fix_hairline=True)
        driver.custom_temp_path = temp_dir
        return driver

def blitz_send(driver, text):
    """High-speed dispatch that bypasses Selenium's internal event lag."""
    try:
        # Direct JS injection is 3x faster than element.send_keys()
        driver.execute_script("""
            var box = document.querySelector('div[role="textbox"], textarea');
            if (box) {
                box.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
                document.execCommand('insertText', false, arguments[0]);
                
                // Force dispatch for immediate delivery
                var e = new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, which:13, bubbles:true});
                box.dispatchEvent(e);
            }
        """, text)
        return True
    except: return False

def run_life_cycle(agent_id, machine_id, cookie, target, custom_text):
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        temp_path = None
        try:
            driver = get_driver(agent_id, machine_id)
            temp_path = getattr(driver, 'custom_temp_path', None)
            
            driver.get("https://www.instagram.com/")
            # Faster injection for Blitz mode
            time.sleep(2) 
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            
            # Agent 1 waits less; others wait for handshake
            handshake = 6 if int(agent_id) == 1 else 10
            time.sleep(handshake)
            
            session_start = time.time()
            while (time.time() - session_start) < SESSION_RESTART_SEC:
                payload = get_blitz_payload(custom_text)
                if blitz_send(driver, payload):
                    with COUNTER_LOCK:
                        global GLOBAL_SENT
                        GLOBAL_SENT += 1
                    # Flush print for real-time GitHub Action logs
                    sys.stdout.write(f"[M{machine_id}-A{agent_id}] BLITZ: {GLOBAL_SENT}\n")
                    sys.stdout.flush()
                
                time.sleep(random.uniform(*BURST_SPEED))
        except: pass
        finally:
            if driver: driver.quit()
            if temp_path and os.path.exists(temp_path):
                shutil.rmtree(temp_path, ignore_errors=True)
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    custom_text = os.environ.get("MESSAGES", "BLITZ OWNED").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, machine_id, cookie, target, custom_text)

if __name__ == "__main__":
    main()
