from create_3d_obj import *
from transformations import *

if __name__=='__main__':
    # Generate random 3D objects
    path = pipe_Create("/mnt/z/shaw_and_patterns/src/inputs")
    # Transformed random 3d objects
    pipe_Transform(path,"/mnt/z/shaw_and_patterns/src/outputs/transformed_points.json")