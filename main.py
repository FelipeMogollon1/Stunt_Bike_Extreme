import pygame
import sys
import os
import random
import json
from datetime import datetime
from abc import ABC, abstractmethod

# ==================== CONSTANTES ====================
ANCHO, ALTO = 800, 600
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
GRIS_CLARO = (180, 180, 180)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 100, 255)
BLANCO = (255, 255, 255)
AZUL_OSCURO = (0, 50, 100)


# Rutas de recursos
RUTA_IMAGES = "assets/images/"
RUTA_SOUNDS = "assets/sounds/"
RUTA_MUSIC = "assets/music/"
RUTA_DATA = "data/"

# ==================== GESTORES DE RECURSOS ====================
class GestorRecursos:
    """Gestiona la carga de recursos como fuentes, imágenes y sonidos"""
    
    def __init__(self):
        pygame.init()
        self.fuentes = self._cargar_fuentes()
        self.sprites = self._cargar_sprites()
        self.sonidos = self._cargar_sonidos()
        self.fondo = self._cargar_fondo()

    def _crear_directorios(self):
        """Crea los directorios necesarios si no existen"""
        for directorio in [RUTA_IMAGES, RUTA_SOUNDS, RUTA_MUSIC, RUTA_DATA]:
            os.makedirs(directorio, exist_ok=True)
    
    def _cargar_fuentes(self):
        return {
            'titulo': pygame.font.SysFont("arial", 48, bold=True),
            'menu': pygame.font.SysFont("arial", 32),
            'texto': pygame.font.SysFont("arial", 24),
            'pequeña': pygame.font.SysFont("arial", 18)
        }
    
    def _cargar_sprites(self):
        sprites = {}
        try:
            sprites['personaje'] = pygame.transform.scale(
                pygame.image.load(f"{RUTA_IMAGES}personaje.png").convert_alpha(), (64, 64)
            )
            
            sprites['acrobacias'] = {
                pygame.K_a: pygame.transform.scale(
                    pygame.image.load(f"{RUTA_IMAGES}acrobacia1.png").convert_alpha(), (64, 64)
                ),
                pygame.K_w: pygame.transform.scale(
                    pygame.image.load(f"{RUTA_IMAGES}acrobacia2.png").convert_alpha(), (64, 64)
                ),
                pygame.K_s: pygame.transform.scale(
                    pygame.image.load(f"{RUTA_IMAGES}acrobacia3.png").convert_alpha(), (64, 64)
                ),
                pygame.K_q: pygame.transform.scale(
                    pygame.image.load(f"{RUTA_IMAGES}acrobacia4.png").convert_alpha(), (64, 64)
                ),
            }
        except:
            # Crear sprites básicos si no se pueden cargar
            sprites['personaje'] = pygame.Surface((64, 64))
            sprites['personaje'].fill(AZUL)
            
            sprites['acrobacias'] = {}
            for tecla in [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_q]:
                sprite = pygame.Surface((64, 64))
                sprite.fill(VERDE)
                sprites['acrobacias'][tecla] = sprite
        
        return sprites
    
    def _cargar_sonidos(self):
        try:
            exito = pygame.mixer.Sound(f"{RUTA_SOUNDS}sonido_exito.wav")
            fallo = pygame.mixer.Sound(f"{RUTA_SOUNDS}sonido_fallo.wav")
            exito.set_volume(1.0)
            fallo.set_volume(1.0)
            return {'exito': exito, 'fallo': fallo}
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
            return {'exito': None, 'fallo': None}
    
    def _cargar_fondo(self):
        try:
            fondo = pygame.image.load(f"{RUTA_IMAGES}fondo.png").convert()
            return pygame.transform.scale(fondo, (ANCHO, ALTO))
        except:
            # Crear fondo degradado
            fondo = pygame.Surface((ANCHO, ALTO))
            for y in range(ALTO):
                color_r = int(135 * (1 - y / ALTO))
                color_g = int(206 * (1 - y / ALTO))
                color_b = int(235 * (1 - y / ALTO))
                pygame.draw.line(fondo, (color_r, color_g, color_b), (0, y), (ANCHO, y))
            return fondo
    
    def iniciar_musica(self):
        try:
            pygame.mixer.music.load(f"{RUTA_MUSIC}musica_fondo.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            print("No se pudo cargar la música de fondo")

# ==================== GESTORES DE DATOS ====================
class GestorPuntajes:
    """Gestiona la persistencia de puntajes y récords"""
    
    ARCHIVO_RECORD = f"{RUTA_DATA}record.txt"
    ARCHIVO_PUNTAJES = f"{RUTA_DATA}puntajes.json"
    
    def __init__(self):
        self.record = self._cargar_record()
        self.puntajes_altos = self._cargar_puntajes()
    
    def _cargar_record(self):
        try:
            if os.path.exists(self.ARCHIVO_RECORD):
                with open(self.ARCHIVO_RECORD, "r") as file:
                    return int(file.read())
        except:
            pass
        return 0
    
    def guardar_record(self, puntos):
        if puntos > self.record:
            self.record = puntos
            try:
                with open(self.ARCHIVO_RECORD, "w") as file:
                    file.write(str(self.record))
            except:
                pass
            return True
        return False
    
    def _cargar_puntajes(self):
        try:
            if os.path.exists(self.ARCHIVO_PUNTAJES):
                with open(self.ARCHIVO_PUNTAJES, "r") as file:
                    return json.load(file)
        except:
            pass
        return []
    
    def guardar_puntaje(self, puntos):
        try:
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            nuevo_puntaje = {"puntos": puntos, "fecha": fecha}
            self.puntajes_altos.append(nuevo_puntaje)
            self.puntajes_altos.sort(key=lambda x: x["puntos"], reverse=True)
            self.puntajes_altos = self.puntajes_altos[:10]
            
            with open(self.ARCHIVO_PUNTAJES, "w") as file:
                json.dump(self.puntajes_altos, file)
        except:
            pass

# ==================== ENTIDADES DEL JUEGO ====================
class Personaje:
    """Representa al personaje jugable"""
    
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.angulo = 0
        self.en_suelo = True
        self.sprites = sprites
        self.acrobacia_actual = None
        self.acrobacia_timer = 0
        
        # Constantes de física
        self.gravedad = 0.4
        self.fuerza_salto = -13
        self.rotacion_vel = 10
    
    def saltar(self):
        if self.en_suelo:
            self.vel_y = self.fuerza_salto
            self.en_suelo = False
            return True
        return False
    
    def actualizar_fisica(self):
        self.vel_y += self.gravedad
        self.y += self.vel_y
    
    def rotar_izquierda(self):
        if not self.en_suelo:
            self.angulo += self.rotacion_vel
            return 5  # Puntos por rotación
        return 0
    
    def rotar_derecha(self):
        if not self.en_suelo:
            self.angulo -= self.rotacion_vel
            return 5  # Puntos por rotación
        return 0
    
    def realizar_acrobacia(self, tecla):
        if not self.en_suelo and tecla in self.sprites['acrobacias']:
            self.acrobacia_actual = self.sprites['acrobacias'][tecla]
            self.acrobacia_timer = 20
            return True
        return False
    
    def aterrizar(self, y_suelo):
        self.y = y_suelo
        self.vel_y = 0
        self.en_suelo = True
        self.angulo = 0
    
    def verificar_aterrizaje_correcto(self):
        angulo_normalizado = abs(self.angulo % 360)
        return angulo_normalizado <= 50 or angulo_normalizado >= 310
    
    def dibujar(self, ventana, offset_x=0):
        sprite = self.sprites['personaje']
        
        if self.acrobacia_actual and self.acrobacia_timer > 0:
            sprite = self.acrobacia_actual
            self.acrobacia_timer -= 1
        else:
            self.acrobacia_actual = None
        
        sprite_rotado = pygame.transform.rotate(sprite, self.angulo)
        rect = sprite_rotado.get_rect(center=(self.x + 32, self.y + 32))
        ventana.blit(sprite_rotado, rect.topleft)


class Rampa:
    """Representa una rampa en el nivel"""
    
    def __init__(self, base_x, base_y, ancho, altura):
        self.puntos = [
            (base_x, base_y),
            (base_x + ancho, base_y),
            (base_x + ancho, base_y + altura)
        ]
    
    def detectar_colision(self, x_centro, y_centro, offset_x):
        (x1, y1), (x2, y2), (x3, y3) = self.puntos
        x1 -= offset_x
        x2 -= offset_x
        x3 -= offset_x
        
        if x1 <= x_centro <= x2:
            pendiente = (y3 - y1) / ((x3 - x1) + 0.01)
            altura_rampa = pendiente * (x_centro - x1) + y1
            if abs((y_centro + 64) - altura_rampa) < 20:
                return altura_rampa - 64
        return None
    
    def dibujar(self, ventana, offset_x=0):
        puntos_ajustados = [(x - offset_x, y) for x, y in self.puntos]
        pygame.draw.polygon(ventana, VERDE, puntos_ajustados)


class GestorRampas:
    """Gestiona la generación y actualización de rampas"""
    
    def __init__(self, suelo_y):
        self.rampas = []
        self.suelo_y = suelo_y
    
    def generar_rampa(self):
        base_x = self.rampas[-1].puntos[1][0] + random.randint(250, 400) if self.rampas else 600
        base_y = self.suelo_y + 64
        
        altura = random.choice([
            random.randint(-150, -100),
            random.randint(-100, -60),
            random.randint(-60, -20)
        ])
        
        ancho = random.choice([
            random.randint(100, 150),
            random.randint(160, 220),
            random.randint(230, 300)
        ])
        
        nueva_rampa = Rampa(base_x, base_y, ancho, altura)
        self.rampas.append(nueva_rampa)
    
    def actualizar(self, offset_x, ancho_pantalla):
        while not self.rampas or self.rampas[-1].puntos[1][0] - offset_x < ancho_pantalla + 200:
            self.generar_rampa()
    
    def detectar_colision(self, x_centro, y_centro, offset_x):
        for rampa in self.rampas:
            colision = rampa.detectar_colision(x_centro, y_centro, offset_x)
            if colision is not None:
                return colision
        return None
    
    def dibujar(self, ventana, offset_x):
        for rampa in self.rampas:
            rampa.dibujar(ventana, offset_x)
    
    def reiniciar(self):
        self.rampas = []


class SistemaAcrobacias:
    """Gestiona las acrobacias y el sistema de puntuación"""
    
    ACROBACIAS = {
        pygame.K_w: ("Backflip", 30),
        pygame.K_s: ("Frontflip", 30),
        pygame.K_q: ("Twist", 50),
        pygame.K_a: ("Spin", 40),
    }
    
    def __init__(self):
        self.acrobacias_realizando = {}
        self.puntos_temp = 0
        self.reiniciar()
    
    def reiniciar(self):
        self.acrobacias_realizando = {k: False for k in self.ACROBACIAS}
        self.puntos_temp = 0
    
    def registrar_acrobacia(self, tecla):
        if tecla in self.ACROBACIAS:
            self.acrobacias_realizando[tecla] = True
    
    def calcular_puntos(self):
        total = self.puntos_temp
        for tecla, realizada in self.acrobacias_realizando.items():
            if realizada:
                nombre, valor = self.ACROBACIAS[tecla]
                total += valor
        return total
    
    def agregar_puntos_temp(self, puntos):
        self.puntos_temp += puntos


class SistemaCombo:
    """Gestiona el sistema de combos y multiplicadores"""
    
    def __init__(self, barra_max=100, timer_max=120):
        self.barra = 0
        self.barra_max = barra_max
        self.timer = 0
        self.timer_max = timer_max
        self.multiplicador = 1.0
    
    def agregar_combo(self, valor):
        self.barra += valor
        if self.barra > self.barra_max:
            self.barra = self.barra_max
        self.timer = self.timer_max
        self._actualizar_multiplicador()
    
    def actualizar(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            if self.barra > 0:
                self.barra -= 1
            if self.barra < 0:
                self.barra = 0
        self._actualizar_multiplicador()
    
    def _actualizar_multiplicador(self):
        self.multiplicador = 1 + self.barra / self.barra_max
    
    def reiniciar(self):
        self.barra = 0
        self.timer = 0
        self.multiplicador = 1.0


class SistemaVida:
    """Gestiona el sistema de vidas"""
    
    def __init__(self, vida_max=3):
        self.vida_max = vida_max
        self.vida = vida_max
    
    def perder_vida(self):
        self.vida -= 1
        return self.vida <= 0
    
    def reiniciar(self):
        self.vida = self.vida_max


# ==================== ESTADOS DEL JUEGO ====================
class Estado(ABC):
    """Clase base para los estados del juego"""
    
    def __init__(self, juego):
        self.juego = juego
    
    @abstractmethod
    def manejar_eventos(self, eventos):
        pass
    
    @abstractmethod
    def actualizar(self):
        pass
    
    @abstractmethod
    def dibujar(self, ventana):
        pass


class MenuPrincipal(Estado):
    """Estado del menú principal"""
    
    def __init__(self, juego):
        super().__init__(juego)
        self.opciones = ["Jugar", "Puntajes", "Créditos", "Salir"]
        self.seleccionado = 0
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.seleccionado = (self.seleccionado - 1) % len(self.opciones)
                elif evento.key == pygame.K_DOWN:
                    self.seleccionado = (self.seleccionado + 1) % len(self.opciones)
                elif evento.key == pygame.K_RETURN:
                    self._ejecutar_opcion()
    
    def _ejecutar_opcion(self):
        if self.seleccionado == 0:  # Jugar
            self.juego.cambiar_estado('jugando')
        elif self.seleccionado == 1:  # Puntajes
            self.juego.cambiar_estado('puntajes')
        elif self.seleccionado == 2:  # Créditos
            self.juego.cambiar_estado('creditos')
        elif self.seleccionado == 3:  # Salir
            pygame.quit()
            sys.exit()
    
    def actualizar(self):
        pass
    
    def dibujar(self, ventana):
        ventana.fill(AZUL_OSCURO)
        recursos = self.juego.recursos
        
        # Título
        titulo = recursos.fuentes['titulo'].render("Stunt Bike Extreme", True, AMARILLO)
        titulo_rect = titulo.get_rect(center=(ANCHO//2, 150))
        ventana.blit(titulo, titulo_rect)
        
        subtitulo = recursos.fuentes['menu'].render("Acrobacia Extrema", True, BLANCO)
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO//2, 200))
        ventana.blit(subtitulo, subtitulo_rect)
        
        # Opciones
        for i, opcion in enumerate(self.opciones):
            color = AMARILLO if i == self.seleccionado else BLANCO
            texto = recursos.fuentes['menu'].render(opcion, True, color)
            texto_rect = texto.get_rect(center=(ANCHO//2, 300 + i * 60))
            ventana.blit(texto, texto_rect)
            
            if i == self.seleccionado:
                pygame.draw.rect(ventana, AMARILLO, texto_rect.inflate(20, 10), 3)
        
        # Controles
        controles = recursos.fuentes['pequeña'].render(
            "Usa las flechas para navegar y ENTER para seleccionar", True, GRIS_CLARO
        )
        controles_rect = controles.get_rect(center=(ANCHO//2, ALTO - 50))
        ventana.blit(controles, controles_rect)


class EstadoJugando(Estado):
    """Estado principal del juego"""
    
    def __init__(self, juego):
        super().__init__(juego)
        self.reiniciar()
    
    def reiniciar(self):
        self.personaje = Personaje(ANCHO // 2, ALTO - 150, self.juego.recursos.sprites)
        self.gestor_rampas = GestorRampas(ALTO - 100)
        self.sistema_acrobacias = SistemaAcrobacias()
        self.sistema_combo = SistemaCombo()
        self.sistema_vida = SistemaVida()
        
        self.puntos = 0
        self.offset_x = 0
        self.velocidad = 5
        self.suelo_y = ALTO - 100
        
        self.mensaje = ""
        self.mensaje_color = ROJO
        self.contador_mensaje = 0
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.personaje.saltar():
                        self.sistema_acrobacias.reiniciar()
                elif evento.key == pygame.K_ESCAPE:
                    self.juego.cambiar_estado('menu')
    
    def actualizar(self):
        teclas = pygame.key.get_pressed()
        
        # Movimiento de cámara
        if teclas[pygame.K_RIGHT]:
            self.offset_x += self.velocidad
        if teclas[pygame.K_LEFT]:
            self.offset_x = max(0, self.offset_x - self.velocidad)
        
        # Rotación y acrobacias en el aire
        if not self.personaje.en_suelo:
            if teclas[pygame.K_a]:
                pts = self.personaje.rotar_izquierda()
                self.sistema_acrobacias.agregar_puntos_temp(pts)
            if teclas[pygame.K_d]:
                pts = self.personaje.rotar_derecha()
                self.sistema_acrobacias.agregar_puntos_temp(pts)
            
            for tecla in self.sistema_acrobacias.ACROBACIAS:
                if teclas[tecla]:
                    if self.personaje.realizar_acrobacia(tecla):
                        self.sistema_acrobacias.registrar_acrobacia(tecla)
        
        # Actualizar físicas
        self.personaje.actualizar_fisica()
        self.sistema_combo.actualizar()
        
        # Detectar colisiones
        colision = self.gestor_rampas.detectar_colision(
            self.personaje.x, self.personaje.y, self.offset_x
        )
        
        if colision is not None:
            if not self.personaje.en_suelo:
                self._procesar_aterrizaje()
            self.personaje.aterrizar(colision)
        elif self.personaje.y >= self.suelo_y:
            if not self.personaje.en_suelo:
                self._procesar_aterrizaje()
            self.personaje.aterrizar(self.suelo_y)
        
        # Generar rampas
        self.gestor_rampas.actualizar(self.offset_x, ANCHO)
        
        # Actualizar mensajes
        if self.contador_mensaje > 0:
            self.contador_mensaje -= 1
    
    def _procesar_aterrizaje(self):
        if self.personaje.verificar_aterrizaje_correcto():
            self._aterrizaje_exitoso()
        else:
            self._aterrizaje_fallido()
    
    def _aterrizaje_exitoso(self):
        if self.juego.recursos.sonidos['exito']:
            self.juego.recursos.sonidos['exito'].play()
        
        puntos_base = self.sistema_acrobacias.calcular_puntos()
        self.sistema_combo.agregar_combo(puntos_base)
        
        puntos_totales = int(puntos_base * self.sistema_combo.multiplicador)
        self.puntos += puntos_totales
        
        self.mensaje = f"¡Aterrizaje! +{puntos_totales} pts (x{self.sistema_combo.multiplicador:.1f})"
        self.mensaje_color = VERDE
        self.contador_mensaje = 120
        
        self.juego.gestor_puntajes.guardar_record(self.puntos)
    
    def _aterrizaje_fallido(self):
        if self.juego.recursos.sonidos['fallo']:
            self.juego.recursos.sonidos['fallo'].play()
        
        mensajes_fallidos = [
            "¡Ese bache era invisible, lo juro!",
            "¡Ups! No era la pista de aterrizaje...",
            "¡Creo que olvidé bajar el tren de aterrizaje!",
            "¡Eso dejó una marca en el orgullo!",
            "¡Mal cálculo... otra vez!"
        ]
        
        self.mensaje = random.choice(mensajes_fallidos)
        self.mensaje_color = ROJO
        self.contador_mensaje = 120
        
        if self.sistema_vida.perder_vida():
            self.juego.gestor_puntajes.guardar_puntaje(self.puntos)
            self.juego.cambiar_estado('game_over', puntos_finales=self.puntos)
        
        self.sistema_combo.reiniciar()
    
    def dibujar(self, ventana):
        ventana.blit(self.juego.recursos.fondo, (0, 0))
        
        # Suelo
        pygame.draw.rect(ventana, GRIS, (0, self.suelo_y + 64, ANCHO, 100))
        
        # Rampas
        self.gestor_rampas.dibujar(ventana, self.offset_x)
        
        # Personaje
        self.personaje.dibujar(ventana, self.offset_x)
        
        # UI
        self._dibujar_ui(ventana)
    
    def _dibujar_ui(self, ventana):
        recursos = self.juego.recursos
        
        # Puntos y récord
        texto_puntos = recursos.fuentes['menu'].render(f"Puntos: {self.puntos}", True, BLANCO)
        ventana.blit(texto_puntos, (20, 20))
        
        texto_record = recursos.fuentes['texto'].render(
            f"Récord: {self.juego.gestor_puntajes.record}", True, AZUL
        )
        ventana.blit(texto_record, (20, 60))
        
        # Vida
        for i in range(self.sistema_vida.vida_max):
            color = ROJO if i < self.sistema_vida.vida else GRIS
            pygame.draw.rect(ventana, color, (20 + i * 40, 100, 30, 30))
        
        # Barra de combo
        pygame.draw.rect(ventana, GRIS, (20, 140, 200, 25))
        ancho_combo = int((self.sistema_combo.barra / self.sistema_combo.barra_max) * 200)
        pygame.draw.rect(ventana, AMARILLO, (20, 140, ancho_combo, 25))
        texto_combo = recursos.fuentes['texto'].render(
            f"Combo x{self.sistema_combo.multiplicador:.1f}", True, BLANCO
        )
        ventana.blit(texto_combo, (230, 140))
        
        # Mensajes
        if self.contador_mensaje > 0:
            texto = recursos.fuentes['menu'].render(self.mensaje, True, self.mensaje_color)
            ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 180))
        
        # Controles (solo al inicio)
        if self.offset_x < 100:
            controles = [
                "ESPACIO: Saltar",
                "A/D: Rotar",
                "W/S/Q/A: Acrobacias",
                "←/→: Mover cámara",
                "ESC: Menú"
            ]
            for i, control in enumerate(controles):
                texto = recursos.fuentes['pequeña'].render(control, True, GRIS_CLARO)
                ventana.blit(texto, (ANCHO - 200, 20 + i * 20))


class EstadoPuntajes(Estado):
    """Estado de visualización de puntajes"""
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.juego.cambiar_estado('menu')
    
    def actualizar(self):
        pass
    
    def dibujar(self, ventana):
        ventana.fill(AZUL_OSCURO)
        recursos = self.juego.recursos
        gestor = self.juego.gestor_puntajes
        
        # Título
        titulo = recursos.fuentes['titulo'].render("MEJORES PUNTAJES", True, AMARILLO)
        titulo_rect = titulo.get_rect(center=(ANCHO//2, 80))
        ventana.blit(titulo, titulo_rect)
        
        # Récord actual
        record_texto = recursos.fuentes['menu'].render(f"Récord Actual: {gestor.record}", True, VERDE)
        record_rect = record_texto.get_rect(center=(ANCHO//2, 130))
        ventana.blit(record_texto, record_rect)
        
        # Lista de puntajes
        if gestor.puntajes_altos:
            for i, puntaje in enumerate(gestor.puntajes_altos[:10]):
                y_pos = 180 + i * 35
                posicion = recursos.fuentes['texto'].render(f"{i+1}.", True, BLANCO)
                puntos = recursos.fuentes['texto'].render(f"{puntaje['puntos']} pts", True, AMARILLO)
                fecha = recursos.fuentes['pequeña'].render(puntaje['fecha'], True, GRIS_CLARO)
                
                ventana.blit(posicion, (200, y_pos))
                ventana.blit(puntos, (250, y_pos))
                ventana.blit(fecha, (400, y_pos + 5))
        else:
            no_puntajes = recursos.fuentes['texto'].render(
                "No hay puntajes registrados", True, GRIS_CLARO
            )
            no_puntajes_rect = no_puntajes.get_rect(center=(ANCHO//2, 250))
            ventana.blit(no_puntajes, no_puntajes_rect)
        
        # Instrucciones
        volver = recursos.fuentes['pequeña'].render(
            "Presiona ESC para volver al menú", True, GRIS_CLARO
        )
        volver_rect = volver.get_rect(center=(ANCHO//2, ALTO - 50))
        ventana.blit(volver, volver_rect)


class EstadoCreditos(Estado):
    """Estado de créditos"""
    
    def __init__(self, juego):
        super().__init__(juego)
        self.scroll = 0
        self.creditos_info = [
            "",
            "Stunt Bike Extreme",
            "",
            "Desarrollado con Python & Pygame",
            "",
            "CONTROLES:",
            "ESPACIO - Saltar",
            "A/D - Rotar en el aire",
            "W - Backflip",
            "S - Frontflip",
            "Q - Twist",
            "A - Spin",
            "← → - Mover cámara",
            "",
            "OBJETIVO:",
            "Realiza acrobacias espectaculares",
            "Aterriza correctamente para ganar puntos",
            "Construye combos para multiplicar tu puntaje",
            "¡Evita romperte los huesos!",
            "",
            "¡Gracias por jugar!",
            "",
            ""
        ]
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.scroll = 0
                    self.juego.cambiar_estado('menu')
    
    def actualizar(self):
        self.scroll += 1
        if self.scroll > len(self.creditos_info) * 30 + 200:
            self.scroll = 0
    
    def dibujar(self, ventana):
        ventana.fill(AZUL_OSCURO)
        recursos = self.juego.recursos
        
        # Título
        titulo = recursos.fuentes['titulo'].render("CRÉDITOS", True, AMARILLO)
        titulo_rect = titulo.get_rect(center=(ANCHO//2, 80))
        ventana.blit(titulo, titulo_rect)
        
        # Información scrolleando
        y_offset = 150 - self.scroll
        for linea in self.creditos_info:
            if y_offset > -30 and y_offset < ALTO + 30:
                if linea.startswith("HUESOS ROTOS") or linea.startswith("CONTROLES") or linea.startswith("OBJETIVO"):
                    texto = recursos.fuentes['menu'].render(linea, True, AMARILLO)
                elif linea == "":
                    y_offset += 10
                    continue
                else:
                    texto = recursos.fuentes['texto'].render(linea, True, BLANCO)
                
                texto_rect = texto.get_rect(center=(ANCHO//2, y_offset))
                ventana.blit(texto, texto_rect)
            
            y_offset += 30
        
        # Instrucciones
        volver = recursos.fuentes['pequeña'].render(
            "Presiona ESC para volver al menú", True, GRIS_CLARO
        )
        volver_rect = volver.get_rect(center=(ANCHO//2, ALTO - 50))
        ventana.blit(volver, volver_rect)


class EstadoGameOver(Estado):
    """Estado de Game Over"""
    
    def __init__(self, juego, puntos_finales=0):
        super().__init__(juego)
        self.puntos_finales = puntos_finales
        self.es_nuevo_record = (puntos_finales == juego.gestor_puntajes.record)
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    self.juego.cambiar_estado('menu')
    
    def actualizar(self):
        pass
    
    def dibujar(self, ventana):
        ventana.fill(ROJO)
        recursos = self.juego.recursos
        
        # Título
        titulo = recursos.fuentes['titulo'].render("GAME OVER", True, BLANCO)
        titulo_rect = titulo.get_rect(center=(ANCHO//2, 200))
        ventana.blit(titulo, titulo_rect)
        
        # Puntaje final
        puntaje = recursos.fuentes['menu'].render(
            f"Puntaje Final: {self.puntos_finales}", True, AMARILLO
        )
        puntaje_rect = puntaje.get_rect(center=(ANCHO//2, 280))
        ventana.blit(puntaje, puntaje_rect)
        
        # Nuevo récord
        if self.es_nuevo_record:
            nuevo_record = recursos.fuentes['texto'].render("¡NUEVO RÉCORD!", True, VERDE)
            nuevo_record_rect = nuevo_record.get_rect(center=(ANCHO//2, 320))
            ventana.blit(nuevo_record, nuevo_record_rect)
        
        # Instrucciones
        continuar = recursos.fuentes['texto'].render(
            "Presiona ENTER para volver al menú", True, BLANCO
        )
        continuar_rect = continuar.get_rect(center=(ANCHO//2, ALTO - 100))
        ventana.blit(continuar, continuar_rect)


# ==================== JUEGO PRINCIPAL ====================
class Juego:
    """Clase principal que gestiona el juego"""
    
    def __init__(self):
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Stunt Bike Extreme")
        
        self.recursos = GestorRecursos()
        self.gestor_puntajes = GestorPuntajes()
        self.reloj = pygame.time.Clock()
        
        # Iniciar música
        self.recursos.iniciar_musica()
        
        # Estados del juego
        self.estados = {
            'menu': MenuPrincipal(self),
            'jugando': None,  # Se crea cuando se necesita
            'puntajes': EstadoPuntajes(self),
            'creditos': EstadoCreditos(self),
            'game_over': None  # Se crea cuando se necesita
        }
        
        self.estado_actual = self.estados['menu']
    
    def cambiar_estado(self, nombre_estado, **kwargs):
        if nombre_estado == 'jugando':
            self.estados['jugando'] = EstadoJugando(self)
            self.estados['jugando'].reiniciar()
            self.estado_actual = self.estados['jugando']
        elif nombre_estado == 'game_over':
            puntos = kwargs.get('puntos_finales', 0)
            self.estados['game_over'] = EstadoGameOver(self, puntos)
            self.estado_actual = self.estados['game_over']
        else:
            self.estado_actual = self.estados[nombre_estado]
    
    def ejecutar(self):
        while True:
            # Capturar eventos
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Manejar eventos del estado actual
            self.estado_actual.manejar_eventos(eventos)
            
            # Actualizar estado actual
            self.estado_actual.actualizar()
            
            # Dibujar estado actual
            self.estado_actual.dibujar(self.ventana)
            
            # Actualizar pantalla
            pygame.display.flip()
            self.reloj.tick(60)


# ==================== PUNTO DE ENTRADA ====================
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()