from flask import Flask, render_template, request, session
from crypto import w3, send_tx, wait_for_receipt
from contacts import get_contact_info, set_contact_info

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def index():
    return render_template("index.html", connected=w3.isConnected())

@app.route("/contact_info")
def contact_info():
    return render_template("contact_info.html",
                            connected=w3.isConnected(),
                            network=w3.net,
                            contact_info=get_contact_info())

@app.route('/contact_info', methods=['GET', 'POST'])
def update_info():
    contact_info = get_contact_info()
    receipts = []
    changes = []

    # collect changes, when diff found send transaction to contract to update value
    # collect receipts, track balance updates, and return receipts when finished
    for key, value in contact_info.items():
        if (value != request.form[key]):
            fnName = f"set{key.capitalize()}" # convert "bitcoin" to "setBitcoin"
            receipt = set_contact_info(fnName, request.form[key], w3.eth.accounts[0])
            changes.append(key)
            receipts.append(receipt)

    return render_template("success.html",
                            connected=w3.isConnected(),
                            changes=changes,
                            receipts=receipts)

@app.route("/send_tx")
def raw_tx():
    # generate blank raw tx metadata
    tx_meta = { "from": "", "to": "", "value": "" }
    return render_template("transact.html", connected=w3.isConnected(), tx_meta=tx_meta)

@app.route("/send_tx", methods=['GET', 'POST'])
def send_tx_form():
    # send tx, then wait for receipt, add more metadata to it
    tx = send_tx(request.form['from'], request.form['to'], request.form['value'])
    receipt = {
        **wait_for_receipt(w3, tx, 0.3),
        "balance": w3.eth.getBalance(request.form['from']),
        "operation": "sendTransaction"
    }
    changes = [f"Sent transaction to {request.form['to']}"]
    return render_template("success.html", connected=w3.isConnected(), receipts=[receipt], changes=changes)

@app.route('/latest_block')
def block_number():
    return f"Latest block: {w3.eth.getBlock('latest')}"

@app.route('/tx')
def tx_receipt():
    tx_hash = request.args.get('hash')
    if tx_hash:
        return f"Transaction Receipt: {w3.eth.getTransaction(tx_hash)}"
    return "No transaction hash provided!"
