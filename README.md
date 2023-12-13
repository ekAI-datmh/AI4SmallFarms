
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

## Pipeline steps
Before running the pipeline, you need to configure some variables in the base.py file. These are the most important:

```
INPUT_DIR: Input directory of data
AREA: Area to analyse, Asia or NL
SOURCE: Source data, S2 or Google
IMAGE_SIZE: The image size of the patches that you want to create and use as model input
NUM_CHANNELS: 3
MODEL = SelectedModel.SATELLITE_UNET
FROM_SCRATCH = True
BATCH_SIZE = 1
LEARNING_RATE = 1e-4
EPOCHS = 1000
PATIENCE = 10
BIN_THRESHOLD = .5

```

* Split dataset: splits the data in the train, validate and test set. These splits are predetermined in input/tilesAsia.gpkg. The dataset in DANS is already split into these three parts.
* Create patches: Because the original image tiles are too big and do not have a standard size, we need to create smaller image patches. In this step 
* Create model
* Train model
* Evaluate model
* Make predictions
