from typing import Literal, Optional, Union
from sdks.novavision.src.base.model import Package, Images, Inputs, Configs, Outputs, Response, Request, Config, Input, Output

# ==========================================
# 1. GİRDİ VE ÇIKTI TİPLERİ (SOCKETS)
# ==========================================

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Images
    type: Literal["Images"] = "Images"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Images
    type: Literal["Images"] = "Images"

class InputMetadata(Input):
    name: Literal["targetLabels"] = "targetLabels"
    value: str = "human"
    type: Literal["str"] = "str"

class OutputLogs(Output):
    name: Literal["analyticsLog"] = "analyticsLog"
    value: str = ""
    type: Literal["str"] = "str"


# ==========================================
# 2. FRAME PROCESSOR EXECUTOR
# ==========================================

class GaussianBlur(Config):
    name: Literal["Gaussian"] = "Gaussian"
    kernel_size: int = 5
    sigma: float = 1.0
    value: None = None          # <-- EKLENDİ, UI'da görünmez
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "GaussianBlur"

class Canny(Config):
    name: Literal["Canny"] = "Canny"
    threshold: int = 100
    padding: bool = True
    value: None = None          # <-- EKLENDİ
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Canny"

class FilterType(Config):
    name: Literal["FilterType"] = "FilterType"
    value: Union[GaussianBlur, Canny] = GaussianBlur()
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Filtre Seçimi"
        schema_extra = {"target": "value"}   # dropdownlist için gerekli

class ProcessorConfigs(Configs):
    filtertype: FilterType = FilterType()

class ProcessorConfigsInput(Inputs):
    inputImage: InputImage = InputImage()

class ProcessorConfigsOutput(Outputs):
    outputImage: OutputImage = OutputImage()

class ProcessorExecutorRequest(Request):
    inputs: Optional[ProcessorConfigsInput] = ProcessorConfigsInput()
    configs: ProcessorConfigs = ProcessorConfigs()
    # schema_extra YOK (böylece inputs ve configs birlikte render olur)

class ProcessorExecutorResponse(Response):
    outputs: ProcessorConfigsOutput = ProcessorConfigsOutput()

class FrameProcessorExecutor(Config):
    name: Literal["FrameProcessorExecutor"] = "FrameProcessorExecutor"
    value: Union[ProcessorExecutorRequest, ProcessorExecutorResponse] = ProcessorExecutorRequest()
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "FrameProcessorExecutor"
        schema_extra = {"target": {"value": 0}}   # 0. eleman (Request) seçili


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
    value: Union[YOLOFields, HaarFields] = YOLOFields()
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Model Tipi"
        schema_extra = {"target": "value"}

class TrackerConfigs(Configs):
    modelType: TrackerConfig = TrackerConfig()

class TrackerInputs(Inputs):
    inputImage: InputImage = InputImage()
    targetLabels: InputMetadata = InputMetadata()

class TrackerOutputs(Outputs):
    outputImage: OutputImage = OutputImage()
    analyticsLog: OutputLogs = OutputLogs()

class TrackerExecutorRequest(Request):
    inputs: Optional[TrackerInputs] = TrackerInputs()
    configs: TrackerConfigs = TrackerConfigs()
    # schema_extra YOK

class TrackerExecutorResponse(Response):
    outputs: TrackerOutputs = TrackerOutputs()

class IntrusionTrackerExecutor(Config):
    name: Literal["IntrusionTrackerExecutor"] = "IntrusionTrackerExecutor"
    value: Union[TrackerExecutorRequest, TrackerExecutorResponse] = TrackerExecutorRequest()
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "IntrusionTrackerExecutor"
        schema_extra = {"target": {"value": 0}}   # 0. eleman (Request) seçili


# ==========================================
# 4. ANA PAKET VE EXECUTOR SEÇİMİ
# ==========================================

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FrameProcessorExecutor, IntrusionTrackerExecutor] = FrameProcessorExecutor()
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        # schema_extra KESİNLİKLE YOK (dokümana uygun)

class PackageConfigs(Configs):
    executor: ConfigExecutor = ConfigExecutor()

class PackageModel(Package):
    configs: PackageConfigs = PackageConfigs()
    type: Literal["capsule"] = "capsule"
    name: Literal["SmartGuardPackage"] = "SmartGuardPackage"
    uID: str = "1331112"