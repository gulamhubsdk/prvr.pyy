# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V111 EAGER-BLITZ)
# 📅 STATUS: ZERO-WAIT-ACTIVE | DUAL-MACHINE | FIXED-CRASH

import os, time, re, random, datetime, threading, sys, gc, tempfile, subprocess, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ GLOBAL CONSTANTS ---
TOTAL_DURATION = 21000             # 5.8 Hours
INTERNAL_DELAY_MS = 30             # 🔥 33 msgs/sec per machine (66 total)
SESSION_RESTART_SEC = 1200         # 20-minute stable cycles

def get_master_driver(machine_id):
    """Initializes the browser with Eager strategy and Image Blocking."""
    chrome_options = Options()
    
    # 🏎️ EAGER LOADING: Fired as soon as basic HTML is ready
    chrome_options.page_load_strategy = 'eager' 
    
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 🛡️ SPEED: Block images to save 90% bandwidth & CPU
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Auto-manages the Driver Version for GitHub environment
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def start_turbo_worker(driver, text, delay):
    """Fires messages via internal JS loop to bypass Selenium lag."""
    driver.execute_script("""
        window.praveer_active = true;
        (async function blitz(msg, ms) {
            const getBox = () => document.querySelector('div[role="textbox"], textarea');
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    const salt = Math.random().toString(36).substring(7);
                    // Entropy injection + Custom Secret Text
                    document.execCommand('insertText', false, msg + " \\u200B" + salt);
                    
                    const e = new KeyboardEvent('keydown', {
                        key: 'Enter', code: 'Enter', keyCode: 13, which: 13, 
                        bubbles: true, cancelable: true
                    });
                    box.dispatchEvent(e);
                }
                // High-precision wait
                await new Promise(r => setTimeout(r, ms));
            }
        })(arguments[0], arguments[1]);
    """, text, delay)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    custom_text = os.environ.get("MESSAGES", "V111 OWNED").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    if not cookie or not target:
        print("❌ CRITICAL ERROR: Missing Secrets.")
        return

    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        try:
            print(f"🚀 [M{machine_id}] INITIALIZING BLITZ...")
            driver = get_master_driver(machine_id)
            driver.get("https://www.instagram.com/")
            
            # Injection delay
            time.sleep(4)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            
            # Direct Jump
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(10) # Handshake wait for DOM to settle
            
            print(f"🔥 [M{machine_id}] WORKER STARTING...")
            start_turbo_worker(driver, custom_text, INTERNAL_DELAY_MS)
            
            # Keep active for the session cycle
            time.sleep(SESSION_RESTART_SEC)
            driver.execute_script("window.praveer_active = false;")
            
        except Exception as e:
            print(f"⚠️ [M{machine_id}] STALL: {e}")
        finally:
            if driver:
                try: driver.quit()
                except: pass
            time.sleep(20) # Cooldown

if __name__ == "__main__":
    main()
