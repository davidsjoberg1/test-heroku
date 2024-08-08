import tempfile
import os

import pytest

from . import db 
from . import app


@pytest.fixture
def client():
    db_fd, name = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(name)
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    os.close(db_fd)
    os.unlink(name)


def add(client, name):
    mail = 'david@david.com'
    if name == 'erik':
        mail = 'erik@erik.com'
    client.post('http://localhost:5012/user',
                json={'name': 'erik', 'email': mail,
                      'gender': 'Male', 'birthdate': "1998-04-08",
                      'hcp': '1.0',
                      'password': 'erikdavid'})  # Adds a user


def login(client, name):
    mail = 'david@david.com'
    if name == 'erik':
        mail = 'erik@erik.com'
    log_in = client.post('http://localhost:5012/user/login',
                         json={'email': mail, 'password': 'erikdavid'})
    token = log_in.json['token']
    header = {"Authorization": "Bearer " + token}
    return header


def test_add_user_get_users(client):
    no_users = client.get('http://localhost:5012/user')
    assert no_users.status_code == 400  # There are users yet
    assert no_users.json == "There are no users"

    client.post('http://localhost:5012/user',
                json={'name': 'david', 'email': 'david8@david.com',
                      'gender': 'Male', 'birthdate': "1998-04-08",
                      'hcp': "1.0",
                      'hcp': '1.0',
                      'password': 'erikdavid'})  # Adds a user

    add_existing_user = client.post('http://localhost:5012/user',
                                    json={'name': 'david', 'email': 'david8@david.com',
                                          'gender': 'Male', 'birthdate': "1998-04-08",
                                          'hcp': '1.0',
                                          'password': 'erikdavid'})
    assert add_existing_user.status_code == 400  # email finns redan
    assert add_existing_user.json == 'This email already has an account'

    add_user = client.post('http://localhost:5012/user',
                           json={'name': 'david', 'email': 'david1@david.com',
                                 'gender': 'Male', 'birthdate': "1998-04-08",
                                 'hcp': '1.0',
                                 'password': 'erikdavid'})
    assert add_user.status_code == 200  # Successfully adds a user
    assert add_user.json == "Your user has successfully been created"

    add_user_gender = client.post('http://localhost:5012/user',
                                  json={'name': 'david', 'email': 'david2@david.com',
                                        'gender': 'Mal', 'birthdate': "1998-04-08",
                                        'hcp': '1.0',
                                        'password': 'erikdavid'})
    assert add_user_gender.status_code == 400  # Gender not correct
    assert add_user_gender.json == 'Gender not correct'

    add_user_name_long = client.post('http://localhost:5012/user', json={
        'name': 'd',
        'email': 'david3@david.com',
        'gender': 'Male', 'birthdate': "1998-04-08",
        'hcp': '1.0',
        'password': 'erikdavid'})
    assert add_user_name_long.status_code == 400  # Name too long
    assert add_user_name_long.json == 'Name must be between 1 and 51 characters'

    add_user_hcp = client.post('http://localhost:5012/user',
                               json={'name': 'david', 'email': 'david5@david.com',
                                     'gender': 'Male', 'birthdate': "1998-04-08",
                                     'hcp': '58',
                                     'password': 'erikdavid'})
    assert add_user_hcp.status_code == 400  # Invalid hcp
    assert add_user_hcp.json == "Not valid HCP"

    add_user_password = client.post('http://localhost:5012/user',
                                    json={'name': 'david', 'email': 'david6@david.com',
                                          'gender': 'Male', 'birthdate': "1998-04-08",
                                          'hcp': '1.0',
                                          'password': 'short'})
    assert add_user_password.status_code == 400  # incorrect password
    assert add_user_password.json == 'Password must be between 7 and 101 characters'

    add_user_method = client.put('http://localhost:5012/user',
                                 json={'name': 'david', 'email': 'david7@david.com',
                                       'gender': 'Male', 'birthdate': "1998-04-08",
                                       'hcp': '1.0',
                                       'password': 'erikdavid'})
    assert add_user_method.status_code == 405  # Wrong method

    all_fields = client.post('http://localhost:5012/user',
                             json={'name': 'david', 'email': 'erik@david.com',
                                   'gender': 'Male', 'birthdate': "1998-04-08",
                                   'hcp': '1.0'})
    assert all_fields.status_code == 400
    assert all_fields.json == 'Please enter all fields of data'

    no_users = client.get('http://localhost:5012/user')
    assert no_users.status_code == 200  # Successfully gets all users


def test_get_delete_put_user(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    wrong_method = client.post('http://localhost:5012/user/1', headers=header_david)
    assert wrong_method.status_code == 405  # Wrong method

    no_such_user = client.get('http://localhost:5012/user/2', headers=header_david)
    assert no_such_user.status_code == 400  # No such user
    assert no_such_user.json == "No such user"

    get_user = client.get('http://localhost:5012/user/1', headers=header_david)
    assert get_user.status_code == 200  # Successfully gets a user

    put_wrong_json = client.put('http://localhost:5012/user/1', json={'wronginput': 'Erik'}, headers=header_david)
    assert put_wrong_json.status_code == 400  # Wrong input of json
    assert put_wrong_json.json == "Wrong input"

    add(client, 'erik')  # Adds erik as a user

    put_email_already_exists = client.put('http://localhost:5012/user/1',
                                          json={'name': 'david', 'email': 'erik@erik.com',
                                                'gender': 'Male', 'birthdate': "1998-04-08",
                                                'hcp': '1.0',
                                                'password': 'erikdavid'}, headers=header_david)  # Email already exists

    assert put_email_already_exists.status_code == 400  # Email occupied
    assert put_email_already_exists.json == "This email already has an account"


    put_same_json = client.put('http://localhost:5012/user/1',
                               json={'name': 'Henrik', 'name': 'Erik'}, headers=header_david)  # puts name two times
    assert put_same_json.status_code == 200  # Successfully puts the new name, but it becomes the latest of them
    assert put_same_json.json == "User edited successfully"
    print(put_same_json.status_code, "DÅDÅDÅ")

    delete_user = client.delete('http://localhost:5013/user/1', headers=header_david)
    print(delete_user.status_code, "NEJNEJN")
    assert delete_user.status_code == 200  # Successfully deletes a user
    assert delete_user.json == "User deleted"


def test_add_get_post(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    add_post_no_user = client.post('http://localhost:5012/user/2/post', json={'text': 'hejsan'}, headers=header_david)
    assert add_post_no_user.status_code == 400  # No such user
    assert add_post_no_user.json == 'There is no such user'

    get_post_no_user = client.get('http://localhost:5012/user/2/post', headers=header_david)
    assert get_post_no_user.status_code == 400  # No such user
    assert get_post_no_user.json == 'There is no such user'

    get_post_no_post = client.get('http://localhost:5012/user/1/post', headers=header_david)
    assert get_post_no_post.status_code == 200
    assert get_post_no_post.json == []

    add_post_method = client.delete('http://localhost:5012/user/1/post', json={'text': 'hejsan'}, headers=header_david)
    assert add_post_method.status_code == 405  # Wrong method

    add_post_msg = client.post('http://localhost:5012/user/1/post', json={'text': ''}, headers=header_david)
    assert add_post_msg.status_code == 400  # wrong length of message
    assert add_post_msg.json == 'Text must be between 0 to 501 signs'

    add_post_erik = client.post('http://localhost:5012/user/1/post', json={'text': 'hejsan'}, headers=header_david)
    assert add_post_erik.status_code == 200  # Successfully add a post
    assert add_post_erik.json == "Your post has successfully been uploaded"

    client.post('http://localhost:5012/user/1/post', json={'text': 'hejsan2'}, headers=header_david)

    get_post_erik = client.get('http://localhost:5012/user/1/post', headers=header_david)
    assert get_post_erik.status_code == 200  # Successfully add a post

    # Tested this way because it is hard to test the time which is included in the json return
    assert get_post_erik.json[0]['text'] == 'hejsan'
    assert get_post_erik.json[0]['id'] == 1
    assert get_post_erik.json[0]['likes'] == []
    assert get_post_erik.json[0]['user_id'] == 1
    assert get_post_erik.json[1]['text'] == 'hejsan2'
    assert get_post_erik.json[1]['id'] == 2
    assert get_post_erik.json[1]['likes'] == []
    assert get_post_erik.json[1]['user_id'] == 1

    post_no_json = client.post('http://localhost:5012/user/1/post', headers=header_david)
    assert post_no_json.status_code == 400
    assert post_no_json.json == 'Cannot find text'


def test_get_put_delete_post(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    get_post_no_post = client.get('http://localhost:5012/user/1/post/1', headers=header_david)
    assert get_post_no_post.status_code == 400
    assert get_post_no_post.json == 'There is no such post'

    client.post('http://localhost:5012/user/1/post', json={'text': 'hejsan'}, headers=header_david)

    get_post_no_user = client.get('http://localhost:5012/user/2/post/1', headers=header_david)
    assert get_post_no_user.status_code == 400
    assert get_post_no_user.json == 'There is no such user'

    add(client, 'erik')
    header_erik = login(client, 'erik')

    client.post('http://localhost:5012/user/2/post', json={'text': 'hejsan2'}, headers=header_erik)

    get_post_success = client.get('http://localhost:5012/user/1/post/1', headers=header_david)
    assert get_post_success.status_code == 200
    assert get_post_success.json['text'] == 'hejsan'
    assert get_post_success.json['comment'] == []
    assert get_post_success.json['id'] == 1
    assert get_post_success.json['likes'] == []
    assert get_post_success.json['user_id'] == 1

    # Vad testas här egentligen?????
    put_post_fail = client.put('http://localhost:5012/user/1/post/1', json={'id': '2'}, headers=header_david)
    assert put_post_fail.status_code == 400
    assert put_post_fail.json == 'You can only edit the text of your own post'

    put_post_success = client.put('http://localhost:5012/user/1/post/1', json={'text': 'detta är nya meddelandet'},
                                  headers=header_david)
    assert put_post_success.status_code == 200
    assert put_post_success.json == 'Text edited successfully'
    get_edited_post_success = client.get('http://localhost:5012/user/1/post/1', headers=header_david)
    assert get_edited_post_success.status_code == 200
    assert get_edited_post_success.json['text'] == 'detta är nya meddelandet'
    assert get_edited_post_success.json['comment'] == []
    assert get_edited_post_success.json['id'] == 1
    assert get_edited_post_success.json['likes'] == []
    assert get_edited_post_success.json['user_id'] == 1

    delete_post_success = client.delete('http://localhost:5012/user/1/post/1', headers=header_david)
    assert delete_post_success.status_code == 200
    assert delete_post_success.json == 'Post deleted successfully'
    try_get_deleted_post = client.get('http://localhost:5012/user/1/post/1', headers=header_david)
    assert try_get_deleted_post.status_code == 400
    assert try_get_deleted_post.json == 'There is no such post'


def test_post_comment(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    client.post('http://localhost:5012/user/1/post', json={'text': 'hejsan'}, headers=header_david)

    add_post_comment_method = client.get('http://localhost:5012/user/1/post/1/comment', json={'comment': 'hejsan'},
                                         headers=header_david)
    assert add_post_comment_method.status_code == 405  # wrong method

    add_post_comment_no_post = client.post('http://localhost:5012/user/1/post/2/comment', json={'comment': 'hejsan'},
                                           headers=header_david)
    assert add_post_comment_no_post.status_code == 400  # No such post
    assert add_post_comment_no_post.json == 'There is no such post'

    add_post_comment_no_user = client.post('http://localhost:5012/user/2/post/1/comment', json={'comment': 'hejsan'},
                                           headers=header_david)
    assert add_post_comment_no_user.status_code == 400  # No such user
    assert add_post_comment_no_user.json == 'There is no such user'

    add_post_comment_com = client.post('http://localhost:5012/user/1/post/1/comment', json={'comment': ''},
                                       headers=header_david)
    assert add_post_comment_com.status_code == 200  # wrong comment
    assert add_post_comment_com.json == 'Comment must be between 0 to 201 signs'

    add_post_comment = client.post('http://localhost:5012/user/1/post/1/comment', json={'comment': 'hejsan'},
                                   headers=header_david)
    assert add_post_comment.status_code == 200  # Successfully adds a comment
    assert add_post_comment.json == "You have successfully added a comment"

    add_post_comment = client.post('http://localhost:5012/user/1/post/1/comment', json={'comment': 'hejsan'},
                                   headers=header_david)
    assert add_post_comment.status_code == 200  # Add the same comment on the same post from the same user
    assert add_post_comment.json == "You have successfully added a comment"


def test_get_delete_comment(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    client.post('http://localhost:5012/user/1/post', json={'text': 'hejsan'}, headers=header_david)

    client.post('http://localhost:5012/user/1/post/1/comment', json={'comment': 'detta är en kommentar'},
                headers=header_david)

    comment_method = client.post('http://localhost:5012/user/1/post/1/comment/1', json={'comment': 'hejsan'},
                                 headers=header_david)
    assert comment_method.status_code == 405  # wrong method

    comment_no_post = client.get('http://localhost:5012/user/1/post/2/comment/1', json={'comment': 'hejsan'},
                                 headers=header_david)
    assert comment_no_post.status_code == 400  # No such post
    assert comment_no_post.json == 'There is no such post'

    comment_no_user = client.get('http://localhost:5012/user/2/post/1/comment/1', json={'comment': 'hejsan'},
                                 headers=header_david)
    assert comment_no_user.status_code == 400  # No such user
    assert comment_no_user.json == 'There is no such user'

    comment_get = client.get('http://localhost:5012/user/1/post/1/comment/1', headers=header_david)
    assert comment_get.status_code == 200
    assert comment_get.json['comment'] == 'detta är en kommentar'
    assert comment_get.json['id'] == 1
    assert comment_get.json['post_id'] == 1
    assert comment_get.json['user_id'] == 1

    comment_delete_fail = client.delete('http://localhost:5012/user/1/post/1/comment/2', headers=header_david)
    assert comment_delete_fail.status_code == 400
    assert comment_delete_fail.json == 'No such comment'

    comment_delete = client.delete('http://localhost:5012/user/1/post/1/comment/1', headers=header_david)
    assert comment_delete.status_code == 200
    assert comment_delete.json == 'Comment deleted successfully'

    comment_get_fail = client.get('http://localhost:5012/user/1/post/1/comment/1', headers=header_david)
    assert comment_get_fail.status_code == 400
    assert comment_get_fail.json == 'No such comment'


def test_like(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    wrong_method = client.get('http://localhost:5012/user/1/post/1/like', headers=header_david)
    assert wrong_method.status_code == 405

    no_such_post = client.post('http://localhost:5012/user/1/post/1/like', headers=header_david)
    assert no_such_post.status_code == 400
    assert no_such_post.json == 'Post to like does not exist'

    no_such_user = client.post('http://localhost:5012/user/2/post/1/like', headers=header_david)
    assert no_such_user.status_code == 400
    assert no_such_user.json == 'User id does not exist'

    add(client, 'erik')  # adds erik as a user
    header_erik = login(client, 'erik')  # Logs in erik

    client.post('http://localhost:5012/user/1/post', json={'text': 'hejsan'}, headers=header_david)  # Adds a post



    like_added = client.post('http://localhost:5012/user/2/post/1/like', json={'post_id': 1}, headers=header_erik)
    assert like_added.status_code == 200
    assert like_added.json == 'Like added'

    already_liked = client.post('http://localhost:5012/user/2/post/1/like', json={'post_id': 1}, headers=header_erik)
    assert already_liked.status_code == 200
    assert already_liked.json == 'This user already likes this post'


def test_unlike(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    wrong_method = client.get('http://localhost:5012/user/1/post/1/like/1', headers=header_david)
    assert wrong_method.status_code == 405

    no_such_user = client.delete('http://localhost:5012/user/2/post/1/like/1', headers=header_david)
    assert no_such_user.status_code == 400
    assert no_such_user.json == 'This user does not exist'

    no_such_post = client.delete('http://localhost:5012/user/1/post/1/like/1', headers=header_david)
    assert no_such_post.status_code == 400
    assert no_such_post.json == 'This post does not exist'

    client.post('http://localhost:5012/user/1/post', json={'text': 'hejsan'}, headers=header_david)  # Adds a post

    no_such_like = client.delete('http://localhost:5012/user/1/post/1/like/1', headers=header_david)
    assert no_such_like.status_code == 200
    assert no_such_like.json == 'The like to be removed does not exist'

    add(client, 'erik')  # adds erik as a user
    header_erik = login(client, 'erik')  # Logs in erik

    client.post('http://localhost:5012/user/2/post/1/like', headers=header_erik)  # Adds a like

    like_deleted = client.delete('http://localhost:5012/user/2/post/1/like/1', headers=header_erik)
    assert like_deleted.status_code == 200
    assert like_deleted.json == "Like removed"


def test_follow(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    wrong_method = client.get('http://localhost:5012/user/1/following', json={'user_id': 2}, headers=header_david)
    assert wrong_method.status_code == 405

    no_such_user = client.post('http://localhost:5012/user/2/following', json={'user_id': 2}, headers=header_david)
    assert no_such_user.status_code == 400
    assert no_such_user.json == 'User id does not exist'

    no_such_follow_id = client.post('http://localhost:5012/user/1/following', json={'user_id': 2}, headers=header_david)
    assert no_such_follow_id.status_code == 400
    assert no_such_follow_id.json == 'User to follow does not exist'

    add(client, 'erik')  # adds erik as a user

    successful_follow = client.post('http://localhost:5012/user/1/following', json={'user_id': 2}, headers=header_david)
    assert successful_follow.status_code == 200
    assert successful_follow.json == 'Follow added'

    follow_already_exists = client.post('http://localhost:5012/user/1/following', json={'user_id': 2},
                                        headers=header_david)
    assert follow_already_exists.status_code == 200
    assert follow_already_exists.json == 'User is already following this user'


    cant_follow_self = client.post('http://localhost:5012/user/1/following', json={'user_id': 1}, headers=header_david)
    assert cant_follow_self.status_code == 200
    assert cant_follow_self.json == 'You cannot follow yourself'


def test_unfollow(client):
    add(client, 'david')  # adds david as a user
    header_david = login(client, 'david')  # Logs in david

    wrong_method = client.get('http://localhost:5012/user/1/following/2', headers=header_david)
    assert wrong_method.status_code == 405

    no_such_user = client.delete('http://localhost:5012/user/2/following/2', headers=header_david)
    assert no_such_user.status_code == 400
    assert no_such_user.json == 'User id does not exist'

    no_user_to_follow = client.delete('http://localhost:5012/user/1/following/2', headers=header_david)
    assert no_user_to_follow.status_code == 400
    assert no_user_to_follow.json == 'User to follow does not exist'

    add(client, 'erik')  # adds erik as a user

    doesnt_follow = client.delete('http://localhost:5012/user/1/following/2', headers=header_david)
    assert doesnt_follow.status_code == 200
    assert doesnt_follow.json == 'User is currently not following this user'

    cant_follow_self = client.delete('http://localhost:5012/user/1/following/1', headers=header_david)
    assert cant_follow_self.status_code == 200
    assert cant_follow_self.json == 'You cannot unfollow yourself'

    client.post('http://localhost:5012/user/1/following', json={'user_id': 2}, headers=header_david)

    unfollow_success = client.delete('http://localhost:5012/user/1/following/2', headers=header_david)
    assert unfollow_success.status_code == 200
    assert unfollow_success.json == 'Unfollowed user'


def test_login(client):
    log_in_no_user = client.post('http://localhost:5012/user/login', json={'email': 'david@david.com',
                                                                           'password': 'erikdavid'})
    assert log_in_no_user.status_code == 400
    assert log_in_no_user.json == "Wrong username or password"

    add(client, 'david')  # Adds david as a user

    log_in = client.post('http://localhost:5012/user/login', json={'email': 'david@david.com', 'password': 'erikdavid'})
    assert log_in.status_code == 200


def test_logout(client):
    logout_no_user = client.post('http://localhost:5012/user/logout')
    assert logout_no_user.status_code == 401
    assert logout_no_user.json == {'msg': 'Missing Authorization Header'}

    add(client, 'david')  # Adds david a