import subprocess
import os
import tempfile
import json
import threading

class Exec():
    def __init__(self, problem, solver):
        self.problem = problem
        self.solver_path = solver
        self.problem_path = tempfile.mktemp()
        with open(self.problem_path, "w+") as f:
            f.write(json.dumps(self.problem))

    def exe_cpp(self, callback):
        try:
            # args = ["/Users/tanakatoshiyuki/repos/procon35_kyougi/solvers/beam/build/solver_simple"]
            args = [self.solver_path]
            args.append(self.problem_path)
            self.proc = subprocess.Popen(args, stdout=subprocess.PIPE, text=True)

            def wait_proc():
                self.proc.wait()
                answer = json.loads(self.proc.stdout.read())
                callback(answer)

            self.thread = threading.Thread(target=wait_proc)
            self.thread.start()
        except subprocess.CalledProcessError as error:
            print("failed")
            print(f"code: {error.returncode}")
            print(f"error output: {error.stderr}")

        return json.loads(self.proc.stdout.read())

def print_answer(answer):
    print("answer generated")
    print(answer)




