from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import emoji

def text_wrap(text, font, max_width):
	lines = []
	# If the width of the text is smaller than image width
	# we don't need to split it, just add it to the lines array
	# and return
	if font.getsize(text)[0] <= max_width:
		lines.append(text) 
	else:
	# split the line by spaces to get words
		words = text.split(' ')  
		i = 0
		#print('i : ',i)
		#print(len(words))
	# append every word to a line while its width is shorter than image width
		while i < len(words):
			line = ''         
			while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
				line = line + words[i] + " "
				i += 1
			if not line:
				line = words[i]
				i += 1
	# when the line gets longer than the max width do not append the word, 
	# add the line to the lines array
			lines.append(line)    
	return lines


def draw_text(text,x=100,y=80):    
	# open the background file
	img = Image.open('bg.png')
	# size() returns a tuple of (width, height) 
	image_size = img.size 
	draw = ImageDraw.Draw(img)
	print(text)
	# create the ImageFont instance
	font_file_path = 'Roboto-Bold.ttf'
	font = ImageFont.truetype(font_file_path, size=50, encoding="unic")
	color = 'rgb(255,0,0)'
	print("wrapping")
	# get shorter lines
	print(image_size[0])
	lines = text_wrap(text, font, image_size[0]-400)
	print( lines) # ['This could be a single line text ', 'but its too long to fit in one. ']
	line_height = font.getsize('hg')[1]
	#x = 100
	#y = 80
	for line in lines:
		draw.text((x,y),line,fill=color,font=font)
		y = y +line_height
	print("saving ..")
	img.save('poster.png',optimize=True)
def setColor(clr):
	color = clr
	return color

def setFont(size):
	font_file_path = 'Roboto-Bold.ttf'
	font =ImageFont.truetype(font_file_path,size=size,encoding="unic")
	return font

def simbolfont(size):
	font_file_path = 'Symbola.ttf'
	font =ImageFont.truetype(font_file_path,size=size,encoding="unic")
	return font


def setContent(width, draw, pos,text,color,font):
	lines = text_wrap(text,font,width)
	line_h = font.getsize('hg')[1]
	x,y = pos
	for line in lines:
		draw.text((x,y),line,fill=color,font=font)
		y = y + line_h
 
def create_banner(content) :
	agenda = content['agenda']
	ustadz = content['pemateri']
	materi =content['materi']
	cal = content['tanggal']
	wkt = content['waktu']
	tmpt = content['tempat']
	host = content['host']

	print(agenda)
	print(ustadz)
	'''
	materi = content[2]
	tempat = content[3]
	hari = content[4]
	tanggal = content[5]
	waktu = content[6]
	host = content[7]
	'''
	# open the background file
	img = Image.open('bg_3.png')
	# size() returns a tuple of (width, height) 
	image_size = img.size 
	draw = ImageDraw.Draw(img)
	#print(text)
	# create the ImageFont instance
	#font_file_path = 'Roboto-Bold.ttf'
	#font = ImageFont.truetype(font_file_path, size=50, encoding="unic")
	agFont = setFont(72)
	red = setColor('rgb(255,255,255)')

	#agenda
	agLines = text_wrap(agenda,agFont,image_size[0]-200)
	agLine_h = agFont.getsize('hg')[1]
	agX = 100
	agY = 80
	agW = image_size[0]-agX-100
	for ag in agLines:
		draw.text((agX,agY),ag,fill=red,font=agFont)
		agY = agY + agLine_h
	setContent(agW,draw,(100,320),materi,red,setFont(48))
	
	#simbol ustadz
	draw.text((530,580),emoji.emojize(":man_with_turban:",use_aliases=True),fill=red,font=simbolfont(48))
	#ustadz
	ustFont = setFont(36)
	ustLines = text_wrap(ustadz,ustFont,image_size[0]-540)
	ustLine_h = ustFont.getsize('hg')[1]
	print(ustLine_h)
	ustX = 580
	ustY = 580
	ustW = image_size[0]-ustX-100
	for ust in ustLines:
		draw.text((ustX,ustY),ust,fill=red,font=ustFont)
		ustY = ustY+ustLine_h
	#waktu
	draw.text((530,650),emoji.emojize(":date:",use_aliases=True),fill=red,font=simbolfont(48))
	setContent(ustW,draw,(580,650),cal,red,setFont(36))
	draw.text((530,730),emoji.emojize(":alarm_clock:",use_aliases=True),fill=red,font=simbolfont(48))
	setContent(ustW,draw,(580,730),wkt,red,setFont(36))
	#tempat
	draw.text((530,800),emoji.emojize(":office:",use_aliases=True),fill=red,font=simbolfont(48))
	setContent(ustW,draw,(580,800),tmpt,red,setFont(36))
	#host
	draw.text((530,1030),emoji.emojize("::",use_aliases=True),fill=red,font=simbolfont(36))
	setContent(ustW,draw,(580,1030),host,red,setFont(24))
	#cp
	print('saving...')
	img.save('my_banner.png',optimize=True)

if __name__ == "__main__":
	print(emoji.emojize("test ... :man_with_turban: :mosque: ",use_aliases=True))
	content = {}
	content['agenda'] ="Pengajian Kamis Malam AMM Sleman"
	content['materi'] ='\"Kaum Perempuan dan Politik\"'
	content['pemateri'] = "Ustadz Sri Purnomo"
	content['waktu'] = "20.00 WIB - 21.30 WIB"
	content['tempat'] = "Gedung Dakwah Muhammadiyah Sleman Jl Pendowoharjo"
	content['host'] = "AMM Sleman"
	content['tanggal'] ="Kamis, 21 Februari 2019"
	#content.append("Pengajian Kamis Malam : AMM Sleman")
	#content.append("Ustadz Bersurban Putih")
	create_banner(content)
	#draw_text("Percobaaan nulis yang panjang biar tau seberapa pemengaggalan katanyanya")

