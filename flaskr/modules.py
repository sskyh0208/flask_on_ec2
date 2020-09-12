import io
from PIL import Image

# 160*160
def image_resize(img):
    img = Image.open(io.BytesIO(img))
    img.thumbnail((160, 160), Image.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='JPEG')
    return output.getvalue()

def make_id_to_obj_dict(objects):
    new_dict = {}
    for obj in objects:
        new_dict[obj.id] = obj
    return new_dict