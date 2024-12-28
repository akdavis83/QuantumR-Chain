from flask import Flask, jsonify, request, render_template, send_file
from blockchain import Blockchain
import json
import io

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response)

@app.route('/transactions/sign', methods=['POST'])
def sign_transaction():
    values = request.json
    required = ['address', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify({"error": "Missing fields for signing"}), 400

    try:
        signature = blockchain.sign_transaction(
            values['address'], values['recipient'], values['amount']
        )
        return jsonify({'signature': signature})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.json
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in values for k in required):
        return jsonify({"error": "Missing transaction fields"}), 400

    try:
        index = blockchain.add_transaction(
            values['sender'], values['recipient'], values['amount'], values['signature']
        )
        return jsonify({'message': f'Transaction will be added to Block {index}'})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    user_id = request.json.get('user_id')
    password = request.json.get('password')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    keys = blockchain.generate_keys(user_id, password=password)
    if "error" in keys:
        return jsonify(keys), 400

    return jsonify(keys)

@app.route('/get_keys/<user_id>', methods=['GET'])
def get_keys(user_id):
    keys = blockchain.get_keys(user_id)
    if "error" in keys:
        return jsonify(keys), 404
    return jsonify(keys)

@app.route('/export_keys/<user_id>/<address>', methods=['GET'])
def export_keys(user_id, address):
    keys = blockchain.export_keys(user_id, address)
    if "error" in keys:
        return jsonify(keys), 404

    json_data = json.dumps(keys, indent=4)
    return send_file(
        io.BytesIO(json_data.encode()),
        mimetype='application/json',
        as_attachment=True,
        download_name=f"{address}_keys.json"
    )

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance})

@app.route('/mine', methods=['GET'])
def mine():
    """
    Perform proof-of-work and mine a new block.
    """
    last_block = blockchain.last_block
    if not last_block:
         return jsonify({'error': 'Cannot mine the genesis block'}), 400
    proof = blockchain.proof_of_work(last_block['proof'])
    miner_address = "7Ji6To9ucp1Z7KvngWRx8BvgDEr7okL2r"
    blockchain.balances[miner_address] = blockchain.balances.get(miner_address, 0)
    blockchain.add_transaction(sender="0", recipient=miner_address, amount=10, signature="miner_signature")
    block = blockchain.create_block(proof, blockchain.hash(last_block))
    return jsonify({'message': "New Block Mined", 'block': block})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)