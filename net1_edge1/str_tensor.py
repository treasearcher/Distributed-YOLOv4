# import torch
import json


def tensor2str(*args):
    out = []
    for ag in args:
        shape=list(ag.shape)
        ag=ag.view(1,-1).cpu()
        tmp={'data':ag,'shape':shape}
        out.append(tmp)

    return json.dumps(out)


def str2tensor(str):
    dcs = json.loads(str)
    out=[]
    for dc in dcs:
        out.append(dc.data.cuda().view(*dc.shape))

    return out

