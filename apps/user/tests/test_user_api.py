import requests

# def test_user_register():
#     data={        
#     "username":"miya",
#     "email":"miyahe1275@sablecc.com",
#     "password":"miya1234",
#     "confirm_password":"miya1234"

#     }

#     url = 'http://localhost:8000/user/register/'
#     response = requests.post(url,data=data, )
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 201

# def test_login():

#     data={
#         "username":"miya",
#         "password":"miya1234"
#     }

#     url="http://localhost:8000/user/login/"
#     response=requests.post(url,data=data)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200

    

# def test_change_passsword():
#     token='acfa7a9d209f7c194f2b45685030d9165ac58912'

#     headers = {
#         'Authorization': f'Token {token}'
#     }
#     data={
#     "old_password":"miya1234",
#     "new_password": "miya123",
#     "confirm_new_password":"miya123"

#     }
#     url='http://localhost:8000/user/change_password/'
#     response=requests.post(url,data=data,headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200

# def test_forgot_password():
#     data={
#     "email":"miyahe1275@sablecc.com",
#     }
#     url='http://localhost:8000/user/forgot_password/'
#     response=requests.post(url,data=data,)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200

# def test_logout():
#     token = 'acfa7a9d209f7c194f2b45685030d9165ac58912'
#     headers={
#        'Authorization': f'Token {token}'
#     }

#     url='http://localhost:8000/user/logout/'
#     response=requests.post(url,headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200






