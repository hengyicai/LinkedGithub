#! coding=utf-8
from mongo_client import MyMongoClient
import networkx as nx
import pickle

IP = '112.74.50.127'
PORT = 27017

graph_data = {}
bad_projects = ["pytest","ansible","ansible-modules-core", "pip","ansible-modules-extras","easybuild-easyblocks","pytest-cov","travis-ci","ipython","sh","conda"]


def writeG2csv(G, node2id, path_id2id, path_node2id):
    with open(path_id2id, 'w') as f:
        f.write(','.join(['Source', 'Target']))
        f.write('\n')
        for e in G.edges_iter():
            f.write(','.join([str(node2id[item]) for item in e]))
            f.write('\n')
    with open(path_node2id, 'w') as f:
        f.write(','.join(['Label', 'Id']))
        f.write('\n')
        for node, id in dict(node2id).iteritems():
            if node not in bad_projects:
                f.write(node)
                f.write(',')
                f.write(str(id))
                f.write('\n')


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


def construct_G_from_collection(collection_names, vertex_is_project=True, cross_project=True):
    '''
    :param collection_names: e.g., ['i_i', 'i_p', 'p_p', 'p_i']
    :param vertex_is_project:
    :param cross_project:
    :return: Graph
    '''
    mongo_client = MyMongoClient(ip=IP, port=PORT)

    # colls = ['i_i', 'i_p', 'p_p', 'p_i']

    collections = []
    for col in collection_names:
        collections.append(mongo_client.get_document(db_name='link_sample_stu', collection_name=col))

    G = nx.MultiDiGraph()

    for m_collection in collections:
        for item in m_collection:
            if u'type' in item:
                if cross_project and item[u'type'] == u'crossed':
                    if item[u'_id'] and \
                                    u'source' in item[u'_id'] and \
                                    u'target' in item[u'_id']:
                        if vertex_is_project:
                            source = str(item[u'_id'][u'source']).split('/')[4]
                            target = str(item[u'_id'][u'target']).split('/')[4]
                        else:
                            source = str(item[u'_id'][u'source'])
                            target = str(item[u'_id'][u'target'])
                        if source and target:
                            G.add_edge(source, target)
                elif not cross_project:
                    if item[u'_id'] and \
                                    u'source' in item[u'_id'] and \
                                    u'target' in item[u'_id']:
                        if vertex_is_project:
                            source = str(item[u'_id'][u'source']).split('/')[4]
                            target = str(item[u'_id'][u'target']).split('/')[4]
                        else:
                            source = str(item[u'_id'][u'source'])
                            target = str(item[u'_id'][u'target'])
                        if source and target:
                            G.add_edge(source, target)
    return G


if __name__ == '__main__':
    # G = construct_G_from_collection(['i_i', 'i_p'], vertex_is_project=False, cross_project=True)
    # pickle.dump(G, open('./MultiDiGraph.vertexIsIssueUnit.txt', 'w'))
    G = pickle.load(open('./AllMultiDiGraph.txt'))
    # nodes = G.nodes()
    # node2id = {}
    # index = 1
    # for node in nodes:
    #     node2id[node] = index
    #     index += 1
    # pickle.dump(node2id, open('./AllMultiDiGraph.Node2ID','w'))
    # G.remove_node('pytest')
    # node2id = pickle.load(open('./AllMultiDiGraph.Node2ID'))
    # writeG2csv(G, node2id, './AllMultiDiGraph.id2id.rmPytest.csv', './AllMultiDiGraph.node2id.rmPytest.csv')
    sort_by_in_degree(G)

    #################################################
    '''
    G = pickle.load(open('./AllMultiDiGraph.txt'))
    for b_proj in bad_projects:
        G.remove_node(b_proj)
    node2id = pickle.load(open('./AllMultiDiGraph.Node2ID'))
    writeG2csv(G, node2id, './AllMultiDiGraph.id2id.rmBadProjects.csv', './AllMultiDiGraph.node2id.rmBadProjects.csv')
    '''
