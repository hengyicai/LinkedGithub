# coding: utf-8
import csv
import networkx as nx
import matplotlib.pyplot as plt

nodes_need_merge = [
    ('bug', 'type: bug'),
    ('feature', 'feature request'),
    ('documentation', 'docs'),
    ('testing', 'tests')
]

nodes_dic = {}


def extract_edges(edges_f, nodes_f):
    with open(nodes_f, 'rb') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip header
        for row in csv_reader:
            nodes_dic[row[0]] = row[1]

    edges_lst = []
    with open(edges_f, 'rb') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip header
        for row in csv_reader:
            source = nodes_dic[row[0]]
            target = nodes_dic[row[1]]
            weight = int(row[-1])
            edges_lst.append((source, target, weight))
    return edges_lst


def construct_graph(edges_data):
    di_weighted_graph = nx.DiGraph()
    for edge in edges_data:
        di_weighted_graph.add_edge(edge[0], edge[1], weight=edge[-1])
    return di_weighted_graph


def merge_nodes(nodes, G):
    merged_G = G
    for duplicated_nodes in nodes:
        merged_G = nx.contracted_nodes(merged_G, duplicated_nodes[0], duplicated_nodes[1])
    return merged_G


def plot_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos,
                           node_color=None, node_size=100)
    nx.draw_networkx_labels(G, pos)
    # nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True)
    plt.show()


def main():
    edges_f = './data/id2id.csv'
    nodes_f = './data/id2label.csv'
    merged_G = merge_nodes(
        nodes_need_merge,
        construct_graph(
            extract_edges(edges_f, nodes_f)
        )
    )
    import graph_utils
    node2id = graph_utils.gen_node2id_dic(merged_G)
    import gen_gephi_data
    gen_gephi_data.writeG2csv(
        merged_G,
        node2id,
        './result/merged_label_graph_id2id_final_V2.csv',
        './result/merged_label_graph_node2id_final_V2.csv',
        weight=True
    )
    # plot_graph(merged_G)


if __name__ == '__main__':
    main()
