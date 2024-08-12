import json
import random

def random_float(min_value, max_value):
    """
    Generates a random float between two specified values, rounded to two decimal places.

    Args:
        min_value (float): The minimum value of the random float.
        max_value (float): The maximum value of the random float.

    Returns:
        float: A random float between min_value and max_value, rounded to two decimal places.
    """
    return round(random.uniform(min_value, max_value), 2)

def create_random_object():
    """
    Creates a random 3D object with random position, scale, and rotation values.

    The object type is randomly chosen from 'sphere', 'cube', or 'cylinder'.
    The position, scale, and rotation values are randomly generated within specified ranges.

    Returns:
        dict: A dictionary representing the random 3D object with 'type', 'position', 'scale', and 'rotation' keys.
    """
    object_types = ['sphere', 'cube', 'cylinder']
    obj = {
        "type": random.choice(object_types),
        "position": {
            "x": random_float(-10, 10),
            "y": random_float(-10, 10),
            "z": random_float(-10, 10)
        },
        "scale": {
            "x": random_float(0.5, 2.0),
            "y": random_float(0.5, 2.0),
            "z": random_float(0.5, 2.0)
        },
        "rotation": {
            "x": random_float(0, 360),
            "y": random_float(0, 360),
            "z": random_float(0, 360)
        }
    }
    return obj

def create_random_objects(num_objects):
    """
    Creates a list of random 3D objects.

    Args:
        num_objects (int): The number of random 3D objects to create.

    Returns:
        list: A list of dictionaries, each representing a random 3D object.
    """
    objects = []
    for _ in range(num_objects):
        objects.append(create_random_object())
    return objects

def pipe_Create(path):
    """
    Pipeline for creating random 3D objects and saving them to a JSON file.

    Args:
        path (str): The directory path where the JSON file will be saved.

    Returns:
        str: The complete path to the saved JSON file containing the random 3D objects.
    """
    complete_path = path + '/random_3d_objects.json'
    num_objects = 2  # Number of objects to create
    random_objects = create_random_objects(num_objects)
    
    with open(complete_path, 'w') as f:
        json.dump(random_objects, f, indent=4)

    print(f"Random 3D objects have been saved to {path}.")
    return complete_path
