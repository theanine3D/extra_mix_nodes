import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Extra Mix Nodes",
    "description": "Adds extra varieties of the Mix node, with additional color inputs, allowing for blending of more than just 2 textures",
    "author": "Theanine3D",
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "category": "Node",
    "location": "Shader Editor",
    "support": "COMMUNITY"
}

groups_to_add = ["Mix Color (3-Sequential)",
                 "Mix Color (4-Sequential)",
                 "Mix Color (5-Sequential)",
                 "Mix Color (Splat, RGB)",
                 "Mix Color (Splat, RGBA)"]

@persistent
def add_mix_nodes(dummy):
    # Check if we're in headless mode (no UI)
    if bpy.app.background:
        return

    for group_name in groups_to_add:
        if group_name not in bpy.data.node_groups:
            if group_name == "Mix Color (3-Sequential)":
                _create_3_sequential_mix()
            elif group_name == "Mix Color (4-Sequential)":
                _create_4_sequential_mix()
            elif group_name == "Mix Color (5-Sequential)":
                _create_5_sequential_mix()
            elif group_name == "Mix Color (Splat, RGB)":
                _create_splat_rgb_mix()
            elif group_name == "Mix Color (Splat, RGBA)":
                _create_splat_rgba_mix()

def _create_3_sequential_mix():
    node_group = bpy.data.node_groups.new(name="Mix Color (3-Sequential)", type="ShaderNodeTree")
    node_group.use_fake_user = True

    # Create group inputs
    group_inputs = node_group.nodes.new("NodeGroupInput")
    group_inputs.location = (-600, 0)
    group_inputs.width = 180.0

    # Create group outputs
    group_outputs = node_group.nodes.new("NodeGroupOutput")
    group_outputs.location = (600, 0)

    # Create group inputs
    group_inputs_node = node_group.nodes.new("NodeGroupInput")
    group_inputs_node.location = (-600, 0)
    group_inputs_node.width = 180.0
    interface = node_group.interface
    a_input = interface.new_socket("A", description="", in_out='INPUT', socket_type='NodeSocketColor', parent=None)
    b_input = interface.new_socket("B", description="", in_out='INPUT', socket_type='NodeSocketColor', parent=None)
    c_input = interface.new_socket("C", description="", in_out='INPUT', socket_type='NodeSocketColor', parent=None)
    a_input.default_value, b_input.default_value, c_input.default_value = (0,0,0,1), (0,0,0,1), (0,0,0,1)
    factor_input = interface.new_socket("Factor", description="", in_out='INPUT', socket_type='NodeSocketFloat', parent=None)
    factor_input.default_value = 0.5
    factor_input.min_value = 0.0
    factor_input.max_value = 1.0
    factor_input.subtype = "FACTOR"
        
    interface.new_socket("Result", in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add internal nodes - using ShaderNodeMix instead of ShaderNodeMixRGB
    mix_node_1 = node_group.nodes.new(type="ShaderNodeMix")
    mix_node_1.location = (0, 100)
    mix_node_1.data_type = 'RGBA'
    mix_node_1.clamp_factor = True
    mix_node_1.clamp_result = True
    mix_node_1.blend_type = 'MIX'

    mix_node_2 = node_group.nodes.new(type="ShaderNodeMix")
    mix_node_2.location = (200, 100)
    mix_node_2.data_type = 'RGBA'
    mix_node_2.clamp_factor = True
    mix_node_2.clamp_result = True
    mix_node_2.blend_type = 'MIX'

    map_range_1 = node_group.nodes.new(type="ShaderNodeMapRange")
    map_range_1.location = (-200, -100)
    map_range_1.inputs['From Min'].default_value = 0.0
    map_range_1.inputs['From Max'].default_value = 0.5
    map_range_1.inputs['To Min'].default_value = 0.0
    map_range_1.inputs['To Max'].default_value = 1.0
    map_range_1.clamp = True

    map_range_2 = node_group.nodes.new(type="ShaderNodeMapRange")
    map_range_2.location = (-200, -325)
    map_range_2.inputs['From Min'].default_value = 0.5
    map_range_2.inputs['From Max'].default_value = 1.0
    map_range_2.inputs['To Min'].default_value = 0.0
    map_range_2.inputs['To Max'].default_value = 1.0
    map_range_2.clamp = True

    # Link nodes
    links = node_group.links
    links.new(group_inputs.outputs['A'], mix_node_1.inputs[6])  # A input
    links.new(group_inputs.outputs['B'], mix_node_1.inputs[7])  # B input
    links.new(group_inputs.outputs['Factor'], map_range_1.inputs['Value'])
    links.new(map_range_1.outputs['Result'], mix_node_1.inputs[0])  # Factor input

    links.new(mix_node_1.outputs[2], mix_node_2.inputs[6])  # Result to A input
    links.new(group_inputs.outputs['C'], mix_node_2.inputs[7])  # C to B input
    links.new(group_inputs.outputs['Factor'], map_range_2.inputs['Value'])
    links.new(map_range_2.outputs['Result'], mix_node_2.inputs[0])  # Factor input

    links.new(mix_node_2.outputs[2], group_outputs.inputs['Result'])

def _create_4_sequential_mix():
    node_group = bpy.data.node_groups.new(name="Mix Color (4-Sequential)", type="ShaderNodeTree")
    node_group.use_fake_user = True

    # Create group inputs
    group_inputs = node_group.nodes.new("NodeGroupInput")
    group_inputs.location = (-600, 0)

    # Create group outputs
    group_outputs = node_group.nodes.new("NodeGroupOutput")
    group_outputs.location = (700, 0)

    # Add interface sockets
    node_group.interface.new_socket("A", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("B", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("C", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("D", in_out='INPUT', socket_type='NodeSocketColor')
    
    factor_socket = node_group.interface.new_socket("Factor", in_out='INPUT', socket_type='NodeSocketFloat')
    factor_socket.default_value = 0.5
    factor_socket.min_value = 0.0
    factor_socket.max_value = 1.0
    factor_socket.subtype = 'FACTOR'
    
    node_group.interface.new_socket("Result", in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add internal nodes
    mix_nodes = []
    for i in range(3):
        mix_node = node_group.nodes.new(type="ShaderNodeMix")
        mix_node.location = (i * 200, 100)
        mix_node.data_type = 'RGBA'
        mix_node.clamp_factor = True
        mix_node.clamp_result = True
        mix_node.blend_type = 'MIX'
        mix_nodes.append(mix_node)

    map_ranges = []
    ranges = [(0.0, 0.333), (0.333, 0.666), (0.666, 1.0)]
    for i, (from_min, from_max) in enumerate(ranges):
        map_range = node_group.nodes.new(type="ShaderNodeMapRange")
        map_range.location = (-200, -100 - i * 200)
        map_range.inputs['From Min'].default_value = from_min
        map_range.inputs['From Max'].default_value = from_max
        map_range.inputs['To Min'].default_value = 0.0
        map_range.inputs['To Max'].default_value = 1.0
        map_range.clamp = True
        map_ranges.append(map_range)

    # Link nodes
    links = node_group.links
    
    # First mix
    links.new(group_inputs.outputs['A'], mix_nodes[0].inputs[6])
    links.new(group_inputs.outputs['B'], mix_nodes[0].inputs[7])
    links.new(group_inputs.outputs['Factor'], map_ranges[0].inputs['Value'])
    links.new(map_ranges[0].outputs['Result'], mix_nodes[0].inputs[0])

    # Second mix
    links.new(mix_nodes[0].outputs[2], mix_nodes[1].inputs[6])
    links.new(group_inputs.outputs['C'], mix_nodes[1].inputs[7])
    links.new(group_inputs.outputs['Factor'], map_ranges[1].inputs['Value'])
    links.new(map_ranges[1].outputs['Result'], mix_nodes[1].inputs[0])

    # Third mix
    links.new(mix_nodes[1].outputs[2], mix_nodes[2].inputs[6])
    links.new(group_inputs.outputs['D'], mix_nodes[2].inputs[7])
    links.new(group_inputs.outputs['Factor'], map_ranges[2].inputs['Value'])
    links.new(map_ranges[2].outputs['Result'], mix_nodes[2].inputs[0])

    links.new(mix_nodes[2].outputs[2], group_outputs.inputs['Result'])

def _create_5_sequential_mix():
    node_group = bpy.data.node_groups.new(name="Mix Color (5-Sequential)", type="ShaderNodeTree")
    node_group.use_fake_user = True

    # Create group inputs and outputs
    group_inputs = node_group.nodes.new("NodeGroupInput")
    group_inputs.location = (-600, 0)
    group_outputs = node_group.nodes.new("NodeGroupOutput")
    group_outputs.location = (800, 0)

    # Add interface sockets
    node_group.interface.new_socket("A", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("B", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("C", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("D", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("E", in_out='INPUT', socket_type='NodeSocketColor')
    
    factor_socket = node_group.interface.new_socket("Factor", in_out='INPUT', socket_type='NodeSocketFloat')
    factor_socket.default_value = 0.5
    factor_socket.min_value = 0.0
    factor_socket.max_value = 1.0
    factor_socket.subtype = 'FACTOR'
    
    node_group.interface.new_socket("Result", in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add internal nodes
    mix_nodes = []
    for i in range(4):
        mix_node = node_group.nodes.new(type="ShaderNodeMix")
        mix_node.location = (i * 200, 100)
        mix_node.data_type = 'RGBA'
        mix_node.clamp_factor = True
        mix_node.clamp_result = True
        mix_node.blend_type = 'MIX'
        mix_nodes.append(mix_node)

    map_ranges = []
    ranges = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)]
    for i, (from_min, from_max) in enumerate(ranges):
        map_range = node_group.nodes.new(type="ShaderNodeMapRange")
        map_range.location = (-200, -100 - i * 200)
        map_range.inputs['From Min'].default_value = from_min
        map_range.inputs['From Max'].default_value = from_max
        map_range.inputs['To Min'].default_value = 0.0
        map_range.inputs['To Max'].default_value = 1.0
        map_range.clamp = True
        map_ranges.append(map_range)

    # Link nodes
    links = node_group.links
    
    # Link all mix nodes in sequence
    inputs = ['A', 'B', 'C', 'D', 'E']
    
    # First mix
    links.new(group_inputs.outputs[inputs[0]], mix_nodes[0].inputs[6])
    links.new(group_inputs.outputs[inputs[1]], mix_nodes[0].inputs[7])
    links.new(group_inputs.outputs['Factor'], map_ranges[0].inputs['Value'])
    links.new(map_ranges[0].outputs['Result'], mix_nodes[0].inputs[0])

    # Subsequent mixes
    for i in range(1, 4):
        links.new(mix_nodes[i-1].outputs[2], mix_nodes[i].inputs[6])
        links.new(group_inputs.outputs[inputs[i+1]], mix_nodes[i].inputs[7])
        links.new(group_inputs.outputs['Factor'], map_ranges[i].inputs['Value'])
        links.new(map_ranges[i].outputs['Result'], mix_nodes[i].inputs[0])

    links.new(mix_nodes[3].outputs[2], group_outputs.inputs['Result'])

def _create_splat_rgb_mix():
    node_group = bpy.data.node_groups.new(name="Mix Color (Splat, RGB)", type="ShaderNodeTree")
    node_group.use_fake_user = True

    # Create group inputs and outputs
    group_inputs = node_group.nodes.new("NodeGroupInput")
    group_inputs.location = (-600, 0)
    group_outputs = node_group.nodes.new("NodeGroupOutput")
    group_outputs.location = (600, 0)

    # Add interface sockets
    node_group.interface.new_socket("R", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("G", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("B", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("Splat Map", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("Result", in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add internal nodes
    mix_nodes = []
    for i in range(3):
        mix_node = node_group.nodes.new(type="ShaderNodeMix")
        mix_node.location = (i * 200, 100)
        mix_node.data_type = 'RGBA'
        mix_node.clamp_factor = True
        mix_node.clamp_result = True
        mix_node.blend_type = 'MIX'
        mix_nodes.append(mix_node)

    # Use Separate RGB instead of Separate Color
    separate_rgb_node = node_group.nodes.new(type="ShaderNodeSeparateColor")
    separate_rgb_node.location = (-200, -100)

    # Link nodes
    links = node_group.links
    
    # Connect splat map to separate RGB
    links.new(group_inputs.outputs['Splat Map'], separate_rgb_node.inputs[0])
    
    # Connect RGB channels to mix nodes
    links.new(group_inputs.outputs['R'], mix_nodes[0].inputs[7])  # B input
    links.new(separate_rgb_node.outputs[0], mix_nodes[0].inputs[0])  # Factor
    
    links.new(group_inputs.outputs['G'], mix_nodes[1].inputs[7])  # B input
    links.new(separate_rgb_node.outputs[1], mix_nodes[1].inputs[0])  # Factor
    
    links.new(group_inputs.outputs['B'], mix_nodes[2].inputs[7])  # B input
    links.new(separate_rgb_node.outputs[2], mix_nodes[2].inputs[0])  # Factor

    # Chain mix nodes together
    links.new(mix_nodes[0].outputs[2], mix_nodes[1].inputs[6])  # A input
    links.new(mix_nodes[1].outputs[2], mix_nodes[2].inputs[6])  # A input
    
    links.new(mix_nodes[2].outputs[2], group_outputs.inputs['Result'])

def _create_splat_rgba_mix():
    node_group = bpy.data.node_groups.new(name="Mix Color (Splat, RGBA)", type="ShaderNodeTree")
    node_group.use_fake_user = True

    # Create group inputs and outputs
    group_inputs = node_group.nodes.new("NodeGroupInput")
    group_inputs.location = (-600, 0)
    group_outputs = node_group.nodes.new("NodeGroupOutput")
    group_outputs.location = (800, 0)

    # Add interface sockets
    node_group.interface.new_socket("R", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("G", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("B", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("A", in_out='INPUT', socket_type='NodeSocketColor')
    node_group.interface.new_socket("Splat Map (RGB)", in_out='INPUT', socket_type='NodeSocketColor')
    
    alpha_socket = node_group.interface.new_socket("Splat Map (Alpha)", in_out='INPUT', socket_type='NodeSocketFloat')
    alpha_socket.default_value = 0.5
    alpha_socket.min_value = 0.0
    alpha_socket.max_value = 1.0
    alpha_socket.subtype = 'FACTOR'
    
    node_group.interface.new_socket("Result", in_out='OUTPUT', socket_type='NodeSocketColor')

    # Add internal nodes
    mix_nodes = []
    for i in range(4):
        mix_node = node_group.nodes.new(type="ShaderNodeMix")
        mix_node.location = (i * 200, 100)
        mix_node.data_type = 'RGBA'
        mix_node.clamp_factor = True
        mix_node.clamp_result = True
        mix_node.blend_type = 'MIX'
        mix_nodes.append(mix_node)

    # Use Separate RGB instead of Separate Color
    separate_rgb_node = node_group.nodes.new(type="ShaderNodeSeparateColor")
    separate_rgb_node.location = (-200, -100)

    # Link nodes
    links = node_group.links
    
    # Connect splat map to separate RGB
    links.new(group_inputs.outputs['Splat Map (RGB)'], separate_rgb_node.inputs[0])
    
    # Connect RGB channels to mix nodes
    links.new(group_inputs.outputs['R'], mix_nodes[0].inputs[7])  # B input
    links.new(separate_rgb_node.outputs[0], mix_nodes[0].inputs[0])  # Factor
    
    links.new(group_inputs.outputs['G'], mix_nodes[1].inputs[7])  # B input
    links.new(separate_rgb_node.outputs[1], mix_nodes[1].inputs[0])  # Factor
    
    links.new(group_inputs.outputs['B'], mix_nodes[2].inputs[7])  # B input
    links.new(separate_rgb_node.outputs[2], mix_nodes[2].inputs[0])  # Factor
    
    links.new(group_inputs.outputs['A'], mix_nodes[3].inputs[7])  # B input
    links.new(group_inputs.outputs['Splat Map (Alpha)'], mix_nodes[3].inputs[0])  # Factor

    # Chain mix nodes together
    links.new(mix_nodes[0].outputs[2], mix_nodes[1].inputs[6])  # A input
    links.new(mix_nodes[1].outputs[2], mix_nodes[2].inputs[6])  # A input
    links.new(mix_nodes[2].outputs[2], mix_nodes[3].inputs[6])  # A input
    
    links.new(mix_nodes[3].outputs[2], group_outputs.inputs['Result'])

def register():
    # Create nodes immediately and also on file load
    add_mix_nodes(None)
    bpy.app.handlers.load_post.append(add_mix_nodes)

def unregister():
    if add_mix_nodes in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(add_mix_nodes)

if __name__ == "__main__":
    register()
