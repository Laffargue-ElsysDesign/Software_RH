HoloSoft est le projet contenant le code de la carte chassis pour le contrôle des moteurs et la lecture des encodeurs.

Il a été ecrit lors du stage de 2020 et modifié pour le faire fonctionner en 2021. 

Il faut utiliser l'environnement CUBE IDE de chez stm pour l'edition, le flashage du µC, et le debuggage.

Le code permet de communniquer en UART entre l'U96 et le stm pour échanger des consignes de vitesse et les vitesses mesurées par les 
encodeurs des roues. il gère l'asservissement des moteurs via un correcteur PI et un watchdog à été mis en place afin de set
la consigne de vitesse à zero en cas de perte de communication UART pendant plus de 1 sec. 