import PIL.Image
import PIL.ImageDraw

def make_placeholder(path, size=(512, 512), color=(0, 123, 255)):
    img = PIL.Image.new('RGB', size, color=color)
    draw = PIL.ImageDraw.Draw(img)
    # Simple cross for medical
    draw.rectangle([200, 100, 312, 412], fill="white")
    draw.rectangle([100, 200, 412, 312], fill="white")
    img.save(path)

make_placeholder('frontend/assets/icon.png')
make_placeholder('frontend/assets/splash-icon.png', size=(1024, 1024))
make_placeholder('frontend/assets/favicon.png', size=(48, 48))
make_placeholder('frontend/assets/adaptive-icon.png', size=(1024, 1024))
