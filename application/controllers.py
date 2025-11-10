from flask import Flask, render_template,redirect,request
from flask import current_app as app
from .models import *

@app.route("/login",methods=["GET","POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    pwd = request.form.get("pwd")
    this_user = User.query.filter_by(username=username).first()
    if this_user:
      if this_user.password == pwd:
        if this_user.type == "manager":
          return redirect("/manager")
        else:
          return redirect(f"/home/{this_user.id}")
      else:
        return render_template("incorrect_p.html")
    else:
      return render_template("not_exist.html")
        
  return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    pwd = request.form.get("pwd")
    user_name= User.query.filter_by(username=username).first()
    user_email= User.query.filter_by(email=email).first()
    if user_name or user_email:
      return render_template("already.html")
    else:
      new_user = User(username=username,email=email,password=pwd)#LHS > column name, RHS > value
      db.session.add(new_user)
      db.session.commit()
      return redirect("/login")

  return render_template("register.html")

@app.route("/manager")
def manager():
  this_user = User.query.filter_by(type="manager").first()
  all_prod = Product.query.all()
  return render_template("manager_dash.html", this_user=this_user, all_prod=all_prod)

@app.route("/home/<int:user_id>")
def home(user_id):
  this_user = User.query.filter_by(id=user_id).first()
  all_prod = Product.query.all()
  return render_template("user_dash.html", this_user=this_user, all_prod=all_prod)

@app.route("/create",methods=["GET","POST"])
def create():
  if request.method == "POST":
    name = request.form.get("name")
    cat = request.form.get("cat")
    iq = request.form.get("iq")
    cu = request.form.get("cu")
    new_prod = Product(name=name,category=cat,quantity=iq,cost=cu)
    db.session.add(new_prod)
    db.session.commit()
    return redirect("/manager")
  return render_template("create_product.html")

@app.route("/update/<int:prod_id>",methods=["GET","POST"])
def update(prod_id):
  prod=Product.query.filter_by(id=prod_id).first()
  if request.method == "POST":
    cat = request.form.get("cat")
    qu = request.form.get("qu")
    cu = request.form.get("cu")
    prod.category=cat
    prod.quantity=qu
    prod.cost=cu
    db.session.commit()
    return redirect("/manager")

  return render_template("update_product.html",prod=prod)

@app.route("/manager/requests")
def m_requests():
  this_user = User.query.filter_by(type="manager").first()
  all_prod = Product.query.filter_by(status="requested").all()
  return render_template("manager_request.html", this_user=this_user, all_prod=all_prod)

@app.route("/user/requests/<int:user_id>")
def u_requests(user_id):
  this_user = User.query.filter_by(id=user_id).first()
  return render_template("user_request.html", this_user=this_user)
# @app.route
# 1. from models import * >will look for this file in root directory
# 2. from .models import * >will look for this file in current directory(application folder)
# 3. from application.models import * > controllers.py will think that there is one more application folder in the root directory(application folder) with respect to controllers.py
