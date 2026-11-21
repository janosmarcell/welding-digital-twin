import cv2
import numpy as np

def load_image(image_path):
    """Kép betöltése a megadott elérési útról"""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Hiba a kép beolvasásakor. Kérjük, ellenőrizze a fájl elérési útját.")
    return image

def convert_to_grayscale(image):
    """Kép átalakítása szürkeárnyalatossá"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_clahe(gray_image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """CLAHE (Contrast Limited Adaptive Histogram Equalization) alkalmazása a kontraszt javításához"""
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(gray_image)

def apply_gaussian_blur(image, kernel_size=(5, 5)):
    """Gauss-elmosás alkalmazása a zajcsökkentéshez"""
    return cv2.GaussianBlur(image, kernel_size, 0)

def detect_edges(image, sigma=0.33):
    """Élek felismerése adaptív küszöbértékek használatával"""
    median_val = np.median(image)
    lower_thresh = int(max(0, (1.0 - sigma) * median_val))
    upper_thresh = int(min(255, (1.0 + sigma) * median_val))
    return cv2.Canny(image, lower_thresh, upper_thresh)

def dilate_edges(edges, kernel_size=11):
    """Élek kitágítása a jobb kontúrfelismeréshez"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(edges, kernel, iterations=1)

def find_contours(dilated_image):
    """Kontúrok keresése a bináris képen"""
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def filter_contours_by_area(contours, image_area, max_area, threshold_factor=0.1):
    """Kontúrok szűrése terület alapján"""
    area_threshold = max(0.1, min(0.2, 5000 / image_area)) * max_area
    return [cnt for cnt in contours if cv2.contourArea(cnt) > area_threshold]

def combine_contours(contours, image_shape):
    """Kontúrok egyesítése egy maszkban"""
    combined_mask = np.zeros(image_shape, dtype=np.uint8)
    for contour in contours:
        cv2.drawContours(combined_mask, [contour], -1, 255, thickness=cv2.FILLED)
    return combined_mask

def apply_morphological_closing(mask, kernel_size=(5, 5)):
    """Morfológiai záróművelet alkalmazása a kis lyukak kitöltéséhez"""
    kernel = np.ones(kernel_size, np.uint8)
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

def find_largest_contour(contours):
    """Legnagyobb kontúr megkeresése"""
    return max(contours, key=cv2.contourArea)

def draw_contours(image, contours):
    """Kontúrok kirajzolása a képre"""
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    return contour_image

# Új funkciók a továbbfejlesztett feldolgozáshoz

def determine_weld_orientation(contour):
    """Hegesztési varrat orientációjának meghatározása (vízszintes vagy függőleges)"""
    rect = cv2.minAreaRect(contour)
    angle = rect[2]
    width_is_height = False
    
    # Ellenőrzés, hogy az OpenCV felcserélte-e a szélességet és magasságot
    if abs(angle) < 45 or abs(angle - 90) < 45:
        width_is_height = rect[1][0] > rect[1][1]
    
    # Általában a vízszintes hegesztések gyakoribbak
    return not width_is_height

def calculate_weld_dimensions(contour, mask, is_horizontal):
    """Hegesztési varrat méreteinek pontosabb kiszámítása"""
    x_values = [point[0][0] for point in contour]
    y_values = [point[0][1] for point in contour]
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    
    weld_width = max_x - min_x
    original_height = max_y - min_y
    
    # Vízszintes hegesztések esetén finomítjuk a magasság számítását
    if is_horizontal:
        # Függőleges profil elemzése
        vertical_projection = np.sum(mask, axis=1)
        
        if np.sum(vertical_projection) > 0:
            y_indices = np.arange(len(vertical_projection))
            center_y = np.sum(y_indices * vertical_projection) / np.sum(vertical_projection)
            
            # Függőleges profil szórásának kiszámítása
            y_squared_diff = (y_indices - center_y) ** 2
            std_dev_y = np.sqrt(np.sum(y_squared_diff * vertical_projection) / np.sum(vertical_projection))
            
            # Szórás használata a hegesztési magasság meghatározásához
            height_factor = 1.5
            adjusted_height = int(std_dev_y * height_factor * 2)
            
            # Ésszerű értékek biztosítása
            adjusted_height = max(adjusted_height, original_height // 4)
            adjusted_height = min(adjusted_height, original_height)
            
            new_min_y = int(center_y - adjusted_height // 2)
            new_max_y = int(center_y + adjusted_height // 2)
            
            # Koordináták képen belül tartása
            height = mask.shape[0]
            new_min_y = max(0, new_min_y)
            new_max_y = min(height - 1, new_max_y)
            
            weld_height = new_max_y - new_min_y
        else:
            weld_height = original_height
            new_min_y = min_y
            new_max_y = max_y
    else:
        # Függőleges hegesztések esetén az eredeti magasságot használjuk
        weld_height = original_height
        new_min_y = min_y
        new_max_y = max_y
    
    return weld_width, weld_height, min_x, max_x, new_min_y, new_max_y



def measure_average_height(mask, min_x, max_x, num_measurements=100):
    """Hegesztési varrat magasságának mérése több pontban és az átlag kiszámítása"""
    heights = []
    measurements = []  # (x_pos, min_y, max_y) értékek tárolása
    margin = (max_x - min_x) // 10  # Széleket kihagyjuk
    
    # Szisztematikus mintavétel a konzisztensebb mérésekhez
    step = max(1, (max_x - min_x - 2 * margin) // num_measurements)
    
    for i in range(num_measurements):
        x_pos = min_x + margin + (i * step)
        if x_pos >= max_x - margin:
            break
            
        column = mask[:, x_pos]
        y_coords = np.where(column > 0)[0]
        
        if len(y_coords) > 1:
            min_y_at_x = min(y_coords)
            max_y_at_x = max(y_coords)
            height_at_x = max_y_at_x - min_y_at_x
            heights.append(height_at_x)
            measurements.append((x_pos, min_y_at_x, max_y_at_x))
    
    # Kiugró értékek szűrése mediánnal
    if heights:
        median_height = np.median(heights)
        mad = np.median([abs(h - median_height) for h in heights])
        threshold = 2.5 * mad
        
        filtered_indices = [i for i, h in enumerate(heights) if abs(h - median_height) <= threshold]
        filtered_measurements = [measurements[i] for i in filtered_indices] if filtered_indices else measurements
        
        filtered_heights = [heights[i] for i in filtered_indices] if filtered_indices else heights
        average_height = sum(filtered_heights) / len(filtered_heights)
    else:
        average_height = 0
        filtered_measurements = []
    
    return average_height, filtered_measurements

def draw_measurement_lines(image, mask, min_x, max_x, measurements, min_y, max_y):
    """Mérési vonalak rajzolása, amelyek pontosan követik a kontúrt az adott x pozícióban"""
    result_image = image.copy()
    
    # Minden mérési vonalat a pontos pozíciójára rajzolunk
    for x_pos, local_min_y, local_max_y in measurements:
        # Vonal rajzolása pontosan a maszk tetejétől az aljáig az adott x pozícióban
        cv2.line(result_image, (x_pos, local_min_y), (x_pos, local_max_y), (255, 0, 0), 1)
    
    return result_image


def annotate_image(image, width, height, avg_height):
    """Mérési adatok feliratozása a képre"""
    annotated = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(annotated, f"Szélesség: {width}px", (10, 30), font, 0.7, (0, 255, 255), 2)
    cv2.putText(annotated, f"Magasság: {height}px", (10, 60), font, 0.7, (0, 255, 255), 2)
    cv2.putText(annotated, f"Átlag magasság: {avg_height:.1f}px", (10, 90), font, 0.7, (0, 255, 255), 2)
    return annotated

def analyze_weld_seam(image_path):
    """Hegesztési varrat elemzése a megadott képen"""
    try:
        # Kép betöltése és előfeldolgozása
        original_image = load_image(image_path)
        gray_image = convert_to_grayscale(original_image)
        clahe_image = apply_clahe(gray_image)
        blurred_image = apply_gaussian_blur(clahe_image)
        edges = detect_edges(blurred_image)
        dilated_edges = dilate_edges(edges)
        contours = find_contours(dilated_edges)

        if not contours:
            raise ValueError("Nem található hegesztési varrat a képen.")

        # Kontúrok szűrése terület alapján
        height, width = gray_image.shape[:2]
        image_area = height * width
        max_area = max(cv2.contourArea(cnt) for cnt in contours)
        significant_contours = filter_contours_by_area(contours, image_area, max_area)

        if not significant_contours:
            # Egyszerűbb küszöbértékre váltás
            significant_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > max_area * 0.1]
            
        if not significant_contours:
            raise ValueError("Nem található jelentős hegesztési varrat a képen.")

        # Kontúrok egyesítése és finomítása
        combined_mask = combine_contours(significant_contours, gray_image.shape)
        closed_mask = apply_morphological_closing(combined_mask)
        final_contours = find_contours(closed_mask)
        largest_contour = find_largest_contour(final_contours)
        
        # Nyers maszk létrehozása a legnagyobb kontúrból
        raw_mask = np.zeros_like(gray_image)
        cv2.drawContours(raw_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
        
        # Hegesztési varrat orientációjának meghatározása (vízszintes/függőleges)
        is_horizontal = determine_weld_orientation(largest_contour)
        
        # Hegesztési varrat méreteinek pontosabb kiszámítása
        weld_width, weld_height, min_x, max_x, min_y, max_y = calculate_weld_dimensions(
            largest_contour, raw_mask, is_horizontal
        )
        
        # Finomított maszk létrehozása a módosított határértékekkel
        refined_mask = np.zeros_like(gray_image)
        if is_horizontal:
            # Vízszintes hegesztéseknél maszk készítése a módosított határokból
            points = np.array([[min_x, min_y], [max_x, min_y], 
                              [max_x, max_y], [min_x, max_y]])
            cv2.fillPoly(refined_mask, [points], 255)
        else:
            # Függőleges hegesztéseknél az eredeti kontúrt használjuk
            cv2.drawContours(refined_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
        
        # Átlagos magasság mérése szisztematikus mintavétellel
        average_height, heights_data = measure_average_height(refined_mask, min_x, max_x)
        
        # Kontúrkép létrehozása mérési vonalakkal
        contour_image = draw_contours(original_image, [largest_contour])
        measured_image = draw_measurement_lines(contour_image, refined_mask, min_x, max_x, heights_data, min_y, max_y)
        
        # Szöveges feliratok hozzáadása a méretekkel
        final_image = annotate_image(measured_image, weld_width, weld_height, average_height)
        
        # Mérési adatok és feldolgozott képek visszaadása
        return {
            "measurements": {
                "width": weld_width,
                "height": weld_height,
                "average_height": average_height,
            },
            "images": {
                "original": original_image,
                "gray": gray_image,
                "clahe": clahe_image,
                "blurred": blurred_image,
                "edges": edges,
                "dilated": dilated_edges,
                "contours": contour_image,
                "final": final_image
            }
        }

    except Exception as e:
        raise RuntimeError(f"Hiba az elemzés során: {str(e)}")

def process_image(image_path, save_result=False):
    """Kép feldolgozása és opcionálisan az eredmény mentése"""
    try:
        results = analyze_weld_seam(image_path)
        
        if save_result:
            output_path = image_path.rsplit('.', 1)[0] + '_eredmeny.jpg'
            cv2.imwrite(output_path, results["images"]["final"])
            print(f"Eredmény mentve: {output_path}")
        
        return results
    except Exception as e:
        print(f"Hiba: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Használat: python analyzer.py <kep_eleresi_utja> [--save]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    save_result = "--save" in sys.argv
    
    results = process_image(image_path, save_result)
    if results:
        print("Hegesztési varrat méretei:")
        for key, value in results["measurements"].items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")
        
        # Képek megjelenítése
        for step, img in results["images"].items():
            cv2.imshow(step, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()