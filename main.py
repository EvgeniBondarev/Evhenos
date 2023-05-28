import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Параметры волны
A = 1  # Амплитуда
k = 2 * np.pi / 10  # Волновой вектор
ω = 2 * np.pi / 5  # Угловая частота
φ = 0  # Начальная фаза
damping_factor = 0.1  # Коэффициент затухания

# Время и пространственная сетка
t = np.linspace(0, 10, 100)  # Временные отсчеты
x = np.linspace(0, 10, 100)  # Пространственные отсчеты

# Создание сетки для визуализации
T, X = np.meshgrid(t, x)

# Функция для обновления анимации
def update(frame):
    """
    A: Это амплитуда волны. Задает максимальную величину колебаний.
        np.exp(-damping_factor * frame): Эта часть отвечает за затухание колебаний. np.exp(x) - это функция экспоненты, которая возводит число e (экспонента) в степень x. 
        Здесь x равно -damping_factor * frame, поэтому с увеличением значения frame и увеличением damping_factor амплитуда колебаний будет уменьшаться экспоненциально.
    np.sin(k * X - ω * frame + φ): Эта часть отвечает за форму колебаний волны. 
        np.sin(x) - это функция синуса, где x - угол, выраженный в радианах. 
        Здесь x равен (k * X - ω * frame + φ), что представляет комбинацию фазы, волнового вектора, угловой частоты и текущего времени. 
        Разность (k * X - ω * frame + φ) дает пространственную и временную зависимость колебаний, 
        а функция синуса преобразует эту зависимость в значения от -1 до 1.
    """
    # Вычисление значения волны в каждой точке сетки
    Y = A * np.exp(-damping_factor * frame) * np.sin(k * X - ω * frame + φ)

    # Очистка предыдущего кадра
    ax.clear()

    # Визуализация симуляции
    ax.plot_surface(T, X, Y, cmap='viridis')

    # Настройка осей
    ax.set_xlabel('Time')
    ax.set_ylabel('Space')
    ax.set_zlabel('Amplitude')
    ax.set_title('Damped Wave Animation')

# Создание трехмерной фигуры
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Создание анимации
animation = FuncAnimation(fig, update, frames=np.linspace(0, 10, 100), interval=50)

# Сохранение анимации в файл
animation.save('img\\damped_wave_animation.gif', writer='imagemagick')

# Отображение анимации в реальном времени
plt.show()
