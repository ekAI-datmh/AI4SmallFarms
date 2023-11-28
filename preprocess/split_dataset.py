import os
import shutil
import geopandas as gp
import numpy as np

from base import Base
from itertools import cycle
from pathlib import Path


class SplitDataset(Base):

    def __init__(self):
        super().__init__()
        self.split_1 = self.split_1
        self.split_2 = self.split_2

    def split_dataset(self):
        tiles_gdf = gp.read_file(r'input/tilesAsia.gpkg', layer='tiles')
        tiles_gdf = tiles_gdf[['id', 'split', 'country']]

        for index, row in tiles_gdf.iterrows():
            filename = str(row['id']) + '_' + row['country'] + '.tif'
            if row['split'] == 'train':
                shutil.copyfile(os.path.join(self.data_dir, self.images_dir, filename),
                                os.path.join(self.train_dir, self.images_dir, filename))
                shutil.copyfile(os.path.join(self.data_dir, self.masks_dir, filename),
                                os.path.join(self.train_dir, self.masks_dir, filename))
            if row['split'] == 'validate':
                shutil.copyfile(os.path.join(self.data_dir, self.images_dir, filename),
                                os.path.join(self.validate_dir, self.images_dir, filename))
                shutil.copyfile(os.path.join(self.data_dir, self.masks_dir, filename),
                                os.path.join(self.validate_dir, self.masks_dir, filename))
            if row['split'] == 'test':
                shutil.copyfile(os.path.join(self.data_dir, self.images_dir, filename),
                                os.path.join(self.test_dir, self.images_dir, filename))
                shutil.copyfile(os.path.join(self.data_dir, self.masks_dir, filename),
                                os.path.join(self.test_dir, self.masks_dir, filename))

    # def split_dataset_nl(self):
    #     file_names = list(os.listdir(os.path.join(self.data_dir, self.images_dir)))
    #     file_names = [file.replace("tile-", "") for file in file_names]
    #
    #     lower_split_index = int(self.split_1 * len(file_names))
    #     upper_split_index = int(self.split_2 * len(file_names))
    #     np.random.seed(42)
    #     np.random.shuffle(file_names)
    #
    #     collect = {}
    #     collect.update(dict(zip(file_names[:lower_split_index], cycle(['train']))))
    #     collect.update(dict(zip(file_names[lower_split_index:upper_split_index], cycle(['validate']))))
    #     collect.update(dict(zip(file_names[upper_split_index:], cycle(['test']))))
    #
    #     for key, value in collect.items():
    #         if value == 'train':
    #             shutil.copyfile(os.path.join(self.data_dir, self.images_dir, "tile-" + key),
    #                             os.path.join(self.train_dir, self.images_dir, "tile-" + key))
    #             shutil.copyfile(os.path.join(self.data_dir, self.masks_dir, "tile-" + key),
    #                             os.path.join(self.train_dir, self.masks_dir, "mask-" + key))
    #         if value == 'validate':
    #             shutil.copyfile(os.path.join(self.data_dir, self.images_dir, "tile-" + key),
    #                             os.path.join(self.validate_dir, self.images_dir, "tile-" + key))
    #             shutil.copyfile(os.path.join(self.data_dir, self.masks_dir, "tile-" + key),
    #                             os.path.join(self.validate_dir, self.masks_dir, "mask-" + key))
    #         if value == 'test':
    #             shutil.copyfile(os.path.join(self.data_dir, self.images_dir, "tile-" + key),
    #                             os.path.join(self.test_dir, self.images_dir, "tile-" + key))
    #             shutil.copyfile(os.path.join(self.data_dir, self.masks_dir, "tile-" + key),
    #                             os.path.join(self.test_dir, self.masks_dir, "mask-" + key))
