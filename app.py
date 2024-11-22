
import sys
import os

# Add the `src` directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


from flask import Flask, request, render_template, jsonify
from ai_researcher.crew import AiResearcher

# Initialize the Crew instance
ai_researcher = AiResearcher()

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def index():
    """
    Render the home page with a simple UI.
    """
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_task():
    """
    Handle 'Run Query' task via Flask.
    """
    query = request.form.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        inputs = {"query": query}
        result = ai_researcher.crew().kickoff(inputs=inputs)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/train", methods=["POST"])
def train_task():
    """
    Handle 'Train Crew' task via Flask.
    """
    n_iterations = request.form.get("iterations", type=int)
    filename = request.form.get("filename")

    if not n_iterations or not filename:
        return jsonify({"error": "Iterations and filename are required"}), 400

    try:
        inputs = {"query": "What is Direct Incurred Loss?"}
        ai_researcher.crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        return jsonify({"success": True, "message": f"Training completed and saved to {filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/replay", methods=["POST"])
def replay_task():
    """
    Handle 'Replay Task' task via Flask.
    """
    task_id = request.form.get("task_id")
    if not task_id:
        return jsonify({"error": "Task ID is required"}), 400

    try:
        ai_researcher.crew().replay(task_id=task_id)
        return jsonify({"success": True, "message": f"Replayed task {task_id}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/test", methods=["POST"])
def test_task():
    """
    Handle 'Test Crew' task via Flask.
    """
    n_iterations = request.form.get("iterations", type=int)
    model_name = request.form.get("model_name")

    if not n_iterations or not model_name:
        return jsonify({"error": "Iterations and model name are required"}), 400

    try:
        inputs = {"query": "What is Direct Incurred Loss?"}
        ai_researcher.crew().test(n_iterations=n_iterations, openai_model_name=model_name, inputs=inputs)
        return jsonify({"success": True, "message": "Testing completed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
