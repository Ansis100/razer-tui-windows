from effects import hex_to_bgr


def calculate_gradient_step(color_tuple1, color_tuple2, t):
    r = str(hex(int(
        color_tuple1[0]
        + (color_tuple2[0] - color_tuple1[0])
        * t
    )))[2:]

    g = str(hex(int(
        (color_tuple2[1] - color_tuple1[1])
        * t
    )))[2:]

    b = str(hex(int(
        color_tuple1[2]
        + (color_tuple2[2] - color_tuple1[2])
        * t
    )))[2:]

    if (len(r) == 1):
        r = '0' + r
    if (len(g) == 1):
        g = '0' + g
    if (len(b) == 1):
        b = '0' + b

    return '#' + r + g + b


"""Send a gradient from color1 to color2 with a length of time.

Arguments:
    color1 {str} -- Color in the format "#FFFFFF" (hex)
    color2 {str} -- Color in the format "#FFFFFF" (hex)
    time {float} -- Gradient length in seconds
"""
color1 = "#000000"
color2 = "#ffffff"
color_tuple1 = (
    int(color1[1:3], 16),
    int(color1[3:5], 16),
    int(color1[5:], 16)
)
color_tuple2 = (
    int(color2[1:3], 16),
    int(color2[3:5], 16),
    int(color2[5:], 16)
)

# Create an array of gradient hex codes
gradient = []
steps = 100
for i in range(steps):
    # Gradient code calculation
    gradient.append(
        calculate_gradient_step(
            color_tuple1,
            color_tuple2,
            i/steps
        )
    )
gradient.append(color2)

for i in range(len(gradient)):
    print(gradient[i])
    print(hex_to_bgr(gradient[i]))
