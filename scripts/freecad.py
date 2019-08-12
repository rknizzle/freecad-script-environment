#!/usr/bin/env python3
# General purpose FreeCAD functions

# Add freeCAD path to access freecad python modules
FREECADPATH = '/usr/lib/freecad/lib'
import sys
import os
sys.path.append(FREECADPATH)
# import FreeCAD modules
try:
    import FreeCAD
    import Part
    import Mesh
    import MeshPart
except:
    print("FreeCAD could not be imported globally")

# Takes in a file and imports it as a part or mesh
# depending on the file type
# Returns the model(part or mesh)
def import_file(file_path):
    # get file type
    file_type = os.path.splitext(file_path)[1][1:]

    model_type = get_file_category(file_type)
    if model_type is "mesh":
        #upload as mesh
        model = Mesh.Mesh(file_path)
    elif model_type is "part":
        #upload as part
        model = Part.Shape()
        model.read(file_path)

    # Check for empty part (Probably caused by incorrect file being used
    if model.Area == 0 and model.Volume == 0:
        raise Exception('File has no dimensions. Check file and make sure it is a supported file type')
    return model

# Checks the file type and determines if the file should be uploaded to FreeCAD as part or mesh
def get_file_category(file_extension):
    # TODO: add handling for proprietary file types
    proprietary_file_extensions = []
    mesh_extensions = ["stl", "obj"]
    part_extensions = ["step", "stp", "igs", "iges"]

    file_extension = file_extension.lower()

    if file_extension in mesh_extensions:
        return "mesh"
    elif file_extension in part_extensions:
        return "part"
    else:
        raise Exception("Files with extension %s not supported" % file_extension)

# Takes in a part or mesh and returns the dimensions
# Area, volume, and bounding box
def get_dimensions(model):
    try:
        # Used for FreeCAD shape objects to more accurately get the bounding box dimensions
        model.tessellate(0.1)
    except:
        pass

    bounding_box = model.BoundBox
    bounding_box = {
        "x": bounding_box.XLength,
        "y": bounding_box.YLength,
        "z": bounding_box.ZLength
    }
    dimensions = {
        "bounding_box": bounding_box,
        "area": model.Area,
        "volume": model.Volume
    }
    return dimensions


if __name__=='__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        file = sys.argv[1]
    except:
        file = '../fixtures/test.stl'
    model = import_file(dir_path + "/" + file)
    print('file: ' + file)
    print('model info: ' + str(model))
    dimensions = get_dimensions(model)
    print('dimensions: ' + str(dimensions))
