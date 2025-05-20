import json

def vis_tree(parsed_chunks):
    ##Initiating nodes and edges variables
    nodes = []
    edges = []
    node_id = 0

    ## Method to add node to tree
    def add_node(label):
        nonlocal node_id
        nodes.append({"id": node_id, "label": label})
        current_id = node_id
        node_id += 1
        return current_id

    def process_chunk(label, tokens):
        parent_id = add_node(label)

        ##For loop to add nodes to edges
        for word, tag in tokens:
            tag_id = add_node(tag)
            word_id = add_node(word)
            edges.append({"from": parent_id, "to": tag_id})
            edges.append({"from": tag_id, "to": word_id})
        return parent_id

    ##Special case for the root node
    root_id = add_node("S")  
    for label, tokens in parsed_chunks:
        subtree_id = process_chunk(label, tokens)
        edges.append({"from": root_id, "to": subtree_id})

    return json.dumps({"nodes": nodes, "edges": edges})

# Example usage
if __name__ == "__main__":
    sample = [
        ("NP", [("The", "DT"), ("cat", "NN")]),
        ("VP", [("plays", "VBZ"), ("piano", "NN")])
    ]
    vis_json = vis_tree(sample)
    print(vis_json)
