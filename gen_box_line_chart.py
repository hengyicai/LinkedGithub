# coding: utf-8
import mongo_client as mc
import config
import pickle
import numpy as np
from sklearn import preprocessing


def dump_box_line_data(dump_f):
    db_name = 'verify'
    table_name = 'prior_label_issues'

    mongo_client = mc.MyMongoClient(config.MONGO_IP, config.MONGO_PORT)

    docs = mongo_client.get_document(db_name=db_name, collection_name=table_name)

    res_dic = {
        'high': [],
        'low': []
    }
    for doc in docs:
        type = doc['type']
        in_d_len = doc['in_degree_len']
        out_d_len = doc['out_degree_len'] if 'out_degree_len' in doc else None

        if type is None or in_d_len is None or (int(in_d_len) == 0 and (out_d_len is None or int(out_d_len) == 0)):
            pass
        else:
            res_dic[type].append(int(in_d_len))
    pickle.dump(res_dic, open(dump_f, 'w'))


def five_number(arr):
    arr = np.asarray(arr)
    median = np.median(arr)
    scaler = preprocessing.StandardScaler().fit(arr)
    arr = scaler.transform(arr)
    quartile_4_1 = np.percentile(arr, 25)
    quartile_4_3 = np.percentile(arr, 75)
    min_arr = np.min(arr)
    max_arr = np.max(arr)
    return median, quartile_4_1, quartile_4_3, min_arr, max_arr


def box_plot(box_line_data):
    high_arr = np.asarray(box_line_data['high'])
    low_arr = np.asarray(box_line_data['low'])
    print(five_number(high_arr))
    print(five_number(low_arr))


def print_data():
    dump_f = './result/prior_label_issues.data'
    dump_box_line_data(dump_f)
    box_line_data = pickle.load(open(dump_f))
    for key in dict(box_line_data).keys():
        print(key)
        print(','.join([str(item) for item in box_line_data[key]]))


if __name__ == '__main__':
    dump_f = './result/prior_label_issues_rm_single_nodes.data'
    # dump_box_line_data(dump_f)
    box_line_data = pickle.load(open(dump_f))
    box_plot(box_line_data)
