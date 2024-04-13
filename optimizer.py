import numpy as np
from action_link import ActionLink
import sys
import itertools
import copy


def adjacancyMatrixGeneration(actions, sub_tasks_dependence,merge):
    action_list = []
    action_lens = []
    for task_action in actions:
        action_list += task_action
        action_lens.append(len(task_action))

    nodes_name = np.array(["start"] + action_list)
    # done_counter = 0
    # for i in range(len(nodes_name)):
    #     if nodes_name[i] == "Done":
    #         nodes_name[i] +=str(done_counter)
    #         done_counter+=1

    incremental_action_lens = [0]
    for i in action_lens:
        incremental_action_lens.append(max(incremental_action_lens) + i)
    incremental_action_lens = incremental_action_lens[1:]

    sub_tasks_dependence_action_index = [
        incremental_action_lens[x - 1] for x in sub_tasks_dependence.keys()
    ]
    #
    if merge:
        sub_tasks_dependence_action_index = [
            incremental_action_lens[x - 1] for x in [1]
        ]


    matrix_size = incremental_action_lens[-1] + 1
    adjacent_matrix = np.zeros((matrix_size, matrix_size))
    for i in incremental_action_lens[:-1]:
        if i not in sub_tasks_dependence_action_index:
            adjacent_matrix[0][i + 1] = 1
    adjacent_matrix[0][1] = 1

    counter = 1
    for i in action_lens:
        diag_matrix = np.diag([1] * i)
        shifted_matrix = np.zeros((diag_matrix.shape[0], diag_matrix.shape[1] + 1))
        shifted_matrix[:, 1:] = diag_matrix
        shifted_matrix = shifted_matrix[:, :-1]
        shifted_matrix[shifted_matrix == 0] = 0
        # print(shifted_matrix)
        adjacent_matrix[counter : i + counter, counter : i + counter] = shifted_matrix
        counter += i

    # print(adjacent_matrix)

    for i in range(len(incremental_action_lens) - 1):
        for action_index in range(
            incremental_action_lens[i], incremental_action_lens[i + 1]
        ):
            select_action = action_list[action_index]

            for candidate_action_index in range(0, incremental_action_lens[i]):
                candidate_action = action_list[candidate_action_index]
                paired_result = int(ActionLink(select_action, candidate_action)[0])
                paired_result_inverse = int(
                    ActionLink(candidate_action, select_action)[0]
                )
                # if paired_result:
                #     print(select_action)
                #     print(candidate_action)
                #     print("-" * 10)
                # if paired_result_inverse:
                #     print(candidate_action)
                #     print(select_action)
                #     print("*" * 10)

                adjacent_matrix[action_index + 1][
                    candidate_action_index + 1
                ] = paired_result
                adjacent_matrix[candidate_action_index + 1][
                    action_index + 1
                ] = paired_result_inverse
    vis = False
    if vis:
        # print(adjacent_matrix)

        locations = np.where(adjacent_matrix == 1)
        start_nodes = nodes_name[locations[0]]
        end_nodes = nodes_name[locations[1]]

        start_nodes = [
            str(list(x.keys())[0]) + " " + str(list(x.values())[0]["Parameter"])
            if x != "start"
            else x
            for x in start_nodes
        ]
        end_nodes = [
            str(list(x.keys())[0]) + " " + str(list(x.values())[0]["Parameter"])
            if x != "start"
            else x
            for x in end_nodes
        ]
        nodes_pair = list(zip(start_nodes, end_nodes))
        print(nodes_pair)

        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()
        G.add_edges_from(nodes_pair)
        nx.draw_networkx(G)
        plt.show()
    return {"graph": adjacent_matrix, "action_names": nodes_name}


class Graph:
    def __init__(self, node_name):
        self.node_name = node_name
        self.V = len(node_name)
        self.graph = [[0 for column in range(self.V)] for row in range(self.V)]
        self.pre = {}

    def printSolution(self, src, dist):
        print(f'Vertex \tDistance from Source "{self.node_name[src]}"')
        for node in range(self.V):
            print(self.node_name[node], "\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
        # Initialize minimum distance for next node
        min = sys.maxsize
        # min_index = sys.maxsize
        # Search not nearest vertex not in the
        # shortest path tree
        min_index = sys.maxsize
        for u in range(self.V):
            if dist[u] < min and sptSet[u] == False:
                min = dist[u]
                min_index = u

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
        self.pre = {}
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # x is always equal to src in first iteration
            x = self.minDistance(dist, sptSet)
            if x == sys.maxsize:
                continue

            # Put the minimum distance vertex in the
            # shortest path tree
            # if x != sys.maxsize:
            sptSet[x] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for y in range(self.V):
                if (
                    self.graph[x][y] > 0
                    and sptSet[y] == False
                    and dist[y] > dist[x] + self.graph[x][y]
                ):
                    self.pre[y] = x
                    dist[y] = dist[x] + self.graph[x][y]

        return dist, copy.deepcopy(self.pre)


def Optimizer(actions, sub_tasks_dependence,merge=False):
    result = adjacancyMatrixGeneration(actions, sub_tasks_dependence,merge)
    action_names = result["action_names"]
    g = Graph(result["action_names"])
    g.graph = result["graph"]
    # sub_tasks_without_done = [x - 1 for x in sub_tasks_dependence]
    sub_tasks_without_done = [
        x
        for x in sub_tasks_dependence.values()
        if x not in list(sub_tasks_dependence.keys())
    ]
    action_mustpass_points = [0]
    count = 0
    for i, subtaks_actions in enumerate(actions):
        count += len(subtaks_actions)
        if i not in sub_tasks_without_done:
            action_mustpass_points.append(count)
    target_points = {}
    traces = {}
    for action_idx in action_mustpass_points:
        target_point_dist, track = g.dijkstra(action_idx)
        traces[action_idx] = track
        tmp_points = [x for x in action_mustpass_points if x != action_idx]
        related_dist = {}
        for x in tmp_points:
            related_dist[x] = target_point_dist[x]
        target_points[action_idx] = related_dist
    #     print(traces)
    # print(target_points)
    min_distance = sys.maxsize
    min_visiting_sequence = None
    for path in itertools.permutations(action_mustpass_points):
        dist = 0
        # print(path)
        for idx in range(len(action_mustpass_points) - 1):
            dist += target_points[path[idx]][path[idx + 1]]
        if dist < min_distance:
            min_distance = dist
            min_visiting_sequence = path

    # print(min_visiting_sequence)
    # print(traces)
    final_actions = [0]
    for i in range(len(min_visiting_sequence) - 1):
        startnode = min_visiting_sequence[i]
        endnode = min_visiting_sequence[i + 1]
        cur_action = [endnode]
        while endnode != startnode:
            endnode = traces[startnode][endnode]
            cur_action.append(endnode)
        cur_action.reverse()
        final_actions += cur_action[1:]
    final_actions = [action_names[x] for x in final_actions]
    # print(final_actions)
    vis = False
    if vis:
        for x in final_actions:
            print(x)
    return final_actions


if __name__ == "__main__":
    action1 = [
        {"Goto": {"Parameter": "table1", "items": "", "environment": "table1"}},
        {"Pick": {"Parameter": "box", "items": "box", "environment": "table1"}},
        {"Goto": {"Parameter": "table2", "items": "box", "environment": "table2"}},
        {"Place": {"Parameter": "box", "items": "", "environment": "table2"}},
        {"Done": {"Parameter": "0", "items": "", "environment": "table2"}},
    ]
    action2 = [
        {"Goto": {"Parameter": "table1", "items": "", "environment": "table1"}},
        {"Pick": {"Parameter": "rubber", "items": "rubber", "environment": "table1"}},
        {"Goto": {"Parameter": "table2", "items": "rubber", "environment": "table2"}},
        {"Place": {"Parameter": "rubber", "items": "", "environment": "table2"}},
        {"Done": {"Parameter": "1", "items": "", "environment": "table2"}},
    ]
    action3 = [
        {"Goto": {"Parameter": "table2", "items": "", "environment": "table2"}},
        {"Pick": {"Parameter": "pencil", "items": "pencil", "environment": "table2"}},
        {"Goto": {"Parameter": "table1", "items": "pencil", "environment": "table1"}},
        {"Place": {"Parameter": "pencil", "items": "", "environment": "table1"}},
        {"Done": {"Parameter": "2", "items": "", "environment": "table1"}},
    ]
    actions = [action1, action2, action3]  # input
    Optimizer(actions)
    # result = adjacancyMatrixGeneration(actions)
    # print(result["graph"])
    # action_names = result["action_names"]
    # g = Graph(result["action_names"])
    # g.graph = result["graph"]

    # action_mustpass_points = [0]
    # for subtaks_actions in actions:
    #     action_mustpass_points.append(
    #         max(action_mustpass_points) + len(subtaks_actions)
    #     )
    # target_points = {}
    # traces = {}
    # for action_idx in action_mustpass_points:
    #     target_point_dist, track = g.dijkstra(action_idx)
    #     traces[action_idx] = track
    #     tmp_points = [x for x in action_mustpass_points if x != action_idx]
    #     related_dist = {}
    #     for x in tmp_points:
    #         related_dist[x] = target_point_dist[x]
    #     target_points[action_idx] = related_dist
    #     print(traces)
    # print(target_points)
    # min_distance = sys.maxsize
    # min_visiting_sequence = None
    # for path in itertools.permutations(action_mustpass_points):
    #     dist = 0
    #     # print(path)
    #     for idx in range(len(action_mustpass_points) - 1):
    #         dist += target_points[path[idx]][path[idx + 1]]
    #     if dist < min_distance:
    #         min_distance = dist
    #         min_visiting_sequence = path

    # print(min_visiting_sequence)
    # print(traces)
    # final_actions = [0]
    # for i in range(len(min_visiting_sequence) - 1):
    #     startnode = min_visiting_sequence[i]
    #     endnode = min_visiting_sequence[i + 1]
    #     cur_action = [endnode]
    #     while endnode != startnode:
    #         endnode = traces[startnode][endnode]
    #         cur_action.append(endnode)
    #     cur_action.reverse()
    #     final_actions += cur_action[1:]
    # final_actions = [action_names[x] for x in final_actions]
    # print(final_actions)
    # for x in final_actions:
    #     print(x)
