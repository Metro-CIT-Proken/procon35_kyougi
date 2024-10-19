import subprocess
import numpy as np
import json
import glob
import tempfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filed', type=str,default="")
parser.add_argument('-s', '--solver', type=str,default="solver_simple")
args = parser.parse_args()

files = glob.glob(f"../problems/{args.filed}*.json")
print(files)
count_all = 0
for x in files:
    print(x)
    cp1 = subprocess.run([f"beam/build/{args.solver}",x], text=True, capture_output=True)
    # cp1.wait()
    try:
        print(cp1.stdout)
        print(cp1.stderr)

        out = json.loads(cp1.stdout)
        print(out["n"])
        count_all += out["n"]
        temp_file_path = tempfile.mktemp()
        problem_json = open(temp_file_path, 'w')
        json.dump(out, problem_json)
        problem_json.close()
        chack = subprocess.run(["python3","check_answer.py",x,temp_file_path], text=True, capture_output=True)
        print(chack.stdout,end="")
        if chack.stdout != "correct\n":
            print(cp1.stderr)
        # pass
    except:
        print("ソルバーで問題が発生しました", 500)
        raise TypeError("ソルバーで問題が発生しました")
        # return resp
print("averege = ",count_all/len(files))