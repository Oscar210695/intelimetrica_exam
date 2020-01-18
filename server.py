from flask import render_template
import config

#Application instance
connex_app = config.connex_app

#swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

#Create a URL route
@connex_app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    connex_app.run(debug=True)