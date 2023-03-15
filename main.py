from flask import Flask, request, render_template, redirect, session
from flask_session import Session
import helper as ffw

app = Flask(__name__)
# configure app to use sessions
app.config["SESSION_PERMANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# to set session variables --> session["varname"] = value
# to get session variables --> session.get("varname") or session["varname"]
# to "clear" session variables --> session["varname"] = None

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET": # they clicked the link/button
    return render_template("login.html")
  else: # filled out the login form
    # get the email from the form
    email = request.form.get("member_email")
    # load the current members
    index, member = ffw.get_member(email)
    if member: # there was a match for the email
      #set the logged_in session variable
      session["logged_in"] = True
      session["cur_member"] = member
      session["member_index"] = index
      return redirect("/")
    else: # not match was found
      return render_template("join.html", email=email)

@app.route("/join", methods=["GET", "POST"])
def join():
  if request.method == "POST": # filled out the form
    # get all the data from the form
    member = {
      "email": request.form.get("email"),
      "first_name": request.form.get("first_name"),
      "last_name": request.form.get("last_name")
    }
    # now add the new member dict to the list of MEMBERS
    ind = ffw.add_member(member)
    session["logged_in"] = True
    session["cur_member"] = member
    session["member_index"] = ind
    return redirect("/")
  return render_template("join.html")

@app.route("/update/<int:ind>", methods=["GET","POST"])
def update_member(ind):
  if request.method == "GET": #clicked the link
    # check for user access
    if ind == session.get("member_index"):
      # get the member info by their index number
      member = ffw.get_member_by_index(ind)
      if not member:
        return "<h1>No Member with that index</h1>"
      # show a form that will allow them to make changes
      return render_template("update_mem.html", member=member)
    else: # index did NOT match the session
      return "<h1>You Do NOT have Permission to access this page!!!</h1>"
  else: # they updated their info with the form (POST)
    # get the form data
    member = {
      "first_name": request.form.get("first_name"),
      "last_name": request.form.get("last_name")
    }
    # update the member info
    ffw.update_member_information(ind, member)
    # update the session 
    session.get("cur_member").update(member)
    return redirect("/")

@app.route("/logout")
def logout():
  # clear out all session variables and go back to the home page
  # session["logged_in"] = None
  # session["cur_member"] = None
  session.clear()
  return redirect("/")

if __name__ == "__main__":
  app.run("0.0.0.0", debug=True)
