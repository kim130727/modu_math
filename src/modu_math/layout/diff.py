from typing import Any
from .models.node import LayoutNode
from .models.group import LayoutGroup

def apply_layout_diff(nodes: list[LayoutNode], patches: list[dict[str, Any]]) -> None:
    """Applies a list of layout patches to the nodes.
    Currently supports: 'move'
    """
    # Build node map
    node_map: dict[str, LayoutNode] = {}
    
    def _traverse(node: LayoutNode):
        node_map[node.id] = node
        if isinstance(node, LayoutGroup):
            for child in node.children:
                _traverse(child)

    for node in nodes:
        _traverse(node)

    for patch in patches:
        target_id = patch.get("target")
        op = patch.get("op")
        
        if target_id not in node_map:
            continue
            
        target_node = node_map[target_id]
        
        if op == "move":
            dx = patch.get("dx", 0.0)
            dy = patch.get("dy", 0.0)
            target_node.x += dx
            target_node.y += dy
