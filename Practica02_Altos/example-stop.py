import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
# Nombre: Armenta Fuentes Lobsang Leonardo
#Codigo para detectar los altos en base a texto y el color.



ruta_imagen = "stop.png"
#ruta_imagen = "noStop02.png"
imagen = cv2.imread(ruta_imagen)


imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)


lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])


mask1 = cv2.inRange(imagen_hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(imagen_hsv, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)


kernel = np.ones((5, 5), np.uint8)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)


lector = easyocr.Reader(["es", "en"])
resultado = lector.readtext(imagen)
detecto_alto = False


print("Texto extraído de la imagen:")
for bbox, texto, prob in resultado:
    print(f"{texto} (Confianza: {prob:.2f})")
    texto_mayus = texto.upper()
    
    if "ALTO" in texto_mayus or "STOP" in texto_mayus:
        
        xs = [pt[0] for pt in bbox]
        ys = [pt[1] for pt in bbox]
        x_min, y_min = int(min(xs)), int(min(ys))
        x_max, y_max = int(max(xs)), int(max(ys))
        
        
        region_mask = red_mask[y_min:y_max, x_min:x_max]
        total_pixels = region_mask.shape[0] * region_mask.shape[1]
        red_pixels = cv2.countNonZero(region_mask)
        
        
        red_ratio = red_pixels / total_pixels if total_pixels > 0 else 0
        print(f"Area de rojo: {red_ratio:.2f}")
        
    
        if red_ratio > 0.5:
            detecto_alto = True
            cv2.rectangle(imagen_rgb, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(imagen_rgb, texto, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            
            cv2.rectangle(imagen_rgb, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.putText(imagen_rgb, texto, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    else:
        
        xs = [pt[0] for pt in bbox]
        ys = [pt[1] for pt in bbox]
        x_min, y_min = int(min(xs)), int(min(ys))
        x_max, y_max = int(max(xs)), int(max(ys))
        cv2.rectangle(imagen_rgb, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        cv2.putText(imagen_rgb, texto, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)


resultado_texto = "ALTO" if detecto_alto else "NO ALTO"
color_texto = (0, 255, 0) if detecto_alto else (0, 0, 255)
cv2.putText(imagen_rgb, resultado_texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color_texto, 2)

plt.imshow(imagen_rgb)
plt.axis("off")
plt.show()