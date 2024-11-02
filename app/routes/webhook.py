from flask import Blueprint, request, jsonify
import os
import subprocess
import stat

webhook_bp = Blueprint('webhook', __name__)

REPO_DIR = '/opt/bdatalab/repos/BaseballCV'
REPO_URL = 'https://github.com/dylandru/BaseballCV.git'
REPO_BRANCH = '26-create-streamlit-app-designed-for-open-source-annotations'

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    # Get the branch name from the request (default to the specified branch if not provided)
    branch = request.args.get('branch', REPO_BRANCH)

    # Remove the existing repository directory if it exists
    if os.path.exists(REPO_DIR):
        print(jsonify({"message": "Trying to delete existing repo."}))
        subprocess.run(["rm", "-rf", REPO_DIR])
        print(jsonify({"message": "Existing repo deleted"}))

    # Clone the specified branch of the repository
    clone_command = ["git", "clone", "--branch", branch, REPO_URL, REPO_DIR]
    clone_result = subprocess.run(clone_command, capture_output=True, text=True)

    if clone_result.returncode != 0:
        return jsonify({"error": clone_result.stderr, "message": "Clone failed"}), 500

    # Set permissions for the cloned directory and files
    for root, dirs, files in os.walk(REPO_DIR):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)  # 775
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)  # 664

    return jsonify({"message": "Repository successfully cloned", "branch": branch}), 200
