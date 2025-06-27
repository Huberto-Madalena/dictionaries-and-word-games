import requests

r = requests.get("https://api.datamuse.com/words?rel_syn=angry")
print(r.status_code)
print(r.text[:200])