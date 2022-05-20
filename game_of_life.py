import dearpygui.dearpygui as dpg
from threading import Thread
from time import sleep

columnAmt = 70
rowAmt = 35

colorsId = []
nextFrame = []

configuration = []

simSpeed = 0.20
running = False

wrappingLR = True
wrappingTD = True


def get_near_cells_amount(cell):
    # get the cells near another one, and returns the count of live cells
    topLeft, top, topRight, left, right, bottomLeft, bottom, bottomRight = [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]

    if cell[1] != 0:
        top = colorsId[(cell[0] - 0)][(cell[1] - 1)]
    if cell[1] != rowAmt - 1:
        bottom = colorsId[(cell[0] - 0)][(cell[1] + 1)]
    if cell[0] != 0:
        left = colorsId[(cell[0] - 1)][(cell[1] - 0)]
    if cell[0] != columnAmt - 1:
        right = colorsId[(cell[0] + 1)][(cell[1] - 0)]
    if cell[0] != 0 and cell[1] != 0:
        topLeft = colorsId[(cell[0] - 1)][(cell[1] - 1)]
    if cell[0] != 0 and cell[1] != rowAmt - 1:
        bottomLeft = colorsId[(cell[0] - 1)][(cell[1] + 1)]
    if cell[0] != columnAmt - 1 and cell[1] != 0:
        topRight = colorsId[(cell[0] + 1)][(cell[1] - 1)]
    if cell[0] != columnAmt - 1 and cell[1] != rowAmt - 1:
        bottomRight = colorsId[(cell[0] + 1)][(cell[1] + 1)]

    if wrappingTD:
        topLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] - 1) % rowAmt]
        top = colorsId[(cell[0] - 0) % columnAmt][(cell[1] - 1) % rowAmt]
        topRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] - 1) % rowAmt]
        bottomLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] + 1) % rowAmt]
        bottom = colorsId[(cell[0] - 0) % columnAmt][(cell[1] + 1) % rowAmt]
        bottomRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] + 1) % rowAmt]

    if wrappingLR:
        topLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] - 1) % rowAmt]
        left = colorsId[(cell[0] - 1) % columnAmt][(cell[1] - 0) % rowAmt]
        bottomLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] + 1) % rowAmt]
        topRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] - 1) % rowAmt]
        right = colorsId[(cell[0] + 1) % columnAmt][(cell[1] - 0) % rowAmt]
        bottomRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] + 1) % rowAmt]

    near_cells = topLeft, top, topRight, left, right, bottomLeft, bottom, bottomRight

    return list(i[1] for i in near_cells).count(1)


def gen_life(cell):
    """
    RULES
    Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by overpopulation.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    amt = get_near_cells_amount(cell)
    data = colorsId[cell[0]][cell[1]]  # [id, isAlive]

    if data[1] is True and amt < 2:
        nextFrame.append(data[0])
    elif data[1] is True and (amt == 2 or amt == 3):
        pass
    elif data[1] is True and amt > 3:
        nextFrame.append(data[0])
    elif data[1] is False and amt == 3:
        nextFrame.append(data[0])


def update():
    for i in range(columnAmt):
        for j in range(rowAmt):
            if get_near_cells_amount([i, j]) != 0 or colorsId[i][j][1]:
                gen_life([i, j])

    # after getting the frame situation, apply it
    for i in nextFrame:
        change_color(0, (0, i))

    nextFrame.clear()


def run():
    # thread function, starts the simulation in another thread
    dpg.set_value("RUNNING_SIMULATION_TEXT", "Running")
    dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[20, 200, 20])
    while running:
        update()
        sleep(simSpeed)


def start_sim():
    global running

    # starts the simulation
    if not running:
        running = True
        Thread(target=run, daemon=True).start()
    else:
        running = False
        dpg.set_value("RUNNING_SIMULATION_TEXT", "Stopped")
        dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[200, 30, 20])


def next_frame():
    # generate the next frame only
    if running is False:
        update()


def clear_board():
    for i in range(columnAmt):
        for j in range(rowAmt):
            if colorsId[i][j][1]:
                change_color(0, (0, colorsId[i][j][0]))


def stop_sim():
    # stop the simulation
    global running
    running = False

    # set texts
    dpg.set_value("RUNNING_SIMULATION_TEXT", "Stopped")
    dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[200, 30, 20])

    clear_board()


def save():
    global configuration
    configuration = [[[k for k in j] for j in i] for i in colorsId]


def load():
    global colorsId

    clear_board()

    # load config
    for i in range(columnAmt):
        for j in range(rowAmt):
            if configuration[i][j][1]:
                change_color(0, (0, configuration[i][j][0]))


def change_color(_s, data):
    if data[0] == 0:
        # set color
        v = dpg.get_value(data[1])
        dpg.set_value(data[1], [255 - v[0], 255 - v[1], 255 - v[2]])

        # change value on 2D - array
        cell = dpg.get_item_user_data(data[1])
        colorsId[cell[0]][cell[1]][1] = not colorsId[cell[0]][cell[1]][1]


def pause_sim():
    # pauses the simulation
    global running
    running = False
    dpg.set_value("RUNNING_SIMULATION_TEXT", "Stopped")
    dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[200, 30, 20])


def change_sim_speed(s, data):
    # changes the simulation speed
    global simSpeed
    simSpeed = data
    if data <= 1:
        data = 1 / data
    else:
        # warning math
        tension = 0.92
        t = 1 - (4 * tension) / ((1 + tension) ** 2)
        data = 2 * (data - 1)
        data = 1 + ((t ** data - 1) / (t - 1)) * (0.01 - 1)

    simSpeed = round(data, 2)
    dpg.configure_item(s, format=f"Simulation Speed: x{round(1 / data, 2)}")


def set_wrapping(s, data):
    # set the wrapping option
    global wrappingLR, wrappingTD
    if "LR" in dpg.get_item_label(s):
        wrappingLR = data
    elif "TD" in dpg.get_item_label(s):
        wrappingTD = data


def main():
    with dpg.item_handler_registry(tag="reg"):
        dpg.add_item_clicked_handler(callback=change_color)

    with dpg.window():
        dpg.set_primary_window(dpg.last_item(), True)
        with dpg.child_window(width=-1, height=90):
            with dpg.group(horizontal=True, horizontal_spacing=60):
                with dpg.child_window(width=470, height=35):
                    with dpg.group(horizontal=True, horizontal_spacing=15):
                        dpg.add_button(label="Start / Pause Simulation", callback=start_sim)
                        dpg.add_button(label="Stop / Clear Simulation", callback=stop_sim)
                        dpg.add_button(label="Next Frame", callback=next_frame)
                with dpg.child_window(width=266, height=35):
                    with dpg.group(horizontal=True):
                        dpg.add_slider_float(min_value=0.5, max_value=1.5, width=250, default_value=1, callback=change_sim_speed, format="Simulation Speed: x1")
                with dpg.child_window(width=156, height=35):
                    with dpg.group(horizontal=True):
                        dpg.add_text("Simulation: ")
                        dpg.add_text("Stopped", color=[200, 20, 20], tag="RUNNING_SIMULATION_TEXT")
            with dpg.group(horizontal=True, horizontal_spacing=60):
                with dpg.child_window(width=230, height=35):
                    with dpg.group(horizontal=True, horizontal_spacing=15):
                        dpg.add_checkbox(label="TD Wrapping", default_value=True, callback=set_wrapping)
                        dpg.add_checkbox(label="LR Wrapping", default_value=True, callback=set_wrapping)
                with dpg.child_window(width=187, height=35):
                    with dpg.group(horizontal=True, horizontal_spacing=15):
                        dpg.add_button(label="Save Board", callback=save)
                        dpg.add_button(label="Load Board", callback=load)

        # generating the grid
        for i in range(columnAmt):
            temp = []
            for j in range(rowAmt):
                # the dpg.add_color_button haven't a `tooltip` parameter, instead it's used a color_edit with a clicked handler
                x = dpg.generate_uuid()
                dpg.add_color_edit(no_tooltip=True, no_inputs=True, no_picker=True, no_drag_drop=True, pos=[i * 18 + 11, j * 18 + 105], tag=x, user_data=[i, j])
                dpg.bind_item_handler_registry(x, "reg")
                temp.append([x, False])
            colorsId.append(temp)
            configuration.append(temp)

    with dpg.theme() as theme:
        with dpg.theme_component():
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)

    dpg.bind_theme(theme)


if __name__ == '__main__':
    width = 18 * columnAmt + 39
    height = 18 * rowAmt + 156

    dpg.create_context()
    dpg.create_viewport(width=width, max_width=width, min_width=width, height=height, min_height=height, max_height=height, resizable=False, title="DPG Conway's Game Of Life", large_icon="src/GMF.ico", small_icon="src/GMF.ico")
    dpg.setup_dearpygui()

    main()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
