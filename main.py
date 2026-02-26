# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (MULTI-MACHINE V103)
# 📅 STATUS: CONCURRENCY-SAFE | 4-AGENTS PER MACHINE | 2-MACHINE TOTAL

import os, time, re, random, datetime, threading, sys, gc, tempfile, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- ⚡ CONFIGURATION ---
THREADS = 4                        
TOTAL_DURATION = 21600             # 6 Hours (Matches GitHub Action Timeout)
BURST_SPEED = (0.6, 1.2)           # 🛡️ Safe concurrency for 8 total agents
SESSION_RESTART_SEC = 120          # ♻️ 2-Minute Hard Reset to clear logs

GLOBAL_SENT = 0
COUNTER_LOCK = threading.Lock()
BROWSER_LAUNCH_LOCK = threading.Lock()

def get_dominance_payload(custom_text):
    """Generates massive vertical displacement using your secret text."""
    filler, glue, cgj = "\u3164", "\u2060", "\u034F"
    # Pushes history up/down
    padding = (f"{filler}{glue}{cgj}" * 10 + "\n") * 35 
    u_id = random.randint(100, 999)
    header = f"👑 PRAVEER PAPA 👑 [{u_id}]"
    return f"{padding}\n{header}\n{custom_text}\n{padding}"[:9998]

def get_driver(agent_id):
    with BROWSER_LAUNCH_LOCK:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        mobile_emulation = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 1{random.randint(4,7)}_0 like Mac OS X) AppleWebKit/605.1.15"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        temp_dir = os.path.join(tempfile.gettempdir(), f"praveer_v103_{int(time.time())}_{agent_id}")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")

        driver = webdriver.Chrome(options=chrome_options)
        stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="iPhone", fix_hairline=True)
        driver.custom_temp_path = temp_dir
        return driver

def atomic_send(driver, text):
    try:
        driver.execute_script("""
            var box = document.querySelector('div[role="textbox"], textarea');
            if (box) {
                box.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
                document.execCommand('insertText', false, arguments[0]);
                box.dispatchEvent(new Event('input', { bubbles: true }));
                var e = new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, which:13, bubbles:true});
                box.dispatchEvent(e);
            }
        """, text)
        return True
    except: return False

def run_life_cycle(agent_id, cookie, target, custom_text):
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        temp_path = None
        session_start = time.time()
        try:
            driver = get_driver(agent_id)
            temp_path = getattr(driver, 'custom_temp_path', None)
            driver.get("https://www.instagram.com/")
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(15) 
            
            while (time.time() - session_start) < SESSION_RESTART_SEC:
                payload = get_dominance_payload(custom_text)
                if atomic_send(driver, payload):
                    with COUNTER_LOCK:
                        global GLOBAL_SENT
                        GLOBAL_SENT += 1
                    print(f"[{agent_id}] SENT: {GLOBAL_SENT}", flush=True)
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
    custom_text = os.environ.get("MESSAGES", "SYSTEM OWNED").strip()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, cookie, target, custom_text)

if __name__ == "__main__":
    main()
