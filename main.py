import os

#Modules - Please check they are installed
import numpy
import nibabel
import imageio

def clear_console():
    lambda: os.system('clr')

def create_directory(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)
        return True
    else:
        return False

def get_files_of_type(file_path, extension_name):
    return_list = []
    for file in os.listdir(file_path):
        if file.endswith(extension_name):
            return_list.append([file, os.path.join(file_path, file)])
            print([file, os.path.join(file_path, file)])
    return return_list

def export_slice_image(filepath, slice):
    # Increase brightness and scale colour values from 0 - 1 to 0 - 255
    for x in range(len(slice)):
        for y in range(len(slice[x])):
            slice[x, y] = slice[x, y] * 255 * 2
            pass

    # Convert slice to 8bit integer before exporting
    converted_slice = slice.astype(numpy.uint8)
    #Export image
    imageio.imwrite(filepath, converted_slice)
    return

def print_status(file_name,slice_number,totalSliceCount):
    statement = """
    --------
    Exporting : {0}
    On Slice: {1} / {2}
    --------
    """.format(file_name,slice_number,totalSliceCount)

    print(statement)
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Current path of script
    absolute_path = os.path.dirname(__file__)
    # Export folder path
    exportDirPath = os.path.join(absolute_path, "ImageExport")
    # Create export folder if it does not exist
    create_directory(exportDirPath)

    # Get files of type and export them in seperate folders.
    for file in get_files_of_type(absolute_path, ".gz"):
        subpath = os.path.join(exportDirPath, file[0])
        create_directory(
            os.path.join(subpath)
        )
        openFile = nibabel.load(file[1])
        fileData = openFile.get_fdata()

        for i in range(openFile.shape[1]):
            dataSlice = fileData[:, i, :]
            filepath = os.path.join(subpath, "{0}.png".format(i));
            print_status(filepath,i,openFile.shape[1])
            export_slice_image(filepath, dataSlice)

        

