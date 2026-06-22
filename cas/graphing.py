import graphviz
import uuid
import tempfile

from .ast_node import ASTNode
from .expression import Expression


def fromNode(head: ASTNode) -> graphviz.Digraph:
    graph = graphviz.Digraph(format='png')

    def traverse_tree(curr: ASTNode, parent=None):
        curr_id = gen_id()
        graph.node(curr_id, label=curr.literal())
        if parent:
            graph.edge(parent, curr_id)
        if curr.children() and len(curr.children()) > 0:
            for child in curr.children():
                traverse_tree(child, curr_id)

    def gen_id():
        length = 16
        return str(uuid.uuid4()).replace("-", "")[:length]

    traverse_tree(head)
    return graph


def fromExpr(exp: Expression) -> graphviz.Digraph:
    return fromNode(exp._expression)


def view(graph: graphviz.Digraph, dir: str = "graphs/"):
    graph.view(tempfile.mktemp(".gv", dir=dir))
