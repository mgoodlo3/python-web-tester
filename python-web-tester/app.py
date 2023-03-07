from flask import Flask, request, jsonify, render_template
from axe_selenium_python import Axe
from selenium import webdriver
import platform


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/checker", methods=["POST"])
def checker():
    url = request.form.get("url")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
 
    if platform.system() == "Linux":
        driver = webdriver.Chrome(executable_path="./drivers/chromedriver", options=options)
    elif platform.system() == "Windows":
        driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe", options=options)
    else:
        return jsonify({"msg": "Unsupported operating system"})
    
    driver.get(url)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    driver.quit()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
