# coding: utf-8
import config
from mongo_client import MyMongoClient


def get_issue_link_count():
    mongo_client = MyMongoClient(ip=config.MONGO_IP, port=config.MONGO_PORT)

    collections = []
    collection_names = ['i_i', 'i_p', 'p_p', 'p_i']
    for col in collection_names:
        collections.append(mongo_client.get_document(db_name='link_sample_stu', collection_name=col))

    issue_units_map_count = {}
    for m_collection in collections:
        for item in m_collection:
            source = None
            if item[u'_id'] and \
                    u'source' in item[u'_id'] and \
                    u'target' in item[u'_id']:
                s_arr = str(item[u'_id'][u'source']).split('/')
                # t_arr = str(item[u'_id'][u'target']).split('/')
                s_flag = s_arr[5][0]
                source = '/'.join(s_arr[3:5] + [s_flag, s_arr[6]])
                # target = '/'.join(t_arr[3:5].extend([t_flag, t_arr[6]]))
            if source:
                if source in issue_units_map_count:
                    issue_units_map_count[source] += 1
                else:
                    issue_units_map_count[source] = 1
    return issue_units_map_count


def write_map(m, file_p):
    with open(file_p, 'w') as f:
        for key in dict(m).keys():
            f.write(str(key))
            f.write(',')
            f.write(str(m[key]))
            f.write('\n')


def read_map(file_p):
    ret_map = {}
    with open(file_p) as f:
        line = f.readline()
        while line:
            item_arr = line.strip().split(',')
            ret_map[item_arr[0]] = item_arr[-1]
            line = f.readline()
    return ret_map


def main():
    # res_map = get_issue_link_count()
    m_f = './result/issue_unit_map_link_count.csv'
    # write_map(res_map, m_f)
    issue_unit_map_count = read_map(m_f)
    count_map_issue_unit = {}
    for key, val in dict(issue_unit_map_count).iteritems():
        if val in count_map_issue_unit:
            count_map_issue_unit[val] += 1
        else:
            count_map_issue_unit[val] = 1
    write_map(count_map_issue_unit, './result/count_map_issue_unit.csv')


if __name__ == '__main__':
    main()
