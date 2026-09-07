"""Call a REST endpoint and read the response object.

.status_code, .headers and .json() are three DIFFERENT things — the exam
tests whether you know which one holds the data.
"""
import requests

URL = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token"

try:
    r = requests.post(URL, auth=("devnetuser", "Cisco123!"), verify=False, timeout=10)
    print("status_code:", r.status_code)          # an int, e.g. 200
    print("content-type:", r.headers.get("Content-Type"))
    if r.status_code == 200:
        print("token:", r.json().get("Token", "")[:40], "...")
    elif r.status_code == 401:
        print("401 - the credentials are wrong or the token expired")
    elif r.status_code == 403:
        print("403 - authenticated, but this account lacks permission")
except requests.exceptions.RequestException as e:
    print("Request failed (are you offline?):", e)
