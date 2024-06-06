from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import chess_main


app = Flask(__name__)
CORS(app)

game = chess_main.game()

@app.route("/validate_move", methods=['POST'])
def check_move():
	# EXAMPLE JSON DATA:
	# [[4,7], [3,5]]
	data = request.get_json()
	print(data)
	assert data is not None, "Data is not in json format"
	move = (tuple(data[0]), tuple(data[1]))
	valid = game.make_move(move)
	print(valid)
	response = {
		"valid": valid,
		"game over": game.game_over,
		"check": game.check,
		"turn": "error" if not valid else "white" if game.moves%2 else "black",
	}
	print(response)
	return jsonify(response)