import requests

hej = requests.post('http://localhost:5012/user',
                    json={'name': 'david',
                          'email': 'david@david.com',
                          'gender': 'Male',
                          'birthdate': '980408',

                          'birthdate': '1998-04-08',

                          'hcp': '1.0',
                          'password': 'erikerik'})
requests.post('http://localhost:5012/user',
                    json={'name': 'david',
                          'email': 'david@david.co',
                          'gender': 'Male',
                          'birthdate': '980408',

                          'birthdate': '1998-04-08',

                          'hcp': '1.0',
                          'password': 'erikerik'})
print(hej.status_code)
print(hej.json())
token2 = requests.post('http://localhost:5012/user/login', json={'email': 'david@david.co', "password": 'erikerik'}).json()['token']
token = requests.post('http://localhost:5012/user/login', json={'email': 'david@david.com', "password": 'erikerik'}).json()['token']
header = {"Authorization": "Bearer " + token}
header2 = {"Authorization": "Bearer " + token2}
post = requests.post('http://localhost:5012/user/1/post', json={'text': "testingtesting"}, headers=header)
post = requests.post('http://localhost:5012/user/2/post', json={'text': "testingtesting"}, headers=header2)
print(post)
like = requests.post('http://localhost:5012/user/1/post/1/like', headers=header)
like = requests.post('http://localhost:5012/user/2/post/1/like', headers=header2)
print(like)
get = requests.get('http://localhost:5012/user/1/post/1', headers=header)
print(get.json())


"""
requests.post('http://localhost:5012/user',
                               json={'name': 'david',
                                     'email': 'david2@david.com',
                                     'gender': 'Male',
                                     'birthdate': '980408',
                                     'hcp': '1.0',
                                     'password': 'erik'})

requests.post('http://localhost:5012/user/1/post')

requests.post('http://localhost:5012/user/2/post/1')

getusr2 = requests.get('http://localhost:5012/user/1')
print(getusr2.json())

getusr3 = requests.get('http://localhost:5012/user/2')
print(getusr3.json())

requests.post('http://localhost:5012/add_remove_follow/2/1')

getall = requests.get('http://localhost:5012/user')
print(getall.json())


requests.post('http://localhost:5012/user',
                               json={'name': 'david',
                                     'email': 'david1@david.com',
                                     'gender': 'Male',
                                     'birthdate': '980408',
                                     'hcp': '1.0',
                                     'password': 'erik'})
requests.post('http://localhost:5012/user',
                               json={'name': 'david3',
                                     'email': 'david2@david.com',
                                     'gender': 'Male',
                                     'birthdate': '980408',
                                     'hcp': '1.0',
                                     'password': 'erik'})
requests.post('http://localhost:5012/user',
                               json={'name': 'david3',
                                     'email': 'david3@david.com',
                                     'gender': 'Male',
                                     'birthdate': '980408',
                                     'hcp': '1.0',
                                     'password': 'erik'})


f = requests.post('http://localhost:5012/add_post/1', json={'text': 'hejsan'})

requests.post('http://localhost:5012/add_post/1', json={'text': 'hejsan12'})
requests.post('http://localhost:5012/add_post/1', json={'text': 'hejsan2'})
e = requests.get('http://localhost:5012/add_post/1')
de = requests.get('http://localhost:5012/user')
#hej = requests.get('http://localhost:5012/post/1/1')
#print(hej.status_code, hej.json())
server.hej()
requests.put('http://localhost:5012/post/1/1', json={'text': 'tja erik'})
server.hej()
#print(hejj.status_code, hejj.json())
hejjj = requests.get('http://localhost:5012/post/1/1')

#hejjjjj= requests.delete('http://localhost:5012/post/1/1')
#print(hejjjjj.status_code, hejjjjj.json(), '1500000')
print('GET', requests.get('http://localhost:5012/post/1/1').json())
add = requests.post('http://localhost:5012/add_comment/1/1', json={'comment':'vilken fin cykel du har'})
print(add.status_code, add.json())
print('GET', requests.get('http://localhost:5012/post/1/1').json())
put = requests.put('http://localhost:5012/add_comment/1/1', json={'comment':'du har en ful cykel menade jag'})
print(put.status_code)
print('GET', requests.get('http://localhost:5012/post/1/1').json())
put = requests.delete('http://localhost:5012/add_comment/1/1')
print(put.status_code, put.json())
print('GET', requests.get('http://localhost:5012/post/1/1').json())







david_follow_erik = requests.post('http://localhost:5012/add_remove_follow/1/2')
print(david_follow_erik.status_code)
print(david_follow_erik.json())

david_follow_erik2 = requests.post('http://localhost:5012/add_remove_follow/1/3')
print(david_follow_erik2.status_code)
print(david_follow_erik2.json())

david_follow_erik3 = requests.post('http://localhost:5012/add_remove_follow/2/3')
print(david_follow_erik3.status_code)
print(david_follow_erik3.json())

david_follow_erik4 = requests.post('http://localhost:5012/add_remove_follow/4/3')
print(david_follow_erik4.status_code)
print(david_follow_erik4.json())

david_follow_erik5 = requests.post('http://localhost:5012/add_remove_follow/4/4')
print(david_follow_erik5.status_code)
print(david_follow_erik5.json())

david_follow_erik6 = requests.post('http://localhost:5012/add_remove_follow/4/3')
print(david_follow_erik6.status_code)
print(david_follow_erik6.json(), "HEJHEJ")
like1 = requests.post('http://localhost:5012/add_remove_like/1/2')
requests.post('http://localhost:5012/add_remove_like/1/1')
requests.post('http://localhost:5012/add_remove_like/1/3')
requests.post('http://localhost:5012/add_remove_like/1/3')

usr = requests.get('http://localhost:5012/get_post/1')
print(usr.json(), 'pssst')

usr = requests.get('http://localhost:5012/get_user/1')
print(usr.json())




david_follow_erik2 = requests.post('http://localhost:5012/add_remove_follow/1/1')
print(david_follow_erik2.status_code)
print(david_follow_erik2.json())
david_follow_erik3 = requests.post('http://localhost:5012/add_remove_follow/2/1')
print(david_follow_erik3.json())

add_post_2 = requests.post('http://localhost:5012/add_post/2', json={'text': 'hejsan'})
david_follow_erik = requests.post('http://localhost:5012/add_remove_follow/1/2')
print(david_follow_erik.status_code)


add_comment_1 = requests.post('http://localhost:5012/add_comment/1/1', json={'comment': 'hejsan'})
add_comment_2 = requests.post('http://localhost:5012/add_comment/1/1', json={'comment': 'hejsan'})
requests.post('http://localhost:5012/add_remove_like/1/1')
requests.post('http://localhost:5012/add_remove_like/1/2')
requests.post('http://localhost:5012/add_remove_like/1/2')
requests.post('http://localhost:5012/add_remove_like/1/2')

requests.post('http://localhost:5012/add_remove_follow/1/2')
add_post_1 = requests.post('http://localhost:5012/add_post/1', json={'text': 'hejsan'})
"""
