from PIL import Image, ImageDraw, ImageFont
image = Image.open('./1.jpg')
text = '我是大水印'
# 指定字体和大小
font = ImageFont.truetype('./SimHei.ttf', 300)
layer = image.convert('RGBA')
# 生成同等大小图片
text_overlay = Image.new('RGBA', layer.size, (255, 255, 255, 0))
# 画图
image_draw = ImageDraw.Draw(text_overlay)
# 获取文本大小
text_size_x, text_size_y = image_draw.textsize(text, font=font)
# 设置文本文字位置
text_xy = (layer.size[0]//2 - text_size_x//2, layer.size[1] - text_size_y)
# 设置文本颜色和透明度和位置
image_draw.text(text_xy, text, font=font, fill=(255, 255, 255, 50))
# 将新生成的图片覆盖到需要加水印的图片上
after = Image.alpha_composite(layer, text_overlay)
after.save('img_after.png')

# ++++++++++++++++++
# img = Image.open('./1.jpg')   #需要加水印的图片
# logo = Image.open('./logo.jpg')   #水印图片
# layer = image.new('RGBA', image.size, (255, 255, 255, 0))   #图层
# layer.paste(logo, (img.size[0] - logo.size[0], img.size[1] - logo.size[1]))
# img_after = Image.composite(layer, img, layer)
# img_after.show()
# img_after.save('addLogo_after.png')


