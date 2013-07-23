# -*- coding: utf-8 -*-
"""
    SmallMan
    ~~~~~~
    It can let you type words and output an image.

"""


from flask import Flask, jsonify, url_for
from flask import request
from flask import render_template

# image
#import Image, ImageFont, ImageDraw
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# system
import thread


# create our little application :)
app = Flask(__name__)


#首頁
@app.route('/')
def index():    
    return render_template('index.html')

def transformImg(srcImg):
    '''
    變形圖片, 使其往一邊傾斜
    '''
    width, height = srcImg.size
    m = 0.5
    xshift = abs(m) * width
    new_width = width + int(round(xshift))
    img = srcImg.transform((new_width, height), Image.AFFINE,
            (1, m, xshift if m < 0 else 0, 0, 1, 0), Image.BICUBIC)

    return img

@app.route('/getNewImg',  methods=['POST'])
def getNewImg():
    print "0000000000000"
    if request.method == 'POST':
        print "11111111111111111"
        #print json.loads(request.data)
        #return jsonify(rst=request.json)
        #font = ImageFont.truetype("/usr/share/fonts/truetype/takao/TakaoPGothic.ttf", 24, encoding='unicode')
        words = request.json['words']
        wordSize = 30
        wordlist_ = words.split('\n')
        imgH = len(wordlist_) * wordSize + 130
        imgW = 0
        for line in wordlist_:
            imgW = max(imgW, len(line))
        imgW = imgW * wordSize + 350

        #create background image
        print "22222222222222"
        bgImg = Image.new('RGBA', (imgW, imgH), (255, 255, 255, 255))
        # load cat
        catImg = Image.open("static/cat.png")
        print "33333333333333"

        font_path = "."+url_for('static', filename="LIHEI_PROPC_0.TTF")
        font = ImageFont.truetype(font_path, wordSize, encoding='unicode')
        print "44444444444444"
        #size = font.getsize(request.json['words'])
        lineIdx = 0
        wordIdx = 0
        wordGap = 70
        catGap = 70
        for line in wordlist_:
            wordIdx = 0
            for word in line:
                #print word
                txtImg = Image.new('RGBA', (wordSize+10, wordSize), (0, 0, 0, 0))
                draw = ImageDraw.Draw(txtImg)
                draw.text((0, 0), word, font=font, fill='#000000')
                #txtImg = transformImg(txtImg)
                txtImg = txtImg.rotate(-35, resample=Image.BILINEAR, expand=1)
                #bgImg.paste(txtImg, (wordGap*wordIdx+150, (wordSize+10)*lineIdx), txtImg)
                bgImg.paste(catImg, (catGap*wordIdx+120, (wordSize+10)*lineIdx), catImg)
                bgImg.paste(txtImg, (wordGap*wordIdx+158, (wordSize+10)*lineIdx+8), txtImg)
                wordIdx = wordIdx + 1
            lineIdx = lineIdx + 1

        # sign cello's studio
        print "5555555555555"
        font1 = ImageFont.truetype(font_path, 12, encoding='unicode')
        txtImg = Image.new('RGBA', (200, 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(txtImg)
        draw.text((10, 0), "Powered by Cello's studio", font=font1, fill='#000000')
        bgImg.paste(txtImg, (0, imgH-20), txtImg)

        #rows_ = len(wordlist_)
        #height_ = 24 * rows_
        #image = Image.new('RGBA', (300, height_), (0, 0, 0, 0))
        #image = Image.new('RGBA', (size[0]+10, size[1]+height_), (255, 255, 255, 255))
        #image = image.rotate(20.5, expand=1)
        #draw = ImageDraw.Draw(image)
        # use a truetype font
        # count_ = 0
        # for line in wordlist_:
        #     draw.text((0, 24*count_), line, font=font, fill='#000000')
        #     count_ = count_ + 1
        #save the image
        #image = transformImg(image)
        #imgName_ = str(thread.get_ident()) + ".png"
        #bgImg.save("static/data/"+imgName_, 'PNG')
        print "======"
        imgName_ = "temp.png"
        bgImg.save("static/data/"+imgName_, 'PNG')
        #return jsonify(rst=imgName_)
        print jsonify(rst=url_for('static', filename="data/"+imgName_))
        return jsonify(rst=url_for('static', filename="data/"+imgName_))
    return "NG"
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    #app.run()
