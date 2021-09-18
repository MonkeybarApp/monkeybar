import wikipedia
import requests
from bs4 import BeautifulSoup
from .word import get_wordlist_for_article
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

        return [(self.nodes[i], self.edge_weight(node, self.nodes[i])) for i in self.connections[node_hash] if self.edge_weight(node, self.nodes[i]) > min_weight]

    def edge_weight(self, a, b):
        edge_hash = self._hash_edge(a, b)
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

    for article in wikipedia.search(phrase, results=20):
        wordlist = get_wordlist_for_article(article)

        for i in range(0, len(wordlist)):
            for j in range(i+1, min(i+31, len(wordlist))):
                if wordlist[i] != wordlist[j]:
                    graph.connect(wordlist[i], wordlist[j], (j-i)/len(wordlist))

    threshold = 0
    queue = phrase.lower().split(' ')
    visited = set()
    edges = set()

    while len(queue) > 0:
        current_node = queue.pop(0)
        if current_node in visited:
            continue
        visited.add(current_node)

        node_edges = graph.node_edges(current_node, threshold)
        node_edges.sort(key=lambda x:x[1])
        node_edges.reverse()

        if len(node_edges) > 5:
            node_edges = node_edges[:5]

        for i in node_edges:
            a = copy.copy(current_node)
            b = copy.copy(i[0])
            if a > b: a, b = b, a
            edges.add((a, b, i[1]))

            queue.append(i[0])

    return visited, edges
