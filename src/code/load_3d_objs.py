import bpy
import json
import math

def load_objects_from_json(file_path):
    """
    Loads 3D object data from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the 3D object data.

    Returns:
        dict: A dictionary containing the loaded 3D object data.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def create_objects_from_json(objects):
    """
    Creates or updates 3D objects in the Blender scene based on JSON data.

    This function reads object data, including type, position, scale, and rotation,
    and then creates the corresponding 3D objects (sphere, cube, or cylinder) in the Blender scene.

    Args:
        objects (list): A list of dictionaries, each representing a 3D object with 'type', 'position', 'scale', and 'rotation' keys.
    """
    for obj_data in objects:
        obj_type = obj_data['type']
        pos = obj_data['position']
        scale = obj_data['scale']
        rotation = obj_data['rotation']

        # Create the object if it doesn't exist
        if obj_type == 'sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(pos['x'], pos['y'], pos['z']))
        elif obj_type == 'cube':
            bpy.ops.mesh.primitive_cube_add(size=1, location=(pos['x'], pos['y'], pos['z']))
        elif obj_type == 'cylinder':
            bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(pos['x'], pos['y'], pos['z']))

        # Get the last created object
        created_object = bpy.context.object

        # Set the scale, rotation, and position
        created_object.scale = (scale['x'], scale['y'], scale['z'])
        created_object.rotation_euler = (
            math.radians(rotation['x']),
            math.radians(rotation['y']),
            math.radians(rotation['z'])
        )
        created_object.location = (pos['x'], pos['y'], pos['z'])

def setup_camera_light_and_render(output_filepath):
    """
    Sets up the camera, light, and renders the scene in Blender.

    This function adds a camera and a sunlight to the scene, configures their positions and rotations,
    and then renders the scene to an image file.

    Args:
        output_filepath (str): The file path where the rendered image will be saved.
    """
    # Add a camera
    if 'Camera' in bpy.data.objects:
        bpy.data.objects['Camera'].select_set(True)
        bpy.ops.object.delete()  # Remove existing camera

    bpy.ops.object.camera_add(location=(10, -10, 10))
    camera = bpy.context.object
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = camera

    # Add a SUN light
    if 'Sun' in bpy.data.objects:
        bpy.data.objects['Sun'].select_set(True)
        bpy.ops.object.delete()  # Remove existing light

    bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))

    # Render the scene and save the image
    bpy.context.scene.render.filepath = output_filepath
    bpy.ops.render.render(write_still=True)

# JSON file paths
random_objects_path = 'Z:\\shaw_and_patterns\\src\\inputs\\random_3d_objects.json'
transformed_objects_path = 'Z:\\shaw_and_patterns\\src\\outputs\\transformed_points.json'

# Load random and transformed objects
random_objects = load_objects_from_json(random_objects_path)
transformed_objects = load_objects_from_json(transformed_objects_path)['objects']

# Create random objects in the scene
create_objects_from_json(random_objects)

# Create transformed objects in the scene
create_objects_from_json(transformed_objects)

# Set up the camera, light, and render the scene
output_filepath = "/tmp/rendered_image.png"
setup_camera_light_and_render(output_filepath)

print(f"The rendered image has been saved to {output_filepath}")
