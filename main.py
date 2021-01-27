from flask import Flask, render_template, request
import routes
import data
from google.cloud import datastore


app = Flask(__name__)
requestMethods = routes.RequestMethods()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/projects', methods=['GET', 'POST'])
def get_and_post_projects():
    return requestMethods.get_and_post(data.PROJECTS)


@app.route('/users', methods=['GET', 'POST'])
def get_and_post_users():
    return requestMethods.get_and_post(data.USERS)


@app.route('/projects/<projectid>/tasks', methods=['GET', 'POST'])
def get_and_post_tasks(projectid):
    return requestMethods.get_and_post(data.TASKS, projectid)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)