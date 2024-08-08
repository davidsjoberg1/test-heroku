from . import app, db
from flask_bcrypt import Bcrypt
#from golfbuddy.helper import sort_list_by_time




bcrypt = Bcrypt(app)

follows = db.Table('follows',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                   db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

feed = db.Table('feed',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))

db.Model.id = db.Column(db.Integer, primary_key=True)


class User(db.Model):
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    hcp = db.Column(db.Float(precision=1), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    following = db.relationship("User", follows, primaryjoin=lambda: User.id == follows.c.user_id,
                                secondaryjoin=lambda: User.id == follows.c.followed_id,
                                backref="followers")

    def __init__(self, name, gender, birthdate, hcp, email, password):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.hcp = hcp
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def to_dict(self):
        result = {'name': self.name,
                  'gender': self.gender,
                  'email': self.email,
                  'birthdate': self.birthdate,
                  'hcp': self.hcp,
                  'password': self.password,
                  'id': self.id,
                  'posts': [x.to_dict() for x in self.posts],
                  'following': [user_.name for user_ in self.following],
                  'followers': [user_.name for user_ in self.followers],
                  'feed': self.feed()}
        return result

    def feed(self):
        """ Skapar en lista med alla ens följares samt ens egna inlägg """
        list_of_users_id = [x.id for x in self.following] + [self.id]
        feed_list = []
        for usr_id in list_of_users_id:
            usr = User.query.get(usr_id)
            for post in usr.posts:
                feed_list = sort_list_by_time(feed_list, post.to_dict())
        return feed_list

    """
    def follow(self, follow_id):
        ""Kollar om vi kan göra en ny follow och gör isf det ""
        if self.id == follow_id:
            raise ValueError("You can not follow yourself")
        if follow_id in [user_.id for user_ in self.following]:
            raise ValueError("User is already following this user")
        self.following.append(User.query.get(follow_id))
        db.session.commit()

    def unfollow(self, follow_id):
        "" Kollar om en follow kan tas väck och gör isf det ""
        if self.id == follow_id:
            raise ValueError("You can not unfollow yourself")
        if follow_id not in [user_.id for user_ in self.following]:
            raise ValueError("User is currently not following this user")
        self.following.remove(User.query.get(follow_id))
        db.session.commit()
        """


class Post(db.Model):
    text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    like = db.relationship('Like', backref='post', lazy=True)
    time = db.Column(db.String(100))

    def to_dict(self):
        result = {'text': self.text,
                  'id': self.id,
                  'user_id': self.user_id,
                  'likes': [Like.query.get(like_.id).to_dict() for like_ in self.like],
                  'comment': self.comment_list(),
                  'time': self.time}
        return result

    def comment_list(self):
        """ Sorterar kommentarer sett till när de publicerades """
        list_of_comment_id = [x.id for x in self.comments]
        comments_list = []
        for comment_id in list_of_comment_id:
            comment = Comment.query.get(comment_id)
            comments_list = sort_list_by_time(comments_list, comment.to_dict())
        return comments_list

    """

    def liked(self, user_id):
        if Like.query.filter_by(post_id=self.id, user_id=user_id).first():
            raise ValueError("This user already likes this post")
        if self.id in [post.id for post in User.query.get(user_id).posts]:
            raise ValueError("You cannot like your own post")
        new_like = Like(post_id=self.id, user_id=user_id)
        db.session.add(new_like)
        db.session.commit()
        """



class Comment(db.Model):
    comment = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    time = db.Column(db.String(100))

    def to_dict(self):
        result = {'id': self.id,
                  'comment': self.comment,
                  'user_id': self.user_id,
                  'post_id': self.post_id,
                  'time': self.time}
        return result


class Like(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        result = {"post_id": self.post_id,
                  "user_id": self.user_id,
                  "id": self.id}
        return result


class TokenBlockList(db.Model):
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
