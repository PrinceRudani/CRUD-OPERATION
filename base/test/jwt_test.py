# # import jwt
# # import datetime
# #
# # SECRET_KEY = "mysecretkey"
# #
# # def generate_jwt(user_id, role):
# #     payload = {
# #         "user_id": user_id,
# #         "role": role,
# #         "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
# #     }
# #     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
# #
# #
# # def decode_jwt(token):
# #         return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
# #
# #
# # token = generate_jwt(1, "admin")
# # print(token)
# #
# # print(decode_jwt(token))
#
# import jwt
# import datetime
# from flask import Flask, request
#
# app = Flask(__name__)
# SECRET_KEY = "your_secret_key"
#
# def generate_jwt(user_id):
#     payload = {
#         "user_id": user_id,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
#     }
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#
# @app.route('/login', methods=['POST'])
# def login():
#     token = generate_jwt(1)
#     return {"token": token}
#
# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#     token = request.headers.get("Authorization")
#     if not token:
#         return "Unauthorized", 401
#
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return "Welcome to dashboard"
#     except jwt.ExpiredSignatureError:
#         return "Token expired", 401

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this!
jwt = JWTManager(app)

# Mock user data
users = {
    "testuser": "password123"
}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username not in users or users[username] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username, expires_delta=False)

    refresh_token = create_refresh_token(identity=username)

    return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    return jsonify(logged_in_as=identity), 200

if __name__ == '__main__':
    app.run(debug=True)