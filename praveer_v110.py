# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V112 SAFE-BLITZ)
# 📅 STATUS: BYPASS-ACTIVE | STAGGERED-START | RESOURCE-LEAN

import os, time, re, random, datetime, threading, sys, gc, tempfile, subprocess, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ GLOBAL CONSTANTS ---
TOTAL_DURATION = 21000             
INTERNAL_DELAY_MS = 45             # 🛡️ Safe threshold for GitHub stability
SESSION_RESTART_SEC = 900          

def get_master_driver(machine_id):
    chrome_options = Options()
    
    # 🏎️ EAGER LOADING: Start acting before the full page renders
    chrome_options.page_load_strategy = 'eager' 
    
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 🛡️ RESOURCE SHIELD: Block Images (2) and Stylesheets (2) to prevent CPU spikes
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def start_turbo_worker(driver, text, delay):
    """Fires messages via internal JS loop for zero-lag dispatch."""
    driver.execute_script("""
        window.praveer_active = true;
        (async function blitz(msg, ms) {
            const getBox = () => document.querySelector('div[role="textbox"], textarea');
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    const salt = Math.random().toString(36).substring(7);
                    document.execCommand('insertText', false, msg + " \\u200B" + salt);
                    
                    const e = new KeyboardEvent('keydown', {
                        key: 'Enter', code: 'Enter', keyCode: 13, which: 13, 
                        bubbles: true, cancelable: true
                    });
                    box.dispatchEvent(e);
                }
                await new Promise(r => setTimeout(r, ms));
            }
        })(arguments[0], arguments[1]);
    """, text, delay)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    custom_text = os.environ.get("MESSAGES", "V112 OWNED").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    if not cookie or not target:
        print("❌ CRITICAL: Missing Secrets.")
        return

    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        try:
            print(f"🚀 [M{machine_id}] INITIALIZING ENGINE...")
            driver = get_master_driver(machine_id)
            driver.get("https://www.instagram.com/")
            
            # Injection delay to avoid "bot cluster" flag
            time.sleep(random.randint(5, 8))
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            
            # Direct Jump to Target
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            
            # 🛡️ HANDSHAKE WAIT: Essential to prevent 'Operation Canceled'
            print(f"⌛ [M{machine_id}] Waiting for Socket Stabilization...")
            time.sleep(15) 
            
            print(f"🔥 [M{machine_id}] WORKER ACTIVE - BLITZING...")
            start_turbo_worker(driver, custom_text, INTERNAL_DELAY_MS)
            
            time.sleep(SESSION_RESTART_SEC)
            driver.execute_script("window.praveer_active = false;")
            
        except Exception as e:
            print(f"⚠️ [M{machine_id}] STALL: {e}")
        finally:
            if driver:
                try: driver.quit()
                except: pass
            time.sleep(25)

if __name__ == "__main__":
    main()
