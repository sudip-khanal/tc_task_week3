import requests

def test_add_review():
    token = 'acfa7a9d209f7c194f2b45685030d9165ac58912'
    headers={
       'Authorization': f'Token {token}'
    }

    data={
    "review_text":"this is good book testinnngggg",
    "rating":5,
    "book": 1
    }
    url='http://localhost:8000/review/'
    response = requests.post(url,data=data,headers=headers)
    print(f"Response: {response.status_code}, {response.text}")  
    assert response.status_code == 201


def test_get_review():

    token = 'acfa7a9d209f7c194f2b45685030d9165ac58912'
    headers={
       'Authorization': f'Token {token}'
    }
    url='http://localhost:8000/review/'
    response = requests.get(url,headers=headers)
    print(f"Response: {response.status_code}, {response.text}")  
    assert response.status_code == 200
