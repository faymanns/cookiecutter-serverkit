![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🪐 Algorithm Server Template

Use this [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template to jumpstart the creation of your own Imaging Server Kit algorithm server.

## Usage

First, install `cookiecutter`:

```
pip install cookiecutter
```

Then, run it to create a new algorithm server project:

```
cookiecutter https://github.com/Imaging-Server-Kit/cookiecutter-serverkit
```

You'll be asked to provide:

- **project_name**: The name of the algorithm or project (e.g. StarDist)
- **project_url**: A URL to the original project homepage
- **project_slug**: A lowercase, URL-friendly name for your project
- **author**: The author to credit for the algorithm server project development
- **python_version**: The Python version to use

Running the cookiecutter will generate the following file structure for your algorithm server project:

```
serverkit-project-slug
├── sample_images               # Sample images
│   ├──blobs.tif
├── tests                       # Tests (pytest)
│   ├──test_run_algorithm.py
└── .gitignore
└── docker-compose.yml
└── Dockerfile
└── main.py                     # Implementation of the algorithm server
└── metadata.yaml               # Project metadata
└── README.md
└── requirements.txt
```

After generating the project, you should customize these files to implement the desired functionality of your algorithm server.

### Editing `main.py`

The `main.py` file implements a `Server` class for your algorithm, inheriting from the Imaging Server Kit's `Server` class. Moreover, it defines a `Parameters` model for your algorithm as a Pydantic `BaseModel`.

**Parameters**

The Parameters model is used to validate algorithm parameters that are sent as input to the processing endpoint of the server. If something is wrong with the parameters (for example, a `threshold` parameter exceeds the maximum value), the server will reply with a `403` error and an informative message will be displayed to the user.

The **class attributes** of the Parameters model should match the parameters of your server's `run_algorithm` method (see below).

The Parameters model also provides default values, and metadata (title, description...) about each parameter. Finally, it provides information on how the user interface should look in client apps (dropdown, float slider, etc.) for each parameter.

Here is the example from the template:

```{python}
class Parameters(BaseModel):
    """Defines the algorithm parameters"""
    image: str = Field(
        ...,
        title="Image",
        description="Input image (2D, 3D).",
        json_schema_extra={"widget_type": "image"},
    )
    model_name: Literal['model1', 'model2'] = Field(
        default='model1',
        title="Model",
        description="Model description.",
        json_schema_extra={"widget_type": "dropdown"},
    )
    threshold: float = Field(
        default=100.0,
        title="Threshold",
        description="",
        ge=0.0,  # Greater or equal to
        le=255.0,  # Lower or equal to
        json_schema_extra={
            "widget_type": "float", 
            "step": 1.0,  # The incremental step to use in the widget (only applicable to numbers)
        },
    )
    # Numpy arrays should be validated:
    @field_validator("image", mode="after")
    def decode_image_array(cls, v) -> np.ndarray:
        image_array = serverkit.decode_contents(v)
        if image_array.ndim not in [2, 3]:
            raise ValueError("Array has the wrong dimensionality.")
        return image_array
```

This example shows how to validate three parameters:

- `image`: Input image. Numpy arrays, such as the input image, are sent to the server as byte strings. To validate properties of the (decoded) image, such as its dimensionality or intensity range, a `field_validator` can be used (see the example in the template). The three dots (`...`) indicate that this parameter is required, but *does not* have a default value.
- `model_name`: A choice of values, such as the model name, can be represented using `Literal['v1', 'v2']` and a `widget_type: "dropdown"`.
- `threshold`: A numeric value, such as a threshold, can be represented as a `widget_type: "float"`.

Supported widget types:

- `bool`
- `float`
- `int`
- `str`
- `dropdown`
- `image`
- `labels`
- `points`
- `shapes`
- `vectors`
- `tracks`

**run_algorithm**

Your algorithm server class should implement the `run_algorithm()` method. Function parameters should match the class attributes of the Pydantic `Parameters` model, which define the input parameters of your algorithm.

Here is the example from the template:

```{python}
    def run_algorithm(
        self,
        image: np.ndarray,
        model_name: str,
        threshold: float,  # No need to add default values here; instead, add them as `default=` in the Parameters model.
        **kwargs
    ) -> List[tuple]:
        """Runs the algorithm."""
        segmentation = image > threshold  # Adjust as necessary

        segmentation_params = {"name": "Threshold result"}  # Add information about the result (optional)
        
        return [(segmentation, segmentation_params, "labels")]  # Choose the right output type (`labels` for a segmentation mask)
```

The body of the function should handle running your algorithm.

The **return type** of the function should be a list of tuples ("data tuples"). Each data tuple represents an output of your algorithm.

The data tuples follow the convention defined by Napari's [LayerDataTuple](https://napari.org/0.4.15/guides/magicgui.html?highlight=layerdatatuple) annotation.
- The *first element* of the tuple is the data in the form of a Numpy array. 
- The *second element* is a dictionnary of parameters associated with the output, which can affect how the output is displayed in client apps. For example:
  - `{"name": "Detected Keypoints"}
- The *third element* represents the type of output: 
  - `image`: An image or image-like data (incl. 3D and RGB) as a nD array
  - `labels`: A segmentation mask (2D, 3D) as integer nD array. Integers represent the **object class**.
  - `instance_mask`: A segmentation mask (2D, 3D) as integer nD array. Integers represent **object instances**.
  - `points`: A collection of point coordinates (array of shape (N, 2) or (N, 3))
  - `boxes`: A collection of boxes (array of shape (N, 4))
  - `vectors`: Array of vectors in the Napari Vectors data format
  - `tracks`: Array of tracks in the Napari Tracks data format
  - `class`: A class label (for image classification)
  - `text`: A string of text (for example, for image captioning)


**load_sample_image**

Your server class should also implement the `load_sample_images()` method to define how the sample images are loaded (see dedicated section below).

### Editing `metadata.yaml`

This metadata file gathers information about the algorithm, which is displayed at the server's `/info` endpoint. Most of it should already be pre-filled from the cookiecutter template. Extra fields to edit include:

| Key           | Description                                                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `description` | A brief description of what the algorithm is used for                                                                            |
| `used_for`    | A list of tags from: `Segmentation`, `Registration`, `Filtering`, `Tracking`, `Restoration`, `Points detection`, `Box detection` |
| `tags`        | Extra tags used to categorize the algorithm, for example `Deep learning`, `EPFL`, `Cell biology`, `Digital pathology`            |

### Providing `sample images`

The images included in the `sample_images/` folder are served at the server's `/sample_images` endpoint. By default, they are read using the `skimage.io.imread` function, which is compatible with most common image formats (`.tif`, `.png`, `.jpg`). To match specific use cases, the `load_sample_images()` method in `main.py` can be edited.

We recommend to provide only **small** sample images as (for now) they are included in the Git repository of the algorithm server.

The license terms of the sample images used should be respected. For example, for images under [CC-BY](https://creativecommons.org/licenses/by/2.0/deed.en) license, proper attribution should be included.

### Writing `unit tests`

The template includes an example test in the `tests/` folder. You can use this test to verify that the algorithm runs successfully on the provided sample images and returns the expected results. Other unit tests can be added if necessary.

### Other files to edit

Consider editing the `requirements.txt`, `Dockerfile`, and `README.md` to match your use case.

## Contributing

Contributions are very welcome.

## License

This software is distributed under the terms of the [BSD-3](http://opensource.org/licenses/BSD-3-Clause) license.

## Issues

If you encounter any problems, please file an issue along with a detailed description.
