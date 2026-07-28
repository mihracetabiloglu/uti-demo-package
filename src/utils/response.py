from sdks.novavision.src.helper.package import PackageHelper

from components.DemoPackage.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    FrameProcessorExecutor,
    FrameProcessorExecutorResponse,
    FrameProcessorExecutorOutputs,
    ProcessorOutputImage,
    IntrusionTrackerExecutor,
    IntrusionTrackerExecutorResponse,
    IntrusionTrackerExecutorOutputs,
    IntrusionTrackerExecutorOutputImage,
    AnalyticsLog
)

def build_response_frame_processor(context):
    """Frame Processor (Görüntü İşleme) için response modeli oluşturur."""
    output_image = ProcessorOutputImage(value=context.image)
    outputs = FrameProcessorExecutorOutputs(outputImage=output_image)
    response = FrameProcessorExecutorResponse(outputs=outputs)
    
    executor = FrameProcessorExecutor(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    
    return package_model


def build_response_intrusion_tracker(context, default_log=""):
    """Intrusion Tracker (YOLO/Haar Cascade vb. Takip) için response modeli oluşturur."""
    output_image = IntrusionTrackerExecutorOutputImage(value=context.image)
    
    # Eğer context içinden bir log metni dönüyorsa onu alır, yoksa varsayılan boş string atar
    log_value = getattr(context, 'analyticsLog', default_log)
    analytics_log = AnalyticsLog(value=log_value)
    
    outputs = IntrusionTrackerExecutorOutputs(outputImage=output_image, analyticsLog=analytics_log)
    response = IntrusionTrackerExecutorResponse(outputs=outputs)
    
    executor = IntrusionTrackerExecutor(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    
    return package_model