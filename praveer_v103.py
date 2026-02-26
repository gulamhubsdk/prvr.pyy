# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V110 DUAL-MASTER)
# 📅 STATUS: TURBO-ACTIVE | 1-MASTER PER MACHINE | 2-MACHINE TOTAL

import os, time, re, random, datetime, threading, sys, gc, tempfile, subprocess, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# --- ⚡ TURBO MASTER CONFIG ---
TOTAL_DURATION = 21000             # ~5.8 Hours
INTERNAL_DELAY_MS = 50             # 🔥 TURBO: 20 msgs/sec per machine
SESSION_RESTART_SEC = 900          # 15-minute stable sessions

def get_master_driver(machine_id):
    """Initializes the Master Browser instance with full CPU priority."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/12{random.randint(1,5)}.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={ua}")
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_master_{machine_id}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    driver = webdriver.Chrome(options=chrome_options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    driver.custom_temp_path = temp_dir
    return driver

def start_turbo_worker(driver, text, delay):
    """Injects the high-speed JS worker into the Instagram DOM."""
    driver.execute_script("""
        window.praveer_active = true;
        async function turboLoop(msg, ms) {
            const box = document.querySelector('div[role="textbox"], textarea');
            if (!box) return;
            
            while(window.praveer_active) {
                box.focus();
                // Invisible entropy to bypass spam filters
                const salt = Math.floor(Math.random() * 99999);
                document.execCommand('insertText', false, msg + " \\u200B" + salt);
                
                const e = new KeyboardEvent('keydown', {
                    key: 'Enter', code: 'Enter', keyCode: 13, which: 13, 
                    bubbles: true, cancelable: true
                });
                box.dispatchEvent(e);
                
                // Wait for the internal worker delay
                await new Promise(r => setTimeout(r, ms));
            }
        }
        turboLoop(arguments[0], arguments[1]);
    """, text, delay)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    custom_text = os.environ.get("MESSAGES", "V110 MASTER").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        try:
            print(f"🚀 Machine {machine_id} launching Master Agent...")
            driver = get_master_driver(machine_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(15) # Wait for UI to settle
            
            print(f"🔥 Machine {machine_id} starting Turbo Worker Loop...")
            start_turbo_worker(driver, custom_text, INTERNAL_DELAY_MS)
            
            # Keep browser alive for the session duration
            time.sleep(SESSION_RESTART_SEC)
            driver.execute_script("window.praveer_active = false;")
            
        except Exception as e:
            print(f"⚠️ Machine {machine_id} Error: {e}")
        finally:
            if driver: driver.quit()
            time.sleep(30) # Cool-down before next master login

if __name__ == "__main__":
    main()
