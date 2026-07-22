import os
import sys
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

class FrameProcessor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        # Girdileri ve konfigürasyonları okuma
        self.image = self.request.get_param("inputImage")
        self.filter_config = self.request.get_param("filterType")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process(self, img_frame):
        """Filtreyi uygulamanın ana işlemi"""
        filter_name = self.filter_config.get("name")
        
        if filter_name == "Gaussian":
            k_size = self.filter_config.get("kernel_size")
            sigma_val = self.filter_config.get("sigma")
            
            # OpenCV Gaussian Blur uygulaması
            if k_size % 2 == 0:
                k_size += 1
            img_frame = cv2.GaussianBlur(img_frame, (k_size, k_size), sigma_val)
            
        elif filter_name == "Canny":
            # Canny kenar algılama
            thresh = self.filter_config.get("threshold")
            is_padded = self.filter_config.get("padding")
            
            img_frame = cv2.Canny(img_frame, thresh, thresh * 2)
            
            if is_padded:
                img_frame = cv2.copyMakeBorder(img_frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        
        return img_frame

    def run(self):
        # Giriş görüntüsünü Redis'ten al
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        
        # Filtreyi uygula
        processed_frame = self.process(img.value)
        
        # Çıktıyı Redis'e kaydet
        self.outputImage = Image.set_frame(img=processed_frame, package_uID=self.uID, redis_db=self.redis_db)
        
        # Response oluştur
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()