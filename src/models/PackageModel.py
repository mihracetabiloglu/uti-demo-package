from pydantic import Field
from typing import List, Union, Literal, Optional
from sdks.novavision.src.base.model import Package, Config, Inputs, Configs, Outputs, Output, Input, Image, Request, Response

# ==========================================
# 1. FRAME PROCESSOR EXECUTOR - INPUTS
# ==========================================
class ProcessorInputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "Input Image"


class FrameProcessorInputs(Inputs):
    inputImage: ProcessorInputImage


# ==========================================
# 2. FRAME PROCESSOR EXECUTOR - CONFIGS
# ==========================================
class GaussianBlur(Config):
    name: Literal["Gaussian"] = "Gaussian"
    kernel_size: int = 5
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


class FrameProcessorConfigs(Configs):
    filterType: FilterType = Field(default_factory=FilterType)


# ==========================================
# 3. FRAME PROCESSOR EXECUTOR - OUTPUTS
# ==========================================
class ProcessorOutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "Output Image"


class FrameProcessorOutputs(Outputs):
    outputImage: ProcessorOutputImage


# ==========================================
# 4. FRAME PROCESSOR EXECUTOR - REQUEST/RESPONSE
# ==========================================
class FrameProcessorRequest(Request):
    inputs: Optional[FrameProcessorInputs] = None
    configs: FrameProcessorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}


class FrameProcessorResponse(Response):
    outputs: FrameProcessorOutputs


# ==========================================
# 5. INTRUSION TRACKER EXECUTOR - INPUTS
# ==========================================
class TrackerInputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "Input Image"


class IntrusionTrackerInputs(Inputs):
    inputImage: TrackerInputImage


# ==========================================
# 6. INTRUSION TRACKER EXECUTOR - CONFIGS
# ==========================================
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
    value: str = "human"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Target Labels"


class IntrusionTrackerConfigs(Configs):
    modelType: ModelType
    targetLabels: TargetLabels


# ==========================================
# 7. INTRUSION TRACKER EXECUTOR - OUTPUTS
# ==========================================
class TrackerOutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "Output Image"


class AnalyticsLog(Output):
    name: Literal["analyticsLog"] = "analyticsLog"
    value: str = ""
    type: str = "string"
    class Config:
        title = "Analytics Log"


class IntrusionTrackerOutputs(Outputs):
    outputImage: TrackerOutputImage
    analyticsLog: AnalyticsLog


# ==========================================
# 8. INTRUSION TRACKER EXECUTOR - REQUEST/RESPONSE
# ==========================================
class IntrusionTrackerRequest(Request):
    inputs: Optional[IntrusionTrackerInputs] = None
    configs: IntrusionTrackerConfigs
    class Config:
        json_schema_extra = {"target": "configs"}


class IntrusionTrackerResponse(Response):
    outputs: IntrusionTrackerOutputs


# ==========================================
# 9. EXECUTORS SELECTION
# ==========================================
class FrameProcessorExecutor(Config):
    name: Literal["FrameProcessorExecutor"] = "FrameProcessorExecutor"
    value: Union[FrameProcessorRequest, FrameProcessorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Frame Processor"
        json_schema_extra = {"target": {"value": 0}}


class IntrusionTrackerExecutor(Config):
    name: Literal["IntrusionTrackerExecutor"] = "IntrusionTrackerExecutor"
    value: Union[IntrusionTrackerRequest, IntrusionTrackerResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Intrusion Tracker"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FrameProcessorExecutor, IntrusionTrackerExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Select Task"


# ==========================================
# 10. PACKAGE MODEL
# ==========================================
class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"