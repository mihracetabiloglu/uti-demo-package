from typing import Literal, Optional, Union
from sdks.novavision.src.base.model import Package, Images, Inputs, Configs, Outputs, Response, Request, Config, Input, Output

# --- GİRDİ VE ÇIKTI TİPLERİ ---
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Images
    type: Literal["Images"] = "Images"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Images
    type: Literal["Images"] = "Images"

class InputMetadata(Input):  
    name: Literal["targetLabels"] = "targetLabels"  # 's' takısı düzeltildi (Component ile birebir eşleştirildi)
    value: str = "human"
    type: Literal["str"] = "str"

class OutputLogs(Output):
    name: Literal["analyticsLog"] = "analyticsLog"
    value: str
    type: Literal["str"] = "str"

# --- 1. EXECUTOR (FRAME PROCESSOR) ---

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
        schema_extra = {"target": "value"}

class ProcessorConfigs(Configs):
    filtertype: FilterType

class ProcessorConfigsInput(Inputs):
    inputImage: InputImage

class ProcessorConfigsOutput(Outputs):
    outputImage: OutputImage

class ProcessorExecutorRequest(Request):
    inputs: ProcessorConfigsInput
    configs: ProcessorConfigs
    class Config:
        schema_extra = {"target": "configs"}

class ProcessorExecutorResponse(Response):
    outputs: ProcessorConfigsOutput

class FrameProcessorExecutor(Config):
    name: Literal["FrameProcessorExecutor"] = "FrameProcessorExecutor"
    value: Union[ProcessorExecutorRequest, ProcessorExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "FrameProcessorExecutor"
        schema_extra = {"target": {"value": "configs"}}


# ----------- 2. EXECUTOR (TRACKER) ---------

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
        schema_extra = {"target": "value"}

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
        schema_extra = {"target": "configs"}

class TrackerExecutorResponse(Response):
    outputs: TrackerOutputs

class IntrusionTrackerExecutor(Config):
    name: Literal["IntrusionTrackerExecutor"] = "IntrusionTrackerExecutor"
    value: Union[TrackerExecutorRequest, TrackerExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "IntrusionTrackerExecutor"
        schema_extra = {"target": {"value": "configs"}}


# --- ANA PAKET ---

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FrameProcessorExecutor, IntrusionTrackerExecutor] 
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        schema_extra = {"target": "value"}

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["capsule"] = "capsule"
    name: Literal["SmartGuardPackage"] = "SmartGuardPackage"
    uID: str = "1331112"