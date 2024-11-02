# app/routes/webhook.py
from flask import Blueprint, request, jsonify, current_app
import subprocess


webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    # Path to the repository
    repo_path = '/opt/bdatalab/repos/BaseballCV'
    try:
        # Mark repository as safe
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/opt/bdatalab/repos/BaseballCV"])
        # Run the git pull command
        result = subprocess.run(
            ['git', '-C', repo_path, 'pull', 'origin', '26-create-streamlit-app-designed-for-open-source-annotations'],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({'message': 'Pulled successfully', 'output': result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Pull failed', 'error': e.stderr}), 500
