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
    processorOutputImage = ProcessorOutputImage(value=context.image)
    frameProcessorExecutorOutputs = FrameProcessorExecutorOutputs(outputImage=processorOutputImage)
    frameProcessorExecutorResponse = FrameProcessorExecutorResponse(outputs=frameProcessorExecutorOutputs)
    frameProcessorExecutor = FrameProcessorExecutor(value=frameProcessorExecutorResponse)
    configExecutor = ConfigExecutor(value=frameProcessorExecutor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    
    return packageModel


def build_response_intrusion_tracker(context):
    intrusionTrackerExecutorOutputImage = IntrusionTrackerExecutorOutputImage(value=context.image)
    analyticsLog = AnalyticsLog(value=context.analyticsLog)
    intrusionTrackerExecutorOutputs = IntrusionTrackerExecutorOutputs(outputImage=intrusionTrackerExecutorOutputImage, analyticsLog=analyticsLog)
    intrusionTrackerExecutorResponse = IntrusionTrackerExecutorResponse(outputs=intrusionTrackerExecutorOutputs)
    intrusionTrackerExecutor = IntrusionTrackerExecutor(value=intrusionTrackerExecutorResponse)
    configExecutor = ConfigExecutor(value=intrusionTrackerExecutor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    
    return packageModel