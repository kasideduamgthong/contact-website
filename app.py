# ==========================================
# Contact Website - Flask Application
# Developed by Kasided
# ==========================================

# ---------- Import Libraries ----------
from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ---------- App Configuration ----------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "contactwebsite_secret_key_2026"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Database Models ----------


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100))
    feedback = db.Column(db.Text)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# ---------- Routes ----------


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


@app.route("/portfolio/<int:id>")
def portfolio_detail(id):
    return render_template("portfolio_detail.html", id=id)


# ---------- Contact ----------


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

        flash("Your message has been sent successfully!")
        return redirect("/")

    return render_template("contact.html")


@app.route("/delete-message/<int:id>")
def delete_message(id):

    if not session.get("user_id"):
        return redirect("/admin-login")

    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()

    flash("Message deleted successfully!")
    return redirect("/dashboard")


# ---------- Blog System ----------


@app.route("/blog")
def blog():
    posts = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template("blog.html", posts=posts)


@app.route("/blog/<int:id>")
def blog_detail(id):
    post = Blog.query.get_or_404(id)
    return render_template("blog_detail.html", post=post)


@app.route("/add-blog", methods=["GET", "POST"])
def add_blog():

    if not session.get("user_id"):
        return redirect("/admin-login")

    if request.method == "POST":
        new_post = Blog(title=request.form["title"], content=request.form["content"])
        db.session.add(new_post)
        db.session.commit()

        flash("Blog post added successfully!")
        return redirect("/blog")

    return render_template("add_blog.html")


@app.route("/edit-blog/<int:id>", methods=["GET", "POST"])
def edit_blog(id):

    if not session.get("user_id"):
        return redirect("/admin-login")

    post = Blog.query.get_or_404(id)

    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()

        flash("Blog updated successfully!")
        return redirect("/blog")

    return render_template("edit_blog.html", post=post)


@app.route("/delete-blog/<int:id>")
def delete_blog(id):

    if not session.get("user_id"):
        return redirect("/admin-login")

    post = Blog.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    flash("Blog deleted successfully!")
    return redirect("/blog")


# ---------- Dashboard ----------


@app.route("/dashboard")
def dashboard():

    if not session.get("user_id"):
        flash("Please login first!")
        return redirect("/admin-login")

    total_messages = Message.query.count()
    total_posts = Blog.query.count()
    total_testimonials = Testimonial.query.count()
    recent_messages = Message.query.order_by(Message.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_messages=total_messages,
        total_posts=total_posts,
        total_testimonials=total_testimonials,
        recent_messages=recent_messages,
    )


# ---------- Testimonials ----------


@app.route("/testimonials")
def testimonials():
    reviews = Testimonial.query.all()
    return render_template("testimonials.html", reviews=reviews)


# ---------- Authentication ----------


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect("/register")

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.")
        return redirect("/admin-login")

    return render_template("register.html")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!")
            return redirect("/dashboard")
        else:
            flash("Invalid credentials!")

    return render_template("admin_login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")


# ---------- Run Application ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
