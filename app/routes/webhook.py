from flask import Blueprint, request, jsonify
import os
import subprocess

webhook_bp = Blueprint('webhook', __name__)

REPO_DIR = '/opt/bdatalab/repos/BaseballCV'
REPO_URL = 'https://github.com/dylandru/BaseballCV.git'
REPO_BRANCH = '26-create-streamlit-app-designed-for-open-source-annotations'

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    # Get the branch name from the request (default to 'main' if not provided)
    branch = request.args.get('branch', REPO_BRANCH)

    # Remove the existing repository directory
    if os.path.exists(REPO_DIR):
        print(jsonify({"message": "Trying to delete existing repo."}))
        subprocess.run(["rm", "-rf", REPO_DIR])
        print(jsonify({"message": "Existing repo deleted"}))

    # Clone the specified branch of the repository
    clone_command = ["git", "clone", "--branch", branch, REPO_URL, REPO_DIR]
    clone_result = subprocess.run(clone_command, capture_output=True, text=True)

    if clone_result.returncode != 0:
        return jsonify({"error": clone_result.stderr, "message": "Clone failed"}), 500

    return jsonify({"message": "Repository successfully cloned", "branch": branch}), 200
