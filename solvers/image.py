from PIL import Image
import numpy as np
import argparse
import json
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--folder', type=str)
parser.add_argument('-o', '--output', type=str)
parser.add_argument('--start', type=str, default="start")
parser.add_argument('--goal', type=str, default="goal")

args = parser.parse_args()
if not args.output:
    raise FileNotFoundError("フォルダが指定されていません")

# 画像データの読み込み
name = [args.start, args.goal]
file = {}
file[args.start] = f"{args.folder}/{args.start}.png"
file[args.goal] = f"{args.folder}/{args.goal}.png"

# 0が格納された配列を画像のサイズと同じサイズで用意
color = [[255, 0, 0], [0, 225, 0], [0, 0, 255], [255, 255, 0]]

b_output = {}
g_output = {}
for q in name:
    board = []
    img = Image.open(file[q])
    # 画像のサイズ(幅[px] x 高さ[px])を取得し、それぞれを変数に代入
    if q == name[0]:
        width, height = img.size
        g_output = {"n": 0, "patterns": []}
        b_output["width"] = width
        b_output["height"] = height
    for y in range(height):
        line = ""
        for x in range(width):
            # 順次、ピクセルの色の数値を代入している
            # try:
            pic = np.array(img.getpixel((x, y))[0:3])
            mi = -1
            point = 0
            for i, c in enumerate(color):
                a = np.array(c)
                distance = np.linalg.norm(pic-a)
                if mi == -1 or mi > distance:
                    mi = distance
                    point = i
            line += str(point)

        board.append(line)
    b_output[q] = board
patterns = []
files = glob.glob(f"{args.folder}/*.png")
for i in files:
    print(i)
    if name[0] in i or name[1] in i:
        continue
    dic = {}
    img = Image.open(i)
    # 画像のサイズ(幅[px] x 高さ[px])を取得し、それぞれを変数に代入
    width, height = img.size
    cells = []
    num = i[len(args.folder)+1:len(i)-4]
    try:
        num = int(num)
    except:
        raise TypeError("抜き型用のファイル名が異なります\nファイル名は数字にしてください")
    dic["p"] = num
    dic["width"] = width
    dic["height"] = height
    for y in range(height):
        line = ""
        for x in range(width):
            # 順次、ピクセルの色の数値を代入している
            # try:
            pic = np.array(img.getpixel((x, y))[0:3])
            mi = -1
            point = 0
            for i, c in enumerate([[255, 255, 225], [0, 0, 0]]):
                a = np.array(c)
                distance = np.linalg.norm(pic-a)
                if mi == -1 or mi > distance:
                    mi = distance
                    point = i
            line += str(point)

        cells.append(line)
    dic["cells"] = cells
    patterns.append(dic)
g_output["patterns"] = patterns
g_output["n"] = len(patterns)
# print(board)
# 画像データが数値の配列になっていることが確認できる
ans_json = open(f'{args.folder}/{args.output}.json', 'w')
json.dump({"board": b_output, "general": g_output}, ans_json)
ans_json.close()
# print(patterns)
