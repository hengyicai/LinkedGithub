#! coding=utf-8
from mongo_client import MyMongoClient
import networkx as nx
import pickle
from graph_utils import sort_by_out_degree, sort_by_in_degree, gen_node2id_dic
import config


def writeG2csv(G, node2id, path_id2id, path_node2id):
    with open(path_id2id, 'w') as f:
        f.write(','.join(['Source', 'Target', 'Weight']))
        f.write('\n')
        for e in G.edges_iter(data='weight'):
            f.write(','.join([str(node2id[item]) for item in e[0:2]]))
            f.write(',')
            f.write(str(e[-1]))
            f.write('\n')
    import io
    with io.open(path_node2id, 'w', encoding='utf8') as f:
        f.write(u','.join([u'Label', u'Id']))
        f.write(u'\n')
        for node, id in dict(node2id).iteritems():
            f.write(node)
            f.write(u',')
            f.write(unicode(id))
            f.write(u'\n')


def should_merge(u, v):
    if v in u:
        return True
    return False


def construct_label_graph_from_collection():
    mongo_client = MyMongoClient(ip=config.MONGO_IP, port=config.MONGO_PORT)

    collections = []
    for col in ['different_label_link']:
        collections.append(mongo_client.get_document(db_name='verify', collection_name=col))

    G = nx.DiGraph()

    for m_collection in collections:
        for item in m_collection:
            source_v = item['_id']['source_label']
            target_v = item['_id']['target_label']
            e_weight = int(item['count'])
            G.add_edge(source_v, target_v, weight=e_weight)
    return G


def merge_graph(G):
    merged_G = G
    for u in G.nodes():
        for v in G.nodes():
            if should_merge(u, v) and merged_G.has_node(u) and merged_G.has_node(v):
                merged_G = nx.contracted_nodes(merged_G, u, v)
    return merged_G


if __name__ == '__main__':
    dumped_graph = config.DATA_DIR + 'DiGraph.labelGraph.txt'
    dumped_node2id = config.DATA_DIR + 'DiGraph.labelGraph.merged.Node2ID'
    dumped_merged_graph = config.DATA_DIR + 'DiGraph.labelGraph.merged.txt'
    res_G_id2id = config.DATA_DIR + 'DiGraph.labelGraph.id2id.merged.csv'
    res_G_node2id = config.DATA_DIR + 'DiGraph.labelGraph.node2id.merged.csv'

    # G = construct_label_graph_from_collection()
    # pickle.dump(G, open(dumped_graph, 'w'))
    G = pickle.load(open(dumped_graph))
    merged_G = merge_graph(G)
    pickle.dump(merged_G, open(dumped_merged_graph, 'w'))

    merged_G_node2id = gen_node2id_dic(merged_G)
    pickle.dump(merged_G_node2id, open(dumped_node2id, 'w'))
    # merged_G_node2id = pickle.load(open(dumped_node2id))

    writeG2csv(merged_G, merged_G_node2id, res_G_id2id, res_G_node2id)
    sort_by_in_degree(merged_G)
