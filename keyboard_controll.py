import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
import threading
import tempfile
import os
from gtts import gTTS
import pygame
from deep_translator import GoogleTranslator

# ========== 🎌 Japanese Virtual Keyboard ==========
def create_keyboard():
    def on_click(char):
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, current + char)
        update_translation()

    def clear_text():
        entry.delete(0, tk.END)
        translation_label.config(text="")

    def delete_last_char():
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, current[:-1])

    def speak_text():
        text = entry.get()
        if not text.strip():
            return

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_path = tmp_file.name

            tts = gTTS(text=text, lang='ja')
            tts.save(tmp_path)

            pygame.mixer.init()
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.unload()
            pygame.mixer.quit()

            os.remove(tmp_path)

        except Exception as e:
            print("Error during speech playback:", str(e))

    def update_translation():
        text = entry.get()
        if not text.strip():
            translation_label.config(text="")
            return

        try:
            translated = GoogleTranslator(source='ja', target='ar').translate(text)
            translation_label.config(text=f" الترجمة: {translated}")
        except Exception as e:
            translation_label.config(text=f" خطأ في الترجمة: {str(e)}")

    global entry, translation_label
    root = tk.Tk()
    root.title("Eye Controlled Japanese Keyboard")

    entry = tk.Entry(root, width=30, font=("Helvetica", 20))
    entry.pack(pady=10)

    translation_label = tk.Label(root, text="", font=("Helvetica", 16), fg="blue")
    translation_label.pack()

    keys = [
        ['あ', 'い', 'う', 'え', 'お'],
        ['か', 'き', 'く', 'け', 'こ'],
        ['さ', 'し', 'す', 'せ', 'そ'],
        ['た', 'ち', 'つ', 'て', 'と'],
        ['な', 'に', 'ぬ', 'ね', 'の'],
        ['は', 'ひ', 'ふ', 'へ', 'ほ'],
        ['ま', 'み', 'む', 'め', 'も'],
        ['や', '', 'ゆ', '', 'よ'],
        ['ら', 'り', 'る', 'れ', 'ろ'],
        ['わ', '', 'を', '', 'ん']
    ]

    for row in keys:
        frame = tk.Frame(root)
        frame.pack()
        for char in row:
            if char == '':
                tk.Label(frame, text=" ", width=5).pack(side=tk.LEFT)
            else:
                btn = tk.Button(frame, text=char, width=10, height=2, command=lambda c=char: on_click(c))
                btn.pack(side=tk.LEFT, padx=2, pady=2)

    bottom = tk.Frame(root)
    bottom.pack(pady=10)

    tk.Button(bottom, text="🗑 مسح", width=10, command=clear_text).pack(side=tk.LEFT, padx=10)
    tk.Button(bottom, text="⌫ حذف آخر حرف", width=15, command=delete_last_char).pack(side=tk.LEFT, padx=5)
    tk.Button(bottom, text="🔊 نطق", width=10, command=speak_text).pack(side=tk.LEFT, padx=10)

    root.mainloop()

threading.Thread(target=create_keyboard, daemon=True).start()

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            if id == 1:
                screen_x = (screen_w / frame_w) * (x - frame_w / 2) * 2 + screen_w / 2
                screen_y = (screen_h / frame_h) * (y - frame_h / 2) * 2 + screen_h / 2

                try:
                    cur_x, cur_y = pyautogui.position()
                    smooth_factor = 0.5  # زيادة سرعة الحركة
                    final_x = cur_x + (screen_x - cur_x) * smooth_factor
                    final_y = cur_y + (screen_y - cur_y) * smooth_factor
                    pyautogui.moveTo(final_x, final_y)
                except:
                    pyautogui.moveTo(screen_x, screen_y)

        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left_eye[0].y - left_eye[1].y) < 0.007:
            pyautogui.click()
            pyautogui.sleep(1)

    cv2.imshow('🖱 Eye Controlled Mouse', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break




# import cv2
# import mediapipe as mp
# import pyautogui
# import tkinter as tk
# import threading
# import tempfile
# import os
# from gtts import gTTS
# import pygame
# from deep_translator import GoogleTranslator
#
# # ========== 🎌 Japanese Virtual Keyboard ==========
# def create_keyboard():
#     def on_click(char):
#         current = entry.get()
#         entry.delete(0, tk.END)
#         entry.insert(0, current + char)
#         update_translation()
#
#     def clear_text():
#         entry.delete(0, tk.END)
#         translation_label.config(text="")
#
#     def delete_last_char():
#         current = entry.get()
#         entry.delete(0, tk.END)
#         entry.insert(0, current[:-1])
#
#     def speak_text():
#         text = entry.get()
#         if not text.strip():
#             return
#
#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
#                 tmp_path = tmp_file.name
#
#             tts = gTTS(text=text, lang='ja')
#             tts.save(tmp_path)
#
#             pygame.mixer.init()
#             pygame.mixer.music.load(tmp_path)
#             pygame.mixer.music.play()
#
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
#
#             pygame.mixer.music.unload()
#             pygame.mixer.quit()
#
#             os.remove(tmp_path)
#
#         except Exception as e:
#             print("Error during speech playback:", str(e))
#
#     def update_translation():
#         text = entry.get()
#         if not text.strip():
#             translation_label.config(text="")
#             return
#
#         try:
#             translated = GoogleTranslator(source='ja', target='ar').translate(text)
#             translation_label.config(text=f" الترجمة: {translated}")
#         except Exception as e:
#             translation_label.config(text=f" خطأ في الترجمة: {str(e)}")
#
#     global entry, translation_label
#     root = tk.Tk()
#     root.title("Eye Controlled Japanese Keyboard")
#
#     entry = tk.Entry(root, width=30, font=("Helvetica", 20))
#     entry.pack(pady=10)
#
#     translation_label = tk.Label(root, text="", font=("Helvetica", 16), fg="blue")
#     translation_label.pack()
#
#     keys = [
#         ['あ', 'い', 'う', 'え', 'お'],
#         ['か', 'き', 'く', 'け', 'こ'],
#         ['さ', 'し', 'す', 'せ', 'そ'],
#         ['た', 'ち', 'つ', 'て', 'と'],
#         ['な', 'に', 'ぬ', 'ね', 'の'],
#         ['は', 'ひ', 'ふ', 'へ', 'ほ'],
#         ['ま', 'み', 'む', 'め', 'も'],
#         ['や', '', 'ゆ', '', 'よ'],
#         ['ら', 'り', 'る', 'れ', 'ろ'],
#         ['わ', '', 'を', '', 'ん']
#     ]
#
#     for row in keys:
#         frame = tk.Frame(root)
#         frame.pack()
#         for char in row:
#             if char == '':
#                 tk.Label(frame, text=" ", width=5).pack(side=tk.LEFT)
#             else:
#                 btn = tk.Button(frame, text=char, width=10, height=2, command=lambda c=char: on_click(c))
#                 btn.pack(side=tk.LEFT, padx=2, pady=2)
#
#     bottom = tk.Frame(root)
#     bottom.pack(pady=10)
#
#     tk.Button(bottom, text="🗑️ مسح", width=10, command=clear_text).pack(side=tk.LEFT, padx=10)
#     tk.Button(bottom, text="⌫ حذف آخر حرف", width=15, command=delete_last_char).pack(side=tk.LEFT, padx=5)
#     tk.Button(bottom, text="🔊 نطق", width=10, command=speak_text).pack(side=tk.LEFT, padx=10)
#
#     root.mainloop()
#
# # ========== ⌨️ Start keyboard in separate thread ==========
# threading.Thread(target=create_keyboard, daemon=True).start()
#
# # ========== 👁️ Eye Tracking Mouse ==========
# cam = cv2.VideoCapture(0)
# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# screen_w, screen_h = pyautogui.size()
#
# while True:
#     _, frame = cam.read()
#     frame = cv2.flip(frame, 1)
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output = face_mesh.process(rgb)
#     landmark_points = output.multi_face_landmarks
#     frame_h, frame_w, _ = frame.shape
#
#     if landmark_points:
#         landmarks = landmark_points[0].landmark
#         for id, landmark in enumerate(landmarks[474:478]):
#             x = int(landmark.x * frame_w)
#             y = int(landmark.y * frame_h)
#             cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
#
#             if id == 1:
#                 screen_x = (screen_w / frame_w) * (x - frame_w / 2) * 2 + screen_w / 2
#                 screen_y = (screen_h / frame_h) * (y - frame_h / 2) * 2 + screen_h / 2
#
#                 try:
#                     cur_x, cur_y = pyautogui.position()
#                     smooth_factor = 0.5
#                     final_x = cur_x + (screen_x - cur_x) * smooth_factor
#                     final_y = cur_y + (screen_y - cur_y) * smooth_factor
#                     pyautogui.moveTo(final_x, final_y)
#                 except:
#                     pyautogui.moveTo(screen_x, screen_y)
#
#         left_eye = [landmarks[145], landmarks[159]]
#         if (left_eye[0].y - left_eye[1].y) < 0.007:
#             pyautogui.click()
#             pyautogui.sleep(1)
#
#     cv2.imshow('🖱️ Eye Controlled Mouse', frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

#              First V                #
# import cv2
# import mediapipe as mp
# import pyautogui
# import tkinter as tk
# import threading
# import tempfile
# import os
# from gtts import gTTS
# import pygame
#
# # ========== 🎌 Japanese Virtual Keyboard ==========
# def create_keyboard():
#     def on_click(char):
#         current = entry.get()
#         entry.delete(0, tk.END)
#         entry.insert(0, current + char)
#
#     def clear_text():
#         entry.delete(0, tk.END)
#
#     def speak_text():
#         text = entry.get()
#         if not text.strip():
#             return
#
#         try:
#             # استخدم ملف مؤقت فريد عشان تتجنب مشاكل الاسم
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
#                 tmp_path = tmp_file.name
#
#             tts = gTTS(text=text, lang='ja')
#             tts.save(tmp_path)
#
#             pygame.mixer.init()
#             pygame.mixer.music.load(tmp_path)
#             pygame.mixer.music.play()
#
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
#
#             pygame.mixer.music.unload()
#             pygame.mixer.quit()
#
#             os.remove(tmp_path)
#
#         except Exception as e:
#             st = str(e)
#             print("🔴 Error during speech playback:", st)
#
#     global entry, root
#     root = tk.Tk()
#     root.title("Eye Controlled Japanese Keyboard")
#     entry = tk.Entry(root, width=50, font=("Helvetica", 20))
#     entry.pack(pady=10)
#
#     keys = [
#         ['あ', 'い', 'う', 'え', 'お'],
#         ['か', 'き', 'く', 'け', 'こ'],
#         ['さ', 'し', 'す', 'せ', 'そ'],
#         ['た', 'ち', 'つ', 'て', 'と'],
#         ['な', 'に', 'ぬ', 'ね', 'の'],
#         ['は', 'ひ', 'ふ', 'へ', 'ほ'],
#         ['ま', 'み', 'む', 'め', 'も'],
#         ['や', '', 'ゆ', '', 'よ'],
#         ['ら', 'り', 'る', 'れ', 'ろ'],
#         ['わ', '', 'を', '', 'ん']
#     ]
#
#     for row in keys:
#         frame = tk.Frame(root)
#         frame.pack()
#         for char in row:
#             if char == '':
#                 tk.Label(frame, text=" ", width=5).pack(side=tk.LEFT)
#             else:
#                 btn = tk.Button(frame, text=char, width=5, height=2, command=lambda c=char: on_click(c))
#                 btn.pack(side=tk.LEFT, padx=2, pady=2)
#
#     bottom = tk.Frame(root)
#     bottom.pack(pady=10)
#
#     tk.Button(bottom, text="🗑️ مسح", width=10, command=clear_text).pack(side=tk.LEFT, padx=10)
#     tk.Button(bottom, text="🔊 نطق", width=10, command=speak_text).pack(side=tk.LEFT, padx=10)
#
#     root.mainloop()
#
# # ========== ⌨️ Start keyboard in separate thread ==========
# threading.Thread(target=create_keyboard, daemon=True).start()
#
# # ========== 👁️ Eye Tracking Mouse ==========
# cam = cv2.VideoCapture(0)
# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# screen_w, screen_h = pyautogui.size()
#
# while True:
#     _, frame = cam.read()
#     frame = cv2.flip(frame, 1)
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output = face_mesh.process(rgb)
#     landmark_points = output.multi_face_landmarks
#     frame_h, frame_w, _ = frame.shape
#
#     if landmark_points:
#         landmarks = landmark_points[0].landmark
#         for id, landmark in enumerate(landmarks[474:478]):
#             x = int(landmark.x * frame_w)
#             y = int(landmark.y * frame_h)
#             cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
#
#             if id == 1:
#                 # خليه يتحرك أكتر بناءً على نسبة من الشاشة
#                 screen_x = (screen_w / frame_w) * (x - frame_w / 2) * 2 + screen_w / 2
#                 screen_y = (screen_h / frame_h) * (y - frame_h / 2) * 2 + screen_h / 2
#
#                 try:
#                     cur_x, cur_y = pyautogui.position()
#                     smooth_factor = 0.5  # زوّد الرقم لو عايز تحرك أسرع
#                     final_x = cur_x + (screen_x - cur_x) * smooth_factor
#                     final_y = cur_y + (screen_y - cur_y) * smooth_factor
#                     pyautogui.moveTo(final_x, final_y)
#                 except:
#                     pyautogui.moveTo(screen_x, screen_y)
#
#         # Click by blink
#         left_eye = [landmarks[145], landmarks[159]]
#         if (left_eye[0].y - left_eye[1].y) < 0.007:
#             pyautogui.click()
#             pyautogui.sleep(1)
#
#     cv2.imshow('🖱️ Eye Controlled Mouse', frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
