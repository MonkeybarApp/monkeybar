from googlesearch import search
import requests
from bs4 import BeautifulSoup
from .word import get_wordlist_for_url
import copy
import math

class Graph:
    def __init__(self, nodes={}, connections={}, edges={}):
        self.nodes = nodes
        self.connections = connections
        self.edges = edges

    def _hash_node(self, node):
        node_hash = hash(node)
        self.nodes[node_hash] = node
        return node_hash

    def _hash_edge(self, a, b):
        if a > b:
            a, b = b, a
        return hash((a, b))

    def _create_node(self, node_hash):
        if node_hash not in self.connections:
            self.connections[node_hash] = set()

    def _create_edge(self, edge_hash):
        if edge_hash not in self.edges:
            self.edges[edge_hash] = 0

    def node_edges(self, node, min_weight=0):
        node_hash = self._hash_node(node)

        if node_hash not in self.connections:
            return []

        return [self.nodes[i] for i in self.connections[node_hash] if self.edge_weight(node, self.nodes[i]) > min_weight]

    def edge_weight(self, a, b):
        edge_hash = self._hash_edge(a, b)
        if edge_hash not in self.edges:
            print((a, b))
        return self.edges[edge_hash]

    def connect(self, a, b, weight):
        node_a_hash = self._hash_node(a)
        node_b_hash = self._hash_node(b)
        edge_hash = self._hash_edge(a, b)

        self._create_edge(edge_hash)
        self.edges[edge_hash] += weight

        self._create_node(node_a_hash)
        self._create_node(node_b_hash)
        self.connections[node_a_hash].add(node_b_hash)
        self.connections[node_b_hash].add(node_a_hash)
    
def get_graph_for_phrase(phrase):
    graph = Graph()

    num_urls = 10

    for url in search(phrase, stop=num_urls):
        wordlist = get_wordlist_for_url(url)

        for i in range(0, len(wordlist)):
            for j in range(i+1, len(wordlist)):
                graph.connect(wordlist[i], wordlist[j], 1)

    threshold = num_urls // 2.2
    queue = phrase.lower().split(' ')
    visited = set()
    edges = set()

    while len(queue) > 0:
        current_node = queue.pop(0)
        if current_node in visited:
            continue
        visited.add(current_node)

        node_edges = graph.node_edges(current_node, threshold)

        for i in node_edges:
            edge_weight = graph.edge_weight(current_node, i) 

            a = copy.copy(current_node)
            b = copy.copy(i)
            if a > b: a, b = b, a
            edges.add((a, b, edge_weight))

            queue.append(i)

    return visited, edges
