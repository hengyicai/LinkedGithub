#! coding=utf-8
from mongo_client import MyMongoClient
import networkx as nx
import pickle
from gen_gephi_data import sort_by_out_degree, sort_by_in_degree

IP = '112.74.50.127'
PORT = 27017

graph_data = {}


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


def construct_label_graph_from_collection(merge=False):
    mongo_client = MyMongoClient(ip=IP, port=PORT)

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

    if merge:
        merged_G = G
        for u in G.nodes():
            for v in G.nodes():
                if should_merge(u, v) and merged_G.has_node(u) and merged_G.has_node(v):
                    merged_G = nx.contracted_nodes(merged_G, u, v)
        return merged_G
    return G


if __name__ == '__main__':
    G = construct_label_graph_from_collection(merge=True)
    pickle.dump(G, open('./DiGraph.labelGraph.merged.txt', 'w'))
    G = pickle.load(open('./DiGraph.labelGraph.merged.txt'))
    nodes = G.nodes()
    node2id = {}
    index = 1
    for node in nodes:
        node2id[node] = index
        index += 1
    pickle.dump(node2id, open('./DiGraph.labelGraph.merged.Node2ID', 'w'))
    node2id = pickle.load(open('./DiGraph.labelGraph.merged.Node2ID'))
    writeG2csv(G, node2id, './DiGraph.labelGraph.id2id.merged.csv', './DiGraph.labelGraph.node2id.merged.csv')
    sort_by_in_degree(G)
