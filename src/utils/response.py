from components.Package.src.models.PackageModel import PackageModel

def build_response(context) -> dict:
    """
    Executor icindeki verileri toplar ve PackageModel semasina uygun 
    bir response paketi olusturur.
    """
    # Executor sınıf adını al
    executor_instance = context.request.model.configs.executor.value
    executor_class_name = executor_instance.__class__.__name__
    
    outputs_dict = {}
    
    # FrameProcessorExecutor veya IntrusionTrackerExecutor kontrolü
    if executor_class_name == "FrameProcessorExecutor":
        outputs_dict = {
            "outputImage": {
                "name": "outputImage",
                "value": getattr(context, "outputImage", None),
                "type": "object"
            }
        }
    elif executor_class_name == "IntrusionTrackerExecutor":
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