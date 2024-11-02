from flask import Blueprint, request, jsonify
import os
import subprocess

webhook_bp = Blueprint('webhook', __name__)

REPO_DIR = '/opt/bdatalab/repos/BaseballCV'
REPO_URL = 'https://github.com/dylandru/BaseballCV.git'
REPO_BRANCH = '26-create-streamlit-app-designed-for-open-source-annotations'

# Fetch the sudo password from the system environment variable
SUDO_PASSWORD = os.getenv('SUDO_PASSWORD')
print(SUDO_PASSWORD)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    # Get the branch name from the request (default to specified branch if not provided)
    branch = request.args.get('branch', REPO_BRANCH)

    # Check if the repository directory exists
    if os.path.exists(REPO_DIR):
        # Change permissions recursively to allow deletion
        print(jsonify({"message": "Changing permissions for existing repo."}))
        
        # Run the chmod command with sudo
        chmod_command = f"echo {SUDO_PASSWORD} | sudo -S chmod -R 775 {REPO_DIR}"
        chmod_result = subprocess.run(chmod_command, shell=True, capture_output=True, text=True)

        if chmod_result.returncode != 0:
            return jsonify({"error": chmod_result.stderr, "message": "Failed to change permissions"}), 500
        
        # Remove the existing repository directory
        print(jsonify({"message": "Trying to delete existing repo."}))
        delete_command = f"echo {SUDO_PASSWORD} | sudo -S rm -rf {REPO_DIR}"
        delete_result = subprocess.run(delete_command, shell=True, capture_output=True, text=True)

        if delete_result.returncode != 0:
            return jsonify({"error": delete_result.stderr, "message": "Failed to delete existing repo"}), 500
        
        print(jsonify({"message": "Existing repo deleted."}))

    # Clone the specified branch of the repository without sudo
    print(jsonify({"message": "Cloning the repository."}))
    clone_command = f"git clone --branch {branch} {REPO_URL} {REPO_DIR}"
    clone_result = subprocess.run(clone_command, shell=True, capture_output=True, text=True)

    if clone_result.returncode != 0:
        return jsonify({"error": clone_result.stderr, "message": "Clone failed"}), 500

    return jsonify({"message": "Repository successfully cloned", "branch": branch}), 200
