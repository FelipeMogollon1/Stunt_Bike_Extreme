# Stunt Bike Extreme

**Stunt Bike Extreme** es un juego de acrobacias en motocicleta desarrollado en **Python** utilizando **Pygame**. El objetivo del juego es realizar acrobacias espectaculares en el aire, aterrizar correctamente y acumular puntos, mientras se evitan caídas que puedan hacer perder vidas.
<img width="791" height="629" alt="image" src="https://github.com/user-attachments/assets/494c495c-6daf-4576-a92e-c0f5915b73ca" />


---

## Características

- Juego 2D con físicas básicas de salto y gravedad.
- Sistema de acrobacias con diferentes maniobras:
  - Backflip (`W`)  
  - Frontflip (`S`)  
  - Twist (`Q`)  
  - Spin (`A`)  
- Sistema de combos que multiplica la puntuación según las acrobacias consecutivas.
- Rampas generadas de manera procedural para mayor rejugabilidad.
- Sistema de vidas y Game Over.
- Puntuaciones guardadas localmente en `data/puntajes.json`.
- Récord del jugador guardado en `data/record.txt`.
- Música de fondo y efectos de sonido para aterrizajes exitosos y fallidos.
- Menú interactivo con opciones de jugar, ver puntajes y créditos.
- Mensajes aleatorios cuando se falla un aterrizaje para mayor diversión.

---

## Controles

| Tecla | Acción |
|-------|-------|
| ESPACIO | Saltar |
| A / D   | Rotar en el aire |
| W / S / Q / A | Realizar acrobacias |
| ← / →  | Mover cámara |
| ESC     | Volver al menú |
| ENTER   | Seleccionar opción en menú / volver al menú desde Game Over |

---
<img width="799" height="631" alt="image" src="https://github.com/user-attachments/assets/5234438e-0e50-4ef8-84ca-15d036284192" />

## Instalación

1. Clonar el repositorio o descargar el proyecto.  
2. Instalar Python (3.8 o superior recomendado).  
3. Instalar Pygame:

```bash
pip install pygame
```

4. Asegurarse de que las carpetas de recursos existan:

```
assets/images/
assets/sounds/
assets/music/
data/
```

5. Colocar las imágenes, sonidos y música en sus respectivas carpetas.

---

## Estructura de Carpetas

```
StuntBikeExtreme/
│
├─ assets/
│   ├─ images/       # Sprites y fondos
│   ├─ sounds/       # Efectos de sonido
│   └─ music/        # Música de fondo
│
├─ data/
│   ├─ puntajes.json # Puntajes altos
│   └─ record.txt    # Récord del jugador
│
└─ main.py           # Código principal del juego
```

---

## Cómo jugar

1. Ejecutar `main.py` para iniciar el juego:

```bash
python main.py
```

2. En el **menú principal**, navegar con las flechas y seleccionar con **ENTER**.  
3. Durante el juego, saltar sobre rampas, realizar acrobacias y aterrizar correctamente para acumular puntos.  
4. Evitar fallar aterrizajes repetidamente o perderás todas tus vidas.  
5. Si el juego termina, se mostrará la pantalla de **Game Over** con tu puntaje final y posible récord.

---

## Contribuciones

Se pueden realizar contribuciones para mejorar:

- Nuevas acrobacias y animaciones.
- Diferentes niveles y tipos de rampas.
- Mejoras gráficas y sonoras.
- Sistema de logros y desbloqueables.

---

## Licencia

Este proyecto es de código abierto y puede ser modificado y distribuido libremente bajo los términos de la **Licencia MIT**.

