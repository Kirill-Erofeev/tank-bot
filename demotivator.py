# Телефон: 1080 x 1920
# Планшет 7 дюймов: 1200 x 1920
# Планшет 10 дюймов: 1800 x 2560

from PIL import (
    Image,
    ImageOps,
    ImageDraw,
    ImageFont,
)


class Demotivator:
    # DATA_FOLDER_FILE_PATH = './data/'
    KOEF_1 = 0.07
    KOEF_2 = 0.2
    FONT_PATH = 'gtwalsheimpro_condensedmediumoblique.otf'

    @classmethod
    def create_demotivator(cls, image_path, title, subtitle):
        img = Image.open(image_path)
        img = ImageOps.expand(img, border=20, fill='black')
        img = ImageOps.expand(img, border=5, fill='white')
        width, height = img.size

        right = int(width * cls.KOEF_1)
        left = int(width * cls.KOEF_1)
        top = int(width * cls.KOEF_1)
        bottom = int(width * cls.KOEF_2)
        new_width = width + right + left
        new_height = height + top + bottom

        image = Image.new(img.mode, (new_width, new_height), 'black')
        image.paste(img, (left, top))
        # new_image = ImageOps.expand(image, border=300, fill='black')

        width, height = image.size
        top = int(width * cls.KOEF_1)
        bottom = int(width * cls.KOEF_2)
        
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            cls.FONT_PATH,
            int(width / 12),
            # encoding='WINDOWS-1251'
        )
        text_length = draw.textlength(title, font=font)
        draw.text(
            ((width - text_length) / 2, height - bottom + 50),
            title,
            fill='white',
            font=font
        )

        font = ImageFont.truetype(
            cls.FONT_PATH,
            int(width / 20),
            # encoding='UTF-8'
        )
        text_length = draw.textlength(subtitle, font=font)
        draw.text(
            ((width - text_length) / 2, height - top),
            subtitle,
            fill='white',
            font=font
        )
        return image

    # @property
    # def _constructor(self):
    #     return Demotivator

    def __init__(self, font_path, koef_1=0.07, koef_2=0.2):
        self.font_path = font_path
        self.koef_1 = koef_1
        self.koef_2 = koef_2
        self.demotivator = None

    # def __init__(self, font_path, koef_1=0.07, koef_2=0.2):
    #     self.font_path = font_path
    #     self.koef_1 = koef_1
    #     self.koef_2 = koef_2
    #     self.demotivator = self.create_demotivator(f'Images/dem_image.png', 'MAKSIM', 'MISHA IS устал')
        
    
    def create_demotivator(self, image_path, title, subtitle):
        img = Image.open(image_path)
        img = ImageOps.expand(img, border=20, fill='black')
        img = ImageOps.expand(img, border=5, fill='white')
        width, height = img.size

        right = int(width * self.koef_1)
        left = int(width * self.koef_1)
        top = int(width * self.koef_1)
        bottom = int(width * self.koef_2)
        new_width = width + right + left
        new_height = height + top + bottom

        image = Image.new(img.mode, (new_width, new_height), 'black')
        image.paste(img, (left, top))
        # new_image = ImageOps.expand(image, border=300, fill='black')

        width, height = image.size
        top = int(width * self.koef_1)
        bottom = int(width * self.koef_2)
        
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            self.font_path,
            int(width / 12),
            # encoding='WINDOWS-1251'
        )
        text_length = draw.textlength(title, font=font)
        draw.text(
            ((width - text_length) / 2, height - bottom + 50),
            title,
            fill='white',
            font=font
        )

        font = ImageFont.truetype(
            self.font_path,
            int(width / 20),
            # encoding='UTF-8'
        )
        text_length = draw.textlength(subtitle, font=font)
        draw.text(
            ((width - text_length) / 2, height - top),
            subtitle,
            fill='white',
            font=font
        )
        self.demotivator = image
    
        
    def show(self):
        self.demotivator.show()
        
    
    def save(self, image_path):
        self.demotivator.save(image_path)


if __name__ == '__main__':
    DATA_FOLDER_FILE_PATH = './data/'
    dem = Demotivator(DATA_FOLDER_FILE_PATH + 'gtwalsheimpro_condensedmediumoblique.otf')
    dem.create_demotivator(
        f'Images/f44DycQSvhI.jpg',
        '123456789012345',
        'MISHA IS устал'
    )
    dem.show()
    # dem.save(f'Images/demotivator.jpg')