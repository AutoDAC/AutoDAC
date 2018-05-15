import numpy as np
import shutil
import os
# Understanding of tkinter will help understanding behaviour of this code
from tkinter import Tk, Label, Button, StringVar, Entry, DISABLED, ACTIVE

from PIL import ImageTk, Image
from QuickScorer.qs_segment import segment_region
import ImageProcessing.src.utils as utils
import cv2


class QuickScorer:
    IMG_MAX_SIZE = 400
    DEFAULT_PATH = 'img/ToScore/'
    LABEL_BAD_PATH_TEXT = "Invalid directory path. Re-enter and try again."
    LABEL_BAD_SF = "Invalid dimension. Please check your dimensions."
    curr_img_num = 0
    scores = []
    curr_img_scores = []
    tally = np.zeros((10,), np.uint32)

    def __init__(self, master):
        self.master = master
        master.minsize(width=666, height=444)
        master.title("Quick Scorer")

        self.entry_label = Label(master, text="Enter path to directory with "
                                              "images to score.")
        self.entry_label.pack()

        default_path = StringVar(master, value=self.DEFAULT_PATH)
        self.path = self.DEFAULT_PATH
        self.dir_entry = Entry(master, textvariable=default_path, width=40)
        self.dir_entry.pack()

        self.dimensions_real_label = Label(master, text="Width in μm")
        self.dimensions_real_label.pack()
        default_dimension_real = StringVar(master, value="775")
        self.dimensions_real = Entry(master,
                                     textvariable=default_dimension_real,
                                     width=5)
        self.dimensions_real.pack()

        self.strt_score_btn = Button(master, text="Start Scoring",
                                     command=self.start_score)
        self.strt_score_btn.pack()

        self.error_text = StringVar()
        self.error_label = Label(master, textvariable=self.error_text, fg="red")
        self.error_label.pack()

        self.img = None
        self.image = Label(self.master, image=self.img)
        self.image.pack()

    def start_score(self):
        """
            Segment images to score and display the first one after user
            presses "Start Scoring" button.

        """
        self.curr_img_num = 0
        path = self.dir_entry.get()
        # Append trailing directory separator if it's not already there
        if path and not (path[-1] == os.sep):
            path += os.sep
        self.path = path
        distance = self.dimensions_real.get()
        if self.validate(path, distance):
            self.strt_score_btn.configure(state=DISABLED)
            cell_path = path
            if distance != 0:
                self.error_text.set('Segmenting cells...')
                self.error_label.configure(fg='black')
                Tk.update(self.master)
                cell_path += 'cells/'
                utils.create_or_wipe_dir(cell_path)
                cnt = 0
                for imgPath in sorted(utils.all_images_in_dir(path)):
                    img = cv2.imread(imgPath)
                    resolution = img.shape[0]
                    dist_per_pixel = float(distance) / resolution
                    cnt = segment_region(img, cell_path, cnt, dist_per_pixel)
                cell_path += 'show_'

            self.error_text.set('')
            try:
                img = Image.open(cell_path + str(self.curr_img_num) + '.png')
                img = self.resize_image(img)
                self.img = ImageTk.PhotoImage(img)
                self.image.configure(image=self.img)
                self.image.focus_set()
                self.image.bind("<Key>", self.key)
            except IOError:
                # No images in directory
                self.image.configure(text='There are no images in the '
                                          'directory. Please try again.')
                self.strt_score_btn.configure(state=ACTIVE)
        else:
            if not os.path.isdir(str(path)):
                self.error_text.set(self.LABEL_BAD_PATH_TEXT)
            else:
                self.error_text.set(self.LABEL_BAD_SF)

    def validate(self, entered_path, distance):
        """
            Ensure valid fields have been entered

            :param entered_path: User input path to directory of images to score
            :param distance: User entered distance per pixel for all images
            :return: True if valid values entered, false otherwise.
        """
        if not os.path.isdir(str(entered_path)):
            return False
        try:
            return float(distance) >= 0
        except ValueError:
            return False

    def key(self, event):
        """
            Action fired on keypress

            :param event: Event object for the keypress
        """
        value = event.char
        if value.isdigit() and 0 <= int(value) <= 9:
            self.scores.append(value)
            self.tally[int(value)] += 1
            self.advance_image()

    def advance_image(self):
        """
            Displays the next image in the directory. If there are none left,
            an IOError will be caught and the results of the scoring session
            will be written out.

        """
        try:
            self.curr_img_num += 1
            img = Image.open(self.path + 'cells/show_' + str(
                self.curr_img_num) + '.png')
            img = self.resize_image(img)
            self.img = ImageTk.PhotoImage(img)
            self.image.configure(image=self.img)
            self.image.image = self.img
        except IOError:
            # Reached the end of the directory
            self.image.destroy()
            self.image = Label(self.master, text='Writing...')
            self.image.pack()
            result_dir = self.path + 'result/'
            if not os.path.exists(result_dir):
                os.makedirs(result_dir)
            else:
                shutil.rmtree(result_dir)
                os.makedirs(result_dir)
            # Write individual cell scores
            file = open(result_dir + 'results.txt', 'w')
            for item in self.scores:
                if isinstance(item, list):
                    for val in item:
                        file.write('%s ' % val)
                    file.write('\n')
                else:
                    file.write('%s\n' % item)
            file.close()

            # Write tally to file
            file = open(result_dir + 'tally.txt', 'w')
            totalCells = np.ndarray.sum(self.tally) - self.tally[9]
            file.write('Number of cells of interest: %s\n' % totalCells)
            file.write('Number of rejects: %s\n' % self.tally[0])
            for i, score in enumerate(self.tally[1:9]):
                file.write('Number of cells scoring ' + str(i + 1) + '/8: '
                           + str(score) + ' (' +
                           str(int((score / totalCells) * 100)) + '%)\n')
            file.close()
            self.image.configure(text='All images in the directory have '
                                      'been scored. You may now close the app.')
            self.strt_score_btn.configure(state=ACTIVE)

    def resize_image(self, img):
        """
            Resizes image to correct size for display

            :param img: Given image fo1r resizing
            :return: Resized image
        """
        width, height = img.size
        ratio = min([self.IMG_MAX_SIZE / dim for dim in (width, height)])
        img = img.resize((int(width * ratio), int(height * ratio)),
                         Image.NEAREST)
        return img


if __name__ == "__main__":
    root = Tk()
    my_gui = QuickScorer(root)
    root.mainloop()
