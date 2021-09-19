# monkeybar

## About

Monkeybar is a data visualization platform that can gather and graph a collection of relevant keywords for any high-level concept that has a Wikipedia page. It queries text data from the main page as well as a number of related pages to construct an undirected graph based on connections between individual tokens. Then, the graph data is presented to the user with nodes representing tokens and edges representing relatedness of the tokens.

## Getting Started

You must have Python 3.6 or higher to run this project. The following are instructions to host the application locally.

1. Clone this repository.
```bash
git clone https://github.com/MonkeybarApp/monkeybar && cd monkeybar
```
2. Set up a virtual environment (optional).
```bash
python3 -m venv . && ./bin/activate
```
3. Install the required dependencies.
```bash
pip3 install -r requirements.txt
```
4. Run the application in debug mode.
```bash
python3 app.py
```

## Usage

On the main page, simply type your query in the search bar and click the submit button. If you want to query multiple things at once on the same graph, you can separate them using commas. It is common to have to wait a decent amount of time before getting search results.

The search results page contain another search bar (usage is same as above) as well as the graph of what you queried. On the graph, the size of the nodes represent the node's degree (i.e. how many nodes are connected). The thickness of the edges represent how strong the relationship is between the two nodes. If you click on a node, you will be redirected to a page with the node's term appended with the current query.
