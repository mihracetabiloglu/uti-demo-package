from components.Package.src.models.PackageModel import PackageModel

def build_response(context) -> PackageModel:
    """
    Executor icindeki verileri toplar ve PackageModel semasina uygun 
    bir response paketi olusturur.
    """
  
    executor_name = context.request.model.configs.executor.value.__class__.__name__
    
    outputs_dict = {}
    
    if "FrameProcessorExecutor" in executor_name:
        outputs_dict = {
            "outputImage": {
                "name": "outputImage",
                "value": getattr(context, "outputImage", None),
                "type": "Images"
            }
        }
    elif "IntrusionTrackerExecutor" in executor_name:
        outputs_dict = {
            "outputImage": {
                "name": "outputImage",
                "value": getattr(context, "outputImage", None),
                "type": "Images"
            },
            "analyticsLog": {
                "name": "analyticsLog",
                "value": getattr(context, "analyticsLog", ""),
                "type": "str"
            }
        }
        
    
    response_data = {
        "outputs": outputs_dict
    }
    
    return response_data