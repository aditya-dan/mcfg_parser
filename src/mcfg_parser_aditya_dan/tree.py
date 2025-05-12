class Tree:
    """
    Parse tree node for MCFG parsing results.

    Attributes
    ----------
    variable : str
        The symbol at this node.
    spans : tuple of tuple of int
        Spans indicating the coverage in the input string.
    children : list of Tree
        Child subtrees.
    """
    def __init__(self, variable: str, spans: tuple[tuple[int, int], ...], children=None):
        self.variable = variable
        self.spans = spans
        self.children = children or []

    def add_child(self, child: 'Tree'):
        """Append a child subtree."""
        self.children.append(child)

    def is_leaf(self) -> bool:
        """Return True if the node is a leaf node."""
        return not self.children

    def yield_string(self, tokens: list[str]) -> str:
        """
        Reconstruct the yield of this subtree from the input tokens.
        """
        segments = []
        for (start, end) in self.spans:
            segments.extend(tokens[start:end])
        return ' '.join(segments)

    def __repr__(self) -> str:
        return f"Tree({self.variable!r}, spans={self.spans}, children={self.children})"

    def __str__(self) -> str:
        if self.is_leaf():
            return f"{self.variable}:{self.spans}"
        child_str = ' '.join(str(c) for c in self.children)
        return f"({self.variable}:{self.spans} {child_str})"

    def pretty_print(self, indent: int = 0):
        """Pretty-print the tree."""
        pad = '  ' * indent
        print(f"{pad}{self.variable} {self.spans}")
        for child in self.children:
            child.pretty_print(indent + 1)