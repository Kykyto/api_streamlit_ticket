import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/projet_api')

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
    firstName = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return (f"User(First name = {self.firstName}, name = {self.name}, birthdate = {self.birthdate}, "
                f"email = {self.email}, role = {self.role})")


class TicketModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    clientId = db.Column(db.Integer, db.ForeignKey('client_model.id'), nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('project_model.id'), nullable=False)
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
    firstName = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return (f"User(First name = {self.firstName}, name = {self.name}, company = {self.company}, "
                f"email = {self.email}, phone = {self.phone})")


"""
###########
# PARSING #
###########
"""

user_args = reqparse.RequestParser()
user_args.add_argument('firstName', type=str, required=True, help="First name cannot be blank")
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('birthdate', type=str, required=True, help="Birthdate cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('role', type=str, required=True, help="Role cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")

ticket_args = reqparse.RequestParser()
ticket_args.add_argument('userId', type=int, required=True, help="User ID cannot be blank")
ticket_args.add_argument('projectId', type=int, required=True, help="Project ID cannot be blank")
ticket_args.add_argument('clientId', type=int, required=True, help="Client ID cannot be blank")
ticket_args.add_argument('title', type=str, required=True, help="Title cannot be blank")
ticket_args.add_argument('description', type=str, required=True, help="Description cannot be blank")
ticket_args.add_argument('status', type=str, required=True, help="Status cannot be blank")

project_args = reqparse.RequestParser()
project_args.add_argument('name', type=str, required=True, help="Name cannot be blank")

client_args = reqparse.RequestParser()
client_args.add_argument('firstName', type=str, required=True, help="First name cannot be blank")
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
    'firstName': fields.String,
    'name': fields.String,
    'birthdate': fields.String,
    'email': fields.String,
    'role': fields.String,
    'password': fields.String
}

ticketFields = {
    "id": fields.Integer,
    "userId": fields.Integer,
    "projectId": fields.Integer,
    "clientId": fields.Integer,
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
    "firstName": fields.String,
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
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()

        if args['role'] not in ['developer', 'reporter', 'admin']:
            abort(400, message="Role must be either 'developer', 'reporter' or 'admin'")

        birthdate = datetime.strptime(args["birthdate"], '%Y-%m-%d').date()

        user = UserModel(firstName=args["firstName"], name=args["name"], birthdate=birthdate,
                         email=args["email"], role=args["role"], password=args["password"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201


class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User was not found")
        return user

    @marshal_with(userFields)
    def put(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User was not found")
        user.firstName = args["firstName"]
        user.name = args["name"]
        user.birthdate = datetime.strptime(args["birthdate"], '%Y-%m-%d').date()
        user.email = args["email"]
        user.role = args["role"]
        user.password = args["password"]
        db.session.commit()
        return user

    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User was not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users


class Tickets(Resource):
    @marshal_with(ticketFields)
    def get(self):
        tickets = TicketModel.query.all()
        return tickets

    @marshal_with(ticketFields)
    def post(self):
        args = ticket_args.parse_args()

        if args['status'] not in ['ongoing', 'completed', 'cancelled', 'paused']:
            abort(400, message="Status must be either 'ongoing', 'completed', 'cancelled' or 'paused'")

        ticket = TicketModel(userId=args["userId"], projectId=args["projectId"], clientId=args["clientId"],
                             title=args["title"], description=args["description"], status=args["status"])
        db.session.add(ticket)
        db.session.commit()
        tickets = TicketModel.query.all()
        return tickets, 201


class Ticket(Resource):
    @marshal_with(ticketFields)
    def get(self, id):
        ticket = TicketModel.query.filter_by(id=id).first()
        if not ticket:
            abort(404, message="Ticket was not found")
        return ticket

    @marshal_with(ticketFields)
    def put(self, id):
        args = ticket_args.parse_args()
        ticket = TicketModel.query.filter_by(id=id).first()
        if not ticket:
            abort(404, message="Ticket was not found")
        ticket.userId = args["userId"]
        ticket.clientId = args["clientId"]
        ticket.projectId = args["projectId"]
        ticket.title = args["title"]
        ticket.description = args["description"]
        ticket.status = args["status"]
        db.session.commit()
        return ticket

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
    @marshal_with(projectFields)
    def get(self):
        projects = ProjectModel.query.all()
        return projects

    @marshal_with(projectFields)
    def post(self):
        args = project_args.parse_args()

        project = ProjectModel(name=args["name"])
        db.session.add(project)
        db.session.commit()
        projects = ProjectModel.query.all()
        return projects, 201


class Project(Resource):
    @marshal_with(projectFields)
    def get(self, id):
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404, message="Project was not found")
        return project

    @marshal_with(projectFields)
    def put(self, id):
        args = project_args.parse_args()
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404, message="Project was not found")
        project.name = args["name"]
        db.session.commit()
        return project

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
    @marshal_with(clientFields)
    def get(self):
        clients = ClientModel.query.all()
        return clients

    @marshal_with(clientFields)
    def post(self):
        args = client_args.parse_args()

        client = ClientModel(firstName=args["firstName"], name=args["name"], company=args["company"],
                             email=args["email"], phone=args["phone"])
        db.session.add(client)
        db.session.commit()
        clients = ClientModel.query.all()
        return clients, 201


class Client(Resource):
    @marshal_with(clientFields)
    def get(self, id):
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            abort(404, message="Client was not found")
        return client

    @marshal_with(clientFields)
    def put(self, id):
        args = client_args.parse_args()
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            abort(404, message="Client was not found")
        client.name = args["name"]
        client.firstName = args["firstName"]
        client.company = args["company"]
        client.email = args["email"]
        client.phone = args["phone"]
        db.session.commit()
        return client

    @marshal_with(clientFields)
    def delete(self, id):
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            abort(404, message="Client was not found")
        db.session.delete(client)
        db.session.commit()
        clients = ClientModel.query.all()
        return clients


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

if __name__ == '__main__':
    app.run(debug=True)
