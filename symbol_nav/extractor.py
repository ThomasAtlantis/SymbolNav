from functools import partial
from typing import Dict, Generator, List, Optional, Tuple
from .interpreter.mast import ASTNode
from pylatexenc.latexwalker import LatexMathNode, LatexNode, LatexWalker, LatexEnvironmentNode, LatexGroupNode, ParsingState


class Extractor:

    def extract_symbol(self, ast: ASTNode) -> Generator[ASTNode]:
        """Traverse the AST to collect all SymbolPostfix nodes."""
        if isinstance(ast, ASTNode) and ast.node_type == 'SymbolPostfix':
            symbol = ast.attributes['symbol']
            if symbol is None: return
            if symbol.node_type == 'Symbol' and symbol.attributes['symbol_type'] not in ['greek', 'letter']:
                return
            yield ast
        elif isinstance(ast, ASTNode):
            for key, value in ast.attributes.items():
                yield from self.extract_symbol(value)

    def extract_document(self, latex: str) -> Optional[LatexEnvironmentNode]:
        walker = LatexWalker(latex)
        node_list, *_ = walker.get_latex_nodes()
        for node in node_list:
            if node.isNodeType(LatexEnvironmentNode):
                return node
        return None

    def extract_latex_math(self, latex: Optional[LatexEnvironmentNode]) -> List[Tuple[int, str]]:
        if latex is None:
            return []
        latex_math_list: List[Tuple[int, str]] = []
        math_nodes: Dict[int, LatexNode] = {}
        parent_node_map: Dict[int, LatexNode] = {}

        def _extract_latex_math(node: LatexNode):
            if hasattr(node, 'nodelist') and len(node.nodelist) > 0:  # type: ignore
                for child in node.nodelist:  # type: ignore
                    parent_node_map[child.pos] = node
                    _extract_latex_math(child)
            else:
                assert isinstance(node.parsing_state, ParsingState)
                if node.parsing_state.in_math_mode:
                    node_p = node
                    while (
                        node_p.pos in parent_node_map
                        and isinstance(node_p.parsing_state, ParsingState)
                        and node_p.parsing_state.in_math_mode
                    ):
                        node_p = parent_node_map[node_p.pos]
                    if node_p is not None and isinstance(node_p.pos, int):
                        math_nodes[node_p.pos] = node_p

        def filter_func(x, delimiter):
            if delimiter in x.latex_verbatim():
                return False
            if r'\label' in x.latex_verbatim():
                return False
            return True

        _extract_latex_math(latex)

        for math_node in math_nodes.values():
            if not isinstance(math_node, LatexMathNode):
                continue
            children = math_node.nodelist
            delimiter = children[0].parsing_state.math_mode_delimiter
            children = filter(
                partial(filter_func, delimiter=delimiter), children)
            math_latex = ''.join(child.latex_verbatim() for child in children)
            latex_math_list.append((math_node.pos, math_latex))  # type: ignore
        return latex_math_list
