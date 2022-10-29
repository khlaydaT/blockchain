import json
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError,post_load
from web3 import Web3
# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.defaultAccount = w3.eth.accounts[1]
# Get stored abi and contract_address
with open("data.json", 'r') as f:
    datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]
def check_gender(data):
    print("to validate " , data)
    valid_list = ["male", "female"]
    if data not in valid_list:
        raise ValidationError(
            'Invalid gender. Valid choices are'+ valid_list
    )
    print("all is ok ")
#For api validations
class UserSchema(Schema):
    name = fields.String(required=True)
    gender = fields.String(required=True, validate=check_gender)

#    @post_load
#    def make_user(self,data,**kwargs):
#        return User(**data)

# Initializing flask app
app = Flask(__name__)
# api to set new user every api call
@app.route("/blockchain/user",methods=['POST'])
def user():
    # Create the contract instance with the newly-deployed address
    user = w3.eth.contract(address=contract_address, abi=abi)
    body = request.get_json()
    print(body)
    schema = UserSchema()
    try:
    	result = schema.load(body) # UserSchema()#.load(body)
    	print("nice result", result['name'])
    	tx_hash = user.functions.setUser(
		result['name'],result['gender']).transact()
    	print("wait for transaction ")
    	receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    	print("almost finished")
    	user_data = user.functions.getUser().call()
    	print("send result")
    	return jsonify({"data": user_data}),200
    
    except ValidationError as err: 
        print(err.messages)
        return jsonify(err),422
