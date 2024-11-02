from flask import Blueprint, request, jsonify
import os
import subprocess

webhook_bp = Blueprint('webhook', __name__)

REPO_DIR = '/opt/bdatalab/repos/BaseballCV'
REPO_URL = 'https://github.com/dylandru/BaseballCV.git'
REPO_BRANCH = '26-create-streamlit-app-designed-for-open-source-annotations'

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    # Get the branch name from the request (default to the specified branch)
    branch = request.args.get('branch', REPO_BRANCH)

    # Check if the repository directory exists
    if os.path.exists(REPO_DIR):
        # Change permissions recursively to allow deletion
        print("Changing permissions for existing repo.")
        
        # Change permissions command
        chmod_command = ["sudo", "chmod", "-R", "775", REPO_DIR]
        chmod_result = subprocess.run(chmod_command, capture_output=True, text=True)

        if chmod_result.returncode != 0:
            return jsonify({"error": chmod_result.stderr, "message": "Failed to change permissions"}), 500
        
        # Remove the existing repository directory
        print("Trying to delete existing repo.")
        delete_command = ["sudo", "rm", "-rf", REPO_DIR]
        delete_result = subprocess.run(delete_command, capture_output=True, text=True)

        if delete_result.returncode != 0:
            return jsonify({"error": delete_result.stderr, "message": "Failed to delete existing repo"}), 500
        
        print("Existing repo deleted.")

    return jsonify({"message": "Repository deletion process completed", "branch": branch}), 200
