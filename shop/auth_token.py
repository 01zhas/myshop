import requests

url = 'http://127.0.0.1:8000/api/token/'
 
data = {
    'username' : 'manager',
    'password' : 'fecpum-guCxe3-kymtud',
}

response = requests.post(url,data=data)

json = response.json()
access_token = json['access']
print(access_token)

url_products = 'http://127.0.0.1:8000/api/products/'

print()
print("Без токена")
response = requests.get(url_products)
print(response.json())

print()
print("C токеном")
headers = {
    "Authorization" : f"Bearer {access_token}"
}
response = requests.get(url_products,headers=headers)
print(response.json())