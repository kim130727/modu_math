from typing import Any
from .models.node import LayoutNode, TextNode
from .models.group import LayoutGroup

def apply_layout_diff(nodes: list[LayoutNode], patches: list[dict[str, Any]]) -> None:
    """Applies a list of layout patches to the nodes.
    Supported ops: 'move', 'resize', 'edit_text', 'update_style'
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
            
        elif op == "resize":
            if "width" in patch:
                target_node.width = patch["width"]
            if "height" in patch:
                target_node.height = patch["height"]
            # Handle shape-specific resize attrs
            if "r" in patch:
                target_node.properties["r"] = patch["r"]
            if "rx" in patch:
                target_node.properties["rx"] = patch["rx"]
            if "ry" in patch:
                target_node.properties["ry"] = patch["ry"]
            if "points" in patch:
                target_node.properties["points"] = patch["points"]
                
        elif op == "edit_text":
            if isinstance(target_node, TextNode) and "text" in patch:
                target_node.text = patch["text"]
                
        elif op == "update_style":
            for style_key in ["fill", "stroke", "stroke_width", "font_size", "font_family", "font_weight"]:
                if style_key in patch:
                    target_node.properties[style_key] = patch[style_key]
