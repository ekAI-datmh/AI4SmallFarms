
## Authors
Claudio Persello,
Jeroen Grift,
Xinyan Fan,
Claudia Paris,
Ronny Hänsch,
Mila Koeva and
Andy Nelson

## Paper
- The related paper is available here: https://ieeexplore.ieee.org/document/10278130
- The related benchmark dataset is available here: https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:321745

To cite the paper/benchmark dataset, please use this bib file:
```
@article{ai4small,
  title={AI4SmallholderFarms: A Large-scale Data Set for Crop Field Delineation in Smallholder Farms in Southeast Asia},
  author={Persello, Claudio and Grift, Jeroen and Xinyan, Fan and Paris, Claudia and Hänsch, Ronny and Koeva, Mila and Nelson, Andy},
  journal={{IEEE GEOSCIENCE AND REMOTE SENSING LETTERS},
  volume={}
  number={}
  pages={}
  year={}
}
```

## Pipeline requirements
Before running the pipeline, you need to install external Python packages within a conda environment. Run the following commands in the project directory: 

```
conda env create -f environment.yml
conda activate ai4small
```

## Pipeline configuration
Before running the pipeline, you need to configure some variables in the base.py file. These are the most important:

```
INPUT_DIR: Input directory of the data
AREA: Area to analyse, Asia/NL
SOURCE: Source data, S2/Google
IMAGE_SIZE: The image size of the patches that will be created
NUM_CHANNELS: The number of channels of the imagery, a14small uses 3 channels

MODEL: The deep learning model to use, satellite_unet/custom_unet
FROM_SCRATCH: When training from scratch, set this to True
BATCH_SIZE: Batch size used in the experiment
LEARNING_RATE: Learning rate used in the experiment
EPOCHS: Maximum number of epochs. However, because we use early stopping, it is not very likely that we train for 1000 epochs
PATIENCE: Stop training if the model is not improved after this number of epochs
BIN_THRESHOLD: Threshold for binary classification after the output activation

BEST_NL_S2: The pre-trained weights for NL/S2 in .h5 format
BEST_ASIA_S2: The pre-trained weights for Asia/S2 in .h5 format
BEST_ASIA_S2_SCRATCH: The pre-trained weights for Asia/S2 in .h5 format
BEST_ASIA_GOOGLE: The pre-trained weights for Asia/Google in .h5 format

VISUALIZE_PREDICTIONS: Plot predictions during the prediction step
WRITE_PREDICTIONS: Save the predictions as .tif files
```

## Pipeline steps
* Split dataset: splits the data in the train, validate and test set. These splits are predetermined in input/tilesAsia.gpkg. The dataset in DANS is already split into these three parts, so when using the AI4SmallFarms dataset, this step can be skipped.
* Create patches: Because the original image tiles are too big and do not have a standard size, we need to create smaller image patches. It creates patches for the train, validate and test directory. 
* Create model: 
* Train model
* Evaluate model
* Make predictions
