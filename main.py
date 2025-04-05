import time
from pynput import keyboard
from classes import RenderEngine, Camera3d, Object3d

speed = 0.5

camera = Camera3d(60, 60, 0.25, 6000)
model = Object3d("cube.obj", [0, 0, 0], [0, 0, 0])
render = RenderEngine(100, 500)

# Almacena las teclas presionadas
pressed_keys = set()


def on_press(key):
    try:
        if key.char:
            pressed_keys.add(key.char)
    except:
        pass


def on_release(key):
    try:
        if key.char in pressed_keys:
            pressed_keys.remove(key.char)
    except:
        pass


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Para guardar el último "fotograma" como string
old_screen = ""


while True:
    # --- Movimiento/rotación del modelo según teclas ---
    if "p" in pressed_keys:
        break

    if "w" in pressed_keys:
        model.position[2] += speed
    if "s" in pressed_keys:
        model.position[2] -= speed
    if "a" in pressed_keys:
        model.position[1] += speed
    if "d" in pressed_keys:
        model.position[1] -= speed
    if "q" in pressed_keys:
        model.position[0] += speed
    if "e" in pressed_keys:
        model.position[0] -= speed

    if "1" in pressed_keys:
        model.rotation[0] += 0.25
    if "2" in pressed_keys:
        model.rotation[0] -= 0.25

    # 1) Primero "llenamos" (vaciamos) la matriz para dibujar desde cero
    render.fill_room()

    # 2) Calculamos posiciones
    model_positions = [camera.calculate_x_y(point) for point in model.points()]
    model_positions_normalized = [render.normalize(i, j) for i, j in model_positions]

    # 3) Dibujamos puntos en la matriz
    for i, j in model_positions_normalized:
        render.draw_point(i, j)

    # 4) Dibujamos aristas
    for edge in model.edges:
        for count, value in enumerate(edge):
            if count == len(edge) - 1:
                continue
            i, j = model_positions_normalized[value]
            x, y = model_positions_normalized[edge[count + 1]]
            render.draw_line(i, j, x, y)

    # 5) Convertimos la matriz a un string completo (así sabremos cómo se vería)
    new_screen = render.get_room_as_string()

    # 6) Comparamos con la pantalla anterior
    if new_screen != old_screen:
        # si SON distintos, limpiamos la consola e imprimimos
        render.clear_console()
        print(new_screen)
        old_screen = new_screen  # actualizamos la referencia

    # Dormimos un poco para no saturar CPU
    time.sleep(0.1)
