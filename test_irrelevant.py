import networkx as nx

T = nx.DiGraph([(2,1), (3,1), (4,1), (5,2)])

tweet_author = {1:"A", 2:"B", 3:"C", 4:"D", 5:"A"}

aggregated_labels = {1:"L1", 2:"L2", 3:"L3", 4:"L2", 5:"L1"}

relevant_network_array = [T]

### Here we have an assumption that there is no possibility of isolated set of nodes because in the previous step (conversation building) we construct conneceted graphs with minimum of two messages

conversation_viewpoint = {}
viewpoint_networks = []
multi_graph_key_holder = {}
viewpoint_network_to_graph_id = {}
graph_id_to_viewpoint_network = {}
node_collection = {}

conversation_network_to_graph_id = {}
graph_id_to_conversation_network = {}
binary_user_conversations = 0

index = 0

for graph_id, G in enumerate(relevant_network_array):
    U = nx.MultiDiGraph()
    N = nx.Graph()
    multi_graph_key_holder[graph_id] = {}

    for n, d in dict(G.out_degree).items():
        if d == 0:
            root = n
            break

    N.add_node(tweet_author[root])

    iterations = [root]
    for node in iterations:

        N.add_node(tweet_author[node])

        source = tweet_author[node]
        neighbours = [i for i in nx.Graph.neighbors(G.reverse(), node)]
        iterations += neighbours

        seen = [tweet_author[i] for i in nx.Graph.neighbors(G, node)]

        if (source, source, aggregated_labels[node]) in multi_graph_key_holder[graph_id].keys():
            U.edges[(source, source, multi_graph_key_holder[graph_id][(source, source, aggregated_labels[node])])]["weight"] += 1
        else:
            multi_graph_key_holder[graph_id][(source, source, aggregated_labels[node])] = index
            U.add_edge(source, source, key=index, kind=aggregated_labels[node], weight=1)
            index += 1


        for neighbour in neighbours:

            N.add_node(tweet_author[neighbour])

            destination = tweet_author[neighbour]

            if source == destination:
                pass
            elif destination in seen:
                if (destination, source, aggregated_labels[neighbour]) in multi_graph_key_holder[graph_id].keys():
                    U.edges[(destination, source,
                             multi_graph_key_holder[graph_id][(destination, source, aggregated_labels[neighbour])])][
                        "weight"] += 1
                else:
                    multi_graph_key_holder[graph_id][(destination, source, aggregated_labels[neighbour])] = index
                    U.add_edge(destination, source, key=index, kind=aggregated_labels[neighbour], weight=1)
                    index += 1

            else:
                if (source, destination, aggregated_labels[node]) in multi_graph_key_holder[graph_id].keys():
                    U.edges[(source, destination,
                             multi_graph_key_holder[graph_id][(source, destination, aggregated_labels[node])])][
                        "weight"] += 1
                else:
                    multi_graph_key_holder[graph_id][(source, destination, aggregated_labels[node])] = index
                    U.add_edge(source, destination, key=index, kind=aggregated_labels[node], weight=1)
                    index += 1

                if (destination, source, aggregated_labels[neighbour]) in multi_graph_key_holder[graph_id].keys():
                    U.edges[(destination, source,
                             multi_graph_key_holder[graph_id][(destination, source, aggregated_labels[neighbour])])][
                        "weight"] += 1
                else:
                    multi_graph_key_holder[graph_id][(destination, source, aggregated_labels[neighbour])] = index
                    U.add_edge(destination, source, key=index, kind=aggregated_labels[neighbour], weight=1)
                    index += 1

    # We don't add conversations threads (conversations created by just one user)
    if len(U.nodes) > 1:
        viewpoint_networks.append(U)
        viewpoint_network_to_graph_id[U] = graph_id
        graph_id_to_viewpoint_network[graph_id] = U
        conversation_viewpoint[G] = U

        conversation_network_to_graph_id[G] = graph_id
        graph_id_to_conversation_network[graph_id] = G
    node_collection[graph_id] = N

    if len(U.nodes) == 1:
        print(U.nodes)
        print(U.edges)

    if len(U.nodes) == 2:
        binary_user_conversations += 1