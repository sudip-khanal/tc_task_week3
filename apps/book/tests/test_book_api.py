# import requests

# def test_book_list():
#     url = 'http://localhost:8000/book/'
#     response = requests.get(url)
#     assert response.status_code == 200

# def test_book_retrive():
#     url='http://localhost:8000/book/3'
#     response=requests.get(url)
#     assert response.status_code==200

# def test_add_book():
#     token='8eaa8b33a92ba4dbf56ba8547e4687c05fbcf5fc'

#     headers = {
#         'Authorization': f'Token {token}'
#     }
#     data={
#         "title":"test",
#         "author":"kashyap",
#         "description": "Testing kashyap",
#         "is_active":True
#     }

#     url = 'http://localhost:8000/book/'
#     response = requests.post(url,data=data, headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 201


# def test_book_update():
#     token='77a110a8d9f7c425613f4d13f0eac07803962847'

#     headers = {
#         'Authorization': f'Token {token}'
#     }
#     data={
#         "title":"Two Scoop of Django",
#         "author":"Daniell",
#         "description": "All About django framework",
#         "is_active":True
#     }

#     url = 'http://localhost:8000/book/1/'
#     response = requests.put(url,data=data, headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200


# def test_book_partial_update():
#     token='77a110a8d9f7c425613f4d13f0eac07803962847'

#     headers = {
#         'Authorization': f'Token {token}'
#     }
#     data={
#         "author":"Daniel",
#         "description": "All About django framework",
#     }

#     url = 'http://localhost:8000/book/1/'
#     response = requests.patch(url,data=data, headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200



# def test_book_delete():
#     token='77a110a8d9f7c425613f4d13f0eac07803962847'

#     headers = {
#         'Authorization': f'Token {token}'
#     }
#     url = 'http://localhost:8000/book/1/'
#     response = requests.delete(url, headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200


# def test_add_favourite_book():
#     token='8eaa8b33a92ba4dbf56ba8547e4687c05fbcf5fc'

#     headers = {
#      "accept": "application/json", 
#      "Content-Type": "application/json",
#      'Authorization': f'Token {token}'
#     }
#     url = 'http://localhost:8000/book/3/favorite/'
#     response = requests.post(url, headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 201



# def test_unfavourite_book():
#     token='8eaa8b33a92ba4dbf56ba8547e4687c05fbcf5fc'

#     headers = {
#      "accept": "application/json", 
#      "Content-Type": "application/json",
#      'Authorization': f'Token {token}'
#     }
#     url = 'http://localhost:8000/book/3/unfavorite/'
#     response = requests.delete(url, headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200
    

# def test_top_rated_book():
#     url = 'http://localhost:8000/book/top-10-rated/'
#     response = requests.get(url)
#     assert response.status_code == 200


# def test_my_favourite_book():
#     token='77a110a8d9f7c425613f4d13f0eac07803962847'

#     headers = {
#         'Authorization': f'Token {token}'
#     }
#     url = 'http://localhost:8000/book/my_favorites/'
#     response = requests.get(url, headers=headers)
#     print(f"Response: {response.status_code}, {response.text}")  
#     assert response.status_code == 200