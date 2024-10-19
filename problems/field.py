import random
import numpy as np
import json
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--width', type=int, default=8)
parser.add_argument('--height', type=int, default=8)
parser.add_argument('--seed', type=int)
parser.add_argument('--swap', default=5, type=int)
parser.add_argument('-o', '--output', type=str)
args = parser.parse_args()


def make_field():
    x = args.width  # フィールドの固定サイズ
    y = args.height  # フィールドの固定サイズ
    # x=random.randint(32,256)
    # y=random.randint(32,256)
    # ("フィールド", x, y)
    smallest = ((x * y) // 10) + 1
    # print(smallest)
    field = []
    math_list = []
    # random.seedで固定しています。必要に応じて変更してください。
    if args.seed:
        random.seed(args.seed)
    else:
        pass

    for i in range(4):
        for _ in range(smallest):
            math_list.append(i)
    for _ in range(y):
        cells = []
        for _ in range(x):
            if math_list:
                selected = random.choice(math_list)
                math_list.remove(selected)
                cells.append(selected)
            else:
                cells.append(random.randint(0, 3))
        field.append(cells)
    field = np.array(field)
    return x, y, field


def make_nuki(amount_created):
    answer = []
    for _ in range(amount_created):
        x = random.randint(1, 5)
        y = random.randint(1, 5)
        nukis = [[random.randint(0, 1) for _ in range(x)] for _ in range(y)]
        nukis = np.array(nukis)
        answer.append(nukis)
    return answer


def defo_form():
    defo_dict = {}
    defo_dict[1] = np.array([[1]])

    data_range = [2, 4, 8, 16, 32, 64, 128, 256]
    kataban_1 = 2
    for i in data_range:
        kara_list = [[1]*i]*i
        kara_list = np.array(kara_list)
        defo_dict[kataban_1] = kara_list
        kataban_1 += 3

    kataban_2 = 3
    for i in data_range:
        kara_list = [[1]*i]
        for w in range(len(kara_list)):
            if w % 2 == 1:
                kara_list[w] = [0]*i
        kara_list *= i
        kara_list = np.array(kara_list)
        defo_dict[kataban_2] = kara_list
        kataban_2 += 3

    kataban_3 = 4
    for i in data_range:
        kara_list = []
        for n in range(i):
            if n % 2 == 0:
                kara_list.append([1]*i)
            else:
                kara_list.append([0]*i)
        kara_list = np.array(kara_list)
        defo_dict[kataban_3] = kara_list
        kataban_3 += 3
    return defo_dict


def field_to_string(field):
    return ["".join(map(str, row)) for row in field]


def moved(nu_key, x, y, move, field, k_dict, fsize_x, fsize_y):
    nukigata = k_dict[nu_key]
    nukigata_tatenagasa, yokononagasa = nukigata.shape

    if x < 0:
        nukigata = nukigata[:, -x:]
        x = 0
    if y < 0:
        nukigata = nukigata[-y:, :]
        y = 0
    if x + yokononagasa > fsize_x:
        nukigata = nukigata[:, :fsize_x - x]
    if y + nukigata_tatenagasa > fsize_y:
        nukigata = nukigata[:fsize_y - y, :]

    nukigata_tatenagasa, yokononagasa = nukigata.shape

    if y > fsize_y or x > fsize_x:
        return "!場外指定"
    move_list = []
    for row in range(nukigata_tatenagasa):
        for col in range(yokononagasa):
            if nukigata[row, col] == 1:
                fcoord_x = x+col
                fcoord_y = y+row
                move_list.append((fcoord_y, fcoord_x))

    grouped_by_column = {}
    for coord_y, coord_x in move_list:
        if coord_x not in grouped_by_column:
            grouped_by_column[coord_x] = []
        grouped_by_column[coord_x].append(coord_y)
    grouped_by_row = {}
    for coord_y, coord_x in move_list:
        if coord_y not in grouped_by_row:
            grouped_by_row[coord_y] = []
        grouped_by_row[coord_y].append(coord_x)

    if move == 0:
        for coord_x in grouped_by_column:
            count = 0
            for coord_y in grouped_by_column[coord_x]:
                for k in range(coord_y, count+1, -1):
                    field[k][coord_x], field[k-1][coord_x] = field[k -
                                                                   1][coord_x], field[k][coord_x]
                count += 1
    if move == 1:
        for coord_x in grouped_by_column:
            grouped_by_column[coord_x].sort(reverse=True)
        for coord_x in grouped_by_column:
            count = 0
            for coord_y in grouped_by_column[coord_x]:
                under_row = (fsize_y-coord_y-1-count)
                count += 1
                for k in range(under_row):
                    field[coord_y+k][coord_x], field[coord_y + k +
                                                     1][coord_x] = field[coord_y+k+1][coord_x], field[coord_y+k][coord_x]
    if move == 2:
        for coord_y in grouped_by_row:
            count = 0
            for coord_x in grouped_by_row[coord_y]:
                for k in range(coord_x, count, -1):
                    field[coord_y][k], field[coord_y][k -
                                                      1] = field[coord_y][k-1], field[coord_y][k]
                count += 1
    if move == 3:
        for coord_y in grouped_by_row:
            grouped_by_row[coord_y].sort(reverse=True)
        for coord_y in grouped_by_row:
            count = 0
            for coord_x in grouped_by_row[coord_y]:
                for k in range(coord_x, fsize_x-count-1, 1):
                    field[coord_y][k], field[coord_y][k +
                                                      1] = field[coord_y][k+1], field[coord_y][k]
    return field


def output():
    # fsize=fieldの大きさ
    fsize_x, fsize_y, field = make_field()
    # create =抜き型の数
    goal_field = field_to_string(field)
    create = 2
    # k_list=createで作成した抜き型
    k_list = make_nuki(create)
    k_dict = {26 + i: n for i, n in enumerate(k_list)}
    # print("フィールド：\n", field)
    # print("抜き型辞書：", k_dict)

    # 全ての抜き型
    all_nuki = {**k_dict, **defo_form()}
    # 　盤面移動はこれをいじってください
    for _ in range(args.swap):
        nu_key = random.choice(list(k_dict.keys()))
        x = random.randint(0, fsize_x - 1)
        y = random.randint(0, fsize_y - 1)
        move = random.randint(0, 3)
        start_field = moved(nu_key, x, y, move, field,
                            all_nuki, fsize_x, fsize_y)
    # outputの作成
    # numpyは参照同じらしいから　.copyを使うらしい
    output = {
        "board": {
            "width": fsize_x,
            "height": fsize_y,
            "start": field_to_string(start_field),  # ぐちゃぐちゃにしたフィールド
            "goal": goal_field  # 最初に作成したフィールド
        },
        "general": {
            "n": len(k_dict),
            "patterns": [{
                "p": key,
                "width": nuki.shape[1],
                "height": nuki.shape[0],
                "cells": field_to_string(nuki)
            } for key, nuki in k_dict.items()]
        }
    }

    return json.dumps(output, ensure_ascii=False, indent=4)

# def main():
#     parser = argparse.ArgumentParser(description='Output to a specified file')
#     parser.add_argument('-o', '--output', type=str, help='Output file')
#     args = parser.parse_args()

#     output_text = "Hello, world!"

#     if args.output:
#         with open(args.output, 'w') as file:
#             file.write(output_text)
#     else:
#         print(output_text)



# print(output())
if __name__ == "__main__":
    output_data = output()
    if args.output:
        with open(args.output, 'w', encoding='utf-8')as f:
            f.write(output_data)
    else:
        print(output_data)
