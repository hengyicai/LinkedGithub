#! coding=utf-8
from mongo_client import MyMongoClient
import networkx as nx
import pickle
import config
import graph_utils

IP = config.MONGO_IP
PORT = config.MONGO_PORT

# BAD_PRJS = ["pytest", "ansible", "ansible-modules-core", "pip", "ansible-modules-extras", "easybuild-easyblocks",
#            "pytest-cov", "travis-ci", "ipython", "sh", "conda"]
BAD_PRJS = ["pytest-dev/pytest"]


def writeG2csv(G, node2id, path_id2id, path_node2id, exclusive_nodes=None, weight=False):
    with open(path_id2id, 'w') as f:
        f.write(','.join(['Source', 'Target']))
        if weight:
            f.write(',Weight')
        f.write('\n')
        for e in G.edges_iter(data=weight):
            if weight:
                f.write(','.join([str(node2id[item]) for item in e[:2]] + [str(e[-1]['weight'])]))
            else:
                f.write(','.join([str(node2id[item]) for item in e]))

            f.write('\n')
    with open(path_node2id, 'w') as f:
        f.write(','.join(['Label', 'Id']))
        f.write('\n')
        for node, id in dict(node2id).iteritems():
            if exclusive_nodes is None or (exclusive_nodes is not None and node not in exclusive_nodes):
                f.write(node)
                f.write(',')
                f.write(str(id))
                f.write('\n')


def construct_G_from_collection(collection_names, vertex_is_project=True, cross_project=True):
    '''
    :param collection_names: e.g., ['i_i', 'i_p', 'p_p', 'p_i']
    :param vertex_is_project:
    :param cross_project:
    :return: Graph
    '''
    mongo_client = MyMongoClient(ip=IP, port=PORT)

    collections = []
    for col in collection_names:
        collections.append(mongo_client.get_document(db_name='link_sample_stu', collection_name=col))

    G = nx.MultiDiGraph()

    for m_collection in collections:
        for item in m_collection:
            if item[u'project_link'] and \
                    u'source' in item[u'project_link'] and \
                    u'target' in item[u'project_link']:
                source = item[u'project_link'][u'source']
                target = item[u'project_link'][u'target']
                if source and target:
                    G.add_edge(source, target)

    return G


def main():
    dump_file_G = config.DATA_DIR + 'AllMultiDiGraph_UserPrj_New.txt'
    dump_file_node2id = config.DATA_DIR + 'AllMultiDiGraph_UserPrj_New.Node2ID'
    res_id2id = config.DATA_DIR + 'AllMultiDiGraph_UserPrj_New.id2id.csv'
    res_node2id = config.DATA_DIR + 'AllMultiDiGraph_UserPrj_New.node2id.csv'

    # Construct graph then dump it
    G = construct_G_from_collection(['project_link'], vertex_is_project=False, cross_project=True)
    pickle.dump(G, open(dump_file_G, 'w'))

    # Load dumped graph into G
    G = pickle.load(open(dump_file_G))

    # Generate the node->id dict then dump it
    node2id = graph_utils.gen_node2id_dic(G)
    pickle.dump(node2id, open(dump_file_node2id, 'w'))

    # Load dumped node2id and write result to disk
    node2id = pickle.load(open(dump_file_node2id))
    # Remove some nodes in G
    # for bad_prj in BAD_PRJS:
    #    G.remove_node(bad_prj)

    writeG2csv(G, node2id, res_id2id, res_node2id)

    # Check the degree
    # graph_utils.sort_by_in_degree(G)


if __name__ == '__main__':
    main()
    '''
    dump_file_G = config.DATA_DIR + 'AllMultiDiGraph_UserPrj.txt'
    G = pickle.load(open(dump_file_G))
    graph_utils.sort_by_in_degree(G)
    '''
