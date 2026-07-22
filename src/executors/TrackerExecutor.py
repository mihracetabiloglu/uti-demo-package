import os
import sys
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

class IntrusionTracker(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        # Girdi parametrelerini ve konfigürasyon menüsünü okuma
        self.image_param = self.request.get_param("inputImage")
        self.target_label = self.request.get_param("targetLabels")
        self.model_config = self.request.get_param("modelType")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Girdileri kullanıma hazırlama
        img = Image.get_frame(img=self.image_param, redis_db=self.redis_db)
        search_target = str(self.target_label) if self.target_label is not None else "human"
        log_message = ""
        
        selected_model = self.model_config.get("name") if isinstance(self.model_config, dict) else ""
        
        # Bağımlı menü seçimine göre nesne takip simülasyonu
        if selected_model == "YOLOv8":
            yolo_path = self.model_config.get("modelPath", "yolov8n.pt")
            conf_score = self.model_config.get("confidence", 0.5)
            cv2.rectangle(img.value, (100, 100), (300, 300), (0, 255, 0), 3)
            log_message = f"[YOLOv8] {yolo_path} çalıştırıldı. Hedef '{search_target}' arandı. Conf: {conf_score}"
            
        elif selected_model == "HaarCascade":
            xml_path = self.model_config.get("cascadeFile", "haarcascade.xml")
            scale_fac = self.model_config.get("scaleFactor", 1.1)
            cv2.rectangle(img.value, (150, 150), (250, 250), (255, 0, 0), 2)
            log_message = f"[HaarCascade] {xml_path} tarandı. Eşleşme arandı. Scale: {scale_fac}"

        # Çıktıları sisteme kaydetme
        self.outputImage = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        self.analyticsLog = log_message
        
        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()