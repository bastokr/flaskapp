from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
app = Flask(__name__)
api = Api(app)


# MySQL 연결
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'obom'
app.config['MYSQL_DATABASE_PASSWORD'] = 'obom'
app.config['MYSQL_DATABASE_DB'] = 'obomdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('user_name', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            _userEmail = args['email']
            _userName = args['user_name']
            _userPassword = args['password']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_create_user', (_userEmail, _userName, _userPassword))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode': '200', 'Message': 'User creation success'}
            else:
                return {'StatusCode': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)