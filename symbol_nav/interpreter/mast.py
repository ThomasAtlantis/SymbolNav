from typing import Union


class ASTNode:

    def __init__(self, node_type: str, **kwargs):
        self.node_type = node_type
        self.attributes = kwargs
    
    def __repr__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in self.attributes.items() if v is not None)
        return f"{self.node_type}({attrs})"
    
def to_dict(node: Union[ASTNode, list, str, None], recursive: bool = False):
    if isinstance(node, ASTNode):
        result = {'type': node.node_type, **node.attributes}
        if recursive:
            for key, value in node.attributes.items():
                result[key] = to_dict(value, recursive=True)
        return result
    elif isinstance(node, list):
        return [to_dict(item, recursive=recursive) for item in node]
    else:
        return node
