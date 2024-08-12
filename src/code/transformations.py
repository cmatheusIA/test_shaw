import json
import numpy as np
from mathutils import Euler, Vector, Matrix
import random
from create_3d_obj import random_float

def load_points_from_json(filename):
    """
    Loads 3D object data from a JSON file.

    Args:
        filename (str): The path to the JSON file containing the 3D objects.

    Returns:
        list: A list of dictionaries representing the 3D objects.
    """
    with open(filename, 'r') as f:
        return json.load(f)

def scale_object(obj, scale_factors):
    """
    Applies scaling to a 3D object.

    Args:
        obj (dict): The 3D object to scale. It must contain 'scale' keys with 'x', 'y', and 'z' as sub-keys.
        scale_factors (list of float): A list of three scaling factors for the x, y, and z axes.

    Returns:
        dict: The scaled 3D object.
    """
    obj['scale']['x'] *= scale_factors[0]
    obj['scale']['y'] *= scale_factors[1]
    obj['scale']['z'] *= scale_factors[2]
    return obj

def rotate_object(obj, rotation_angles):
    """
    Applies rotation to a 3D object.

    Args:
        obj (dict): The 3D object to rotate. It must contain 'position' and 'rotation' keys with 'x', 'y', and 'z' as sub-keys.
        rotation_angles (dict): A dictionary containing the rotation angles in degrees for the x, y, and z axes.

    Returns:
        dict: The rotated 3D object with updated position and rotation.
    """
    position = Vector((obj['position']['x'], obj['position']['y'], obj['position']['z']))
    
    rotation_euler = Euler((np.radians(rotation_angles['x']), 
                            np.radians(rotation_angles['y']), 
                            np.radians(rotation_angles['z'])))
    
    rotated_position = rotation_euler.to_matrix() @ position
    
    obj['position'] = {'x': rotated_position.x, 'y': rotated_position.y, 'z': rotated_position.z}
    
    current_rotation = Euler((np.radians(obj['rotation']['y']), 
                              np.radians(obj['rotation']['z']), 
                              np.radians(obj['rotation']['x'])))
    
    new_rotation = Euler((current_rotation.x + rotation_euler.x,
                          current_rotation.y + rotation_euler.y,
                          current_rotation.z + rotation_euler.z))
    
    obj['rotation'] = {'x': np.degrees(new_rotation.x), 'y': np.degrees(new_rotation.y), 'z': np.degrees(new_rotation.z)}
    
    return obj

def translate_object(obj, translation_vector):
    """
    Applies translation to a 3D object.

    Args:
        obj (dict): The 3D object to translate. It must contain 'position' keys with 'x', 'y', and 'z' as sub-keys.
        translation_vector (list of float): A list of three translation values for the x, y, and z axes.

    Returns:
        dict: The translated 3D object.
    """
    obj['position']['x'] += translation_vector[0]
    obj['position']['y'] += translation_vector[1]
    obj['position']['z'] += translation_vector[2]
    return obj

def save_transformed_objects(objects, filename, transformations_summary):
    """
    Saves the transformed 3D objects to a JSON file.

    Args:
        objects (list): A list of dictionaries representing the transformed 3D objects.
        filename (str): The path to the output JSON file where the transformed objects will be saved.
        transformations_summary (dict): A dictionary summarizing the transformations applied to the objects.

    Returns:
        None
    """
    data = {
        "objects": objects,
        "transformations": transformations_summary
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def pipe_Transform(path_load, path_save):
    """
    Pipeline for loading 3D objects, applying random transformations (scaling, rotation, translation), and saving the results.

    Args:
        path_load (str): The path to the input JSON file containing the original 3D objects.
        path_save (str): The path to the output JSON file where the transformed objects will be saved.

    Returns:
        None
    """
    objects = load_points_from_json(path_load)

    scalar = random_float(0.5, 2.0)
    scale_factors = [scalar, scalar, scalar]
    scaled_objects = [scale_object(obj, scale_factors) for obj in objects]

    rotation_angles = {'x': 0, 'y': random.randint(0, 360), 'z': 0}
    rotated_objects = [rotate_object(obj, rotation_angles) for obj in scaled_objects]

    translation_vector = [random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)]
    translated_objects = [translate_object(obj, translation_vector) for obj in rotated_objects]

    transformations = {
        "scale_factors": scale_factors,
        "rotation_angles": rotation_angles,
        "translation_vector": translation_vector
    }
    save_transformed_objects(translated_objects, path_save, transformations)
