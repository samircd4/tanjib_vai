from playwright.sync_api import sync_playwright
import requests
import os
import json
import time
import random

PROXY_SERVER = {
        'server': 'http://waterproxy.asuscomm.com:4010',
        'username': 'acczone', 
        'password': 'monthly'   
        }


def get_profile_link():
    with open('profile_links.txt', 'r') as f:
        profile_links = [link.strip() for link in f.readlines()]
        
    return profile_links

def add_friend(tok):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,proxy=PROXY_SERVER, slow_mo=50)
        token = tok
        with open(token, 'r') as f:
            state = json.load(f)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        context = browser.new_context(user_agent=user_agent, storage_state=state)
        context.set_default_timeout(60000)
        page = context.new_page()
        profile_links = get_profile_link()
        
        for link in profile_links:
            time_out = random.randint(10000, 60000)
            page.goto(link)
            print(f'{link} checking...')
            
            checking_btn = page.get_by_role("heading", name="We suspended your account")
            if checking_btn.is_visible():
                print(f'Account suspended! {tok}')
                browser.close()
                return False
            
            add_friend_btn = page.get_by_role("link", name="Add friend")
            cancel_req = page.get_by_role("link", name="Cancel Request")
            
            if add_friend_btn.is_visible():
                try:
                    add_friend_btn.click()
                    page.wait_for_timeout(3000)
                    confirm_btn = page.get_by_role("button", name="Confirm")
                    
                    if confirm_btn.is_visible():
                        confirm_btn.click()
                    
                    print('Friend added!')
                    print(f'Sleeping for {time_out/1000} seconds...')
                    page.wait_for_timeout(time_out)
                except Exception as e:
                    print(f'Error adding friend {link}: {e}')
                    continue
                
                with open('friends.txt', 'a') as f:
                    f.write(f'{link}\n')
                
            elif cancel_req.is_visible():
                print('Friend already added!')
                
                with open('friends.txt', 'a') as f:
                    f.write(f'{link}\n')
                
                print(f'Sleeping for {time_out/1000} seconds...')
                page.wait_for_timeout(time_out)
                
            else:
                with open('not_friends.txt', 'a') as f:
                    f.write(f'{link}\n')
            
        page.wait_for_timeout(1000)
        browser.close()

def get_token():
    json_contents = []
    path = '.'
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            json_contents.append(filename)
    return json_contents

if __name__ == '__main__':
    tokens = get_token()
    for t in tokens:
        print(f'Logging in as {t}')
        
        while True:
            try:
                added = add_friend(tok=t)
                break
            except Exception as e:
                print(f'IP not found: {e}')
                time.sleep(10)
                print(f'Sleeping for 10 seconds...')
                continue
        
        print('Changing IP address...')
        res = requests.get('http://waterproxy.asuscomm.com:38471/092ce50c2f2204c99fa1905e03687fc6/reset?proxy=waterproxy.asuscomm.com:4010')
        print(f'Sleeping for 30 seconds...')
        time.sleep(30)
        print('IP address changed!')




