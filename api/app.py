import os

import bcrypt
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/projet_api')
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

"""
##########
# MODELS #
##########
"""


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return (f"User(First name = {self.firstname}, name = {self.name}, birthdate = {self.birthdate}, "
                f"email = {self.email}, role = {self.role})")


class TicketModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client_model.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'), nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(80), nullable=False)

    user = db.relationship('UserModel', backref='tickets')
    client = db.relationship('ClientModel', backref='tickets')
    project = db.relationship('ProjectModel', backref='tickets')

    def __repr__(self):
        return f"Ticket(Title = {self.title}, description = {self.description}, status = {self.status})"


class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Project(Name = {self.name})"


class ClientModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return (f"Client(First name = {self.firstname}, name = {self.name}, company = {self.company}, "
                f"email = {self.email}, phone = {self.phone})")


"""
###########
# PARSING #
###########
"""

user_args = reqparse.RequestParser()
user_args.add_argument('firstname', type=str, required=True, help="First name cannot be blank")
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('birthdate', type=str, required=True, help="Birthdate cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('role', type=str, required=True, help="Role cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")

ticket_args = reqparse.RequestParser()
ticket_args.add_argument('user_id', type=int, required=True, help="User ID cannot be blank")
ticket_args.add_argument('project_id', type=int, required=True, help="Project ID cannot be blank")
ticket_args.add_argument('client_id', type=int, required=True, help="Client ID cannot be blank")
ticket_args.add_argument('title', type=str, required=True, help="Title cannot be blank")
ticket_args.add_argument('description', type=str, required=True, help="Description cannot be blank")
ticket_args.add_argument('status', type=str, required=True, help="Status cannot be blank")

project_args = reqparse.RequestParser()
project_args.add_argument('name', type=str, required=True, help="Name cannot be blank")

client_args = reqparse.RequestParser()
client_args.add_argument('firstname', type=str, required=True, help="First name cannot be blank")
client_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
client_args.add_argument('company', type=str, required=True, help="Company cannot be blank")
client_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
client_args.add_argument('phone', type=str, required=True, help="Phone cannot be blank")

"""
##########
# FIELDS #
##########
"""

userFields = {
    'id': fields.Integer,
    'firstname': fields.String,
    'name': fields.String,
    'birthdate': fields.String,
    'email': fields.String,
    'role': fields.String,
    'password': fields.String
}

ticketFields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "project_id": fields.Integer,
    "client_id": fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'status': fields.String
}

projectFields = {
    "id": fields.Integer,
    'name': fields.String
}

clientFields = {
    "id": fields.Integer,
    "name": fields.String,
    "firstname": fields.String,
    "company": fields.String,
    "email": fields.String,
    "phone": fields.String
}

"""
#############
# RESOURCES #
#############
"""


class Users(Resource):
    @jwt_required()
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        current_user = get_jwt_identity()
        args = user_args.parse_args()

        if args['role'] not in ['developer', 'reporter', 'admin']:
            abort(400, message="Role must be either 'developer', 'reporter' or 'admin'")

        if args['role'] == 'admin' and current_user['role'] != 'admin':
            abort(400, message='Only admins can create an admin user.')

        birthdate = datetime.strptime(args["birthdate"], '%Y-%m-%d').date()
        hashed_password = bcrypt.hashpw(args['password'].encode('utf-8'), bcrypt.gensalt())

        user = UserModel(firstname=args["firstname"], name=args["name"], birthdate=birthdate,
                         email=args["email"], role=args["role"], password=hashed_password.decode('utf8'))
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201


class User(Resource):
    @jwt_required()
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User was not found")
        return user

    @jwt_required()
    @marshal_with(userFields)
    def put(self, id):
        current_user = get_jwt_identity()

        if current_user['id'] != id and current_user['role'] != 'admin':
            abort(403, message='You are not authorized to modify this account')

        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User was not found")
        user.firstname = args["firstname"]
        user.name = args["name"]
        user.birthdate = datetime.strptime(args["birthdate"], '%Y-%m-%d').date()
        user.email = args["email"]
        user.role = args["role"]
        hashed = bcrypt.hashpw(args['password'].encode('utf-8'), bcrypt.gensalt())
        user.password = hashed.decode('utf8')
        db.session.commit()
        return user

    @jwt_required()
    @marshal_with(userFields)
    def delete(self, id):
        current_user = get_jwt_identity()

        if current_user['id'] != id and current_user['role'] != 'admin':
            abort(403, message='You are not authorized to delete this account')

        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User was not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users


class Tickets(Resource):
    @jwt_required()
    @marshal_with(ticketFields)
    def get(self):
        tickets = TicketModel.query.all()
        return tickets

    @jwt_required()
    @marshal_with(ticketFields)
    def post(self):
        args = ticket_args.parse_args()

        if args['status'] not in ['ongoing', 'completed', 'cancelled', 'paused']:
            abort(400, message="Status must be either 'ongoing', 'completed', 'cancelled' or 'paused'")

        ticket = TicketModel(user_id=args["user_id"], project_id=args["project_id"], client_id=args["client_id"],
                             title=args["title"], description=args["description"], status=args["status"])
        db.session.add(ticket)
        db.session.commit()
        tickets = TicketModel.query.all()
        return tickets, 201


class Ticket(Resource):
    @jwt_required()
    @marshal_with(ticketFields)
    def get(self, id):
        ticket = TicketModel.query.filter_by(id=id).first()
        if not ticket:
            abort(404, message="Ticket was not found")
        return ticket

    @jwt_required()
    @marshal_with(ticketFields)
    def put(self, id):
        args = ticket_args.parse_args()
        ticket = TicketModel.query.filter_by(id=id).first()
        if not ticket:
            abort(404, message="Ticket was not found")
        ticket.user_id = args["user_id"]
        ticket.client_id = args["client_id"]
        ticket.project_id = args["project_id"]
        ticket.title = args["title"]
        ticket.description = args["description"]
        ticket.status = args["status"]
        db.session.commit()
        return ticket

    @jwt_required()
    @marshal_with(ticketFields)
    def delete(self, id):
        ticket = TicketModel.query.filter_by(id=id).first()
        if not ticket:
            abort(404, message="Ticket was not found")
        db.session.delete(ticket)
        db.session.commit()
        tickets = TicketModel.query.all()
        return tickets


class Projects(Resource):
    @jwt_required()
    @marshal_with(projectFields)
    def get(self):
        projects = ProjectModel.query.all()
        return projects

    @jwt_required()
    @marshal_with(projectFields)
    def post(self):
        args = project_args.parse_args()

        project = ProjectModel(name=args["name"])
        db.session.add(project)
        db.session.commit()
        projects = ProjectModel.query.all()
        return projects, 201


class Project(Resource):
    @jwt_required()
    @marshal_with(projectFields)
    def get(self, id):
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404, message="Project was not found")
        return project

    @jwt_required()
    @marshal_with(projectFields)
    def put(self, id):
        args = project_args.parse_args()
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404, message="Project was not found")
        project.name = args["name"]
        db.session.commit()
        return project

    @jwt_required()
    @marshal_with(projectFields)
    def delete(self, id):
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404, message="Project was not found")
        db.session.delete(project)
        db.session.commit()
        projects = ProjectModel.query.all()
        return projects


class Clients(Resource):
    @jwt_required()
    @marshal_with(clientFields)
    def get(self):
        clients = ClientModel.query.all()
        return clients

    @jwt_required()
    @marshal_with(clientFields)
    def post(self):
        args = client_args.parse_args()

        client = ClientModel(firstname=args["firstname"], name=args["name"], company=args["company"],
                             email=args["email"], phone=args["phone"])
        db.session.add(client)
        db.session.commit()
        clients = ClientModel.query.all()
        return clients, 201


class Client(Resource):
    @jwt_required()
    @marshal_with(clientFields)
    def get(self, id):
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            abort(404, message="Client was not found")
        return client

    @jwt_required()
    @marshal_with(clientFields)
    def put(self, id):
        args = client_args.parse_args()
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            abort(404, message="Client was not found")
        client.name = args["name"]
        client.firstname = args["firstname"]
        client.company = args["company"]
        client.email = args["email"]
        client.phone = args["phone"]
        db.session.commit()
        return client

    @jwt_required()
    @marshal_with(clientFields)
    def delete(self, id):
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            abort(404, message="Client was not found")
        db.session.delete(client)
        db.session.commit()
        clients = ClientModel.query.all()
        return clients


class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
        args = parser.parse_args()

        user = UserModel.query.filter_by(email=args['email']).first()
        if user and bcrypt.checkpw(args['password'].encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity={'id': user.id, 'role': user.role})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401


"""
##########
# ROUTES #
##########
"""

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Tickets, '/api/tickets/')
api.add_resource(Ticket, '/api/tickets/<int:id>')
api.add_resource(Projects, '/api/projects/')
api.add_resource(Project, '/api/projects/<int:id>')
api.add_resource(Clients, '/api/clients/')
api.add_resource(Client, '/api/clients/<int:id>')
api.add_resource(Auth, '/api/auth/')

if __name__ == '__main__':
    app.run(debug=True)
