"""A utility module for knowledge graph visualization
"""
import networkx as nx
import matplotlib.pyplot as plt


def get_graph_plot(df):
    G = nx.from_pandas_edgelist(
        df, "subject", "object", edge_attr=True, create_using=nx.MultiDiGraph()
    )
    edge_labels = dict(
        [((x, y), z) for x, y, z in zip(df.subject, df.object, df.relation)]
    )

    # plt.figure(figsize=(10, 10))

    pos = nx.spring_layout(G)
    nx.draw(
        G,
        with_labels=True,
        node_color="skyblue",
        edge_cmap=plt.cm.Blues,
        pos=pos,
    )
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    return plt
