from PIL import Image, ImageDraw, ImageFont

image = Image.open('bg.png')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('Roboto-Bold.ttf',size=72)

(x,y) = (100,100)
message = "Ngaji Tarjih"
color = 'rgb(0,0,0)'
draw.text((x,y),message,fill=color,font=font)
(x,y) =(100,250)
ustad ="Ustadz H. Mulyono"
color = 'rgb(255,0,0)'
draw.text((x,y),ustad,fill=color,font=font)
image.save('contoh_poster-3.png')
