import cv2
import matplotlib.pyplot as plt
import numpy as np

def draw_epipolar_lines(img1, img2, lines, pts1, pts2):
    h, w = img1.shape[:2]  
    if len(img1.shape) == 2:  # si l'image est en niveaux de gris
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    if len(img2.shape) == 2:  # si l'image est en niveaux de gris
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2]/r[1]])
        x1, y1 = map(int, [w, -(r[2]+r[0]*w)/r[1]])  # Et ici
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1[0].astype(int)), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2[0].astype(int)), 5, color, -1)
    return img1, img2


# Charger les images
img1_orig = cv2.imread('ArbreD.tiff', cv2.IMREAD_UNCHANGED) 
img2_orig = cv2.imread('ArbreG.tiff', cv2.IMREAD_UNCHANGED) 

# Convertir en gris
img1 = cv2.cvtColor(img1_orig, cv2.COLOR_BGRA2GRAY)  
img2 = cv2.cvtColor(img2_orig, cv2.COLOR_BGRA2GRAY)  

# Détecter les points de repère (features) avec ORB
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Matcher les features avec BFMatcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Sélectionner les meilleurs matches
matches = sorted(matches, key=lambda x: x.distance)[:50]
pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

# Calculer la matrice fondamentale avec RANSAC
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)

if mask is not None:
    print(f"Fundamental Matrix: \n{F}")
    pts1 = pts1[mask.ravel() == 1]
    pts2 = pts2[mask.ravel() == 1]
    
    # Afficher les images avec une interface graphique interactive
    fig, axs = plt.subplots(1, 2, figsize=(15, 7))
    
    def onclick(event):
        try:  # Ajouter une gestion des exceptions pour déboguer
          print("Click detected")  # Vérifier si le clic est détecté
          global img1, img2
          
          # Trouver le point cliqué le plus proche dans pts1 ou pts2
          if event.inaxes == axs[0]:
              idx = np.argmin(np.sum((pts1 - [event.xdata, event.ydata]) ** 2, axis=2))
              pt1_selected = pts1[idx]
              pt2_selected = pts2[idx]
          else:
              idx = np.argmin(np.sum((pts2 - [event.xdata, event.ydata]) ** 2, axis=2))
              pt1_selected = pts1[idx]
              pt2_selected = pts2[idx]
          
          lines1 = cv2.computeCorrespondEpilines(pt2_selected.reshape(-1, 1, 2), 2, F).reshape(-1, 3)
          lines2 = cv2.computeCorrespondEpilines(pt1_selected.reshape(-1, 1, 2), 1, F).reshape(-1, 3)
          
          img1, img2 = draw_epipolar_lines(img1_orig, img2_orig, lines1, [pt1_selected], [pt2_selected])
          img2, img1 = draw_epipolar_lines(img2_orig, img1_orig, lines2, [pt2_selected], [pt1_selected])

          axs[0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
          axs[1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

          fig.canvas.draw()

          print("Click processed")  # Vérifier si le clic est traité sans erreurs
        except Exception as e:
            print(f"Error: {str(e)}")  # Imprimer l'erreur si elle se produit
        
    axs[0].imshow(cv2.cvtColor(img1_orig, cv2.COLOR_BGR2RGB))
    axs[0].set_title("Image 1")
    axs[1].imshow(cv2.cvtColor(img2_orig, cv2.COLOR_BGR2RGB))
    axs[1].set_title("Image 2")
    
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
else:
    print("Fondamental matrix computation failed.")
