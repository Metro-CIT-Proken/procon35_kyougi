from flask import Flask
from flask import request
from flask import make_response
import json.scanner
import subprocess
import json
import tempfile


class solver_kind:
    def __init__(self, name, path):
        self.name = name
        self.path = path


solvers = {"solver_simple": solver_kind("solver_simple", "../solvers/beam/build/solver_simple"),
           "solver_beam": solver_kind("solver_beam", "../solvers/beam/build/solver")}

app = Flask(__name__)


@app.route("/get_solvers")
def get_solvers():
    solver_all = json.dumps({"solvers": [i for i in solvers]})
    return solver_all


@app.route("/solve", methods=["POST"])
def solve():
    solve = json.loads(request.get_data())
    # return "<p>Hello, World!</p>"
    if "solver" in list(solve) and "problem" in list(solve):
        pass
    else:
        resp = make_response("キーが不足しています", 500)
        return resp
    # else:
    # eroor
    temp_file_path = tempfile.mktemp()
    problem_json = open(temp_file_path, 'w')
    json.dump(solve["problem"], problem_json)
    problem_json.close()
    cp1 = subprocess.Popen([solvers[solve["solver"]].path,
                              temp_file_path], text=True, stdout=subprocess.PIPE)
    cp1.wait()
    try:
       return json.loads(cp1.stdout.read())
    except:
        resp = make_response("ソルバーで問題が発生しました", 500)
        return resp
