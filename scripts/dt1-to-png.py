import glob
import os
import sys
import getopt
from PIL import Image
from ssi_filetypes.dt1file import DT1File

working_dir = sys.argv[1]
output_dir = os.path.join(working_dir, "output")


def create_output_directory():
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

def get_dt1_list():
    """
    Get a list of DT1s in the specified directory, strip extensions
    :return:
    """
    dt1_files = glob.glob(working_dir + "\*.DT1")
    working_file_list = []
    for dt1_file_path in dt1_files:
        folder, filename = os.path.split(dt1_file_path)
        filename, extension = os.path.splitext(filename)
        print folder, filename, extension

        working_file_list.append(os.path.join(folder, filename))

    return working_file_list


if __name__ == "__main__":

    create_output_directory()

    working_file_list = get_dt1_list()

    dt1 = DT1File()
    uid = 0

    for dt1_file_path in working_file_list:
        if dt1.opened:
            dt1.close()
        dt1.open_for_read(dt1_file_path)

        folder, file_name = os.path.split(dt1_file_path)

        png_width = 400
        png_height = 400
        pos = 0
        noIndexError = True

        while noIndexError:
            traces = dt1.get_traces(pos, pos+png_width)[0]
            pos += png_width

            doi = traces['data']
            doi += 32768
            scale_fact = 255. / (65536)
            doi *= scale_fact
            doi = doi.astype(dtype='uint8')
            img_name = '{}{}_{}.png'.format(dt1.filename, pos/png_width, uid)
            key = "positive"

            try:
                save_as = os.path.join(output_dir, img_name)
                img_dict[key].append(
                    ' '.join(["./{}_images/".format(key) + img_name, "1", "0", "0", str(len(doi)), str(len(doi[0]))]))
                image = Image.fromarray(doi.transpose())
                image.save(os.path.join(output_dir, img_name))
            
            except IndexError as e:
                noIndexError = False
                print "Error generating image " + save_as
