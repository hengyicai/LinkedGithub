# encoding: utf-8
import networkx as nx
import pickle


def find_communities(G, k):
    return list(nx.k_clique_communities(G, k))


def main():
    # Load graph
    import sys
    k = int(sys.argv[1])
    G = pickle.load(open('./AllMultiDiGraph.txt'))
    undi_G = G.to_undirected()
    res_lst = find_communities(undi_G, k)
    for item in res_lst:
        print(item)


if __name__ == '__main__':
    main()
