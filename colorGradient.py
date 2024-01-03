#code to generate color gradients from any given color
from math import trunc

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)

CYAN = (0, 255, 255)
SCREAMIN_GREEN = (48, 255, 96)
YELLOW_ORANGE = (255, 153, 65)

HOT_PINK = (255, 105, 180)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ROYAL_BLUE = (65, 105, 225)

GRASS_GREEN = (0, 154, 23)

CYBERPUNK_GRADIENT = (CYAN, SCREAMIN_GREEN, YELLOW_ORANGE)

def mixColors(intensity1, intensity2, color1, color2, brightness):

    r = trunc((color1[0]*intensity1 + color2[0]*intensity2)*brightness)
    g = trunc((color1[1]*intensity1 + color2[1]*intensity2)*brightness)
    b = trunc((color1[2]*intensity1 + color2[2]*intensity2)*brightness)

    return (r, g, b)

def generateGradient(RGB, targetColors, gradientLength):

    gradient = []
    brightness = (RGB[0]*.2126 + RGB[1]*.7152 + RGB[2]*.0722) / 255
    transitionPeriod = trunc(gradientLength / len(targetColors)) - 1

    for colorIndex in range(0, len(targetColors) - 1):
        gradient.append(mixColors(0.5, 0.5, targetColors[colorIndex], targetColors[colorIndex], brightness))
        for afterImage in range(transitionPeriod - 1, -1, -1):
            color1Str = afterImage / transitionPeriod
            color2Str = 1 - color1Str
            color1 = targetColors[colorIndex]
            color2 = targetColors[colorIndex + 1]
            mixedColor = mixColors(color1Str, color2Str, color1, color2, brightness)
            gradient.append(mixedColor)
    
    remainingAfterImages = gradientLength - len(gradient) - 1
    gradient.append(mixColors(0.5, 0.5, targetColors[-1], targetColors[-1], brightness))
    for afterImage in range(remainingAfterImages - 1, -1, -1):
        color1Str = afterImage / remainingAfterImages
        color2Str = 1 - color1Str
        color1 = targetColors[-1]
        color2 = targetColors[0]
        mixedColor = mixColors(color1Str, color2Str, color1, color2, brightness)
        gradient.append(mixedColor)

    return gradient

print(len(generateGradient(WHITE, CYBERPUNK_GRADIENT, 120)))
