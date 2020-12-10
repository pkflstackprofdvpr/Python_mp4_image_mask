from PIL import Image


THRESHOLD = 37

def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])


def is_similar_luminance(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) < threshold

def is_similar(pixel_a, pixel_b, threshold):
    dist = pow((pixel_a[0]-pixel_b[0])**2 + (pixel_a[1]-pixel_b[1])**2 + (pixel_a[2]-pixel_b[2])**2, 0.5)
    return dist < threshold



file_path = "src_imgs\\1.jpg"
im = Image.open(file_path) # Can be many different formats.

width, height = im.size
pixels = im.load();
fill_color = (1, 178, 64)
bg_colors = [[1, 178, 64], [76, 72, 57], [32, 27, 18]]
# except_colors = [[255,255,255],[28, 24, 25]]
except_colors = [[255,255,255]]

similar_arr_len = 10

for y in range(height):
    if y < 5 or y > 600:
        continue
    is_similar_arr = []
    face_found_status = 0
    old_color_arr = []
    for x in range(width):
        old_color_arr.append(pixels[x, y])
        if len(old_color_arr) > similar_arr_len:
            old_color_arr.pop(0)

        if face_found_status == 2:
            #face ended
            pixels[x, y] = fill_color
            continue
        is_except_val = False
        for i in range(len(except_colors)):
            if is_similar(pixels[x, y], except_colors[i], THRESHOLD):
                is_except_val = True
        if is_except_val:
            #skip those colors
            continue

        is_similar_val = False
        for i in range(len(bg_colors)):
            if is_similar(pixels[x, y], bg_colors[i], THRESHOLD):
                is_similar_val = True

        is_similar_arr.append(is_similar_val)
        if len(is_similar_arr) > similar_arr_len:
            is_similar_arr.pop(0)

        org_color = pixels[x, y]
        pixels[x, y] = fill_color


        if face_found_status == 0:
            if is_similar_arr.count(False) > 8:
                # found the face
                face_found_status = 1

                for k in range(similar_arr_len):
                    pixels[x-k, y] = old_color_arr[similar_arr_len-k-1]
            else:
                pixels[x, y] = fill_color
        elif face_found_status == 1:
            if is_similar_arr.count(True) > 8:
                # face ended
                face_found_status = 2

                for k in range(similar_arr_len):
                    pixels[x-k, y] = fill_color

            else:
                pixels[x, y] = org_color
        else:
            # face ended
            pixels[x, y] = fill_color

im.save('dest_imgs\\output.jpg')  # Save the modified pixels as .png
