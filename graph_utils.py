# coding: utf-8


def sort_by_in_degree(G, top_k=20):
    from operator import itemgetter

    print('{},{},{}'.format('node_name', 'out_d', 'in_d'))
    for item in sorted(G.in_degree_iter(), key=itemgetter(1), reverse=True)[:top_k]:
        node = item[0]
        out_d = G.out_degree(node)
        in_d = item[1]
        print('{},{},{}'.format(node, out_d, in_d))


def sort_by_out_degree(G, top_k=20):
    from operator import itemgetter

    print('{},{},{}'.format('node_name', 'out_d', 'in_d'))
    for item in sorted(G.out_degree_iter(), key=itemgetter(1), reverse=True)[:top_k]:
        node = item[0]
        in_d = G.in_degree(node)
        out_d = item[1]
        print('{},{},{}'.format(node, out_d, in_d))


def gen_node2id_dic(G):
    node2id = {}
    index = 1
    for node in G.nodes():
        node2id[node] = index
        index += 1
    return node2id
