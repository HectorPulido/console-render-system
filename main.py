from classes import RenderEngine, Camera3d, Object3d
import keyboard
import time

speed = 5

camera = Camera3d(90, 60, 0.25, 6000)
model = Object3d("aircraft.obj", [0, 0, 0], [0, 0, 0])
render = RenderEngine(50, 100)

while True:
    model_positions = [camera.calculate_x_y(point) for point in model.points()]

    for i, j in model_positions:
        i, j = render.normalize(i, j)
        render.draw_point(i, j)

    render.print_room()

    if keyboard.is_pressed("p"):
        quit()

    if keyboard.is_pressed("w"):
        model.position[2] += speed

    if keyboard.is_pressed("s"):
        model.position[2] -= speed

    if keyboard.is_pressed("a"):
        model.position[1] += speed

    if keyboard.is_pressed("d"):
        model.position[1] -= speed

    if keyboard.is_pressed("q"):
        model.position[0] += speed

    if keyboard.is_pressed("e"):
        model.position[0] -= speed

    if keyboard.is_pressed("1"):
        model.rotation[0] += 0.25

    if keyboard.is_pressed("2"):
        model.rotation[0] -= 0.25

    time.sleep(0.1)
    render.clear()
