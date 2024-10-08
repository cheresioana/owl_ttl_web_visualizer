import json
from typing import List, Union, Dict, Any


class Node:
    intra_id: int
    statement: str
    tag: str
    id: int
    community: int
    n: Dict[str, Union[str, int]] = None
    degree: int = None

    def __init__(self, intra_id: int, statement: str, id: int, tag: str = '', community: int = 0,
                 n: Dict[str, Union[str, int]] = None, degree: int = None):
        self.intra_id = intra_id
        self.statement = statement
        self.tag = tag
        self.id = id
        self.community = community
        if n:
            self.n = n
        if degree:
            self.degree = degree

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.intra_id == other.intra_id
        return False

    def __hash__(self):
        return hash(self.intra_id)

class FakeStatement:
    def __init__(self, date, intra_id, statement, words, url):
        self.type = "Fake_Statement"
        self.date = date
        self.intra_id = intra_id
        self.statement = statement
        self.words = words
        self.id = intra_id
        self.url = url

    def to_dict(self):
        return {
            "type": self.type,
            "date": self.date,
            "intra_id": self.intra_id,
            "statement": self.statement,
            "words": self.words,
            "id": self.id,
            "url": self.url
        }

class SimpleNode:
    def __init__(self, name, type, id):
        self.type = type
        self.name = name
        self.id = id
        self.intra_id = id

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "id": self.id,
            "intra_id": self.intra_id
        }

class BigNode:
    def __init__(self, type, id, connections, node):
        self.id = id
        self.connections = connections
        if type not in ['Fake_Statement', 'Language', 'Channel', 'Country', 'Entity', 'Location', 'Record']:
            raise ValueError(f"Invalid type: {type} for BigNode ")
        self.type = type
        if not isinstance(node, (FakeStatement, SimpleNode)):
            raise TypeError("Node must be an instance of FakeStatement or SimpleNode")
        self.node = node

    def increase_connections(self):
        self.connections = self.connections + 1

    def to_dict(self):
        return {
            "id": self.id,
            "connections": self.connections,
            "type": self.type,
            "node": self.node.to_dict()
        }


class Link:
    target: int
    source: int
    tag: str
    value: int

    def __init__(self, target: int, source: int, tag: str = '', value: int = ''):
        self.target = target
        self.source = source
        self.tag = tag
        self.value = value


class ResultItem:
    weight: int
    intra_id: int
    query_id: int
    statement: str
    selected: int
    nodes: List[Node]
    links: List[Link]
    date: str
    channel: List[str]
    location: List[str]
    url: str

    def __init__(self, weight, intra_id, query_id, statement, nodes, links,
                 selected=0, date="", channel=[], location=[], url=""):
        self.weight = weight
        self.intra_id = intra_id
        self.query_id = query_id
        self.selected = selected
        self.statement = statement
        self.nodes = nodes  # This is the list of Node to reach the  target statement
        self.links = links
        self.date = date
        self.channel = channel
        self.location = location
        self.url = url


class SearchResult:
    intra_id: int
    query_id: int
    statement: str
    selected: int
    date: str
    channel: List[str]
    location: List[str]
    url: str
    languages: List[str]

    def __init__(self, intra_id, query_id, statement,
                 selected=0, date="", channel=[], location=[], url="", languages=[]):
        self.intra_id = intra_id
        self.query_id = query_id
        self.selected = selected
        self.statement = statement
        self.date = date
        self.channel = channel
        self.location = location
        self.url = url
        self.languages = languages

    def toJson(self):
        return self.__dict__


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SearchResult):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Node, Link, ResultItem, SearchResult)):
            return obj.__dict__
        return super(ComplexEncoder, self).default(obj)
