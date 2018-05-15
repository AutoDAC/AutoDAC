import javabridge as jv, bioformats as bf
from xml.etree import ElementTree as ETree
import numpy as np
import cv2

def extract_merged_images(lif_file, out_dir):
    """
    Extract merged images, in lif, into output directory

    :param lif: path to lif file
    :param out_dir: path to directory to store images
    :return: {path: (physical_size)} - metadata of images written.
    """
    jv.start_vm(class_path=bf.JARS, max_heap_size='8G')
    merged_images = get_merged_image_ids(lif_file)

    image_data = {}
    for series in merged_images:
        image_ids, max_z, physical_size = merged_images[series]
        image_data[series] = (read_images(image_ids, max_z, lif_file), physical_size[0])

        # Only read first merged image
        break

    # Finished reading data from the lif file
    jv.kill_vm()

    image_metadata = {}
    # Write images to out_dir
    for series in image_data:
        image_data, physical_size = image_data[series]
        # Write data in image_data
        for i, data in enumerate(image_data):
            out_path = out_dir + "/" + series + "_Z" + str(i) + ".tif"
            cv2.imwrite(out_path, data)

            image_metadata[out_path] = (physical_size)

    return image_metadata

def read_images(image_ids, max_zs, lif_file):
    """
    Read rgb images from lif file

    :param image_ids: List of image ids (series #), to extract
    :param max_zs: List of max z-depths for each image
    :param lif_file: Path to lif file to extract images from
    :return: List of images containing image data
    """
    images = []
    with bf.ImageReader(path=lif_file) as reader:
        for i, s in enumerate(image_ids):
                for z in range(0, max_zs[i]):
                    try:
                        image_data = reader.read(c=None, z=z, t=0, series=s, index=None, rescale=False, wants_max_intensity=False, channel_names=None, XYWH=None)
                    except:
                        print('Error reading image data')
                        continue
                    # Need to add blue channel, as microscope only saves red and green
                    rgb_image = add_blue_channel(image_data)
                    images.append(rgb_image)
    return images

def get_merged_image_ids(lif_file):
    """
    Get dictionary of image ids and max z values, for every merged (stitched) image

    :param lif_file: path to lif file
    :return: {"Merged": ([id1, id2, ..], [max_z], [PhysicalSizeX])}
    """
    md = bf.get_omexml_metadata(lif_file)
    mdroot = ETree.fromstring(md)

    # Get images that have 'Merging' in their name
    stitched_z_stack = {}
    for child in mdroot:
        # Get node attributes
        attr = child.attrib
        # If node has a name attribute
        if 'Name' in attr and 'Merging' in attr['Name']:
            image_name = attr['Name']
            # Create pair array if this is the first image we've seen with this name
            if not image_name in stitched_z_stack:
                stitched_z_stack[image_name] = ([], [], [])

            # Add image_id and z-depth for each
            stitched_z_stack[image_name][0].append(attr['ID'])
            stitched_z_stack[image_name][1].append(get_max_z_depth(child))
            stitched_z_stack[image_name][2].append(get_physical_size(child))


    # Get image ids for each scan
    for merged in stitched_z_stack:
        images = stitched_z_stack[merged][0]
        for i, name in enumerate(images):
            # Image:x - x is the id we want to extract
            # Overwrite name with image id
            images[i] = name.split(":")[1]

    return stitched_z_stack

def get_physical_size(image_node):
    """
    Get physical size of pixel in micrometers. Assuming square pixels

    :param image_node: image node containing pixels
    :return: physical pixel size
    """
    pixel_node = get_pixel_node(image_node)
    attr = pixel_node.attrib
    if 'PhysicalSizeX' in attr:
        return float(attr['PhysicalSizeX'])
    raise ValueError("Pixels don't have a physical Size")

def get_max_z_depth(image_node):
    """
    Get max z depth for this image

    :param image_node: image node containing z-planes
    :return: max z depth (eg, 0)
    """
    pixel_node = get_pixel_node(image_node)
    plane_nodes = get_plane_nodes(pixel_node)

    max_z = 0
    for plane in plane_nodes:
        z_depth = int(plane.attrib['TheZ'])
        max_z = max(max_z, z_depth)
    return max_z

def get_pixel_node(image_node):
    """
    Get pixel node, in xml tag tree

    :param image_node: image node containing z-planes
    :return: Pixel node in image_node
    """
    for image_child_node in image_node:
        if 'Pixels' in image_child_node.tag:
            return image_child_node
    raise ValueError("Pixel node doesn't exist")

def get_plane_nodes(pixel_nodes):
    """
    Get plane nodes, in xml tag tree

    :param pixel_nodes: plane node containing z-planes
    :return: List of plane nodes in pixel node
    """
    plane_nodes = []
    for plane_node in pixel_nodes:
        if 'Plane' in plane_node.tag:
            plane_nodes.append(plane_node)
    return plane_nodes

def add_blue_channel(image_data):
    """
    Add blue channel to only red and green channel image

    :param image_data: List of tuples with only red and green channels
    :return: Image with (b, g, r) channels
    """
    rgb_image = []
    for i in range(0, len(image_data)):
        rgb_image.append([])
        for j in range(0, len(image_data[i])):
            rgb_image[i].append([])
            rgb_image[i][j] = np.append([0], image_data[i][j])
    return np.array(rgb_image)
