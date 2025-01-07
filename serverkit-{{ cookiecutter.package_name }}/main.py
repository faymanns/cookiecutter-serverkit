from typing import List, Literal, Type
from pathlib import Path
import numpy as np
from pydantic import BaseModel, Field, field_validator
import uvicorn
import skimage.io
import imaging_server_kit as serverkit

# Import your library
import {{ cookiecutter.package_name }}

# Define a Pydantic BaseModel to validate your algorithm parameters
class Parameters(BaseModel):
    """Defines the algorithm parameters"""
    image: str = Field(
        ...,
        title="Image",
        description="Input image (2D, 3D).",
        json_schema_extra={"widget_type": "image"},
    )
    model_name: Literal['model1', 'model2'] = Field(
        ...,
        title="Model",
        description="Model description.",
        json_schema_extra={"widget_type": "dropdown"},
    )
    threshold: float = Field(
        default=0.5,
        title="Threshold",
        description="",
        ge=0.0,  # Greater or equal to
        le=1.0,  # Lower or equal to
        json_schema_extra={
            "widget_type": "float", 
            "step": 0.05,  # The incremental step to use in the widget (only applicable to numbers)
        },
    )
    # Numpy arrays should be validated:
    @field_validator("image", mode="after")
    def decode_image_array(cls, v) -> np.ndarray:
        image_array = serverkit.decode_contents(v)
        if image_array.ndim not in [2, 3]:
            raise ValueError("Array has the wrong dimensionality.")
        return image_array

# Define the run_algorithm() method for your algorithm
class Server(serverkit.Server):
    def __init__(
        self,
        algorithm_name: str="{{ cookiecutter.package_name }}",
        parameters_model: Type[BaseModel]=Parameters
    ):
        super().__init__(algorithm_name, parameters_model)

    def run_algorithm(
        self,
        image: np.ndarray,
        model_name: str,
        threshold: float,  # Note: do not add default values here; instead, add them as `default=` in the Parameters model.
        **kwargs
    ) -> List[tuple]:
        """ Runs the algorithm. """
        segmentation = np.zeros_like(image)  # Adjust as necessary

        segmentation_params = {}

        return [(segmentation, segmentation_params, "labels")]

    def load_sample_images(self) -> List["np.ndarray"]:
        """Load one or multiple sample images."""
        image_dir = Path(__file__).parent / "sample_images"
        images = [skimage.io.imread(image_path) for image_path in image_dir.glob("*")]
        return images

server = Server()
app = server.app

if __name__=='__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)