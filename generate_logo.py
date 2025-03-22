from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with a white background
    size = (200, 200)
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw a blue circle
    circle_color = (0, 123, 255, 25)  # Light blue with transparency
    draw.ellipse([(10, 10), (190, 190)], fill=circle_color)

    # Draw a book shape
    book_color = (0, 123, 255)  # Solid blue
    draw.rectangle([(60, 40), (140, 160)], fill=book_color)
    draw.rectangle([(70, 50), (130, 150)], fill='white')

    # Draw the letter E
    line_color = (0, 123, 255)  # Blue
    line_width = 8
    # Top line
    draw.line([(85, 70), (115, 70)], fill=line_color, width=line_width)
    # Middle line
    draw.line([(85, 100), (115, 100)], fill=line_color, width=line_width)
    # Bottom line
    draw.line([(85, 130), (115, 130)], fill=line_color, width=line_width)

    # Draw decorative elements
    draw.ellipse([(95, 95), (105, 105)], fill=line_color)  # Center dot
    draw.ellipse([(98, 98), (102, 102)], fill='white')  # White dot in center

    # Create the static/img directory if it doesn't exist
    os.makedirs('static/img', exist_ok=True)

    # Save the logo
    image.save('static/img/logo.png', 'PNG')

if __name__ == '__main__':
    create_logo() 