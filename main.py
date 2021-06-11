import requests
from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS
from app import create_newusers, posts
import sqlite3 as sql
from os import path
import functools

my_app = Flask(__name__)
CORS(my_app)

pic_folder = path.join('static', 'photos')
my_app.config["UPLOAD_FOLDER"] = pic_folder

ROOT = path.dirname(path.relpath(__file__))

con = sql.connect(path.join(ROOT, 'database.db'), check_same_thread=False)
cur = con.cursor()
con.commit()

ROOT = path.dirname(path.join(__file__))
conn = sql.connect(path.join(ROOT, 'postss.db'), check_same_thread=False)
curser = conn.cursor()
query_auther = "SELECT auther FROM data"
query_title = "SELECT title FROM data"
query_post = "SELECT post FROM data"
query_id = "SELECT rowid FROM data"
usr_auther = curser.execute(query_auther).fetchall()
usr_title = curser.execute(query_title).fetchall()
usr_post = curser.execute(query_post).fetchall()
usr_id = curser.execute(query_id).fetchall()
conn.commit()


@my_app.route("/", methods=['POST', 'GET'])
def login_page():
    if request.method == "POST":
        pic1 = path.join(my_app.config["UPLOAD_FOLDER"], "image3.png")
        pic2 = path.join(my_app.config["UPLOAD_FOLDER"], "image1.png")
        name1 = request.form.get('username')
        pwd = request.form.get('password')
        rid = cur.execute("SELECT rowid FROM newusers").fetchall()
        usrname = cur.execute("SELECT username FROM newusers").fetchall()
        pas = cur.execute("SELECT password FROM newusers WHERE username='" + str(name1) + "';").fetchall()
        title = curser.execute("SELECT title FROM data WHERE auther='" + str(name1) + "';").fetchall()
        ptss = curser.execute("SELECT post FROM data WHERE auther='" + str(name1) + "';").fetchall()
        for i in range(len(rid)):
            final = ''.join(usrname[i])
            if name1 == final:
                pw = ''.join(pas[0])
                if pwd == pw:
                    return render_template("my_profile.html", name1=name1.capitalize(), pic=pic1, pic1=pic2, title=title, name=name1, post=ptss)

                else:
                    return render_template("login.html", info='Invalid Password')
            else:
                i += 1
    if request.method == 'GET':
        pass
    return render_template("login.html")


@my_app.route("/users_my_profile", methods=['POST', 'GET'])
def myprofile():
    pic1 = path.join(my_app.config["UPLOAD_FOLDER"], "image3.png")
    pic2 = path.join(my_app.config["UPLOAD_FOLDER"], "image1.png")
    return render_template("my_profile.html", pic=pic1, pic1=pic2)


@my_app.route("/homepage", methods=['POST', 'GET'])
def home_page():
    render_template("login.html")
    pic_1 = path.join(my_app.config["UPLOAD_FOLDER"], "image6.jpg")
    title_1 = curser.execute("SELECT title FROM data").fetchall()
    auther = curser.execute("SELECT auther FROM data").fetchall()
    if request.method == 'POST':
        pic1 = path.join(my_app.config["UPLOAD_FOLDER"], "image4.png")
        username = request.form.get('searchusername')
        title = curser.execute("SELECT title FROM data WHERE auther='" + username + "';").fetchall()
        post = curser.execute("SELECT post FROM data WHERE auther='" + username + "';").fetchall()
        return render_template("search_users.html", name1=username.capitalize(), title=title, pic=pic1, post=post)
    return render_template("homepage.html", pic=pic_1, title=title_1, auther=auther)


# @my_app.route("/homepage_kids",methods= ['POST', 'GET'])
# def homepage_kids():
#     pic_1 = path.join(my_app.config["UPLOAD_FOLDER"], "image7.png")
#     auther = cur.execute("SELECT username FROM newusers WHERE age <18")
#     return render_template("homepage_kids.html", pic=pic_1)
#
# auther = cur.execute("SELECT username FROM newusers WHERE age <18").fetchall()
# for i in range(10):
#     athr = ''.join(auther[i])
#     i+=1
#     print(athr)

@my_app.route("/newuserlogin", methods=['POST', 'GET'])
def new_user_login():
    pic_1 = path.join(my_app.config["UPLOAD_FOLDER"], "image7.png")
    username = ""
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        username = request.form.get('username1')
        password = request.form.get('password1')
        email = request.form.get('email')
        age = request.form.get('age')
        create_newusers(username, password, email, age)
    return render_template("new_user.html", name=username, pic= pic_1)


@my_app.route("/users_posts_page", methods=['POST', 'GET'])
def post_page():
    name1 = request.form.get('username')
    pic3 = path.join(my_app.config["UPLOAD_FOLDER"], "image5.png")
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        auther = request.form.get('auther')
        title = request.form.get('title')
        post = request.form.get('post')
        posts(auther, title, post)
        return render_template("new_post.html", pic=pic3, auther=name1)
    return render_template("new_post.html", pic=pic3, auther=name1)


# @my_app.route("/post_details_default")
# def defaultpost():
#     return render_template("post_details_default.html")

# CHANGE-PASSWORD

@my_app.route("/change_password", methods=['POST', 'GET'])
def new_pass():
    global i
    mail = request.form.get("user_mail")
    mal = cur.execute("SELECT email FROM newusers").fetchall()
    rid = cur.execute("SELECT rowid FROM newusers").fetchall()
    new_pswd = request.form.get("new_pass")
    if request.method == 'POST':
        for i in range(len(rid)):
            abc = ''.join(mal[i])
            if mail == abc:
                cur.execute("UPDATE newusers SET password = (?) WHERE email = (?)", (new_pswd,) + (mail,))
                con.commit()
                return render_template("sucessful_1.html", paswrd=new_pswd)
            else:
                i += 1
    if request.method == 'GET':
        pass
    return render_template("change_password.html")


@my_app.route("/about_me")
def aboutme():
    pic = path.join(my_app.config["UPLOAD_FOLDER"], "ig.png")
    pic1 = path.join(my_app.config["UPLOAD_FOLDER"], "fb.png")
    pic2 = path.join(my_app.config["UPLOAD_FOLDER"], "twitter.png")
    return render_template("/about_me.html", pic=pic, pic1=pic1, pic2=pic2)


@my_app.route("/post_details", methods=['GET', 'POST'])
def details():
    title1 = curser.execute("SELECT title FROM data").fetchall()
    post1 = curser.execute("SELECT post FROM data").fetchall()
    auther = curser.execute("SELECT auther FROM data").fetchall()
    return render_template('post_details.html', post=post1, auther=auther, title=title1)


@my_app.route("/search", methods=['POST', 'GET'])
def search():
    return render_template("search_users.html")


@my_app.route("/log_out", methods=['POST', 'GET'])
def delete_account():
    if request.method == 'POST':
        email = request.form.get("user_mail")
        paswd = request.form.get("pass")
        paswrd = cur.execute("SELECT password FROM newusers WHERE email='" + email + "';").fetchall()
        pswrd = ''.join(paswrd[0])
        if paswd == pswrd:
            cur.execute("DELETE from newusers WHERE email=(?)", (email,))
            con.commit()
            return render_template("sucessful.html")
        else:
            return render_template("delete_account.html", info="Invalid Password")
    if request.method == 'GET':
        pass
    return render_template("delete_account.html")


@my_app.route("/delete_post", methods=['POST', 'GET'])
def delete_post():
    if request.method == 'POST':
        title = request.form.get("user_title")
        password = request.form.get("user_pass")
        ids = curser.execute("SELECT rowid FROM data").fetchall()
        ttle = curser.execute("SELECT title FROM data").fetchall()
        for i in range(len(ids)):
            final_title = ''.join(ttle[i])
            if title == final_title:
                usr_auther = curser.execute("SELECT auther FROM data WHERE title='" + title + "';").fetchall()
                ua = ''.join(usr_auther[0])
                usr_pas = cur.execute("SELECT password FROM newusers WHERE username='" + ua + "';").fetchall()
                pswrd = ''.join(usr_pas[0])
                if password == pswrd:
                    curser.execute("DELETE from data WHERE title=(?)", (title,))
                    conn.commit()
                    return render_template("sucessful_2.html")
                else:
                    return render_template("Delete_post.html", info="Invalid Password")
            else:
                i+=1
    if request.method == 'GET':
        pass
    return render_template("Delete_post.html")


@my_app.route("/search_url", methods=['POST', 'GET'])
def searchurl():
    if request.method == 'POST':
        url = request.form.get('srch')
        aderess = "http://api.linkpreview.net/?key=7f80de09d5a7d26d3cfcb400bcc289b1&q={0}".format(url)
        response = requests.get(aderess)
        data = response.json()
        title = data['title']
        description = data['description']
        image = data['image']
        more = data['url']
        return render_template("search_url.html", title=title, description=description, image=image, url=more)
    if request.method == 'GET':
        pass
    return render_template("search_url.html")


@my_app.route("/all_posts", methods=['POST','GET'])
def all_posts():
    postss = curser.execute("SELECT post FROM data").fetchall()
    return render_template("all_posts.html",post = postss, )


@my_app.route("/edit_post", methods=['POST','GET'])
def editpost():
    title1 = request.form.get('title_old')
    title = request.form.get('title_new')
    post = request.form.get('post_new')
    if request.method == 'POST':
        curser.execute("UPDATE data SET title= (?) WHERE title= (?)", (title,) + (title1,))
        curser.execute("UPDATE data SET post= (?) WHERE title= (?)", (post,) + (title,))
        conn.commit()
    return render_template("edit_post.html")

if __name__ == "__main__":
    my_app.run(debug=True)