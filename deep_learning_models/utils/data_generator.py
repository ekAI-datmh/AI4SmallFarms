import numpy as np
import rasterio
import skimage.io
import skimage.util
import tensorflow as tf
from base import *
import osgeo
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class DataGenerator(Base, tf.keras.utils.Sequence):
    # https://mahmoudyusof.github.io/facial-keypoint-detection/data-generator/

    def __init__(self, data_path, shuffle=True):
        super().__init__()
        self.indices = None
        self.data_path = data_path
        self.batch_size = self.batch_size
        self.images_dir = self.images_dir
        self.masks_dir = self.masks_dir
        self.num_channels = self.num_channels
        self.shuffle = shuffle
        self.image_list = os.listdir(os.path.join(data_path, self.images_dir))
        self.mask_list = os.listdir(os.path.join(data_path, self.masks_dir))
        self.on_epoch_end()

    def on_epoch_end(self):
        self.indices = np.arange(len(self.image_list))
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __len__(self):
        return int(len(self.image_list) / self.batch_size)

    def __getitem__(self, idx):
        indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_img_list = []
        batch_msk_list = []

        #print(indices)
        for i, data_index in enumerate(indices):
            
            img = np.array(skimage.io.imread(os.path.join(self.data_path, self.images_dir, self.image_list[data_index]),
                                             plugin='tifffile'))
            img_nor = np.zeros(img.shape, dtype=np.float32)
            #print("Image: ", os.path.join(self.data_path, self.images_dir, self.image_list[data_index]))
            try:
                for k in range(self.num_channels):
                    band_max = np.max(img[:, :, k])
                    band_min = np.min(img[:, :, k])
                    img_nor[:, :, k] = (img[:, :, k] - band_min) / (band_max - band_min)
            except Exception as e:
                print(e)
            # plt.subplot(1,3,1)
            # plt.imshow(img)
            # plt.subplot(1,3,2)
            # plt.imshow(img_nor)
            batch_img_list.append(img_nor)
            # mask = np.array(skimage.io.imread(os.path.join(self.data_path, self.masks_dir, self.image_list[data_index].replace("image", "mask")),
            #                                plugin='tifffile'))
            # plt.subplot(1,3,3)
            # plt.imshow(mask)
            # plt.show()
            batch_msk_list.append(
                np.array(skimage.io.imread(os.path.join(self.data_path, self.masks_dir, self.image_list[data_index].replace("image", "mask")),
                                           plugin='tifffile')))
            #print("Mask name2: ", os.path.join(self.data_path, self.masks_dir, self.image_list[data_index].replace("image", "mask")))

        batch_img_list = np.array(batch_img_list)
        batch_msk_list = (np.array(batch_msk_list).astype(np.uint8)).astype(np.float32)
        

        return batch_img_list, batch_msk_list

    def get_extent(self, idx):
        indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        extent_list = []
        for i, data_index in enumerate(indices):
            extent_list.append(rasterio.open(os.path.join(self.data_path, self.images_dir,
                                                          self.image_list[data_index])).bounds)

        return extent_list

    def get_name(self, idx):
        # TODO: create better uniform names in FME Workbench
        indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        name_list = []
        for i, data_index in enumerate(indices):
            name_list.append(self.image_list[data_index].replace('images_', ''))

        return name_list
