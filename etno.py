from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="luisaEncoded.png"):
    encoded_image = Image.open(file_location) #abrimos la imagen
    red_channel = encoded_image.split()[0] #codificamos solo para el color rojo

    x_size = encoded_image.size[0] #obtenemos el ancho de la imagen
    y_size = encoded_image.size[1] #obtenemos el lago de la imagen

    decoded_image = Image.new("RGB", encoded_image.size)#abrimos una nueva imagen
    pixels = decoded_image.load()#cargamos los pixeles

    for i in range(x_size):
        for j in range(y_size):#recorremos la imagen
            if bin(red_channel.getpixel((i, j)))[-1] == '0':#Obtenemos el bit menos significativo y miramos si es 0
                pixels[i, j] = (255, 255, 255)#si es de color negro pintamos todo el pixel de negro
            else:
                pixels[i, j] = (0,0,0)#si es de otro color lo pintamos blanco
    decoded_image.save("decoded_image.png")

def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)#abrimos nueva imagen
    font = ImageFont.load_default().font#cargamos una nueva font
    drawer = ImageDraw.Draw(image_text)#dibujaremos en la nueva imagen
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="luisa.jpg"):
    template_image = Image.open(template_image)#abrimos la imagen
    red_template = template_image.split()[0]#cargamos los pixeles rojos
    green_template = template_image.split()[1]#cargamos los pixeles verdes
    blue_template = template_image.split()[2]#cargamos los pixeles azules

    x_size = template_image.size[0]#obtenemos tamano
    y_size = template_image.size[1]

    image_text = write_text(text_to_encode, template_image.size)#escribimos el mensaje
    bw_encode = image_text.convert('1')


    encoded_image = Image.new("RGB", (x_size, y_size))#abrimos una nueva imagen
    pixels = encoded_image.load()#cargamos pixeles
    for i in range(x_size):
        for j in range(y_size):#recorremos imagen
            red_template_pix = bin(red_template.getpixel((i,j)))
            tencode_pix = bin(bw_encode.getpixel((i,j)))
            if tencode_pix[-1] == '1':#cambio del bit menos significativo
                red_template_pix = red_template_pix[:-1] + '1'
            else:
                red_template_pix = red_template_pix[:-1] + '0'
            pixels[i, j] = (int(red_template_pix, 2), green_template.getpixel((i,j)), blue_template.getpixel((i,j)))

    encoded_image.save("luisaEncoded.png")

if __name__ == '__main__':
    encode_image("Hola soy Luisa Arboleda")
    decode_image()
    