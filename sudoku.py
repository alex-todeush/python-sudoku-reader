import cv2
import pytesseract
import numpy
from PIL import Image
from pathlib import Path

path = str(Path(__file__).parent.absolute())

# Include tesseract executable in your path
pytesseract.pytesseract.tesseract_cmd = r"D:\\Python\\Tesseract\\tesseract.exe"

#Import source image
input_img = cv2.imread(path + "\input_image.jpg", 0)
#Blur and then threshold the image for easier character recognition
input_img = cv2.blur(input_img, (10,10)) 
ret, threshed_img = cv2.threshold(input_img, 90, 255, cv2.THRESH_BINARY)
cv2.imwrite(path + "\processed_image.jpg", threshed_img)

img_width = input_img.shape[1]
img_height = input_img.shape[0]

#Read the input image and populate a 9x9 grid with the values in the cells
def readGridPhoto(grid_photo):
    pil_grid = Image.fromarray(grid_photo)
    box_width = img_width / 9
    box_height = img_height / 9
    Matrix = numpy.zeros((9, 9), dtype=int)
    edge_buffer = box_width / 10
    for y in range(0,9):
        for x in range(0,9):
            #Cut the image up into cells
            crop_square = (x * box_width + edge_buffer, y * box_height + edge_buffer, x * box_width + box_width - edge_buffer, y * box_height + box_height - edge_buffer)
            cropped_cell = pil_grid.crop(crop_square)
            cell_number = str(y * 9 + x)
            cropped_cell.save(path + "\Grid\\" + cell_number + ".png")
            #Read the digit in the cell
            digit_in_cell = pytesseract.image_to_string(cropped_cell, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
            #If a digit is found add it to the matrix
            try:
                print(digit_in_cell)
                Matrix[y][x] = int(digit_in_cell[:1])
            except:
                pass
    return Matrix

out_string = ""
sudoku = readGridPhoto(threshed_img)
print(sudoku)

#Make 81-digit sudoku representation
for y in range(0,9):
        for x in range(0,9):
            out_string =  out_string + str(sudoku[y][x])
print(out_string) 