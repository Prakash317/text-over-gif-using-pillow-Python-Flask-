"""Write on GIF using PILLOW"""
from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import os

app = Flask(__name__)

file = Image.open('./oreo.gif')

@app.route('/all_new_oreo_red_velvet')
def generate_gif():
    print(request.query_string)
    name = request.args.get('name')
    phone_number = request.args.get('phone_number')
    # is_download = request.args.get('is_download')
    text = "AVAILABLE NOW"
    frames = []

    file_path = f"./{name}_{phone_number}.gif"
    check_path = os.path.isfile(f'{file_path}')

    if check_path:
        print("File Exist")
        return f'{file_path}'
        # return send_file(file_path, as_attachment=True if is_download else False)
    else:
        for frame in ImageSequence.Iterator(file):
            draw = ImageDraw.Draw(frame)
            font = ImageFont.truetype("./oreo_font.otf", 29)

            W, H = (540,960)
            
            availableW, h = draw.textsize(f"{text}", font=font)
            x = (W-availableW) / 2
            draw.text((x,680), f"{text}", font=font)

            nameW, h = draw.textsize(f"{name}", font=font)
            x = (W-nameW) / 2
            draw.text((x, 710), f"{name}", font=font)

            numberW, h = draw.textsize(f"{phone_number}", font=font)
            x = (W-numberW) / 2
            draw.text((x, 740), f"{phone_number}", font=font)

            del draw
            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)
        
            frames.append(frame)
        frames[0].save(f'{name}_{phone_number}.gif', save_all=True, append_images=frames[1:])
    print("Generated")
    return f'{file_path}'
    # return send_file(file_path, as_attachment=True if is_download else False)

if __name__ == '__main__':
    app.run(debug=True, port=1000)



