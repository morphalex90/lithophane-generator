import os

# Use a non-interactive backend so matplotlib never tries to open a GUI window.
# This must be set before lithophane (which imports pyplot) is imported.
import matplotlib
matplotlib.use("Agg")


def convert_to_lithophane(imagefile, shape="both", width=102, depth=3, offset=0.5):
    """Convert an image into lithophane STL file(s).

    shape:
        "flat"     -> only the flat lithophane
        "cylinder" -> only the cylinder lithophane
        "both"     -> both (default)
    width:  overall width of the model in mm (default 102)
    depth:  depth/thickness range carved by the image in mm (default 3)
    offset: base thickness behind the image in mm (default 0.5)

    Returns a list of the STL paths that were written.
    """

    import lithophane as li

    if shape not in ("flat", "cylinder", "both"):
        raise ValueError(f"Unknown shape: {shape!r}")

    # show=False: we are running headless inside a web request, so we must not
    # pop up any matplotlib windows.
    x, y, z = li.jpg_to_stl(imagefile, width, depth, offset, show=False)

    # Strip the extension correctly (handles .jpg, .jpeg, .png, ...).
    base, _ = os.path.splitext(imagefile)

    outputs = []

    if shape in ("flat", "both"):
        # Generate stl model from pointcloud and save
        model = li.make_mesh(x, y, z)
        flat_filename = base + '_Flat.stl'
        model.save(flat_filename)
        outputs.append(flat_filename)

    if shape in ("cylinder", "both"):
        # Turn the flat pointcloud into a cylinder
        cx, cy, cz = li.make_cylinder(x, y, z)

        # Save the Cylinder Model
        model = li.make_mesh(cx, cy, cz)
        cylinder_filename = base + '_Cylinder.stl'
        model.save(cylinder_filename)
        outputs.append(cylinder_filename)

    return outputs
