import sys
import cv2
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QFrame, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from analyzer import process_image

class ImageViewer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(800, 600)
        self.setStyleSheet("border: 1px solid #cccccc;")
        self.original_pixmap = None
        self.scale_factor = 0.2 
        self.setScaledContents(False)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_image(self, image):
        if image is None:
            self.setText("Nincs megjeleníthető kép")
            self.original_pixmap = None
            return
        
        try:
            if len(image.shape) == 2:
                h, w = image.shape
                bytes_per_line = w
                q_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
            else:
                h, w, c = image.shape
                bytes_per_line = c * w
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                q_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            self.original_pixmap = QPixmap.fromImage(q_image)
            
            self.fit_to_view()
            self.update_pixmap()
        except Exception as e:
            print(f"Hiba a kép megjelenítésekor: {e}")
            self.setText(f"Hiba a kép megjelenítésekor: {str(e)}")
            self.original_pixmap = None

    def fit_to_view(self):
        """A kép átméretezése, hogy teljesen illeszkedjen a nézetbe"""
        if self.original_pixmap is None or self.original_pixmap.isNull():
            return
            
        view_width = self.width() 
        view_height = self.height()
        
        if view_width <= 0 or view_height <= 0:
            view_width = 800
            view_height = 600
        
        width_ratio = view_width / self.original_pixmap.width()
        height_ratio = view_height / self.original_pixmap.height()
        
        self.scale_factor = min(width_ratio, height_ratio) * 0.7  
    
    def update_pixmap(self):
        if self.original_pixmap is None or self.original_pixmap.isNull():
            return
        
        try:
            scaled_width = int(self.original_pixmap.width() * self.scale_factor)
            scaled_height = int(self.original_pixmap.height() * self.scale_factor)
            
            if scaled_width <= 0 or scaled_height <= 0:
                return
                
            scaled_pixmap = self.original_pixmap.scaled(
                scaled_width,
                scaled_height,
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)
            
            self.setMinimumSize(
                min(scaled_width, 800),
                min(scaled_height, 600)
            )
        except Exception as e:
            print(f"Hiba a pixmap frissítésekor: {e}")

    def wheelEvent(self, event):
        if self.original_pixmap is None or self.original_pixmap.isNull():
            return
            
        try:
            zoom_in_factor = 1.15 
            zoom_out_factor = 1 / zoom_in_factor
            
            delta = event.angleDelta().y()
            
            old_scale = self.scale_factor
            
            if delta > 0: 
                self.scale_factor *= zoom_in_factor
            else:  
                self.scale_factor *= zoom_out_factor
            
            self.scale_factor = max(0.05, min(10.0, self.scale_factor))
            
            if abs(old_scale - self.scale_factor) > 0.001:
                self.update_pixmap()
                
            event.accept()
        except Exception as e:
            print(f"Hiba az egérgörgő esemény során: {e}")

    def resizeEvent(self, event):
        """Az átméretezési események kezelése a kép nézetben tartásához"""
        if self.original_pixmap and not self.original_pixmap.isNull():
            if self.scale_factor < 0.3: 
                self.fit_to_view()
                self.update_pixmap()
        super().resizeEvent(event)
class WeldSeamAnalysisGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weld Seam Analysis - Step by Step")
        self.setGeometry(100, 100, 1200, 800)
        self.current_step = 0
        self.steps = ["original", "gray", "clahe", "blurred", "edges", "dilated", "contours", "final"]
        self.explanations = {
            "original": "Eredeti kép: Ez az eredeti kép, amelyet a hegesztési varrat elemzéséhez betöltöttünk.",
            "gray": "Szürkeárnyalatos kép: Az eredeti kép szürkeárnyalatossá alakítása a további feldolgozáshoz.",
            "clahe": "Kontrasztjavított kép (CLAHE): A kontrasztot javítottuk a kép részleteinek kiemeléséhez.",
            "blurred": "Elmosott kép (Gauss-elmosás): A zaj csökkentése érdekében Gauss-elmosást alkalmaztunk.",
            "edges": "Élek detektálása (Canny): Az élek detektálása a hegesztési varrat körvonalainak azonosításához.",
            "dilated": "Kitágított élek: Az élek kitágítása a kontúrok jobb felismerése érdekében.",
            "contours": "Kontúrok megjelenítése: A hegesztési varrat kontúrjainak megjelenítése a képen.",
            "final": "Végső elemzés: A hegesztési varrat méretének meghatározása és vizualizálása."
        }
        self.images = {}
        self.measurements = {}
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.explanation_label = QLabel("Töltsön be egy képet az elemzés megkezdéséhez.")
        self.explanation_label.setAlignment(Qt.AlignCenter)
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setStyleSheet("font-size: 16px; margin: 10px;")
        main_layout.addWidget(self.explanation_label)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        image_frame = QFrame()
        image_frame.setFrameShape(QFrame.StyledPanel)
        image_layout = QVBoxLayout(image_frame)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.image_viewer = ImageViewer()
        self.image_viewer.setText("Töltsön be egy képet a kezdéshez")
        
        scroll_area.setWidget(self.image_viewer)
        image_layout.addWidget(scroll_area)
        
        content_layout.addWidget(image_frame, 4) 
        
        measurement_frame = QFrame()
        measurement_frame.setFrameShape(QFrame.StyledPanel)
        measurement_layout = QVBoxLayout(measurement_frame)
        
        measurement_title = QLabel("Mérési eredmények")
        measurement_title.setAlignment(Qt.AlignCenter)
        measurement_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        measurement_layout.addWidget(measurement_title)
        
        self.width_label = QLabel("Szélesség: -")
        self.height_label = QLabel("Magasság: -")
        self.avg_height_label = QLabel("Átlagos magasság: -")
        self.avg_height_mm_label = QLabel("Átlagos magasság (mm): -")
         
        for label in [self.width_label, self.height_label, self.avg_height_label, self.avg_height_mm_label]:
            label.setStyleSheet("font-size: 14px; margin: 5px;")
            measurement_layout.addWidget(label)
        
        # Archív információs szekció hozzáadása
        archive_title = QLabel("Archív információk")
        archive_title.setAlignment(Qt.AlignCenter)
        archive_title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0 5px 0;")
        measurement_layout.addWidget(archive_title)
        
        self.id_label = QLabel("ID: -")
        self.current_label = QLabel("Áramerősség: -")
        self.voltage_label = QLabel("Feszültség: -")
        self.speed_label = QLabel("Sebesség: -")
        
        for label in [self.id_label, self.current_label, self.voltage_label, self.speed_label]:
            label.setStyleSheet("font-size: 14px; margin: 5px;")
            measurement_layout.addWidget(label)
        
        measurement_layout.addStretch(1)
        content_layout.addWidget(measurement_frame, 1)

        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        self.load_button = QPushButton("Kép betöltése")
        self.load_button.clicked.connect(self.load_image)
        buttons_layout.addWidget(self.load_button)

        self.prev_button = QPushButton("Előző lépés")
        self.prev_button.clicked.connect(self.prev_step)
        self.prev_button.setEnabled(False)
        buttons_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Következő lépés")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setEnabled(False)
        buttons_layout.addWidget(self.next_button)

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.tif);;All Files (*)", options=options)
        if file_path:
            results = process_image(file_path)
            if results:
                self.images = results["images"] 
                self.measurements = results["measurements"]
                
                self.update_measurements()
                self.load_archive_info(file_path)
                
                self.current_step = 0
                self.display_image(self.images[self.steps[self.current_step]])
                self.update_explanation()
                self.next_button.setEnabled(True)
                self.prev_button.setEnabled(False)
                
    def load_archive_info(self, image_path):
        """Archív információk betöltése a kép mappájában található JSON fájlból"""
        try:
            # A kép könyvtárának meghatározása
            directory = os.path.dirname(image_path)
            # Az archive_info.json keresése a könyvtárban
            json_path = os.path.join(directory, "archive_info.json")
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    archive_info = json.load(f)
                
                # Címkék frissítése a betöltött információkkal
                self.id_label.setText(f"ID: {archive_info.get('ID', '-')}")
                self.current_label.setText(f"Áramerősség: {archive_info.get('Current', '-')} A")
                self.voltage_label.setText(f"Feszültség: {archive_info.get('Voltage', '-')} V")
                self.speed_label.setText(f"Sebesség: {archive_info.get('Speed', '-')} cm/min")
            else:
                # Címkék alaphelyzetbe állítása, ha nem található JSON fájl
                self.id_label.setText("ID: -")
                self.current_label.setText("Áramerősség: -")
                self.voltage_label.setText("Feszültség: -")
                self.speed_label.setText("Sebesség: -")
        except Exception as e:
            print(f"Error loading archive info: {e}")
            # Címkék alaphelyzetbe állítása hiba esetén
            self.id_label.setText("ID: -")
            self.current_label.setText("Áramerősség: -")
            self.voltage_label.setText("Feszültség: -")
            self.speed_label.setText("Sebesség: -")

    def update_measurements(self):
        """A mérési címkék frissítése az aktuális adatokkal"""
        self.width_label.setText(f"Szélesség: {self.measurements['width']} px")
        self.height_label.setText(f"Magasság: {self.measurements['height']} px")
        self.avg_height_label.setText(f"Átlagos magasság: {self.measurements['average_height']:.2f} px")
        self.avg_height_mm_label.setText(f"Átlagos magasság (mm): {(self.measurements['average_height']*16.67/2000):.2f}")

    def display_image(self, image):
        self.image_viewer.set_image(image)

    def update_explanation(self):
        step = self.steps[self.current_step]
        self.explanation_label.setText(self.explanations.get(step, "Nincs magyarázat ehhez a lépéshez."))

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.display_image(self.images[self.steps[self.current_step]])
            self.update_explanation()
            self.prev_button.setEnabled(True)
            if self.current_step == len(self.steps) - 1:
                self.next_button.setEnabled(False)

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.display_image(self.images[self.steps[self.current_step]])
            self.update_explanation()
            self.next_button.setEnabled(True)
            if self.current_step == 0:
                self.prev_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeldSeamAnalysisGUI()
    window.show()
    sys.exit(app.exec_())