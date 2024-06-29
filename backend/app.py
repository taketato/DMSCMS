# import details
import sys
sys.path.insert(1, './Database')
sys.path.insert(2, '../Database')
sys.path.insert(3, './contracts')
import json
from flask import Flask, request, make_response, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import db_interaction_add_functions as database
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_jwt_extended import get_jwt, get_jwt_identity
import datetime
from deploy import deploy_contract, compile
from web3 import Web3
import requests


app = Flask(__name__)
api=Api(app,doc='/doc',title="Medical Resources Distribution API",description="API for the system")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_for_9900.db"
app.config['JWT_SECRET_KEY'] = '9900M13ATechtitan'  # Replace with your own secret key
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)
CORS(app, origins=["http://localhost:3000"])
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337

manager_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d" 
# leaving the private key like this is very insecure if you are working on real world project


authorizations = {
    "jsonWebToken": {
        "type": "apiKey", 
        "in": "header",
        "name": "Authorization"
    }
}


app = Flask(__name__)
api = Api(app, doc='/', title='9900 API', description='API for 9900 project.',security='jsonWebToken', authorizations=authorizations)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_for_9900.db"
app.config['JWT_SECRET_KEY'] = '9900M13ATechtitan' 
jwt = JWTManager(app)
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)
CORS(app, origins=["http://localhost:3000"])

adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
session = requests.Session()
session.mount('http://', adapter)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545', session=session))
chain_id = 1337


manager_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d" # leaving the private key like this is very insecure if you are working on real world project

auth = Namespace('Admin authentication and authorisation', description='Auth related operations')
patient = Namespace('Patient operations', description='tracking')
hospital = Namespace('Hospital operations', description='tracking, post demand, check demand')
wholesaler = Namespace('Wholesaler operations', description='tracking, post demand, check demand')
manufacturer = Namespace('Manufacturer operations', description='tracking, post items, check items,check demand')


#================================================================
#                       Auth Models
#================================================================

# Define the expected input model for the /admin/auth/register endpoint
register_model = api.model('Register', {
    'email': fields.String(example='z1234567@unsw.edu.au'),
    'password': fields.String(example='password'),
    'identity': fields.String(example='hospital'),
    'name': fields.String(example='user1234')
})

login_model = api.model('Login', {
    'email': fields.String(example='z1234567@unsw.edu.au'),
    'password': fields.String(example='password'),
    'identity': fields.String(example='hospital'),
    'name': fields.String(example='user1234')
})


#================================================================
#                       Response Models
#================================================================

# Define the model for successful response
token_response_model = api.model('TokenResponse', {
    'token': fields.String(example='token'), 
    #'identity': fields.String(example='hospital')
})

# Define the model for bad input response
bad_input_response_model = api.model('BadInputResponse', {
    'error': fields.String(example='Invalid input')
})

# Define the model for forbidden response
forbidden_response_model = api.model('forbidden', {
    'error': fields.String(example='Invalid token')
})

tracking_response_model = api.model('tracking_respond_model', {
    'departure': fields.String(example='No3 factory'),
    'track_record': fields.String(example='track information'),
    'destination': fields.String(example='xxx hospital'), 
    'status': fields.String(example='shipped, completed, wrong_shippment', 
                            description='shipped when departured, completed when received, wrong_shippment when something wrong in the middle')
})

demand_response_model = api.model('demand_response_model', {
    'demand_record': fields.Integer(example='40', description='demand quantity (integer)')
})

items_response_model = api.model('items_response_model', {
    'item_list': fields.String(example='Phfizer vaccine, 999 Medicine, Panadol', 
                               description='parse a list of item name into a string, separated by comma')
})

inventory_model = api.model('inventory_model', {
    'item_name': fields.String(), 
    'item_quantity': fields.String()
})

tracking_model = api.model('tracking_query_model', {
    'item_name': fields.String(example='Panadol'),
    'destination': fields.String(example='The Hospital'), 
    'source': fields.String(example='The Manufacturer'), 
    'send_date': fields.String(example='20231011')
})

set_inventory_model = api.model('set_inventory_model', {
    'item_name': fields.String(description='item name'), 
    'item_quantity': fields.Integer(description='item quantity'),
    'item_batch_no': fields.Integer(description='item batch no', example='12'),
    'item_production_date': fields.Integer(description='item production date', example='20231011')
})

outbound_model = api.model('outbound_model', {
    'item_name': fields.String(discription='item name'), 
    'item_quantity': fields.Integer(description='item quantity'),
    'item_batch_no': fields.Integer(description='item batch no', example='12'),
    'item_production_date': fields.Integer(description='item production date', example='20231011'),
    'destination': fields.String(discription='destination'),
})

demand_check_model = api.model('demand_check_model', {
    'item_name': fields.String(example='Panadol'),
    'manufacturer': fields.String(example='manufacturer1')
})

#================================================================
#                       Patient Models
#================================================================
patient_model = api.model('product_track_info', {
    'manufacturer': fields.String(example='Panadol Factory'), 
    'departure_date_manufacturer': fields.Integer(example='20231104'),
    'arrival_date_wholesaler': fields.Integer(example='20231106'),
    'wholesaler': fields.String(example='Something Warehouse'), 
    'departure_date_wholesaler': fields.Integer(example='20231104'),
    'arrival_date_hospital': fields.String(example='20231109'),
    'hospital': fields.String(example='Prince Wales Hospital or TerryWhite Pharmacy')
})

patient_query_model = api.model('query_info', {
    'item_name':fields.String(example='item name'),
    'production_date':fields.Integer(description='item production date', example='202310111'),
    'batch_no':fields.Integer(description='item batch number', example='12')
    
})

#================================================================
#                       Hospital Models
#================================================================
hospital_postdemand_model = api.model('hospital_postdemand', {
    'item_name': fields.String(example='Panadol'),
    'manufacturer': fields.String(example='some manufacturer'),
    'demand_amount': fields.Integer(example='100 (could be negative for receiving delievery)'),
})

hospital_postinventory_model = api.model('hospital_postinventory', {
    'item_id': fields.Integer(example='10'),
    'demand_amount': fields.Integer(example='100'),
})

#================================================================
#                       Manufacturer Models
#================================================================
manufacturer_postitem_model = api.model('manufacturer_postdemand', {
    'name': fields.String(example='Ibuprofen'),
    'type': fields.String(example='Medicine')
})

#================================================================
#                       Wholesaler Models
#================================================================
wholesaler_postdemand_model = api.model('wholesaler_postdemand', {
    'item_name': fields.String(example='Panadol'),
    'manufacturer': fields.String(example='some manufacturer'),
    'demand_amount': fields.Integer(example='100 (could be negative for receiving delievery)'),
})

wholesaler_postinventory_model = api.model('wholesaler_postinventory', {
    'item_id': fields.Integer(example='10'),
    'demand_amount': fields.Integer(example='100'),
})


#================================================================
#                       Deployment Helpers
#================================================================

def init_deployer():
    result = compile("contracts/Deployer.sol")
    bytecode = result[0]
    abi = result[1]
    res = deploy_contract(bytecode, abi)
    return res
      
def deploy_producer():
    result = compile("contracts/Producer.sol")
    bytecode = result[0]
    abi = result[1]
    res = deploy_contract(bytecode, abi)
    return res

def deploy_warehouse():
    result = compile("contracts/Warehouse.sol")
    bytecode = result[0]
    abi = result[1]
    res = deploy_contract(bytecode, abi)
    return res

def deploy_Delivery(address_from, address_to):
    result = compile("contracts/Delivery.sol")
    bytecode = result[0]
    abi = result[1]
    
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(manager_address)
    # build transaction
    transaction = contract.constructor(manager_address, address_from, address_to).transact(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": manager_address,
            "nonce": nonce,
        }
    )
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction)
    contract_address = transaction_receipt.contractAddress
    
    return contract_address, abi


def inbound_contract(abi, contract_address, item_name, producer_address, item_quantity): 
    # connect to producer sc and call functions to store inbound on chain
    producer = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count(manager_address)
    
    transaction = producer.functions.inbound(producer_address, item_name, item_quantity).build_transaction(
        {"chainId": chain_id, "from": manager_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    # Send the transaction
    send_transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction_hash)
    #res = transaction_receipt['logs'][0]['data']
    return 0

def inbound_contract_manufacturer(abi, contract_address, item_name, batch_hash, item_quantity): 
    # connect to producer sc and call functions to store inbound on chain
    producer = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count(manager_address)
    
    transaction = producer.functions.inbound(item_name, batch_hash, item_quantity).build_transaction(
        {"chainId": chain_id, "from": manager_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    # Send the transaction
    send_transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction_hash)
    #res = transaction_receipt['logs'][0]['data']
    
    return 0
    
def outbound_contract(abi, contract_address, producer_address, item_name, item_quantity):
    # connect to producer sc and call functions to store inbound on chain
    producer = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count(manager_address)
    
    transaction = producer.functions.outbound(producer_address, item_name, item_quantity).build_transaction(
        {"chainId": chain_id, "from": manager_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    # Send the transaction
    send_transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction_hash)
    #res = transaction_receipt['logs'][0]['data']
    return 0

def outbound_contract_manufacturer(abi, contract_address, item_name, item_quantity):
    # connect to producer sc and call functions to store inbound on chain
    producer = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count(manager_address)
    
    transaction = producer.functions.outbound(item_name, item_quantity).build_transaction(
        {"chainId": chain_id, "from": manager_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    # Send the transaction
    send_transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction_hash)
    #res = transaction_receipt['logs'][0]['data']
    return 0

def set_shippment(abi, address, producer_address, item_name, quantity, time):
    delivery = w3.eth.contract(address=address, abi=abi)
    nonce = w3.eth.get_transaction_count(manager_address)
    
    transaction = delivery.functions.addProduct(producer_address, item_name, quantity).build_transaction(
        {"chainId": chain_id, "from": manager_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    # Send the transaction
    send_transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction_hash)
    nonce = w3.eth.get_transaction_count(manager_address)
    
    transaction1 = delivery.functions.shipping(time).build_transaction(
        {"chainId": chain_id, "from": manager_address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
    )
    sign_transaction1 = w3.eth.account.sign_transaction(
        transaction1, private_key=private_key
    )
    # Send the transaction
    send_transaction_hash1 = w3.eth.send_raw_transaction(sign_transaction1.rawTransaction)
    transaction_receipt1 = w3.eth.wait_for_transaction_receipt(send_transaction_hash1)
    
    return 'ok'

def delivery_receive(abi, address, time):
    #connect to delivery sc
    delivery = w3.eth.contract(address=address, abi=abi)
    nonce = w3.eth.get_transaction_count(manager_address)
    transaction1 = delivery.functions.receiving(time).build_transaction(
        {"chainId": chain_id, "from": manager_address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
    )
    sign_transaction1 = w3.eth.account.sign_transaction(
        transaction1, private_key=private_key
    )
    # Send the transaction
    send_transaction_hash1 = w3.eth.send_raw_transaction(sign_transaction1.rawTransaction)
    transaction_receipt1 = w3.eth.wait_for_transaction_receipt(send_transaction_hash1)
    
    return 'ok'


#================================================================
#                       Init Functions
#================================================================
@app.route('/init')
def initialize():
    result = init_deployer()
    database.add_user(type="admin", email="admin@system.au", password="password", sc_address=result.address)
    database.add_contract_ABI(contract_name="deployer", SC_ABI=result[1])
    print("The server is initialized, route to /login or /register to start up")
    return "The server is initialized, route to /login or /register to start up"


#================================================================
#                       Auth Functions
#================================================================
api.add_namespace(auth, path='/admin/auth')


@auth.route('/register')
@api.doc(security=None)
class RegisterAdmin(Resource):

    @api.expect(register_model)
    # @api.response(200,'OK',token_response_model)
    # @api.response(400,'ERROR',bad_input_response_model)
    def post(self):
        
        user_email = request.json.get('email', None)
        user_identity = request.json.get('identity', None)
        user_name = request.json.get('name', None)
        user_password = request.json.get('password', None)
        #print(user_info)
        
        check_user = database.query_user_email(user_email)
        if not check_user:
            # deploy sc and add address into return value
            #res = []
            if user_identity=="Wholesaler" or user_identity=="Hospital":
                #pass
                res = deploy_warehouse()
                #database.add_user(type=user_identity, email=user_email, )
            #elif user_identity=="Manufacturer":
            else:
                #pass
                res = deploy_producer()
            #database.add_contract_ABI(user_identity, res[1])
            #database.add_user(name=user_name, type=user_identity, email=user_email, password=user_password, token=None, sc_address=None)#res.address)
            database.add_user(name=user_name, type=user_identity, email=user_email, password=user_password, token=None, sc_address=res[0])#res.address)
            #return jsonify({'status': 'ok'}), 200
            response = make_response(jsonify({"status": 'ok'}), 200)
            response.headers["Content-Type"] = "application/json"
            return response
            #resp = make_response({"status": 'ok', "message": 'register success'})
        else:
            #return jsonify('error', 'Account already exists'), 400
            response = make_response(jsonify({"error": 'Account already exists'}), 400)
            response.headers["Content-Type"] = "application/json"
            return response
            #resp = make_response({"error": 'Account already exists'})

    
@auth.route('/login')
@api.doc(security=None)
class LoginAdmin(Resource):

    @api.expect(login_model)
    @api.response(200,'OK',token_response_model)
    @api.response(400,'ERROR',bad_input_response_model)
    def post(self):
        username = request.json.get('email', None)
        password = request.json.get('password', None)
        name = request.json.get('name', None)
        identity = request.json.get('identity', None)
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        users = database.query_user_email(username)
        print(users)
        if not users or users[1] != password or name != users[3] or identity != users[0]:  
            response = make_response(jsonify({'error': 'Login detail incorrect'}), 400)
            response.headers["Content-Type"] = "application/json"
            return response
        
        additional_claims = {"username": name}
        token = create_access_token(users[0], additional_claims=additional_claims)
        
        database.update_user_token(token, username)
        
        response = make_response(jsonify({"token": token}), 200)
        response.headers["Content-Type"] = "application/json"
        return response
        

@auth.route('/logout')
@api.doc(security='jsonWebToken')
class LogoutAdmin(Resource):

    #@api.expect(logout_model)
    @api.expect(auth.parser().add_argument('token', location='header'))
    @api.response(200, 'OK')
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        token = request.headers["Authorization"].split(" ")[1]
        database.delete_token(token)
        response = make_response(jsonify({"status":'ok'}),200)
        response.headers["Content-Type"] = "application/json"
        return response 


#================================================================
#                       Patient Functions
#================================================================
api.add_namespace(patient, path='/patient')

@patient.route('/tracking')
@api.doc(security=None)
class PatientFunction_tracking(Resource):

    @api.expect(patient_query_model)
    @api.response(200, 'OK', patient_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    def post(self):
        
        # locate product info in database
        item_name = request.json.get('item_name', None)
        production_date = request.json.get('production_date', None)
        batch_no = request.json.get('batch_no', None)
        if not item_name or not production_date or not batch_no:
            return 400
        
        pid = database.query_product(item_name)
        if not pid:
            return 400

        item = database.query_item(pid, production_date)
        if not item:
            return 400
        
        # reverse tracking using deliverids inside item
        print(item[2])
        deliveries = item[2].split(" ")
        print(deliveries)
        
        delivery_manufacturer = deliveries[0]
        manufacturer = database.query_delivery_id(delivery_manufacturer)
        print(manufacturer)
        manufacturer_name = manufacturer[1]
        manufacturer_departure = manufacturer[5]
        manufacturer_arrival = manufacturer[4]
        delivery_wholesaler = deliveries[1]
        wholesaler = database.query_delivery_id(delivery_wholesaler)
        wholesaler_name = wholesaler[0]
        wholesaler_departure = wholesaler[5]
        wholesaler_arrival = wholesaler[4]
        hospital_name = wholesaler[1]
        
        # return response
        response = make_response(jsonify({
            "manufacturer": manufacturer_name,
            "departure_date_manufacturer": manufacturer_departure,
            "arrival_date_wholesaler": manufacturer_arrival,
            "wholesaler": wholesaler_name,
            "departure_date_wholesaler": wholesaler_departure, 
            "arrival_date_hospital": wholesaler_arrival,
            "hospital": hospital_name
            }), 200)
        response.headers["Content-Type"] = "application/json"
        return response

        pass
        
    

#================================================================
#                       Hospital Functions
#================================================================
api.add_namespace(hospital, path='/admin/hospital')
@hospital.route('/tracking')
@api.doc(security='jsonWebToken')
class HospitalFunction_tracking(Resource):

    @api.expect(tracking_model)
    @api.response(200, 'OK', tracking_response_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        # find delivery in database
        
        # decide whether is the source or destination
        source = request.json.get('source', None)
        date = request.json.get('send_date', None)
        item_name = request.json.get('item_name', None)
        pid = database.query_product(item_name)

        # find delivery
        
        data = database.query_delivery_track(pid, source, username, date)
        if not data:
            return 400
        status = 'shipped'
        arrival_time = None
        tracking_info = str()
        if data[5]:
            status = 'completed'
            arrival_time = data[5]
            tracking_info = f"Shipped from: {data[2]} on {date}, arrived at {username} on {arrival_time}"
        else:
            status = 'shipped'
            arrival_time = None
            tracking_info = f"Shipped from: {data[2]} on {data[6]}, not yet arrived at {username}"
        
        # return status
        response = make_response(jsonify({"departure": data[2], "track_record": tracking_info, "destination": username, "status": status}), 200)
        response.headers["Content-Type"] = "application/json"
        return response
        

@hospital.route('/demand/new')
@api.doc(security='jsonWebToken')
class HospitalFunction_post_demand(Resource):

    @api.expect(hospital_postdemand_model)
    #@api.expect(hospital_postdemand_model)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        # pass

        item_name = request.json.get('item_name', None)
        manufacturer = request.json.get('manufacturer', None)
        demand_amount = request.json.get('demand_amount', None)
        pid = database.query_product(item_name)
        user_id = database.query_user_name(username)[0]
        
        database.update_inventory_production_demand_quantity(pid, item_name, demand_amount, user_id)
        
        print(f"id is {pid}, quantity is {demand_amount}")
        return {"status": 'ok'}, 200
    
    
@hospital.route('/demand')
@api.doc(security='jsonWebToken')
class HospitalFunction_check_demand(Resource):

    @api.expect(demand_check_model)
    @api.response(200, 'OK', demand_response_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        token = request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]:
            return 403

        item_name = request.json.get('item_name', None)
        manufacturer = request.json.get('manufacturer', None)
        user_id = database.query_user_name(username)[0]
        demand = database.query_inventory_production(user_id, item_name)[2]

        response = make_response(jsonify({"demand_record": demand}))
        response.headers["Content-Type"] = "application/json"
        return response

@hospital.route('/demand/update')
class HospitalFunction_update_demand(Resource):

    @api.expect(hospital_postdemand_model)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def put(self):
        identity = get_jwt_identity()
        token = request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]:
            return 403

        item_name = request.json.get('item_name', None)
        manufacturer = request.json.get('manufacturer', None)
        demand_amount = request.json.get('demand_amount', None)

        pid = database.query_product(item_name)
        user_id = database.query_user_name(username)[0]
        demand = database.query_inventory_production(user_id, item_name)[2]
        demand += demand_amount
        database.update_inventory_production_demand_quantity(pid, item_name,
                                                             demand, user_id)
        return {"status": 'ok'}, 200

@hospital.route('/inventory')
class HospitalFunction_check_inventory(Resource):

    @api.expect(tracking_model)
    #@api.expect(hospital_postdemand_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item = database.query_inventory_production(user[0], item_name)
        if not item:
            return 400
        quantity = item[1]
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": quantity}))
        response.headers["Content-Type"] = "application/json"
        return response
        
    
@hospital.route('/set_inventory')
class Hospital_set_inventory(Resource):
    @api.expect(hospital_postinventory_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token = request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item_quantity = int(request.json.get('item_quantity', None))
        if not item_name or not item_quantity:
            return 400
        
        pid = database.query_product(item_name)
        # pid = product[0]
        user_id = user[0]
        
        # find delivery sc
        # update delivery to fininshed
        delivery = database.query_delivery_DT_pid(pid, username, item_quantity)
        delivery_address = delivery[0]
        delivery_abi = compile("contracts/Delivery.sol")[1]
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d")
        date_int = int(date_string)
        set_delivery = delivery_receive(delivery_abi, delivery_address, date_int)
        if set_delivery != 'ok':
            return 403
        
        # update delivery database
        database.update_delivery(pid, delivery_address, username, date_string)
        item = database.query_product_id(pid)
        item_name = item[1]
        producer_id = item[2]
        producer_address = database.query_user_id(producer_id)[3]
        # update inventory database
        current_inventory = database.query_inventory_production(user_id, item_name)
        if current_inventory:
            # exists, add to it
            updated_quantity = current_inventory[1]+item_quantity
            database.update_inventory_production(user[0], item_name, updated_quantity)
            # check if a demand exists
            demand = current_inventory[2]
            if demand:
                updated_demand = demand - item_quantity
                database.update_inventory_production_demand_quantity(pid, item_name, updated_demand, user_id)
        else:
            # does not exist, create one
            database.add_inventory(user_id, pid, item_name, item_quantity, None)
            updated_quantity = item_quantity
            
        # compile the contract to get ABI
        result = compile("contracts/Warehouse.sol")
        abi = result[1]
        
        address = database.query_token_with_email(user[1])[4]
        res = inbound_contract(abi, address, item_name, producer_address, item_quantity)
        res = updated_quantity
        if updated_quantity != res: 
            return jsonify({'error': 'local database is different compared to blockchain!'}), 400
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": updated_quantity}))
        response.headers["Content-Type"] = "application/json"
        return response


@hospital.route('/set_outbound')
class Hospital_set_outbound(Resource):
    @api.expect(outbound_model)
    #@api.expect(hospital_postdemand_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item_quantity = int(request.json.get('item_quantity', None))
        item_batch_no = request.json.get('item_batch_no', None)
        item_production_date = request.json.get('item_production_date', None)
        destination = request.json.get('destination', None)
        if not item_batch_no or not item_name or not item_production_date or not destination or not item_quantity:
            return 400
        
        #pid = database.query_product(item_name)                
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d")
        date_int = int(date_string)
        
        pid = database.query_product(item_name)
        user_id = database.query_product_id(pid)[2]
        producer_address = database.query_user_id(user_id)[3]

        
        # update database
        current_inventory = database.query_inventory_production(user[0], item_name)
        
        # check if enough inventory
        if current_inventory[1] < item_quantity:
            return 400
        
        # apply change
        updated_quantity = current_inventory[1] - item_quantity
        database.update_inventory_production(user[0], item_name, updated_quantity)
        
        # create instance of delivery
        delivery_name = username+destination+date_string
        database.add_delivery(delivery_name, None, username, destination, date_int, None, pid, item_quantity)
        delivery_id = database.query_delivery(delivery_name)[6]
        
        delivery = database.query_item(pid, item_production_date)[2]
        if not delivery:
            delivery = f"{delivery_id}"
        else:
            delivery = delivery + f" {delivery_id}"
        database.update_item(pid, item_production_date, delivery)
        
        # compile the contract to get ABI
        result = compile("contracts/Warehouse.sol")
        abi = result[1]
        address = database.query_user_email(user[1])[2]
        res = outbound_contract(abi, address, producer_address, item_name, item_quantity)
        res = updated_quantity
        if updated_quantity != res: 
            return jsonify({'error': 'local database is different compared to blockchain!'}), 400
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": updated_quantity}))
        response.headers["Content-Type"] = "application/json"
        return response
        
        
#================================================================
#                       Wholesaler Functions
#================================================================
api.add_namespace(wholesaler, path='/admin/wholesaler')
@wholesaler.route('/tracking')
@api.doc(security='jsonWebToken')
class WholesalerFunction_tracking(Resource):

    @api.expect(tracking_model)
    @api.response(200, 'OK', tracking_response_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        # decide whether is the source or destination
        source = request.json.get('source', None)
        destination = request.json.get('destination', None)
        date = request.json.get('send_date', None)
        item_name = request.json.get('item_name', None)
        
        pid = database.query_product(item_name)

        decision = 'source'
        if not source:
            if not destination:
                return 400
            else: 
                decision = 'destination'
        else: 
            if destination:
                return 400
        # find delivery
        if decision == 'destination':
            data = database.query_delivery_track(pid, username, destination, date)
            if not data:
                print("no data found")
                return 400
            status = 'shipped'
            arrival_time = None
            tracking_info = str()
            if data[5]:
                status = 'completed'
                arrival_time = data[5]
                tracking_info = f"Shipped from: {username} on {date}, arrived at {data[2]} on {arrival_time}"
            else:
                status = 'shipped'
                arrival_time = None
                tracking_info = f"Shipped from: {username} on {data[6]}, not yet arrived at {data[2]}"
            
            # return status
            response = make_response(jsonify({"departure": username, "track_record": tracking_info, "destination": data[2], "status": status}), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            data = database.query_delivery_track(pid, source, username, date)
            if not data:
                return 400
            status = 'shipped'
            arrival_time = None
            tracking_info = str()
            if data[5]:
                status = 'completed'
                arrival_time = data[5]
                tracking_info = f"Shipped from: {data[2]} on {date}, arrived at {username} on {arrival_time}"
            else:
                status = 'shipped'
                arrival_time = None
                tracking_info = f"Shipped from: {data[2]} on {data[6]}, not yet arrived at {username}"
            
            # return status
            response = make_response(jsonify({"departure": data[2], "track_record": tracking_info, "destination": username, "status": status}), 200)
            response.headers["Content-Type"] = "application/json"
            return response


@wholesaler.route('/demand/new')
class WholesalerFunction_post_demand(Resource):

    @api.expect(wholesaler_postdemand_model)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        token = request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]:
            return 403

        item_name = request.json.get('item_name', None)
        manufacturer = request.json.get('manufacturer', None)
        demand_amount = request.json.get('demand_amount', None)
        pid = database.query_product(item_name)
        
        user_id = database.query_user_name(username)[0]
        
        database.update_inventory_production_demand_quantity(pid, item_name, demand_amount, user_id)
        
        print(f"id is {pid}, quantity is {demand_amount}")
        return {"status": 'ok'}, 200


@wholesaler.route('/demand')
class WholesalerFunction_check_demand(Resource):

    @api.expect(demand_check_model)
    @api.response(200, 'OK', demand_response_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        token = request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]:
            return 403
        
        item_name = request.json.get('object_name', None)
        manufacturer = request.json.get('manufacturer', None)
        user_id = database.query_user_name(username)[0]
        demand = database.query_inventory_production(user_id, item_name)

        
        response = make_response(jsonify({"demand_record": demand[2]}))
        response.headers["Content-Type"] = "application/json"
        return response


@wholesaler.route('/demand/update')
class WholesalerFunction_update_demand(Resource):

    @api.expect(wholesaler_postdemand_model)
    #@api.expect(hospital_postdemand_model)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def put(self):
        identity = get_jwt_identity()
        token = request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]:
            return 403

        item_name = request.json.get('item_name', None)
        manufacturer = request.json.get('manufacturer', None)
        demand_amount = int(request.json.get('demand_amount', None))

        pid = database.query_product(item_name)
        user_id = database.query_user_name(username)[0]
        demand = database.query_inventory_production(user_id, item_name)[2]
        demand += demand_amount
        database.update_inventory_production_demand_quantity(pid, item_name, demand, user_id)
        print(f"id is {pid}, quantity is {demand_amount}")
        return {"status": 'ok'}, 200
    
@wholesaler.route('/inventory')
class WholesalerFunction_check_inventory(Resource):

    @api.expect(tracking_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item = database.query_inventory_production(user[0], item_name)
        if not item:
            return 400
        quantity = item[1]
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": quantity}))
        response.headers["Content-Type"] = "application/json"
        return response
        
        pass
    
@wholesaler.route('/set_inventory')
class Wholesaler_set_inventory(Resource):
    @api.expect(wholesaler_postinventory_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item_quantity = int(request.json.get('item_quantity', None))
        
        if not item_name or not item_quantity:
            return 400
        
        pid = database.query_product(item_name)

        user_id = user[0]
        
        # find delivery sc
        # update delivery to fininshed
        delivery = database.query_delivery_DT_pid(pid, username, item_quantity)
        delivery_address = delivery[0]
        delivery_abi = compile("contracts/Delivery.sol")[1]
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d")
        date_int = int(date_string)
        set_delivery = delivery_receive(delivery_abi, delivery_address, date_int)
        if set_delivery != 'ok':
            return 403
        
        # update delivery database
        database.update_delivery(pid, delivery_address, username, date_string)
        item = database.query_product_id(pid)
        item_name = item[1]
        producer_id = item[2]
        producer_address = database.query_user_id(producer_id)[3]
        # update inventory database
        current_inventory = database.query_inventory_production(user_id, item_name)
        if current_inventory:
            # exists, add to it
            updated_quantity = current_inventory[1]+item_quantity
            database.update_inventory_production(user[0], item_name, updated_quantity)
            # check if a demand exists
            demand = current_inventory[2]
            if demand:
                updated_demand = demand - item_quantity
                database.update_inventory_production_demand_quantity(pid, item_name, updated_demand, user_id)

        else:
            # does not exist, create one
            database.add_inventory(user_id, pid, item_name, item_quantity, None)
            updated_quantity = item_quantity
            
        # compile the contract to get ABI
        result = compile("contracts/Warehouse.sol")
        abi = result[1]
        
        address = database.query_token_with_email(user[1])[4]
        res = inbound_contract(abi, address, item_name, producer_address, item_quantity)
        res = updated_quantity
        if updated_quantity != res: 
            return jsonify({'error': 'local database is different compared to blockchain!'}), 400
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": updated_quantity}))
        response.headers["Content-Type"] = "application/json"
        return response

        
        # pass
    
@wholesaler.route('/set_outbound')
class Wholesaler_set_outbound(Resource):
    @api.expect(outbound_model)
    #@api.expect(hospital_postdemand_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item_quantity = int(request.json.get('item_quantity', None))
        item_batch_no = request.json.get('item_batch_no', None)
        item_production_date = request.json.get('item_production_date', None)
        destination = request.json.get('destination', None)
        if not item_batch_no or not item_name or not item_production_date or not destination or not item_quantity:
            return 400
        
        pid = database.query_product(item_name)
        user_id = database.query_product_id(pid)[2]
        producer_address = database.query_user_id(user_id)[3]

        from_address = user[3]
        to_address = database.query_user_name(destination)[3]
        
        result = deploy_Delivery(from_address, to_address)
        contract_address = result[0]
        contract_abi = result[1]
        
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d")
        date_int = int(date_string)
        
        set_shippment(contract_abi, contract_address, user[3], item_name, item_quantity, date_int)
        
        # update database
        current_inventory = database.query_inventory_production(user[0], item_name)
        
        # check if enough inventory
        if current_inventory[1] < item_quantity:
            return 400
        
        # apply change
        updated_quantity = current_inventory[1] - item_quantity
        database.update_inventory_production(user[0], item_name, updated_quantity)
        
        # create instance of delivery
        delivery_name = username+destination+date_string
        database.add_delivery(delivery_name, contract_address, username, destination, date_int, None, pid, item_quantity)
        delivery_id = database.query_delivery(delivery_name)[6]
        
        
        delivery = database.query_item(pid, item_production_date)[2]
        if not delivery:
            delivery = f"{delivery_id}"
        else:
            delivery += f" {delivery_id}"
        database.update_item(pid, item_production_date, delivery)
        
        # compile the contract to get ABI
        result = compile("contracts/Warehouse.sol")
        abi = result[1]
        address = database.query_user_email(user[1])[2]
        res = outbound_contract(abi, address, producer_address, item_name, item_quantity)
        res = updated_quantity
        if updated_quantity != res: 
            return jsonify({'error': 'local database is different compared to blockchain!'}), 400
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": updated_quantity}))
        response.headers["Content-Type"] = "application/json"
        return response

        
        # pass
#================================================================
#                       Manufacturer Functions
#================================================================
api.add_namespace(manufacturer, path='/admin/manufacturer')
@manufacturer.route('/tracking')
@api.doc(security='jsonWebToken')
class ManufacturerFunction_tracking(Resource):

    @api.expect(tracking_model)
    @api.response(200, 'OK', tracking_response_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        # find delivery in database
        date = request.json.get('send_date', None)
        item_name = request.json.get('item_name', None)
        pid = database.query_product(item_name)

        data = database.query_delivery_SD_pid(pid, username, date)
        status = 'shipped'
        arrival_time = None
        tracking_info = str()
        if data[5]:
            status = 'completed'
            arrival_time = data[5]
            tracking_info = f"Shipped from: {username} on {date}, arrived at {data[2]} on {data[5]}"
        else:
            status = 'shipped'
            arrival_time = None
            tracking_info = f"Shipped from: {username} on {date}, not yet arrived at {data[2]}"
        
        # return status
        response = make_response(jsonify({"departure": username, "track_record": tracking_info, "destination": data[2], "status": status}), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@manufacturer.route('/item/new')
class ManufacturerFunction_post_item(Resource):

    @api.expect(manufacturer_postitem_model)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        # read from request to get param
        item_name = request.json.get('name', None)
        item_type = request.json.get('type', None)
        if not item_name or not item_type:
            return 400
        
        item_id = database.query_product(item_name)
        if item_id:
            response = make_response(jsonify({'error': 'item already added'}), 400)
            response.headers["Content-Type"] = "application/json"
            return response
        database.add_product(user[0], item_name, item_type)
        
        return 200
        

@manufacturer.route('/items')
class ManufacturerFunction_check_items(Resource):

    @api.response(200, 'OK', items_response_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def get(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        # query all items from database
        data = database.query_product_user_id(user[1])
        resp = str()
        if len(data) == 1:
            resp = data[0]
            response = make_response(jsonify({"item_list": resp}), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        count = 0
        for item in data:
            if count < len(data) - 1:
                resp = resp + item + ', '
            else:
                resp = resp + item
            count+=1
        
        
        response = make_response(jsonify({"item_list": resp}), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@manufacturer.route('/inventory')
class ManufacturerFunction_check_inventory(Resource):

    @api.expect(tracking_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item = database.query_inventory_production(user[0], item_name)
        if not item:
            return 400
        quantity = item[1]
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": quantity}))
        response.headers["Content-Type"] = "application/json"
        return response
        # pass
    
@manufacturer.route('/set_inventory')
class Manufacturer_set_inventory(Resource):
    @api.expect(set_inventory_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item_quantity = request.json.get('item_quantity', None)
        item_batch_no = request.json.get('item_batch_no', None)
        item_production_date = request.json.get('item_production_date', None)
        if not item_batch_no or not item_name or not item_production_date or not item_quantity:
            return 400
        
        pid = database.query_product(item_name)
        
        # update database
        current_inventory = database.query_inventory_production(user[0], item_name)
        if current_inventory:
            # exists, add to it
            updated_quantity = current_inventory[1]+item_quantity
            database.update_inventory_production(user[0], item_name, updated_quantity)
        else:
            # does not exist, create one
            database.add_inventory(user[0], pid, item_name, item_quantity, None)
            updated_quantity = item_quantity
        
        
        database.add_items(pid, item_production_date, None)
        
        # compile the contract to get ABI
        result = compile("contracts/Producer.sol")
        abi = result[1]
        address = database.query_user_email(user[1])[2]
        res = inbound_contract_manufacturer(abi, address, item_name, hash(item_batch_no), item_quantity)
        res = updated_quantity
        if updated_quantity != res: 
            return jsonify({'error': 'local database is different compared to blockchain!'}), 400
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": updated_quantity}))
        response.headers["Content-Type"] = "application/json"
        return response

    
@manufacturer.route('/set_outbound')
class Manufacturer_set_outbound(Resource):
    @api.expect(outbound_model)
    @api.response(200, 'OK', inventory_model)
    @api.response(400, 'Bad Input', bad_input_response_model)
    @api.response(403, 'Forbidden', forbidden_response_model)
    @jwt_required()
    def post(self):
        
        identity = get_jwt_identity()
        token =  request.headers["Authorization"].split(" ")[1]
        token_string = get_jwt()
        username = token_string["username"]
        user = database.query_user_name_type(username, identity)
        if token != user[2]: 
            return 403
        
        item_name = request.json.get('item_name', None)
        item_quantity = int(request.json.get('item_quantity', None))
        item_batch_no = request.json.get('item_batch_no', None)
        item_production_date = request.json.get('item_production_date', None)
        destination = request.json.get('destination', None)
        if not item_batch_no or not item_name or not item_production_date or not destination or not item_quantity:
            return 400
        
        current_inventory = database.query_inventory_production(user[0], item_name)
        
        # check if enough inventory
        if current_inventory[1] < item_quantity:
            return 400
        
        pid = database.query_product(item_name)
        from_address = user[3]
        to_address = database.query_user_name(destination)[3]
        
        result = deploy_Delivery(from_address, to_address)
        contract_address = result[0]
        contract_abi = result[1]
        
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d")
        date_int = int(date_string)
        
        set_shippment(contract_abi, contract_address, user[3], item_name, item_quantity, date_int)
        
        # update database
        
        
        # apply change
        updated_quantity = current_inventory[1] - item_quantity
        database.update_inventory_production(user[0], item_name, updated_quantity)
        
        # create instance of delivery
        delivery_name = username+destination+date_string
        database.add_delivery(delivery_name, contract_address, username, destination, date_int, None, pid, item_quantity)
        delivery_id = database.query_delivery(delivery_name)[6]
        
        
        delivery = database.query_item(pid, item_production_date)[2]
        if not delivery:
            delivery = f"{delivery_id}"
        else:
            delivery += f" {delivery_id}"
        database.update_item(pid, item_production_date, delivery)
        
        # compile the contract to get ABI
        result = compile("contracts/Producer.sol")
        abi = result[1]
        address = database.query_user_email(user[1])[2]
        res = outbound_contract_manufacturer(abi, address, item_name, item_quantity)
        res = updated_quantity
        if updated_quantity != res: 
            return jsonify({'error': 'local database is different compared to blockchain!'}), 400
        
        response = make_response(jsonify({"item_name": item_name, "item_quantity": updated_quantity}))
        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == '__main__':
    print("The server is initialized, route to /login or /register to start up")
    app.run(port=8000)

