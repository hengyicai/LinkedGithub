# coding: utf-8

def sort_by_in_degree(G):
    from operator import itemgetter

    prj_lst = []
    for item in sorted(G.in_degree_iter(), key=itemgetter(1), reverse=True):
        prj_lst.append('"' + item[0] + '"')
    print(','.join(prj_lst[:20]))


def sort_by_out_degree(G):
    from operator import itemgetter

    prj_lst = []
    for item in sorted(G.out_degree_iter(), key=itemgetter(1), reverse=True):
        prj_lst.append('"' + item[0] + '"')
    print(','.join(prj_lst[:20]))


def gen_node2id_dic(G):
    node2id = {}
    index = 1
    for node in G.nodes():
        node2id[node] = index
        index += 1
    return node2id
