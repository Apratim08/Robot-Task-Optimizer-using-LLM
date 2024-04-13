import networkx as nx
import matplotlib.pyplot as plt

action_chain1 = [
    {"Goto": {"Parameter": "table3", "items": []}},
    {"Pick": {"Parameter": "red_box", "items": ["red_box"]}},
    {"Goto": {"Parameter": " table2", "items": ["red_box"]}},
    {"Place": {"Parameter": "red_box", "items": []}},
    {"Done": {"Parameter": "", "items": []}},
]
action_chain2 = [
    {"Goto": {"Parameter": "table1", "items": []}},
    {"Pick": {"Parameter": "coffee", "items": ["coffee"]}},
    {"Goto": {"Parameter": "table3", "items": ["coffee"]}},
    {"Place": {"Parameter": "coffee", "items": []}},
    {"Done": {"Parameter": "", "items": []}},
]
action_chain3 = [
    {"Goto": {"Parameter": "table2", "items": []}},
    {"Pick": {"Parameter": "green_box", "items": ["green_box"]}},
    {"Goto": {"Parameter": "table4", "items": ["green_box"]}},
    {"Place": {"Parameter": "green_box", "items": []}},
    {"Done": {"Parameter": "", "items": []}},
]

whole_action_chain = [action_chain1 + action_chain2 + action_chain3]

g = nx.DiGraph()
action_list = []

previous_node = None
subg = nx.DiGraph()
for chain in whole_action_chain[0]:
    for key, value in chain.items():
        if key == "Done":
            g = nx.compose(g, subg)
            nx.draw_networkx(subg)
            plt.show()
            subg = nx.DiGraph()
            continue

        name = key + "_" + value["Parameter"]
        if len(value["items"]) != 0:
            name += "_" + value["items"][0]  # TODO hard code

        if previous_node:
            subg.add_edge(previous_node, name)
        previous_node = name


print(action_list)
# nx.draw_networkx(g)
# plt.show()


G = nx.Graph([(0, 1, {"weight": 2.0}), (3, 0, {"weight": 100.0})])
H = nx.Graph([(0, 1, {"weight": 10.0}), (1, 2, {"weight": -1.0})])
nx.set_node_attributes(G, {0: "dark", 1: "light", 3: "black"}, name="color")
nx.set_node_attributes(H, {0: "green", 1: "orange", 2: "yellow"}, name="color")
GcomposeH = nx.compose(G, H)

# nx.draw_networkx(GcomposeH)
# plt.show()
print(GcomposeH.edges)
