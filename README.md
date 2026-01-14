# SymbolNav

SymbolNav is an extractor/navigator for math symbols defined in LaTeX.

## TODO

Ongoing work: A LaTeX math expression parser implemented using PLY (Python Lex-Yacc) library that parses LaTeX mathematical formulas into an AST (Abstract Syntax Tree).

- [] basic logic of symbol collection
- [] hash function to help remove duplicates
- [] rendering symbols back into standard latex
- [] CLI-based result displaying

## Features

- Basic arithmetic operators: `+`, `-`, `*`, `/`, `\times`, `\cdot`, `\div`, `:`
- Relational operators: `=`, `<`, `>`, `\leq`, `\geq`, `\in`
- Superscripts and subscripts: `x^2`, `x_i`, `x^{n+1}_{i+1}`
- Formatting commands: `\mathbf`, `\text`, `\mathbb`, `\mathit`
- Text mode support with `\text{...}` command
- Grouping with braces: `{...}`

## Installation

The project requires Python 3.x and PLY (Python Lex-Yacc).

Install dependencies:
```bash
pip install ply
```

## Usage

```python
from symbol_nav.interpreter.interpreter import LaTeXMathInterpreter
from symbol_nav.interpreter.mast import to_dict
import json

# Create parser instance
interpreter = LaTeXMathInterpreter()

# Parse LaTeX expression
latex = r'x^2 + y^2'
ast = interpreter.parse(latex)

# Convert AST to dictionary
ast_dict = to_dict(ast, recursive=True)
print(json.dumps(ast_dict, indent=2))
```

## AST Node Types

The parser generates AST nodes with the following types:

- `Relation`: Relational expressions (e.g., `x = y`, `x \leq y`, `x \in A`)
- `Additive`: Addition and subtraction operations (e.g., `x + y`, `x - y`)
- `MP`: Multiplication and division operations (e.g., `x * y`, `x \times y`, `x / y`, `x \div y`, `x : y`)
- `Unary`: Unary operators (`+`, `-`)
- `SymbolPostfix`: Symbols with postfix operations (subscripts/superscripts)
- `Supscript`: Superscript expressions (e.g., `x^2`)
- `Subscript`: Subscript expressions (e.g., `x_i`)
- `Format`: Formatted content (e.g., `\mathbf{H}`, `\mathbb{R}`, `\text{in}`)

## Examples

### Simple Expression
```python
latex = r'x + y'
# AST: Additive(op='+', left=..., right=...)
```

### Superscripts and Subscripts
```python
latex = r'x^2 + y_i'
# AST includes Supscript and Subscript nodes
```

### Formatting Commands
```python
latex = r'\mathbf{H}^\text{out} \in \mathbb{R}^{N \times d}'
# AST includes Format nodes with different formatting types
```

### Relational Expressions
```python
latex = r'x \leq y + 1'
# AST: Relation(op='\\leq', left=..., right=...)
```

## Project Structure

The `symbol_nav` package contains:

- `interpreter/interpreter.py`: Main parser class `LaTeXMathInterpreter`
- `interpreter/lexer.py`: Lexical analyzer (tokenizer)
- `interpreter/parser.py`: Syntax parser (grammar rules)
- `interpreter/mast.py`: AST node definition (`ASTNode` class and `to_dict` function)
- `interpreter/exceptions.py`: Custom exception classes (`MathSyntaxError`)

## Error Handling

The parser raises `MathSyntaxError` exceptions for syntax errors, which include:
- Error message
- Token information
- Cursor position indicator

```python
from symbol_nav.interpreter.exceptions import MathSyntaxError

try:
    ast = interpreter.parse(latex)
except MathSyntaxError as e:
    print(f"Syntax error: {e}")
    print(f"Position: {e.cursor}")
```

## Limitations

The current version has limited support for certain complex LaTeX syntax:
- Some LaTeX commands may not be fully supported
- Complex nested expressions may require grammar rule adjustments
- Certain LaTeX command parameter parsing may need special handling

## Dependencies

- Python 3.x
- PLY (Python Lex-Yacc)
