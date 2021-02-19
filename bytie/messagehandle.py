import ast


def bytie_handle_hey_bytie() -> str:
    return "Yes, sir!"


def bytie_handle_ast(command: str) -> str:
    parsed = ast.parse(command)
    tree = ast.dump(parsed)
    return tree


def bytie_handle_latex(command: str) -> str:
    return "https://latex.codecogs.com/gif.latex?" + command
