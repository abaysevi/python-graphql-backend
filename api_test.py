import requests

url = "http://127.0.0.1:8000/graphql"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1ZjllOWEyZTFjY2JjYjc5MTQxNzdkMiJ9.Vszd7yHa5Uf43XbkBnlw_7o_OTmChs-rV0055C5t5LI"
}

response = requests.post(url, json={"query": "query { currentUser { name } }"}, headers=headers)

print(response.json())