from pydantic import Field
from typing import List, Union, Literal, Optional
from sdks.novavision.src.base.model import Package, Config, Inputs, Configs, Outputs, Output, Input, Image, Request, Response

class ProcessorInputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: Literal["object"] = "object"
    class Config:
        title = "Input Image"

class FrameProcessorExecutorInputs(Inputs):
    inputImage: ProcessorInputImage

class GaussianBlur(Config):
    name: Literal["Gaussian"] = "Gaussian"
    kernelSize: int = 5
    sigma: float = 1.0
    value: Literal["Gaussian"] = "Gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Gaussian Blur"

class Canny(Config):
    name: Literal["Canny"] = "Canny"
    threshold: int = 100
    padding: bool = True
    value: Literal["Canny"] = "Canny"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Canny Edge Detection"

class FilterType(Config):
    name: Literal["FilterType"] = "FilterType"
    value: Union[GaussianBlur, Canny] = Field(default=None)
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Filter Selection"

class FrameProcessorExecutorConfigs(Configs):
    filterType: FilterType = Field(default_factory=FilterType)

class ProcessorOutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: Literal["object"] = "object"
    class Config:
        title = "Output Image"

class FrameProcessorExecutorOutputs(Outputs):
    outputImage: ProcessorOutputImage

class FrameProcessorExecutorRequest(Request):
    inputs: Optional[FrameProcessorExecutorInputs] = None
    configs: FrameProcessorExecutorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class FrameProcessorExecutorResponse(Response):
    outputs: FrameProcessorExecutorOutputs

class TrackerInputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: Literal["object"] = "object"
    class Config:
        title = "Input Image"

class IntrusionTrackerExecuterInputs(Inputs):
    inputImage: TrackerInputImage

class YOLOv8(Config):
    name: Literal["YOLOv8"] = "YOLOv8"
    modelPath: str = "yolov8n.pt"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    value: Literal["YOLOv8"] = "YOLOv8"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "YOLOv8 Model"

class HaarCascade(Config):
    name: Literal["HaarCascade"] = "HaarCascade"
    cascadeFile: str = "haarcascade.xml"
    scaleFactor: float = 1.1
    value: Literal["HaarCascade"] = "HaarCascade"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Haar Cascade Model"

class ModelType(Config):
    name: Literal["ModelType"] = "ModelType"
    value: Union[YOLOv8, HaarCascade] = Field(default_factory=YOLOv8)
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Model Selection"

class TargetLabels(Config):
    name: Literal["TargetLabels"] = "TargetLabels"
    value: str = "car"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Target Labels"

class IntrusionTrackerExecutorConfigs(Configs):
    modelType: ModelType
    targetLabels: TargetLabels

class IntrusionTrackerExecutorOutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: Literal["object"] = "object"
    class Config:
        title = "Output Image"

class AnalyticsLog(Output):
    name: Literal["analyticsLog"] = "analyticsLog"
    value: str = ""
    type: Literal["string"] = "string"
    class Config:
        title = "Analytics Log"

class IntrusionTrackerExecutorOutputs(Outputs):
    outputImage: IntrusionTrackerExecutorOutputImage
    analyticsLog: AnalyticsLog

class IntrusionTrackerExecutorRequest(Request):
    inputs: Optional[IntrusionTrackerExecuterInputs] = None
    configs: IntrusionTrackerExecutorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class IntrusionTrackerExecutorResponse(Response):
    outputs: IntrusionTrackerExecutorOutputs

class FrameProcessorExecutor(Config):
    name: Literal["FrameProcessorExecutor"] = "FrameProcessorExecutor"
    value: Union[FrameProcessorExecutorRequest, FrameProcessorExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Frame Processor"
        json_schema_extra = {"target": {"value": 0}}

class IntrusionTrackerExecutor(Config):
    name: Literal["IntrusionTrackerExecutor"] = "IntrusionTrackerExecutor"
    value: Union[IntrusionTrackerExecutorRequest, IntrusionTrackerExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Package"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FrameProcessorExecutor, IntrusionTrackerExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Select Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
  