from interpreter.mast import ASTNode

def render(node: ASTNode | str | list | None):
    if isinstance(node, ASTNode):
        match node.node_type:
            case 'SymbolPostfix':
                return (f"{render(node.attributes['symbol'])}"
                        f"{render(node.attributes['postfix'])}")
            case 'Format':
                return (f"{node.attributes['format']}"
                        "{"
                        f"{render(node.attributes['content'])}"
                        "}")
            case 'Relation':
                return (f"{render(node.attributes['left'])}"
                        f"{node.attributes['op']}"
                        f"{render(node.attributes['right'])}")
            case 'Additive':
                return (f"{render(node.attributes['left'])}"
                        f"{node.attributes['op']}"
                        f"{render(node.attributes['right'])}")
            case 'Supscript':
                return ("^{"
                        f"{render(node.attributes['value'])}"
                        "}")
            case 'MP':
                return (f"{render(node.attributes['left'])}"
                        f" {node.attributes['op']} "
                        f"{render(node.attributes['right'])}")
            case _:
                raise ValueError(f"Unknown node type: {node.node_type}")
    elif isinstance(node, str):
        return node
    elif isinstance(node, list):
        return "".join(render(item) for item in node)
    else:
        return ""
    