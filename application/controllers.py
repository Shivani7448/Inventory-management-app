from flask import Flask, render_template,redirect,request
from flask import current_app as app #it refers to the app object created
from .models import * # both resides in same folder
from application.utils import grandTotal
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

@app.route("/login",methods=["GET","POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    pwd = request.form.get("pwd")
    this_user = User.query.filter_by(username=username).first() #LHS attribute name in table, RHS is data fetched from form 
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

@app.route("/register",methods=["GET","POST"])#url with specific http method gives specific resource
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

@app.route("/request/<int:prod_id>/<int:user_id>",methods=["GET","POST"])
def request_prod(prod_id,user_id):
  prod=Product.query.filter_by(id=prod_id).first()
  user=User.query.filter_by(id=user_id).first()
  if request.method == "POST":
    units = request.form.get("units")
    new_req = Request(user_id=user_id,product_id=prod_id,units_requested=units)
    db.session.add(new_req)
    db.session.commit()
    return redirect(f"/home/{user_id}")
  return render_template("request.html",prod=prod,user=user)

@app.route("/manager/requests")
def m_requests():
  this_user = User.query.filter_by(type="manager").first()
  all_req = Request.query.all()
  return render_template("manager_request.html", this_user=this_user, all_req=all_req)

@app.route("/user/requests/<int:user_id>")
def u_requests(user_id):
  this_user = User.query.filter_by(id=user_id).first()
  all_req = Request.query.filter_by(user_id=user_id).all()
  total = grandTotal(all_req)
  return render_template("user_request.html", this_user=this_user, all_req=all_req, total = total)

@app.route("/approve/<int:req_id>")
def approve(req_id):
  req = Request.query.filter_by(id=req_id).first()
  prod=Product.query.filter_by(id=req.product_id).first()
  if prod.quantity < req.units_requested:
    return "<h1>Insufficient Quantity</h1>"
  req.status = "approved"
  prod.quantity = prod.quantity - req.units_requested
  if prod.quantity == 0:
    prod.status = "unavailable"
  db.session.commit()
  return redirect(f"/manager/requests")

@app.route("/deny/<int:req_id>")
def deny(req_id):
  req = Request.query.filter_by(id=req_id).first()
  req.status = "denied"
  db.session.commit()
  return redirect(f"/manager/requests")

@app.route("/search")
def search():
    search_word = request.args.get("search")
    key = request.args.get("key")
    if key == "user":
        # results = User.query.filter_by(username= search_word).all()
        result = User.query.filter_by(username= search_word).first()
    else:
        # results = Product.query.filter_by(name = search_word).all()
        result = Product.query.filter_by(name = search_word).first()
    # return render_template("results.html",results=results,key=key)
    return render_template("result.html",result=result,key=key)

@app.route("/summary")
def summary():
    re=len(Request.query.filter_by(status="requested").all())
    ap=len(Request.query.filter_by(status="approved").all())
    de=len(Request.query.filter_by(status="denied").all())
    
    #graphs
    #pie chart 
    labels = ["Requested","Approved","Denied"]
    sizes =[re,ap,de]
    colors = ["blue","yellow","green"]
    plt.pie(sizes,labels=labels,colors=colors,autopct = "%1.1f%%")
    plt.title("Status of Requests")
    plt.savefig("static/pie.png")
    plt.clf()

    #bar graph 
    labels = ["Requested","Approved","Denied"]
    sizes =[re,ap,de]
    plt.bar(labels,sizes)
    plt.xlabel("Status of Requests")
    plt.ylabel("No of Requests")
    plt.title("Requests Status Distribution")
    plt.savefig("static/bar.png")
    plt.clf()

    return render_template("summary.html",ap=ap,de=de,re=re)
# @app.route
# 1. from models import * >will look for this file in root directory
# 2. from .models import * >will look for this file in current directory(application folder)
# 3. from application.models import * > controllers.py will think that there is one more application folder in the root directory(application folder) with respect to controllers.py

