from typing import Literal, Optional, Union
from sdks.novavision.src.base.model import Package, Images, Inputs, Configs, Outputs, Response, Request, Config, Input, Output

# --- GİRDİ VE ÇIKTI TİPLERİ ---
class InputImage(Input):  # 1. executor için girdi (ham resim)
    name: Literal["inputImage"] = "inputImage"
    value: Images
    type: Literal["Images"] = "Images"

class OutputImage(Output):  # 1. executor için çıktı (temizlenmiş resim)
    name: Literal["outputImage"] = "outputImage"
    value: Images
    type: Literal["Images"] = "Images"

class InputMetadata(Input):  # 2. Giriş (Aranacak Nesne Adı)
    name: Literal["targetLabel"] = "targetLabel"
    value: str = "human"
    type: Literal["str"] = "str"

class OutputLogs(Output):    # 2. Çıkış (Analiz Raporu/Yazı)
    name: Literal["analyticsLog"] = "analyticsLog"
    value: str
    type: Literal["str"] = "str"

# --- 1. EXECUTOR (FRAME PROCESSOR) ---

class GaussianBlur(Config):
    name: Literal["Gaussian"] = "Gaussian"
    kernel_size: int   
    sigma: float       
    type: Literal["object"] = "object"  # 
    field: Literal["option"] = "option"
    class Config:
        title = "GaussianBlur"

class Canny(Config):
    name: Literal["Canny"] = "Canny"
    threshold: int    
    padding: bool      
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

class ProcessorConfigs(Configs):
    filtertype: FilterType

class ProcessorConfigsInput(Inputs):
    inputImage: InputImage

class ProcessorConfigsOutput(Outputs):
    outputImage: OutputImage

class ProcessorExecutorRequest(Request):
    inputs: Optional[ProcessorConfigsInput]
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
        schema_extra = {"target": {"value": 0}}


# ----------- 2. EXECUTOR (TRACKER) ---------

class YOLOFields(Config):
    name: Literal["YOLOv8"] = "YOLOv8"
    modelPath: str
    confidence: float
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

class HaarFields(Config):
    name: Literal["HaarCascade"] = "HaarCascade"
    cascadeFile: str
    scaleFactor: float
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

class TrackerConfig(Config):
    name: Literal["TrackerConfig"] = "TrackerConfig"
    value: Union[YOLOFields, HaarFields]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

class TrackerConfigs(Configs):
    modelType: TrackerConfig

class TrackerInputs(Inputs):
    inputImage: InputImage
    targetLabels: InputMetadata # 2. Input

class TrackerOutputs(Outputs):
    outputImage: OutputImage
    analyticsLog: OutputLogs # 2. Output

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
        schema_extra = {"target": {"value": 0}}

    

# Ana paket

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    # KURAL: En az 2 adet executor'ı ana menüye bağlıyoruz:
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