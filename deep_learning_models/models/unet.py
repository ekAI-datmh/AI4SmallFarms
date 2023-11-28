import tensorflow as tf
import segmentation_models as sm
from keras_unet.models import satellite_unet, custom_unet
from base import *


class Unet(Base):
    def _custom__unet(self):
        # https://github.com/karolzak/keras-unet/blob/master/keras_unet/models/vanilla_unet
        cu_model = custom_unet(input_shape=(None, None, self.num_channels),
                               num_classes=1,
                               num_layers=5,
                               output_activation='sigmoid')
        return cu_model

    def _satellite__unet(self):
        # https://github.com/karolzak/keras-unet/blob/master/keras_unet/models/satellite_unet
        su_model = satellite_unet(input_shape=(None, None, self.num_channels),
                                  num_classes=1,
                                  num_layers=5,
                                  output_activation='sigmoid')
        return su_model

    def _get_model_config(self):
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=self.LEARNING_RATE,
            decay_steps=10000,
            decay_rate=.9)

        optimizer_ = tf.keras.optimizers.Adam(lr_schedule)
        loss_ = tf.keras.losses.BinaryFocalCrossentropy()
        metrics_ = [tf.keras.metrics.Recall(thresholds=self.BIN_THRESHOLD),
                    tf.keras.metrics.Precision(thresholds=self.BIN_THRESHOLD),
                    sm.metrics.FScore(threshold=self.BIN_THRESHOLD),
                    sm.metrics.IOUScore(threshold=self.BIN_THRESHOLD)
                    ]

        return optimizer_, loss_, metrics_

    def create_model(self):
        if self.model == 'custom_unet':
            model = Unet()._custom__unet()
            model.save(os.path.join(self.model_dir, f'{self.model}_{self.num_channels}'))

        if self.model == 'satellite_unet':
            model = Unet()._satellite__unet()
            model.save(os.path.join(self.model_dir, f'{self.model}_{self.num_channels}'))

    def load_model(self):
        model = tf.keras.models.load_model(os.path.join(self.model_dir, f'{self.model}_{self.num_channels}'),
                                           compile=False)

        optimizer, loss, metrics = self._get_model_config()
        model.compile(optimizer, loss, metrics)

        return model
