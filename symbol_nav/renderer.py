from .interpreter.mast import ASTNode

class Renderer:

    def to_latex(self, node: ASTNode) -> str:
        return self._render_to_latex(node)

    def _render_to_latex(self, node: ASTNode | str | list | None) -> str:
        if isinstance(node, ASTNode):
            match node.node_type:
                case 'SymbolPostfix':
                    return (f"{self._render_to_latex(node.attributes['symbol'])}"
                            f"{self._render_to_latex(node.attributes['postfix'])}")
                case 'Format':
                    return (f"{node.attributes['format']}"
                            "{"
                            f"{self._render_to_latex(node.attributes['content'])}"
                            "}")
                case 'Relation':
                    return (f"{self._render_to_latex(node.attributes['left'])}"
                            f"{node.attributes['op']}"
                            f"{self._render_to_latex(node.attributes['right'])}")
                case 'Additive':
                    return (f"{self._render_to_latex(node.attributes['left'])}"
                            f"{node.attributes['op']}"
                            f"{self._render_to_latex(node.attributes['right'])}")
                case 'Supscript':
                    return ("^{"
                            f"{self._render_to_latex(node.attributes['value'])}"
                            "}")
                case 'MP':
                    return (f"{self._render_to_latex(node.attributes['left'])}"
                            f" {node.attributes['op']} "
                            f"{self._render_to_latex(node.attributes['right'])}")
                case _:
                    raise ValueError(f"Unknown node type: {node.node_type}")
        elif isinstance(node, str):
            return node
        elif isinstance(node, list):
            return "".join(self._render_to_latex(item) for item in node)
        else:
            return ""
        