import os

# Use a non-interactive backend so matplotlib never tries to open a GUI window.
# This must be set before lithophane (which imports pyplot) is imported.
import matplotlib
matplotlib.use("Agg")


def convert_to_lithophane(imagefile):

    import lithophane as li

    # imagefile = '/Users/pieronanni/Desktop/lithophane/piero.jpeg'
    width = 102  # Width in mm
    # show=False: we are running headless inside a web request, so we must not
    # pop up any matplotlib windows.
    x, y, z = li.jpg_to_stl(imagefile, width, 3, 0.5, show=False)

    # Strip the extension correctly (handles .jpg, .jpeg, .png, ...).
    base, _ = os.path.splitext(imagefile)

    # Generate stl model from pointcloud and save
    model = li.make_mesh(x, y, z)
    flat_filename = base + '_Flat.stl'
    model.save(flat_filename)

    # Turn the flat pointcloud into a cylinder
    cx, cy, cz = li.make_cylinder(x, y, z)

    # Save the Cylinder Model
    model = li.make_mesh(cx, cy, cz)
    cylinder_filename = base + '_Cylinder.stl'
    model.save(cylinder_filename)

    return flat_filename, cylinder_filename
