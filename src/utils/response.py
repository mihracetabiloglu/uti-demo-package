from components.Package.src.models.PackageModel import PackageModel

def build_response(context) -> dict:
    """
    Executor icindeki verileri toplar ve PackageModel semasina uygun 
    bir response paketi olusturur.
    """
    
    # Request yapısındaki executor type'ını belirle
    executor_config = context.request.model.configs.executor.value
    executor_name = executor_config.__class__.__name__
    
    outputs_dict = {}
    
    if executor_name == "FrameProcessorExecutor":
        # Frame Processor Executor çıktısı
        outputs_dict = {
            "outputImage": {
                "name": "outputImage",
                "value": getattr(context, "outputImage", None),
                "type": "object"
            }
        }
    elif executor_name == "IntrusionTrackerExecutor":
        # Intrusion Tracker Executor çıktısı
        outputs_dict = {
            "outputImage": {
                "name": "outputImage",
                "value": getattr(context, "outputImage", None),
                "type": "object"
            },
            "analyticsLog": {
                "name": "analyticsLog",
                "value": getattr(context, "analyticsLog", ""),
                "type": "string"
            }
        }
    
    response_data = {
        "outputs": outputs_dict
    }
    
    return response_data
