# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 11:38:11 2023

@author: user
"""

import cv2
import numpy as np
import mediapipe as mp
from pynput.mouse import Listener, Controller
from pynput import mouse
from PIL import ImageGrab

# 初始化 MediaPipe
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# 定义截图区域
screen_area = (0, 0, 1920, 1080)  # 根据您的屏幕分辨率进行调整

# 记录是否按住滑鼠中键
mouse_middle_pressed = False

# 鼠标事件处理函数
def on_click(x, y, button, pressed):
    global mouse_middle_pressed
    if button == mouse.Button.middle:
        mouse_middle_pressed = pressed

# 创建鼠标监听器
mouse_listener = Listener(on_click=on_click)

# 启动鼠标监听器
mouse_listener.start()

# 创建鼠标控制器
mouse_controller = Controller()

# 开始全身姿势检测
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:

    while True:
        # 检测是否按住滑鼠中键
        if mouse_middle_pressed:
            # 捕获屏幕截图
            screenshot = ImageGrab.grab(bbox=screen_area)
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

            # 进行姿势估计
            results = holistic.process(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                # 如果检测到姿势关键点才进行绘制和鼠标操作
                # 绘制姿势关键点和连接线
                skeleton_image = np.zeros_like(screenshot)
                mp_drawing.draw_landmarks(
                    skeleton_image,
                    results.pose_landmarks,
                    mp_holistic.POSE_CONNECTIONS)

                # 合并骨架图像和原始截图
                screenshot_with_skeleton = cv2.addWeighted(screenshot, 0.7, skeleton_image, 0.3, 0)
                
                # 移动鼠标到头部位置
                x = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * 1550)
                y = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * 850)
                mouse_controller.position = (x, y)

                # 在 OpenCV 窗口中显示带有骨架的图像
                cv2.imshow('Real-time Screen', screenshot_with_skeleton)
            else:
                # 如果未检测到姿势关键点，只显示原始截图
                cv2.imshow('Real-time Screen', screenshot)

        # 检查键盘输入
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

# 关闭监听器和 OpenCV 窗口
mouse_listener.stop()
cv2.destroyAllWindows()