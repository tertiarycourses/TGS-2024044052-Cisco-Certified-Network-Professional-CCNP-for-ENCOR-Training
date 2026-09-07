"""Cisco DNA Center Intent API: get a token, then list network devices.

The token flow is examined directly:
  1. POST /dna/system/api/v1/auth/token with BASIC auth  -> returns a Token
  2. Send that token in the X-Auth-Token header on every subsequent call
"""
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = "https://sandboxdnac.cisco.com"
USER, PASS = "devnetuser", "Cisco123!"


def get_token():
    r = requests.post(f"{BASE}/dna/system/api/v1/auth/token",
                      auth=(USER, PASS), verify=False, timeout=15)
    print(f"token request -> HTTP {r.status_code}")
    r.raise_for_status()
    return r.json()["Token"]


def get_devices(token):
    r = requests.get(f"{BASE}/dna/intent/api/v1/network-device",
                     headers={"X-Auth-Token": token}, verify=False, timeout=15)
    print(f"inventory request -> HTTP {r.status_code}")
    r.raise_for_status()
    return r.json()["response"]


if __name__ == "__main__":
    try:
        tok = get_token()
        devices = get_devices(tok)
        print(f"\n{len(devices)} devices returned\n")
        print(f"{'HOSTNAME':<30} {'MGMT IP':<16} {'PLATFORM':<14} REACHABILITY")
        print("-" * 78)
        for d in devices:
            print(f"{str(d.get('hostname'))[:29]:<30} "
                  f"{str(d.get('managementIpAddress')):<16} "
                  f"{str(d.get('platformId'))[:13]:<14} "
                  f"{d.get('reachabilityStatus')}")
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        print(f"\nHTTP {code}: ", end="")
        print({401: "token missing/wrong/expired - request a new one",
               403: "token valid but the account lacks permission - fix the role",
               404: "endpoint does not exist - check the path and API version",
               429: "rate limited - back off and honour Retry-After"}
              .get(code, "see the response body"))
    except requests.exceptions.RequestException as e:
        print("Request failed (offline? sandbox down?):", e)
