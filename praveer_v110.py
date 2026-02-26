# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V111 EAGER-BLITZ)
# 📅 STATUS: ZERO-WAIT-ACTIVE | 2-MACHINE TOTAL | SOCKET-SATURATION

import os, time, re, random, datetime, threading, sys, gc, tempfile, subprocess, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ EAGER-BLITZ CONFIG ---
INTERNAL_DELAY_MS = 20             # 🔥 INSANE SPEED: 50 msgs/sec per machine
SESSION_RESTART_SEC = 1200         # 20-minute sessions for max momentum

def get_master_driver(machine_id):
    chrome_options = Options()
    
    # 🏎️ EAGER LOADING: Don't wait for images/scripts to finish
    chrome_options.page_load_strategy = 'eager' 
    
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 🛡️ MEMORY OPTIMIZATION: Block images to save bandwidth & speed up DOM
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Stealth remains for account safety
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def start_turbo_worker(driver, text, delay):
    """Fires messages using a high-priority micro-task queue."""
    driver.execute_script("""
        window.praveer_active = true;
        (async function blitz() {
            const getBox = () => document.querySelector('div[role="textbox"], textarea');
            
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    const salt = Math.random().toString(36).substring(7);
                    document.execCommand('insertText', false, arguments[0] + " \\u200B" + salt);
                    
                    const e = new KeyboardEvent('keydown', {
                        key: 'Enter', code: 'Enter', keyCode: 13, which: 13, 
                        bubbles: true, cancelable: true
                    });
                    box.dispatchEvent(e);
                }
                // High-precision micro-delay
                await new Promise(r => setTimeout(r, arguments[1]));
            }
        })(arguments[0], arguments[1]);
    """, text, delay)
