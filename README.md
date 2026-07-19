# UTI Demo Package Assignment

Bu paket, Novavision altyapısı üzerinde çalışan, görüntü işleme ve nesne takibi süreçlerini yöneten iki temel işlem birimine (Executor) sahip bir demo paketidir

## 🚀 İşlem Birimleri (Executors)

*   **Processor (FrameProcessor):** Gelen görüntü üzerinde kullanıcının seçtiği dinamik filtreye göre (Gaussian filtreleme veya Canny kenar algılama) pikselsel dönüşümler uygulayan işlemci birimdir.
*   **Tracker (IntrusionTracker):** Seçilen derin öğrenme (YOLOv8) veya geleneksel (HaarCascade) modele göre veri akışı üzerinde hedef nesneleri/ihlal alanlarını tarayan ve analiz günlüğü oluşturan yürütücü birimdir.
