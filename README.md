這是一個簡單的偵測螢幕是否有人，假如有人按下滑鼠中鍵進行瞄準，滑鼠會用mediapipe偵測是否有人，有人會自動把鼠標移動到鼻子也就是0位置

有幾個地方會需要根據使用者電腦不同進行更改

改成自己的螢幕分辨率

# 定义截图区域
screen_area = (0, 0, 1920, 1080)  # 根据您的屏幕分辨率进行调整


改成自己的電腦對應的x,y軸

# 移动鼠标到头部位置
x = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * 1550)
y = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * 850)

