import matplotlib.pyplot as plt
import numpy as np

def plot_parallel_line(A, B, C):
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    # Tính độ dốc của đoạn thẳng AB
    m_AB = (y2 - y1) / (x2 - x1)

    # Xác định phương trình đường thẳng AB
    x_vals = np.array([x1, x2])
    y_vals = m_AB * (x_vals - x1) + y1

    # Xác định phương trình đường thẳng song song đi qua C
    y_vals_parallel = m_AB * (x_vals - x3) + y3

    print(x_vals, y_vals)

    plt.plot(x_vals, y_vals, label='Đoạn thẳng AB')
    plt.plot(x_vals, y_vals_parallel, label='Đường thẳng song song qua C')

    plt.scatter([x1, x2, x3], [y1, y2, y3], color='red')
    plt.text(x1, y1, 'A', fontsize=12, ha='right')
    plt.text(x2, y2, 'B', fontsize=12, ha='right')
    plt.text(x3, y3, 'C', fontsize=12, ha='right')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.show()

# Ví dụ sử dụng
A = (1, 2)
B = (4, 6)
C = (2, 3)
plot_parallel_line(A, B, C)
