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

        self.image = self.request.get_param("inputImage")

        self.filter_config = self.request.get_param("filterType")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
    
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        filter_name = self.filter_config.get("name")
        
        if filter_name == "Gaussian":
          
            k_size = self.filter_config.get("kernel_size")
            sigma_val = self.filter_config.get("sigma")
            
            # OpenCV işlemi (Çift sayı hatası almamak için kernel_size'ı tek sayı yapıyoruz)
            if k_size % 2 == 0:
                k_size += 1
            img.value = cv2.GaussianBlur(img.value, (k_size, k_size), sigma_val)
            
        elif filter_name == "Canny":
            # Modelde tanımladığımız diğer 2 farklı tipteki alanı (int ve bool) okuyoruz
            thresh = self.filter_config.get("threshold")
            is_padded = self.filter_config.get("padding")
            
            # OpenCV işlemi
            img.value = cv2.Canny(img.value, thresh, thresh * 2)
            
            if is_padded:
                # Eğer padding true ise resmin etrafına siyah çerçeve ekle (Örnek bir ekstra işlem)
                img.value = cv2.copyMakeBorder(img.value, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
      
        packageModel = build_response(context=self)
        return packageModel

# processor.py dosyasının en altına geçici test bloğu:
if __name__ == "__main__":
    # 1. Gerçek bir resim yükle (Bilgisayarındaki bir resmin yolunu ver)
    mock_image = cv2.imread("kortex_test_resmi.jpg")
    
    if mock_image is None:
        print("Hata: Test resmi bulunamadı! Lütfen yolu kontrol et.")
    else:
        # 2. Seçimi elinle simüle et (Gaussian seçtiğimizi varsayalım)
        kernel_size = 5
        sigma = 1.5
        
        # 3. OpenCV fonksiyonunu test et
        result = cv2.GaussianBlur(mock_image, (kernel_size, kernel_size), sigma)
        
        # 4. Sonucu ekranda göster
        cv2.imshow("Ham Resim", mock_image)
        cv2.imshow("Filtrelenmiş Resim", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()