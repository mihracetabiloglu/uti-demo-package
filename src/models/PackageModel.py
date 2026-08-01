from typing import List, Optional, Union, Literal
from pydantic import Field, validator
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, 
    Response, Request, Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        if isinstance(val, Image):
            return "object"
        elif isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Input Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        if isinstance(val, Image):
            return "object"
        elif isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Output Image"


class AnalyticsLog(Output):
    name: Literal["analyticsLog"] = "analyticsLog"
    value: str = ""
    type: Literal["string"] = "string"

    class Config:
        title = "Analytics Log"


class GaussianBlur(Config):
    name: Literal["Gaussian"] = "Gaussian"
    kernelSize: int = Field(default=5)
    sigma: float = Field(default=1.0)
    value: Literal["Gaussian"] = "Gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Gaussian Blur"


class Canny(Config):
    name: Literal["Canny"] = "Canny"
    threshold: int = Field(default=100)
    padding: bool = Field(default=True)
    value: Literal["Canny"] = "Canny"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Canny Edge Detection"


class FilterType(Config):
    name: Literal["FilterType"] = "FilterType"
    value: Union[GaussianBlur, Canny]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Filter Selection"


class FrameProcessorExecutorInputs(Inputs):
    inputImage: InputImage


class FrameProcessorExecutorConfigs(Configs):
    filterType: FilterType


class FrameProcessorExecutorOutputs(Outputs):
    outputImage: OutputImage


class FrameProcessorExecutorRequest(Request):
    inputs: Optional[FrameProcessorExecutorInputs]
    configs: FrameProcessorExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class FrameProcessorExecutorResponse(Response):
    outputs: FrameProcessorExecutorOutputs


class FrameProcessorExecutor(Config):
    name: Literal["FrameProcessorExecutor"] = "FrameProcessorExecutor"
    value: Union[FrameProcessorExecutorRequest, FrameProcessorExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Frame Processor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class YOLOv8(Config):
    name: Literal["YOLOv8"] = "YOLOv8"
    modelPath: str = Field(default="yolov8n.pt")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    value: Literal["YOLOv8"] = "YOLOv8"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "YOLOv8 Model"


class HaarCascade(Config):
    name: Literal["HaarCascade"] = "HaarCascade"
    cascadeFile: str = Field(default="haarcascade.xml")
    scaleFactor: float = Field(default=1.1)
    value: Literal["HaarCascade"] = "HaarCascade"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Haar Cascade Model"


class ModelType(Config):
    name: Literal["ModelType"] = "ModelType"
    value: Union[YOLOv8, HaarCascade]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Model Selection"


class TargetLabels(Config):
    name: Literal["TargetLabels"] = "TargetLabels"
    value: str = Field(default="car")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Target Labels"


class IntrusionTrackerExecutorInputs(Inputs):
    inputImage: InputImage


class IntrusionTrackerExecutorConfigs(Configs):
    modelType: ModelType
    targetLabels: TargetLabels


class IntrusionTrackerExecutorOutputs(Outputs):
    outputImage: OutputImage
    analyticsLog: AnalyticsLog


class IntrusionTrackerExecutorRequest(Request):
    inputs: Optional[IntrusionTrackerExecutorInputs]
    configs: IntrusionTrackerExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class IntrusionTrackerExecutorResponse(Response):
    outputs: IntrusionTrackerExecutorOutputs


class IntrusionTrackerExecutor(Config):
    name: Literal["IntrusionTrackerExecutor"] = "IntrusionTrackerExecutor"
    value: Union[IntrusionTrackerExecutorRequest, IntrusionTrackerExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Intrusion Tracker"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FrameProcessorExecutor, IntrusionTrackerExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Select Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["UtiDemoPackage"] = "UtiDemoPackage"