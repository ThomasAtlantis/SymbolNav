from .interpreter.mast import ASTNode

class Renderer:

    def to_latex(self, node: ASTNode) -> str:
        return self._render_to_latex(node)

    def _render_to_latex(self, node: ASTNode | str | list | None) -> str:
        if isinstance(node, ASTNode):
            left = self._render_to_latex(node.attributes['left']) if 'left' in node.attributes else None
            right = self._render_to_latex(node.attributes['right']) if 'right' in node.attributes else None
            left_blank = " " if left else ""
            right_blank = " " if right else ""

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
                    return (f"{left}"
                            f"{left_blank}{node.attributes['op']}{right_blank}"
                            f"{right}")
                case 'Additive':
                    return (f"{left}"
                            f"{left_blank}{node.attributes['op']}{right_blank}"
                            f"{right}")
                case 'Supscript':
                    return ("^{"
                            f"{self._render_to_latex(node.attributes['value'])}"
                            "}")
                case 'Subscript':
                    return ("_{"
                            f"{self._render_to_latex(node.attributes['value'])}"
                            "}")
                case 'List':
                    return node.attributes['separator'].join(self._render_to_latex(item) for item in node.attributes['items'])
                case 'MP':
                    return (f"{left}"
                            f"{left_blank}{node.attributes['op']}{right_blank}"
                            f"{right}")
                case 'Bracket':
                    return (f"{node.attributes['bracket_left']}"
                            f"{self._render_to_latex(node.attributes['content'])}"
                            f"{node.attributes['bracket_right']}")
                case _:
                    raise ValueError(f"Unknown node type: {node.node_type}")
        elif isinstance(node, str):
            return node
        elif isinstance(node, list):
            return "".join(self._render_to_latex(item) for item in node)
        else:
            return ""
        