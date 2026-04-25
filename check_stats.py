import requests
try:
    r = requests.get('http://127.0.0.1:5000/api/dashboard/stats')
    print(r.json())
except Exception as e:
    print(e)
