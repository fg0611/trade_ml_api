from flask import Flask, request, jsonify
import os
from globals_vars import global_state
from init_data import init_data
from train import train
from results import results
from graph import graph
from entry import entry
from tlg import send_chart_via_telegram

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return "working", 200

@app.route("/img/<symbol>", methods=["POST"])
async def process_data(symbol):
    try:
        # Directly parse JSON and process data
        json_data = request.get_json()
        init_data(json_data, global_state)
        train(global_state)
        results(global_state)
        # graph(global_state)
        try: # Create and send the chart
            await send_chart_via_telegram(graph(global_state, symbol), global_state["tlg"]["token"], global_state["tlg"]["chat"])
            print("Chart sent successfully!")
        finally: # Clean up the chart file
            if os.path.exists(global_state["chart_path"]):
                os.remove(global_state["chart_path"])
        return jsonify({"success": True, "result": "img enviada a telegram!"}), 200
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error occurred: {e}")
        # Return an error response with a 500 status code
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/signal/<symbol>", methods=["POST"])
async def process_signal(symbol):
    try:
        # Directly parse JSON and process data
        json_data = request.get_json()
        print(json_data)
        init_data(json_data, global_state)
        train(global_state)
        results(global_state)
        return entry(global_state), 200
        # return jsonify({"success": True, "symbol": symbol, "result": entry(global_state)}), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
