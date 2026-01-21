from itertools import zip_longest
from typing import Union

# class HashableASTNode:

#     def __init__(self, node: ASTNode):
#         self.node_type = node.node_type
#         self.attributes = node.attributes
#         for key, value in self.attributes.items():
#             if isinstance(value, ASTNode):
#                 self.attributes[key] = HashableASTNode(value)
#             elif isinstance(value, (frozenset, tuple, list)):
#                 self.attributes[key] = type(value)(HashableASTNode(item) for item in value)

#     def __repr__(self):
#         attrs = ', '.join(f"{k}={v}" for k, v in self.attributes.items() if v is not None)
#         return f"{self.node_type}({attrs})"
    
#     def __hash__(self) -> int:
#         # Convert attributes to a hashable tuple
#         # Sort items by key for consistency
#         attrs_tuple = tuple(sorted(
#             (k, hash(v)) 
#             for k, v in self.attributes.items()
#         ))
#         return hash((self.node_type, attrs_tuple))
    
#     def __eq__(self, other: 'HashableASTNode') -> bool:
#         if not isinstance(other, HashableASTNode):
#             return False
#         return self.node_type == other.node_type and self.attributes == other.attributes
    
#     def __lt__(self, other: 'HashableASTNode') -> bool:
#         if not isinstance(other, HashableASTNode):
#             raise TypeError(f"Cannot compare HashableASTNode with {type(other)}")
#         if self.node_type != other.node_type:
#             return self.node_type < other.node_type
#         if self.node_type in ['SymbolPostfix', 'GeneralPostfix']:
#             keyword = 'symbol' if self.node_type == 'SymbolPostfix' else 'content'
#             if self.attributes[keyword] != other.attributes[keyword]:
#                 return self.attributes[keyword] < other.attributes[keyword]
#             if len(self.attributes['postfix']) != len(other.attributes['postfix']):
#                 return len(self.attributes['postfix']) < len(other.attributes['postfix'])
#             sorted_postfix_s = sorted(self.attributes['postfix'], key=lambda x: x.node_type)
#             sorted_postfix_o = sorted(other.attributes['postfix'], key=lambda x: x.node_type)
#             for postfix_s, postfix_o in zip(sorted_postfix_s, sorted_postfix_o):
#                 if type(postfix_s) != type(postfix_o):
#                     return Renderer.to_latex(postfix_s) < Renderer.to_latex(postfix_o)
#                 if postfix_s != postfix_o:
#                     return postfix_s < postfix_o
#             return False
#         else:
#             for key in self.attributes.keys():
#                 if type(self.attributes[key]) != type(other.attributes[key]):
#                     return Renderer.to_latex(self.attributes[key]) < Renderer.to_latex(other.attributes[key])
#                 if self.attributes[key] != other.attributes[key]:
#                     return self.attributes[key] < other.attributes[key]
#             return False


class ASTNode:

    def __init__(self, node_type: str, **kwargs):
        self.node_type = node_type
        self.attributes = kwargs
    
    def __repr__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in self.attributes.items() if v is not None)
        return f"{self.node_type}({attrs})"

    def __hash__(self) -> int:
        # Convert attributes to a hashable tuple
        # Sort items by key for consistency
        attrs_tuple = tuple(sorted(
            (k, hash(v)) 
            for k, v in self.attributes.items()
        ))
        return hash((self.node_type, attrs_tuple))
    
    def __eq__(self, other: 'ASTNode') -> bool:
        if not isinstance(other, ASTNode):
            return False
        return self.node_type == other.node_type and self.attributes == other.attributes
    
    def __lt__(self, other: 'ASTNode') -> bool:
        if not isinstance(other, ASTNode):
            raise TypeError(f"Cannot compare ASTNode with {type(other)}")
        if self.node_type != other.node_type:
            return self.node_type < other.node_type
        if self.node_type in ['SymbolPostfix', 'GeneralPostfix']:
            keyword = 'symbol' if self.node_type == 'SymbolPostfix' else 'content'
            if self.attributes[keyword] != other.attributes[keyword]:
                return self.attributes[keyword] < other.attributes[keyword]
            # if len(self.attributes['postfix']) != len(other.attributes['postfix']):
            #     return len(self.attributes['postfix']) < len(other.attributes['postfix'])
            sorted_postfix_s = sorted(self.attributes['postfix'], key=lambda x: x.node_type, reverse=True)
            sorted_postfix_o = sorted(other.attributes['postfix'], key=lambda x: x.node_type, reverse=True)
            for postfix_s, postfix_o in zip_longest(sorted_postfix_s, sorted_postfix_o):
                if postfix_s is None:
                    return True
                if postfix_o is None:
                    return False
                if type(postfix_s) != type(postfix_o):
                    return postfix_s.__repr__() < postfix_o.__repr__()
                if postfix_s != postfix_o:
                    return postfix_s < postfix_o
            return False
        else:
            for key in self.attributes.keys():
                if type(self.attributes[key]) != type(other.attributes[key]):
                    return self.attributes[key].__repr__() < other.attributes[key].__repr__()
                if self.attributes[key] != other.attributes[key]:
                    return self.attributes[key] < other.attributes[key]
            return False
    
def to_dict(node: Union[ASTNode, list, str, None], recursive: bool = False):
    if isinstance(node, ASTNode):
        result = {'type': node.node_type}
        for key, value in node.attributes.items():
            if value is not None:
                result[key] = value
        if recursive:
            for key, value in node.attributes.items():
                result[key] = to_dict(value, recursive=True)
        return result
    elif isinstance(node, list):
        return [to_dict(item, recursive=recursive) for item in node]
    else:
        return node
