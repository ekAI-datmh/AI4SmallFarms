from pathlib import Path
import rasterio
import os
import math
from rasterio.windows import Window
from base import Base
from os.path import normpath, basename
from datetime import datetime

# test tiles must have overlap of at least 50% to create the right predictions
# train and validate tiles do not need this


class CreatePatches(Base):

    def __init__(self):
        super().__init__()
        self.root_dirs = [
            os.path.join(self.train_dir, self.images_dir),
            os.path.join(self.train_dir, self.masks_dir),
            os.path.join(self.validate_dir, self.images_dir),
            os.path.join(self.validate_dir, self.masks_dir),
            os.path.join(self.test_dir, self.images_dir),
            os.path.join(self.test_dir, self.masks_dir)
        ]

    @staticmethod
    def write_patch(img_, window, output_dir, image_type, filename, i_, n_):
        transform = img_.window_transform(window)
        profile = img_.profile
        profile.update({
            "height": window.height,
            "width": window.width,
            "transform": transform
        })

        # only valid for NL
        filename = filename.replace('tile-', '')

        with rasterio.open(os.path.join(output_dir, f'{image_type}_{i_}_{n_}_{filename}'), 'w',
                           **profile) as dataset:
            dataset.write(img_.read(window=window))

    def create_patch(self):
        for root_folder in self.root_dirs:
            image_type = basename(normpath(root_folder))[:-1]
            split_path = os.path.split(root_folder)[0]
            root_output_folder = os.path.join(split_path, self.patches_dir, image_type + 's')
            image_list = os.listdir(root_folder)

            for image_name in image_list:
                image_path = os.path.join(root_folder, image_name)
                with rasterio.open(image_path, 'r', driver='GTiff', dtype='uint16') as img:
                    if 'test' in root_folder:
                        div_factor = 2
                        patches_x = math.floor(img.width / (self.image_size / div_factor))
                        patches_y = math.floor(img.height / (self.image_size / div_factor))
                        stride_x = int((self.image_size / div_factor))
                        stride_y = int((self.image_size / div_factor))

                    if 'train' in root_folder or 'validate' in root_folder:
                        patches_x = math.ceil(img.width / self.image_size)
                        patches_y = math.ceil(img.height / self.image_size)
                        
                        # Check if we have more than one patch
                        if patches_x > 1:
                            patch_step_x_modulo = (self.image_size * patches_x) % img.width
                            stride_x = self.image_size - int(patch_step_x_modulo / (patches_x - 1))
                        else:
                            stride_x = self.image_size  # No stride needed if only one patch

                        if patches_y > 1:
                            patch_step_y_modulo = (self.image_size * patches_y) % img.height
                            stride_y = self.image_size - int(patch_step_y_modulo / (patches_y - 1))
                        else:
                            stride_y = self.image_size  # No stride needed if only one patch

                    for i in range(patches_x):
                        for n in range(patches_y):
                            if i == 0 and n == 0:
                                w = Window(0, 0, self.image_size, self.image_size)
                                self.write_patch(img, w, root_output_folder, image_type, image_name, w.col_off, w.row_off)

                            elif not i == range(patches_x)[-1] and not n == range(patches_y)[-1]:
                                w = Window(i * stride_x, n * stride_y, self.image_size, self.image_size)
                                self.write_patch(img, w, root_output_folder, image_type, image_name, w.col_off, w.row_off)

                            elif i == range(patches_x)[-1] and not n == range(patches_y)[-1]:
                                w = Window(img.width - self.image_size, n * stride_y, self.image_size,
                                           self.image_size)
                                self.write_patch(img, w, root_output_folder, image_type, image_name, w.col_off, w.row_off)

                            elif not i == range(patches_x)[-1] and n == range(patches_y)[-1]:
                                w = Window(i * stride_x, img.height - self.image_size, self.image_size,
                                           self.image_size)
                                self.write_patch(img, w, root_output_folder, image_type, image_name, w.col_off, w.row_off)

                            elif i == range(patches_x)[-1] and n == range(patches_y)[-1]:
                                w = Window(img.width - self.image_size, img.height - self.image_size,
                                           self.image_size, self.image_size)
                                self.write_patch(img, w, root_output_folder, image_type, image_name, w.col_off, w.row_off)
