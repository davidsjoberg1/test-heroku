from datetime import timezone, datetime

from flask_bcrypt import check_password_hash
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, JWTManager


from golfbuddy.helper import validate_user_data
from golfbuddy.models import TokenBlockList, db, User, Comment, Like, Post, app

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlockList.id).filter_by(jti=jti).first()
    return token is not None


@app.route('/user/logout', methods=['POST'])
@jwt_required()
def logout():
    if request.method == 'POST':
        jti = get_jwt()['jti']
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlockList(jti=jti, created_at=now))
        db.session.commit()
        return jsonify('You are out'), 200


@app.route('/user/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        usr = User.query.filter_by(email=email).first()
        if not usr:
            return jsonify('Wrong username or password'), 400
        if check_password_hash(usr.password, password):
            return jsonify({'token': create_access_token(identity=usr.email), "id": usr.id}), 200
        else:
            return jsonify("Wrong username or password"), 400


@app.route('/')
def hello_world():
    return jsonify('hello_world'), 200


@app.route('/test/date', methods=['POST'])
def test_date():
    return request.json, 200


@app.route('/user', methods=['POST', 'GET'])
def add_user_get_users():
    """ Lägger till en eller hämtar alla användare i databasen """
    if request.method == 'POST':
        all_data = {}
        for param in request.json:
            value = request.json[param]
            res = validate_user_data(param, value)
            if not isinstance(res, str):
                all_data[param] = value
            else:
                return jsonify(res), 400
        if len(all_data) == 6:

            new_user = User(name=all_data['name'],
                            gender=all_data['gender'],
                            birthdate=all_data['birthdate'],
                            hcp=all_data['hcp'],
                            email=all_data['email'],
                            password=all_data['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify('Your user has successfully been created'), 200

        else:
            return jsonify('Please enter all fields of data'), 400
    if request.method == 'GET':
        all_users = User.query.all()
        if all_users:
            list_of_all = []
            for usr in all_users:
                list_of_all.append(usr.to_dict())
            return jsonify({'members': list_of_all}), 200
        return jsonify("There are no users"), 400


@app.route('/user/<user_id>', methods=['GET', 'DELETE', 'PUT'])
@jwt_required()
def get_delete_put_user(user_id):
    """ Hämtar, ändrar och tar väck användare """
    is_user = User.query.get(user_id)
    if not is_user:
        return jsonify("No such user"), 400
    if request.method == 'GET':
        return jsonify(is_user.to_dict()), 200
    if request.method == 'DELETE':
        db.session.delete(is_user)
        db.session.commit()
        return jsonify("User deleted"), 200
    if request.method == 'PUT':
        for param in request.json:
            res = validate_user_data(param, request.json[param])
            if not isinstance(res, str) or request.json[param] == is_user.email:
                setattr(is_user, param, request.json[param])
                db.session.commit()
            else:
                return jsonify(res), 400
        return jsonify("User edited successfully"), 200


@app.route('/user/<user_id>/post', methods=['POST', 'GET'])
@jwt_required()
def add_get_post(user_id):
    """ Lägger till ett inlägg från en user i databasen alternativt hämtar alla inlägg från en user i databasen"""
    is_user = User.query.get(user_id)
    if not is_user:
        return jsonify('There is no such user'), 400
    if request.method == 'POST':
        if not (request.json and 'text' in request.json):
            return jsonify('Cannot find text'), 400
        txt = request.json['text']
        if not (1 <= len(txt) <= 500):
            return jsonify('Text must be between 0 to 501 signs'), 400
        new_post = Post(text=txt, user_id=user_id, time=datetime.now())

        db.session.add(new_post)
        db.session.commit()
        return jsonify("Your post has successfully been uploaded"), 200
    if request.method == 'GET':
        all_posts_for_this_user = User.query.get(user_id).posts
        list_of_all = []
        for pst in all_posts_for_this_user:
            list_of_all.append(pst.to_dict())
        return jsonify(list_of_all), 200


@app.route('/user/<user_id>/post/<post_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def get_put_delete_post(post_id, user_id):  # Ska man kunna ändra texten i ens inlägg??? Ta väck put?
    """ Hämtar, ändrar eller tar väck ett inlägg """
    is_post = Post.query.get(post_id)
    if not is_post:
        return jsonify('There is no such post'), 400
    is_user = User.query.get(user_id)
    if not is_user:
        return jsonify('There is no such user'), 400
    if request.method == 'GET':
        print("TJENA")
        return jsonify(is_post.to_dict()), 200
    if not is_post.user_id == is_user.id:
        return jsonify('You cannot delete someone elses post'), 400
    if request.method == 'PUT':
        if not ('text' in request.json):
            return jsonify('You can only edit the text of your own post'), 400
        is_post.text = request.json['text']
        db.session.commit()
        return jsonify('Text edited successfully'), 200
    if request.method == 'DELETE':
        db.session.delete(is_post)
        db.session.commit()
        return jsonify('Post deleted successfully'), 200


@app.route('/user/<user_id>/post/<post_id>/comment', methods=['POST'])
@jwt_required()
def post_comment(post_id, user_id):
    """ Lägger till en kommentar på ett inlägg """
    if request.method == 'POST':
        is_user = User.query.get(user_id)
        if not is_user:
            return jsonify('There is no such user'), 400
        is_post = Post.query.get(post_id)
        if not is_post:
            return jsonify('There is no such post'), 400
        com = request.json['comment']
        if not (1 <= len(com) <= 200):
            return jsonify('Comment must be between 0 to 201 signs'), 200
        new_comment = Comment(user_id=user_id, post_id=post_id, comment=com, time=datetime.now())
        db.session.add(new_comment)
        db.session.commit()
        return jsonify("You have successfully added a comment"), 200


@app.route('/user/<user_id>/post/<post_id>/comment/<comment_id>', methods=['GET', 'DELETE'])
@jwt_required()
def get_delete_comment(post_id, user_id, comment_id):  # Fixa så att vem som helst inte kan ta väck alla kommentarer
    """ Hämtar eller raderar en kommentar på ett inlägg """
    is_user = User.query.get(user_id)
    if not is_user:
        return jsonify('There is no such user'), 400
    is_post = Post.query.get(post_id)
    if not is_post:
        return jsonify('There is no such post'), 400
    is_comment = Comment.query.filter_by(user_id=user_id, post_id=post_id, id=comment_id).first()
    if not is_comment:
        return jsonify("No such comment"), 400
    if request.method == 'GET':
        return jsonify(is_comment.to_dict()), 200
    if request.method == 'DELETE':
        db.session.delete(is_comment)
        db.session.commit()
        return jsonify('Comment deleted successfully'), 200


@app.route("/user/<user_id>/post/<post_id>/like", methods=["POST"])
@jwt_required()
def like(user_id, post_id):
    """ Skapar en like """
    if request.method == "POST":
        user = User.query.get(user_id)
        post = Post.query.get(post_id)
        if not user:
            return jsonify("User id does not exist"), 400
        if not post:
            return jsonify("Post to like does not exist"), 400
        if Like.query.filter_by(post_id=post_id, user_id=user_id).first():
            return jsonify("This user already likes this post"), 200
        new_like = Like(post_id=post_id, user_id=user_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify("Like added"), 200


@app.route("/user/<user_id>/post/<post_id>/like/<like_id>", methods=["DELETE"])
@jwt_required()
def unlike(user_id, post_id, like_id):
    """ Tar väck en like """
    if request.method == "DELETE":
        user = User.query.get(user_id)
        post = Post.query.get(post_id)
        temp_like = Like.query.get(like_id)
        if not user:
            return jsonify("This user does not exist"), 400
        if not post:
            return jsonify("This post does not exist"), 400
        if not temp_like:
            return jsonify("The like to be removed does not exist"), 200
        db.session.delete(temp_like)
        db.session.commit()
        return jsonify("Like removed"), 200




@app.route("/user/<int:user_id>/following", methods=["POST"])
@jwt_required()
def follow(user_id):
    """ Skapar en follow """
    if request.method == "POST":
        data = request.get_json()
        follow_id = data["user_id"]
        user = User.query.get(user_id)
        if not user:
            return jsonify("User id does not exist"), 400
        if not User.query.get(follow_id):
            return jsonify("User to follow does not exist"), 400
        if str(user_id) == str(follow_id):
            return jsonify("You cannot follow yourself"), 200
        if follow_id in [user_.id for user_ in user.following]:
            return jsonify("User is already following this user"), 200
        user.following.append(User.query.get(follow_id))
        db.session.commit()
        return jsonify("Follow added"), 200



@app.route("/user/<int:user_id>/following/<int:follow_id>", methods=["DELETE"])
@jwt_required()
def unfollow(user_id, follow_id):
    """ Tar väck en follow """
    if request.method == "DELETE":
        user = User.query.get(user_id)
        if not user:
            return jsonify("User id does not exist"), 400
        if not User.query.get(follow_id):
            return jsonify("User to follow does not exist"), 400
        if user_id == follow_id:
            return jsonify("You cannot unfollow yourself"), 200
        if follow_id not in [user_.id for user_ in user.following]:
            return jsonify("User is currently not following this user"), 200
        user.following.remove(User.query.get(follow_id))
        db.session.commit()
        return jsonify("Unfollowed user"), 200


@app.route("/create_all")
def create_all():
    db.create_all()
    return jsonify("Tables created"), 200


@app.route("/drop_all")
def drop_all():
    db.drop_all()
    return jsonify("Tables dropped"), 200


@app.errorhandler(ValueError)
def handle_bad_value(e):
    return jsonify(str(e)), 400
