import cv2
import matplotlib.pyplot as plt
import numpy as np

def draw_epipolar_lines(img1, img2, lines, pts1, pts2):
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        
        # Convertir les coordonnées en int avant de les passer à cv2.circle
        img1 = cv2.circle(img1, (int(pt1[0][0]), int(pt1[0][1])), 5, color, -1)
        img2 = cv2.circle(img2, (int(pt2[0][0]), int(pt2[0][1])), 5, color, -1)
    return img1, img2

img1_orig = cv2.imread('/home/e20230010413/Bureau/imagine/Imaginem2VrArXR/strauss/tp1/fichiers/TurtleD.tif', 0)
img2_orig = cv2.imread('/home/e20230010413/Bureau/imagine/Imaginem2VrArXR/strauss/tp1/fichiers/TurtleG.tif', 0)

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
    # Sélectionner uniquement les points inliers
    pts1 = pts1[mask.ravel() == 1]
    pts2 = pts2[mask.ravel() == 1]
    
    # Trouver les épilines
    lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = draw_epipolar_lines(img1, img2, lines1, pts1, pts2)
    
    lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = draw_epipolar_lines(img2, img1, lines2, pts2, pts1)
    
    # Afficher les images avec Matplotlib
    plt.subplot(121), plt.imshow(img5)
    plt.subplot(122), plt.imshow(img3)
    plt.show()
else:
    print("Could not compute fundamental matrix.")

