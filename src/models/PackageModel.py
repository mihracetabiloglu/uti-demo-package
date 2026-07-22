from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

# ==========================================
# 1. GİRDİ VE ÇIKTI TİPLERİ (SOCKETS)
# ==========================================

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

    class Config:
        title = "Image"


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

    class Config:
        title = "Image"


class InputMetadata(Input):  
    name: Literal["targetLabels"] = "targetLabels"
    value: str = "human"
    type: Literal["str"] = "str"

    class Config:
        title = "Target Labels"


class OutputLogs(Output):
    name: Literal["analyticsLog"] = "analyticsLog"
    value: str
    type: Literal["str"] = "str"

    class Config:
        title = "Analytics Log"


# ==========================================
# 2. FRAME PROCESSOR EXECUTOR
# ==========================================

class GaussianBlur(Config):
    name: Literal["Gaussian"] = "Gaussian"
    kernel_size: int = 5
    sigma: float = 1.0
    type: Literal["object"] = "object"  
    field: Literal["option"] = "option"

    class Config:
        title = "GaussianBlur"


class Canny(Config):
    name: Literal["Canny"] = "Canny"
    threshold: int = 100
    padding: bool = True
    type: Literal["object"] = "object"  
    field: Literal["option"] = "option"

    class Config:
        title = "Canny"


class FilterType(Config):
    name: Literal["FilterType"] = "FilterType"
    value: Union[GaussianBlur, Canny]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Filtre Seçimi"
        json_schema_extra = {
            "target": "value"
        }


class ProcessorConfigs(Configs):
    filterType: FilterType


class ProcessorConfigsInput(Inputs):
    inputImage: InputImage


class ProcessorConfigsOutput(Outputs):
    outputImage: OutputImage


class ProcessorExecutorRequest(Request):
    inputs: Optional[ProcessorConfigsInput]
    configs: ProcessorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class ProcessorExecutorResponse(Response):
    outputs: ProcessorConfigsOutput


class FrameProcessorExecutor(Config):
    name: Literal["FrameProcessorExecutor"] = "FrameProcessorExecutor"
    value: Union[ProcessorExecutorRequest, ProcessorExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "FrameProcessorExecutor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# ==========================================
# 3. INTRUSION TRACKER EXECUTOR
# ==========================================

class YOLOFields(Config):
    name: Literal["YOLOv8"] = "YOLOv8"
    modelPath: str = "yolov8n.pt"
    confidence: float = 0.5
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "YOLOv8"


class HaarFields(Config):
    name: Literal["HaarCascade"] = "HaarCascade"
    cascadeFile: str = "haarcascade_frontalface_default.xml"
    scaleFactor: float = 1.1
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "HaarCascade"


class TrackerConfig(Config):
    name: Literal["TrackerConfig"] = "TrackerConfig"
    value: Union[YOLOFields, HaarFields]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Model Tipi"
        json_schema_extra = {
            "target": "value"
        }


class TrackerConfigs(Configs):
    modelType: TrackerConfig


class TrackerInputs(Inputs):
    inputImage: InputImage
    targetLabels: InputMetadata


class TrackerOutputs(Outputs):
    outputImage: OutputImage
    analyticsLog: OutputLogs


class TrackerExecutorRequest(Request):
    inputs: Optional[TrackerInputs]
    configs: TrackerConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class TrackerExecutorResponse(Response):
    outputs: TrackerOutputs


class IntrusionTrackerExecutor(Config):
    name: Literal["IntrusionTrackerExecutor"] = "IntrusionTrackerExecutor"
    value: Union[TrackerExecutorRequest, TrackerExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "IntrusionTrackerExecutor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# ==========================================
# 4. ANA PAKET VE EXECUTOR SEÇİMİ
# ==========================================

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FrameProcessorExecutor, IntrusionTrackerExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["Package"] = "Package_v2"