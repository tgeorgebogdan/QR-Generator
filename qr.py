import os
import csv
import svgwrite
import qrcode
from io import BytesIO
import base64
import logging
from datetime import datetime

# Set up logging for verbose output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

USED_IDS_FILE = "used_ids.csv"
OUTPUT_DIR = "output"

def ensure_output_directory():
    """Ensure the output directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logging.info(f"Created output directory: {OUTPUT_DIR}")

def load_used_ids():
    """Load used IDs from a CSV file."""
    try:
        with open(USED_IDS_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            return set(row[0] for row in reader)
    except FileNotFoundError:
        return set()

def save_ids_to_csv(ids):
    """Save IDs to a CSV file with timestamp."""
    with open(USED_IDS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if f.tell() == 0:
            writer.writerow(["ID", "Generated On"])
        # Write IDs with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for id_ in ids:
            writer.writerow([id_, timestamp])

def generate_qr_code(data, size=46):
    """Generate a QR code for given data."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    # Save QR code as base64-encoded PNG
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def generate_custom_code(area, producer_code, year, model_code, serial_number):
    """
    Generate a custom code based on the specified parameters.

    Parameters:
        area (int): Area of activity code (e.g., 1 for Energy, 2 for Gas).
        producer_code (str): Code representing the producer.
        year (int): Year of production.
        model_code (str): Model identifier (e.g., '00' for AMR2407).
        serial_number (int): Sequential serial number.

    Returns:
        str: Encoded identifier.
    """
    # Format components into the custom code
    formatted_year = str(year)[-2:]  # Use last two digits of the year
    formatted_serial = str(serial_number).zfill(7)  # Zero-padded serial number

    # Construct the custom code
    custom_code = f"{area}{producer_code}{formatted_year}{model_code}{formatted_serial}"
    return custom_code

def generate_ids(start: int, end: int, used_ids: set, config):
    """Generate a list of unique IDs from start to end."""
    logging.info(f"Generating IDs from {start} to {end}")
    all_ids = [
        generate_custom_code(
            config['area'],
            config['producer_code'],
            config['year'],
            config['model_code'],
            serial
        ) for serial in range(start, end + 1)
    ]
    unique_ids = [id_ for id_ in all_ids if id_ not in used_ids]
    logging.info(f"{len(unique_ids)} unique IDs generated.")
    return unique_ids

def split_serial(serial):
    """Split the serial into two lines for display, each 7 characters long."""
    return serial[:7], serial[7:14]

def generate_svg(output_file, rectangles, ids):
    """Generate an SVG with the exact number and size of rectangles from the template."""
    logging.info(f"Starting SVG generation: {output_file}")
    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(595.3, 841.9))

    cls_1_style = {'fill': 'none', 'stroke': 'black', 'stroke-width': 0.5}
    text_style = {'font_size': '10px', 'font_weight': 'bold', 'font_family': 'Arial Narrow', 'fill': 'black', 'text_anchor': 'start'}

    for idx, rect in enumerate(rectangles):
        if idx * 4 >= len(ids):
            logging.warning(f"Not enough IDs for all rectangles. Stopping at rectangle {idx}.")
            break

        x = float(rect['x'])
        y = float(rect['y'])
        width = float(rect['width'])
        height = float(rect['height'])

        dwg.add(dwg.rect(insert=(x, y), size=(width, height), rx=7, ry=7, **cls_1_style))
        
        for part in range(4):
            current_index = idx * 4 + part
            if current_index >= len(ids):
                logging.warning(f"No more IDs available for part {part} in rectangle {idx}.")
                break

            part_width = width / 2
            part_height = height / 2
            part_x = x + (part % 2) * part_width
            part_y = y + (part // 2) * part_height
            part_id = ids[current_index]

            qr_x = part_x + 2
            qr_y = part_y - 2
            qr_size = 46  # Set QR code size to 38x38
            qr_data = generate_qr_code(part_id)
            dwg.add(dwg.image(href=f"data:image/png;base64,{qr_data}", insert=(qr_x, qr_y), size=(qr_size, qr_size)))

            text_x = qr_x + qr_size
            text_y = qr_y + qr_size - 24
            first_line, second_line = split_serial(part_id)
            dwg.add(dwg.text(first_line, insert=(text_x, text_y), **text_style))
            dwg.add(dwg.text(second_line, insert=(text_x, text_y + 10), **text_style))

    dwg.save()
    logging.info(f"SVG generation completed: {output_file}")

def main():
    # Ensure output directory exists
    ensure_output_directory()

    # Rectangle dimensions based on template
    rect_dimensions = [
        {'x': '21.3', 'y': '43.4', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '127.3', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '211.2', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '295.1', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '379', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '462.9', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '546.8', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '630.7', 'width': '180', 'height': '83.9'},
        {'x': '21.3', 'y': '714.6', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '43.4', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '127.3', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '211.2', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '295.1', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '379', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '462.9', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '546.8', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '630.7', 'width': '180', 'height': '83.9'},
        {'x': '207.6', 'y': '714.6', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '43.4', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '127.3', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '211.2', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '295.1', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '379', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '462.9', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '546.8', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '630.7', 'width': '180', 'height': '83.9'},
        {'x': '394', 'y': '714.6', 'width': '180', 'height': '83.9'}
    ]

    # Load used IDs
    used_ids = load_used_ids()

    # Get user input for configuration
    print("Enter encoding configuration:")
    area = int(input("  Area (e.g., 1 for Energy, 2 for Gas): "))
    producer_code = input("  Producer code (e.g., '24'): ")
    year = int(input("  Year (e.g., 2024): "))
    model_code = input("  Model code (e.g., 'D0'): ")
    config = {
        'area': area,
        'producer_code': producer_code,
        'year': year,
        'model_code': model_code
    }

    # Get user input for start and end
    start = int(input("Enter the start ID number: "))
    end = int(input("Enter the end ID number: "))

    # Generate unique IDs
    ids = generate_ids(start, end, used_ids, config)

    # Split into files if needed
    ids_per_file = 27 * 4  # 108 IDs per file
    for file_idx, i in enumerate(range(0, len(ids), ids_per_file)):
        # Get start and stop IDs for current file
        file_start_id = ids[i]
        file_end_id = ids[min(i + ids_per_file - 1, len(ids) - 1)]
        output_file = os.path.join(OUTPUT_DIR, f"sticker_page_{file_start_id}-{file_end_id}.svg")
        generate_svg(output_file, rect_dimensions, ids[i:i + ids_per_file])

    # Save new IDs to CSV
    save_ids_to_csv(ids)

if __name__ == "__main__":
    main()
