# coding: utf-8
from __future__ import division
from datetime import datetime
import time
import config

from mongo_client import MyMongoClient

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
mongo_client = MyMongoClient(ip=config.MONGO_IP, port=config.MONGO_PORT)


def query_duplicated_time(repo_name_id, context):
    db_name = 'github_v2'
    col_name = 'comments'
    id = repo_name_id
    comment = mongo_client.get_document(db_name=db_name, collection_name=col_name, _id=id)
    if u'comments' in comment:
        for c in comment[u'comments']:
            if context in c[u'body']:
                return c[u'created_at']
    return None


def query_issue_time(repo_name_id):
    db_name = 'github_v2'
    col_name = 'issues'
    id = repo_name_id
    issue = mongo_client.get_document(db_name=db_name, collection_name=col_name, _id=id)
    return issue[u'issue_content'][u'created_at'] if u'issue_content' in issue and u'created_at' in issue[
        u'issue_content'] else None


def time_diff(t1, t2):
    # date_str = "2017-07-17T18:38:59Z"
    dt_obj1 = datetime.strptime(t1, DATE_FORMAT)
    dt_obj2 = datetime.strptime(t2, DATE_FORMAT)

    diff = dt_obj2 - dt_obj1
    days_to_hours = diff.days * 24

    return days_to_hours + (diff.seconds) / 3600


def iter_duplicate_issue_link():
    collection_names = ['duplicate_issue_link']
    collections = []
    for col in collection_names:
        collections.append(
            mongo_client.get_document(db_name='link_sample_stu', collection_name=col, no_cursor_timeout=True))

    for m_collection in collections:
        for item in m_collection:
            if u'repo_name_id' in item and \
                    u'context' in item:
                repo_name_id = item[u'repo_name_id']
                context = item[u'context']
                # print('{}-->{}'.format(repo_name_id, context))
                duplicated_time = query_duplicated_time(repo_name_id, context)
                issue_time = query_issue_time(repo_name_id)

                if duplicated_time and issue_time:
                    hour_diff = time_diff(issue_time, duplicated_time)
                    print('{},{}'.format(repo_name_id, hour_diff))


def main():
    iter_duplicate_issue_link()


if __name__ == '__main__':
    main()
