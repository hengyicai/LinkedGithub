#!coding=utf-8
from mongo_client import MyMongoClient
import gen_gephi_data

mongo_client = MyMongoClient(gen_gephi_data.IP, gen_gephi_data.PORT)


def get_issue_by_id(issue_id, another_id=None):
    ret_issue = mongo_client.get_document(db_name='github_v2', collection_name='issues', _id=issue_id)
    if ret_issue is None:
        ret_issue = mongo_client.get_document(db_name='github_v2', collection_name='issues_depended_not_in_download',
                                              _id=another_id)
    return ret_issue


def get_labels_title(issue_id, another_issue_id=None):
    issue = get_issue_by_id(issue_id, another_id=another_issue_id)
    if issue is not None and "issue_content" in issue:
        if "labels" in issue["issue_content"] and "title" in issue["issue_content"]:
            return [item['name'] for item in issue["issue_content"]["labels"]], issue["issue_content"]["title"]


def read_as_tuple_lst(file_name, thres):
    from ast import literal_eval as make_tuple
    lst = []
    with open(file_name) as f:
        line = f.readline()

        while line:
            if int(line.strip()[1:-1].split(',')[-1]) > thres:
                tup = str(line).strip()
                lst.append(make_tuple(tup))
                line = f.readline()
            else:
                break
    return lst


def get_result(issue_lst, direction):
    '''

    :param issue_lst:
    :param direction: in or out
    :return:
    '''
    res_lst = []
    for item in issue_lst:
        issue = item[0]
        freq = item[-1]
        user = issue.split('/')[3]
        project = issue.split('/')[4]
        issue_number = issue.split('/')[6]
        another_issue_id = user + "/" + project + "#" + issue_number
        labels_title_tup = get_labels_title(user + "/" + project + "+" + issue_number, another_issue_id)
        if labels_title_tup is not None:
            res_item = {
                "issue_html_url": issue,
                "direction": direction,
                "freq": freq,
                "labels": labels_title_tup[0],
                "title": labels_title_tup[1]
            }
            res_lst.append(res_item)
    return res_lst


def analyse_label(res_lst, thres):
    # user = "borgbackup"
    # project = "borg"
    # issue_number = "5"
    # print(get_labels_title(user + "/" + project + "+" + issue_number))

    label_dist = {}
    for res in res_lst:
        labels = res['labels']
        for label in labels:
            if label not in label_dist:
                label_dist[label] = 1
            else:
                label_dist[label] += 1
    label_dist_lst = []
    for key, val in label_dist.iteritems():
        label_dist_lst.append((key, val))
    sorted_label_dist_lst = sorted(label_dist_lst, key=lambda x: x[1])
    print("threshold: {}, label distribution: {} ".format(thres, sorted_label_dist_lst))


def analyse_title(res_lst, thres):
    res_tuple_lst = []
    for res in res_lst:
        title = res['title']
        freq = res['freq']
        issue_html_url = res['issue_html_url']
        res_tuple_lst.append((issue_html_url, freq, title))
    sorted_title_tuple_lst = sorted(res_tuple_lst, key=lambda x: x[1], reverse=True)
    # print("threshold: {}, title: {} ".format(thres, sorted_title_tuple_lst))
    for item in sorted_title_tuple_lst:
        print(item)


def main():
    high_out_degree_f = './出度比较高的issues[修正].txt'
    thres = 10
    res_lst = get_result(read_as_tuple_lst(high_out_degree_f, thres), 'out')
    # analyse_label(res_lst, thres)
    analyse_title(res_lst, thres)


if __name__ == '__main__':
    main()
