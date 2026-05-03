import matplotlib.pyplot as plt
# параметри системи Лоренца
sigma = 10
rho = 28
beta = 8/3
delta_t = 0.01
# налаштування
SIMULATION_TIME = 30

def init(x_init, y_init, z_init):
    return [x_init], [y_init], [z_init], [0]

def upd(x_res, y_res, z_res, time_steps):
    # отримуємо крайні значення x, y, z
    x = x_res[-1]
    y = y_res[-1]
    z = z_res[-1]
    t = time_steps[-1]
    # знаходимо нові значення
    delta_x = sigma*(y - x) * delta_t
    delta_y = (rho*x - y - x*z) * delta_t
    delta_z = (x*y - beta*z) * delta_t
    x += delta_x
    y += delta_y
    z += delta_z
    t += delta_t
    # додаємо нові значення в кінець списків
    x_res.append(x)
    y_res.append(y)
    z_res.append(z)
    time_steps.append(t)

def run(x_init, y_init, z_init):
    x_res, y_res, z_res, time_steps = init(x_init, y_init, z_init)
    t = time_steps[-1]
    while t < SIMULATION_TIME:
        upd(x_res, y_res, z_res, time_steps)
        t = time_steps[-1]
    return x_res, y_res, z_res, time_steps

def display(solution1, solution2):
    x1, y1, z1, time1 = solution1[0], solution1[1], solution1[2], solution1[3]
    x2, y2, z2, time2 = solution2[0], solution2[1], solution2[2], solution2[3]
    fig = plt.figure(figsize=(12, 12))
    # створюємо 3 піддіаграми для 2д і  1 для 3д графіків
    ax3d = fig.add_subplot(221, projection="3d")
    ax2d1 = fig.add_subplot(222)
    ax2d2 = fig.add_subplot(223)
    ax2d3 = fig.add_subplot(224)
    # додамєо 3д графік на піддіаграму
    ax3d.set_title("Атрактор лоренца")
    ax3d.plot(x1, y1, z1, label="Початкові умови 1")
    ax3d.plot(x2, y2, z2, label="Початкові умови 2", alpha=0.6)
    ax3d.legend()
    # додамєо 2д графіки на піддіаграму  
    # по X
    ax2d1.set_title("Значення по осі X")
    ax2d1.plot(time1, x1, label="Початкові умови 1")
    ax2d1.plot(time2, x2, label="Початкові умови 2", alpha=0.6)  
    ax2d1.legend()
    # по Y
    ax2d2.set_title("Значення по осі Y")
    ax2d2.plot(time1, y1, label="Початкові умови 1")
    ax2d2.plot(time2, y2, label="Початкові умови 2", alpha=0.6)  
    ax2d2.legend()
    # по Z
    ax2d3.set_title("Значення по осі Z")
    ax2d3.plot(time1, z1, label="Початкові умови 1")
    ax2d3.plot(time2, z2, label="Початкові умови 2", alpha=0.6)
    ax2d3.legend()
    # відображаємо графік
    plt.show()
    
if __name__ == "__main__":
    solution1 = (run(1, 1, 1))
    solution2 = (run(1, 1, 1.0001))
    display(solution1, solution2)
