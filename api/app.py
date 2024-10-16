#######################
# IMPORTING LIBRARIES #
#######################

# Native libraries
import os
from datetime import datetime

# Cryptography library
import bcrypt

# Flask libraries
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


##########
# CONFIG #
##########

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/projet_api')
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Initialize the JWT manager, the database and the migration
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


##########
# MODELS #
##########

# Create the models
# The User model is used to store the information of the users
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


# The Ticket model is used to store the information of the tickets
class TicketModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client_model.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'), nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(80), nullable=False)

    # Relationships
    user = db.relationship('UserModel', backref='tickets')
    client = db.relationship('ClientModel', backref='tickets')
    project = db.relationship('ProjectModel', backref='tickets')

    def __repr__(self):
        return f"Ticket(Title = {self.title}, description = {self.description}, status = {self.status})"


# The Project model is used to store the information of the projects
class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Project(Name = {self.name})"


# The Client model is used to store the information of the clients
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


###########
# PARSING #
###########

# Create the parsers
# The user_args parser is used to parse the arguments of the users
user_args = reqparse.RequestParser()
user_args.add_argument('firstname', type=str, required=True, help="First name cannot be blank")
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('birthdate', type=str, required=True, help="Birthdate cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('role', type=str, required=True, help="Role cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")

# The ticket_args parser is used to parse the arguments of the tickets
ticket_args = reqparse.RequestParser()
ticket_args.add_argument('user_id', type=int, required=True, help="User ID cannot be blank")
ticket_args.add_argument('project_id', type=int, required=True, help="Project ID cannot be blank")
ticket_args.add_argument('client_id', type=int, required=True, help="Client ID cannot be blank")
ticket_args.add_argument('title', type=str, required=True, help="Title cannot be blank")
ticket_args.add_argument('description', type=str, required=True, help="Description cannot be blank")
ticket_args.add_argument('status', type=str, required=True, help="Status cannot be blank")

# The project_args parser is used to parse the arguments of the projects
project_args = reqparse.RequestParser()
project_args.add_argument('name', type=str, required=True, help="Name cannot be blank")

# The client_args parser is used to parse the arguments of the clients
client_args = reqparse.RequestParser()
client_args.add_argument('firstname', type=str, required=True, help="First name cannot be blank")
client_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
client_args.add_argument('company', type=str, required=True, help="Company cannot be blank")
client_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
client_args.add_argument('phone', type=str, required=True, help="Phone cannot be blank")


##########
# FIELDS #
##########

# Create the fields
# The userFields field is used to marshal the fields of the users
userFields = {
    'id': fields.Integer,
    'firstname': fields.String,
    'name': fields.String,
    'birthdate': fields.String,
    'email': fields.String,
    'role': fields.String,
    'password': fields.String
}

# The ticketFields field is used to marshal the fields of the tickets
ticketFields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "project_id": fields.Integer,
    "client_id": fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'status': fields.String
}

# The projectFields field is used to marshal the fields of the projects
projectFields = {
    "id": fields.Integer,
    'name': fields.String
}

# The clientFields field is used to marshal the fields of the clients
clientFields = {
    "id": fields.Integer,
    "name": fields.String,
    "firstname": fields.String,
    "company": fields.String,
    "email": fields.String,
    "phone": fields.String
}


#############
# RESOURCES #
#############

# Create the resources
# The Users resource is used to manage the users
class Users(Resource):
    @jwt_required()
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()

        # Check if the role is valid
        if args['role'] not in ['developer', 'reporter']:
            abort(400, message="Role must be either 'developer'")

        # Check if the birthdate is valid
        birthdate = datetime.strptime(args["birthdate"], '%Y-%m-%d').date()

        # Hash the password
        hashed_password = bcrypt.hashpw(args['password'].encode('utf-8'), bcrypt.gensalt())

        user = UserModel(firstname=args["firstname"], name=args["name"], birthdate=birthdate,
                         email=args["email"], role=args["role"], password=hashed_password.decode('utf8'))
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201


# The User resource is used to manage a specific user
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

        # Check if the user is authorized to modify the account
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
        if args['password'] != '':
            # Hash the password
            hashed = bcrypt.hashpw(args['password'].encode('utf-8'), bcrypt.gensalt())
            user.password = hashed.decode('utf8')
        db.session.commit()
        return user

    @jwt_required()
    @marshal_with(userFields)
    def delete(self, id):
        current_user = get_jwt_identity()

        # Only admins can delete accounts!
        if current_user['role'] != 'admin':
            abort(403, message='You are not authorized to delete this account')

        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User was not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users


# The Tickets resource is used to manage the tickets
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

        # Check if the status is valid
        if args['status'] not in ['ongoing', 'completed', 'cancelled', 'paused']:
            abort(400, message="Status must be either 'ongoing', 'completed', 'cancelled' or 'paused'")

        ticket = TicketModel(user_id=args["user_id"], project_id=args["project_id"], client_id=args["client_id"],
                             title=args["title"], description=args["description"], status=args["status"])
        db.session.add(ticket)
        db.session.commit()
        tickets = TicketModel.query.all()
        return tickets, 201


# The Ticket resource is used to manage a specific ticket
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


# The Projects resource is used to manage the projects
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


# The Project resource is used to manage a specific project
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


# The Clients resource is used to manage the clients
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


# The Client resource is used to manage a specific client
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


# The Auth resource is used to manage the authentication
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
        args = parser.parse_args()

        user = UserModel.query.filter_by(email=args['email']).first()
        # Check if the user exists and if the password is correct
        if user and bcrypt.checkpw(args['password'].encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity={'id': user.id, 'role': user.role})
            # Return the access token and some user info
            return {
                'access_token': access_token,
                'user_info': {
                    'id': user.id,
                    'firstname': user.firstname,
                    'email': user.email,
                    'role': user.role
                }
            }, 200
        else:
            return {'message': 'Invalid credentials'}, 401


##########
# ROUTES #
##########

# Add the routes
# Users
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
# Tickets
api.add_resource(Tickets, '/api/tickets/')
api.add_resource(Ticket, '/api/tickets/<int:id>')
# Projects
api.add_resource(Projects, '/api/projects/')
api.add_resource(Project, '/api/projects/<int:id>')
# Clients
api.add_resource(Clients, '/api/clients/')
api.add_resource(Client, '/api/clients/<int:id>')
# Auth
api.add_resource(Auth, '/api/auth/')


if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
