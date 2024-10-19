import field
import json
import numpy as np
folder = "procon35_kyougi/problems/"


def simple(i,j,n):
    # for i in range(5, 9):
    #     h = 2**i
    #     for j in range(5, 9):
    #         w = 2**j
    #         for s in range(3):
    #             args = field.get(seed=s, width=w, height=h, swap=256*2,
    #                              output=folder + f"{h}_{w}_seed{s}.json")
    #             field.do(args)
        h = 2**i
        w = 2**j
        for s in range(n):
            args = field.get(seed=s, width=w, height=h, swap=256*2,
                            output=folder + f"{h}_{w}_seed{s}.json")
            field.do(args)


def gatagata():
    for i in range(5, 9):
        h = 2**i - i
        if i == 5:
            continue
        for j in range(5, 9):
            w = 2**j - j
            if j == 5:
                continue
            for s in range(3):
                args = field.get(seed=s, width=w, height=h, swap=256*2,
                                 output=folder + f"{h}_{w}_seed{s}.json")
                field.do(args)


def tatesima(w, h, model, s=0):
    # o = "fileld\kari.json"
    # n = 1
    fields = []
    if model == "tateshima" or model == 0:
        r = []
        for x in range(0, w):
            r += f"{x%4}"
            fields = [r for x in range(h)]
    elif model == "yokoshima" or model == 1:
        for x in range(h):
            l = []
            for j in range(w):
                l.append(x % 4)
            fields.append(l)
    elif model == "ichimatu" or model == 2:
        for x in range(h):
            l = []
            for j in range(w):
                l.append((j+x) % 4)
            fields.append(l)

    args = field.get(seed=s, width=w, height=h, swap=256*2,
                     output=folder + f"{model}_{h}_{w}_seed{s}.json")
    field.do(args,np.array(fields))
    # ans_json = open(o, 'w')
    # json.dump(args, ans_json)
    # ans_json.close()


# for i in range(3):
#     tatesima(10,10,i)
simple(6,6,100)