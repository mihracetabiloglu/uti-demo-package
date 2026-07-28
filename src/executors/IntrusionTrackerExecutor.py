import os
import sys
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.utils.response import build_response_intrusion_tracker
from components.DemoPackage.src.models.PackageModel import PackageModel

class IntrusionTrackerExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        # Girdileri ve konfigürasyonları okuma
        self.image_param = self.request.get_param("inputImage")
        self.target_label = self.request.get_param("targetLabels")
        self.model_config = self.request.get_param("modelType")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process(self, img_frame, search_target, selected_model):
        """Nesne takip işleminin ana mantığı"""
        log_message = ""
        
        if selected_model == "YOLOv8":
            yolo_path = self.model_config.get("modelPath", "yolov8n.pt")
            conf_score = self.model_config.get("confidence", 0.5)
            
            # Simülasyon: yeşil dikdörtgen çiz
            cv2.rectangle(img_frame, (100, 100), (300, 300), (0, 255, 0), 3)
            log_message = f"[YOLOv8] {yolo_path} çalıştırıldı. Hedef '{search_target}' arandı. Conf: {conf_score}"
            
        elif selected_model == "HaarCascade":
            xml_path = self.model_config.get("cascadeFile", "haarcascade.xml")
            scale_fac = self.model_config.get("scaleFactor", 1.1)
            
            # Simülasyon: mavi dikdörtgen çiz
            cv2.rectangle(img_frame, (150, 150), (250, 250), (255, 0, 0), 2)
            log_message = f"[HaarCascade] {xml_path} tarandı. Eşleşme arandı. Scale: {scale_fac}"
        
        return img_frame, log_message

    def run(self):
        # Giriş görüntüsünü Redis'ten al
        img = Image.get_frame(img=self.image_param, redis_db=self.redis_db)
        
        # Hedef etiketi hazırla
        search_target = str(self.target_label) if self.target_label is not None else "human"
        
        # Model seçimini belirle
        selected_model = self.model_config.get("name") if isinstance(self.model_config, dict) else ""
        
        # Takip işlemini yap
        processed_frame, log_msg = self.process(img.value, search_target, selected_model)
        
        # Çıktıları sisteme kaydet
        self.outputImage = Image.set_frame(img=processed_frame, package_uID=self.uID, redis_db=self.redis_db)
        self.analyticsLog = log_msg
        
        # Response oluştur
        return build_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()