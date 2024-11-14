from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask( __name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
app.config['SECRET_KEY'] = 'beibfrhcee'

db = SQLAlchemy()
db.init_app(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(300), nullable = False)
    content = db.Column(db.String(1000), nullable = False)

class BlogForm(FlaskForm):
    title = StringField('Add the blog title', validators=[DataRequired()])
    content = StringField('Add your blog' , validators=[DataRequired()])
    add_blog = SubmitField('Add Your Blog')


@app.route('/' , methods = ['POST' , 'GET'])
def home():
    blogs = Blog.query.all()
    return render_template('index.html' , blogs = blogs)

# @app.route('/home')
# def hello():
#     return 'hello world'

@app.route('/add_blog' , methods = ['GET' , 'POST'])
def add_blog():

    form = BlogForm()
    if form.validate_on_submit():
        title = request.form.get('title')
        content = request.form.get('content')
        
        new_blog = Blog(title = title, content = content)
        db.session.add(new_blog)
        db.session.commit()
        print("new blog added successfully")
        return redirect(url_for('home'))

    else:
        print("blog not added!")
    return render_template('add_blog.html', form =form)


@app.route('/edit_blog/<int:blog_id>' , methods = ['GET' , 'POST'])
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = BlogForm(obj = blog)

    if form.validate_on_submit():
        title = request.form.get('title')
        content = request.form.get('content')
        Blog.query.filter_by(id = blog_id).update(dict(title = title, content = content))

        db.session.commit()
        print("Blog successfully updated")
        return redirect(url_for('home'))

    return render_template('edit_blog.html' , form = form)



@app.route('/delete_blog/<int:blog_id>')
def delete_blog(blog_id):
    blog_to_delete = Blog.query.get(blog_id)
    db.session.delete(blog_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

       

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("database created successfully!")
    app.run(debug=True)