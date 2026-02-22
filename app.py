from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "supersecret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100))
    feedback = db.Column(db.Text)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        new_message = Message(
            name=request.form["name"],
            email=request.form["email"],
            subject=request.form["subject"],
            message=request.form["message"],
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect("/")
    return render_template("contact.html")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/messages")
def messages():
    all_messages = Message.query.all()
    return render_template("messages.html", messages=all_messages)


@app.route("/blog")
def blog():
    posts = Blog.query.all()
    return render_template("blog.html", posts=posts)


@app.route("/blog/<int:id>")
def blog_detail(id):
    post = Blog.query.get_or_404(id)
    return render_template("blog_detail.html", post=post)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/testimonials")
def testimonials():
    reviews = Testimonial.query.all()
    return render_template("testimonials.html", reviews=reviews)


@app.route("/portfolio/<int:id>")
def portfolio_detail(id):
    return render_template("portfolio_detail.html", id=id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
