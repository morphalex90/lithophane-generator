def convert_to_lithophane(imagefile):

    import lithophane as li

    # imagefile = '/Users/pieronanni/Desktop/lithophane/piero.jpeg'
    width = 102 #Width in mm
    x,y,z = li.jpg_to_stl(imagefile, 102, 3, 0.5)


    #Show the point cloud
    # li.show_stl(x,y,z)

    #Generate stl model from pointcloud and save
    model = li.make_mesh(x,y,z);
    filename=imagefile[:-4] + '_Flat.stl'
    model.save(filename)

    # Turn the flat pointcloud into a cylinder
    cx,cy,cz = li.make_cylinder(x,y,z)
    li.show_stl(cx,cy,cz)

    #Save the Cylinder Model
    model = li.make_mesh(cx,cy,cz);
    filename=imagefile[:-4] + '_Cylinder.stl'
    model.save(filename)