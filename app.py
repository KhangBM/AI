import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Hàm tạo mê cung ngẫu nhiên
def generate_maze(size):
    maze = np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])
    maze[0][0] = 0 
    maze[-1][-1] = 0  
    return maze

# Hàm tìm đường đi dùng BFS
def solve_maze(maze):
    rows, cols = maze.shape
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
    visited = np.zeros_like(maze)
    queue = deque([(0, 0, [(0, 0)])])  

    while queue:
        x, y, path = queue.popleft()
        if (x, y) == (rows - 1, cols - 1): 
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = 1
                queue.append((nx, ny, path + [(nx, ny)]))

    return None 

# Hàm vẽ mê cung và đường đi
def draw_maze(maze, path=None):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(maze, cmap="binary")

    if path:
        x, y = zip(*path)
        ax.plot(y, x, color="red", linewidth=2)

    ax.axis("off")
    st.pyplot(fig)

# Giao diện Streamlit
st.title("Maze Solver")
maze_size = st.slider("Chọn kích thước mê cung", 5, 20, 10)
maze = generate_maze(maze_size)

if st.button("Tạo mê cung mới"):
    st.session_state.maze = generate_maze(maze_size)

if "maze" not in st.session_state:
    st.session_state.maze = maze

maze = st.session_state.maze
draw_maze(maze)

if st.button("Tìm đường đi"):
    path = solve_maze(maze)
    if path:
        st.success("Tìm được đường đi!")
        draw_maze(maze, path)
    else:
        st.error("Không tìm được đường đi!")
