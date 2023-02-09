from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import easyocr


Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: text_input.text = root.capture()
    TextInput:
        id: text_input
        text: ""
''')


class CameraClick(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        # timestr = time.strftime("%Y%m%d_%H%M%S")
        # camera.export_to_png("IMG_{}.png".format(timestr))
        # print("Captured")
        frame = camera.export_as_image()
        frame.save("tmp.jpg")
        reader = easyocr.Reader(["ru"])
        text = " ".join(reader.readtext("tmp.jpg", detail=0, paragraph=True))
        return text


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()
