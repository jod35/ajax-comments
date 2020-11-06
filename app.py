from flask import Flask,request,make_response,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_migrate import Migrate
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+app.root_path +'/base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='917a14cb33e1870222194e1b'
app.debug=True

db=SQLAlchemy(app)
migrate=Migrate(app,db)


class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime(),default=datetime.utcnow)

    def __repr__(self):
        return f"{self.comment}"

    def save(self):
        db.session.add(self)
        db.session.commit()

class CommentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model=Comment
        slqa_session=db.session

    id=fields.Integer(dump_only=True)
    comment=fields.String(required=True)



@app.route('/hello',methods=['GET'])
def hello():
    message={"message":"Hello Welcome To my API"}
    return make_response(jsonify(message))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_comment',methods=['POST'])
def create_comment():
    comment=request.json.get("comment")

    new_comment=Comment(comment=comment)

    new_comment.save()

    comment_schema=CommentSchema()

    comment_schema.dump(new_comment)

    return make_response(jsonify(
        {"success":True,"comment":comment,"message":"Comment Added"}
    ))


@app.route('/get_comments',methods=['GET'])
def get_comments():
    comments=Comment.query.order_by(Comment.id.desc()).all()

    comment_schema=CommentSchema(many=True)
    comments=comment_schema.dump(comments)

    return make_response(jsonify(
        {"success":True,
         "comments":comments
        }
    ))


@app.shell_context_processor
def make_shell_context():
    return {"db":db,"Comment":Comment}




if __name__ == "__main__":
    app.run(debug=True)