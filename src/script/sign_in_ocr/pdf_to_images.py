import os

import pdf2image
from PIL import Image
import time

# DECLARE CONSTANTS
DPI = 200
OUTPUT_FOLDER = "tmp/"
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = "jpg"
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False


# Taken from https://iq.opengenus.org/pdf_to_image_in_python/
class ImageConverter:
    @staticmethod
    def pdftopil(pdf_path):
        # This method reads a pdf and converts it into a sequence of images
        # PDF_PATH sets the path to the PDF file
        # dpi parameter assists in adjusting the resolution of the image
        # output_folder parameter sets the path to the folder to which the PIL images can be stored (optional)
        # first_page parameter allows you to set a first page to be processed by pdftoppm
        # last_page parameter allows you to set a last page to be processed by pdftoppm
        # fmt parameter allows to set the format of pdftoppm conversion (PpmImageFile, TIFF)
        # thread_count parameter allows you to set how many thread will be used for conversion.
        # userpw parameter allows you to set a password to unlock the converted PDF
        # use_cropbox parameter allows you to use the crop box instead of the media box when converting
        # strict parameter allows you to catch pdftoppm syntax error with a custom type PDFSyntaxError
        os.makedirs(OUTPUT_FOLDER)
        pil_images = pdf2image.convert_from_path(
            pdf_path,
            dpi=DPI,
            output_folder=OUTPUT_FOLDER,
            first_page=FIRST_PAGE,
            last_page=LAST_PAGE,
            fmt=FORMAT,
            thread_count=THREAD_COUNT,
            userpw=USERPWD,
            use_cropbox=USE_CROPBOX,
            strict=STRICT,
        )
        return pil_images
