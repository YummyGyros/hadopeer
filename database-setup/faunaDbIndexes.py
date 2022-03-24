import os
import sys
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient

from faunaTools import createFaunaFieldsArray

def createFaunaIndex(client, name, collection, values=[], terms=[]):
  client.query(q.create_index({
    "name": name,
    "source": q.collection(collection),
    "values": values,
    "terms": terms,
  }))

def createIndexes(client):
    terms = []
    values = []

    # /political_groups #
    values = createFaunaFieldsArray(['group'])
    createFaunaIndex(client, 'elected_members_group', 'elected_members', values)

    # /elected_members #
    values = createFaunaFieldsArray(['name', 'job', 'group', 'department'])
    createFaunaIndex(client, 'all_elected_members_name_job_group_department', 'elected_members', values)

    # /elected_member #
    values = [{'field': ['ref']}]
    terms = createFaunaFieldsArray(['name'])
    createFaunaIndex(client, 'elected_member_ref_by_name', 'elected_members', values, terms)

    # /dates #
    values = createFaunaFieldsArray(['date', 'link'])
    createFaunaIndex(client, 'all_dates_links', 'dates', values)

    # /votes/context #
    values = createFaunaFieldsArray(['date', 'assembly', 'number'])
    createFaunaIndex(client, 'votes_date_assembly_number', 'votes', values)

    # /votes #
    values = createFaunaFieldsArray(['vote_1'])
    terms = createFaunaFieldsArray(['job'])
    createFaunaIndex(client, 'elected_members_vote_1_by_job', 'elected_members', values, terms)

    values = createFaunaFieldsArray(['vote_2'])
    terms = createFaunaFieldsArray(['job'])
    createFaunaIndex(client, 'elected_members_vote_2_by_job', 'elected_members', values, terms)

    values = createFaunaFieldsArray(['vote_1'])
    terms = createFaunaFieldsArray(['job', 'group'])
    createFaunaIndex(client, 'elected_members_vote_1_by_job_group', 'elected_members', values, terms)

    values = createFaunaFieldsArray(['vote_2'])
    terms = createFaunaFieldsArray(['job', 'group'])
    createFaunaIndex(client, 'elected_members_vote_2_by_job_group', 'elected_members', values, terms)