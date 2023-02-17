from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import easyocr
import os


class MainApp(App):

    def build(self):
        self.camera = cv2.VideoCapture(0)
        Clock.schedule_interval(self.camera_update, 1/30)

        bl_1 = BoxLayout(orientation="vertical")
        self.img_1 = Image()
        self.ti_1 = TextInput(size_hint=[1, 0.2])
        btn_1 = Button(size_hint=[1, 0.1], on_press=self.btn_1_press)

        bl_1.add_widget(self.img_1)
        bl_1.add_widget(self.ti_1)
        bl_1.add_widget(btn_1)
        return bl_1

    def camera_update(self, *args):
        _, self.frame = self.camera.read()
        buffer = cv2.flip(self.frame, 0).tostring()
        self.texture = Texture.create(
            size=(self.frame.shape[1], self.frame.shape[0]),
            colorfmt="bgr"
        )
        self.texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
        self.img_1.texture = self.texture

    def btn_1_press(self, *args):
        cv2.imwrite("/tmp.jpg", self.frame)
        img_to_txt_reader = easyocr.Reader(lang_list=["ru"])
        text = " ".join(img_to_txt_reader.readtext("/tmp.jpg", detail=0, paragraph=True))
        self.ti_1.text = text
        os.remove("/tmp.jpg")


if __name__ == "__main__":
    MainApp().run()
