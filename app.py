from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Path for static images and JSON database
IMAGE_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
JSON_DB_PATH = os.path.join(os.getcwd(), 'data', 'art_gallery.json')

# File upload settings
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Ensure the 'data' directory exists
if not os.path.exists(os.path.dirname(JSON_DB_PATH)):
    os.makedirs(os.path.dirname(JSON_DB_PATH))

# Ensure the 'images' directory exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Default data to populate if the JSON file does not exist
DEFAULT_ARTWORKS = [
    {
        "title": "Art Piece 1",
        "description": "A beautiful piece of abstract art.",
        "image": "art1.jpg"
    },
    {
        "title": "Art Piece 2",
        "description": "A modern take on a classic style.",
        "image": "art2.jpg"
    },
    {
        "title": "Art Piece 3",
        "description": "A vibrant and colorful composition.",
        "image": "art3.jpg"
    }
]

# Load the existing image data from JSON (or initialize it if the file doesn't exist)
def load_image_data():
    if os.path.exists(JSON_DB_PATH):
        with open(JSON_DB_PATH, 'r') as file:
            return json.load(file)
    else:
        # If the JSON file does not exist, create it and load the default data
        save_image_data(DEFAULT_ARTWORKS)
        return DEFAULT_ARTWORKS

# Save the updated image data to JSON
def save_image_data(data):
    with open(JSON_DB_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route (loads images from the JSON database)
@app.route('/')
def home():
    artworks = load_image_data()
    return render_template('index.html', artworks=artworks)

# Route to download an image
@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename, as_attachment=True)

# Route to add an image to the gallery
@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form.get('title')
        description = request.form.get('description')
        
        # Handle file upload
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(IMAGE_FOLDER, filename))
            
            # Load the existing data
            artworks = load_image_data()

            # Add the new image data
            new_artwork = {
                "title": title,
                "description": description,
                "image": filename
            }
            artworks.append(new_artwork)

            # Save the updated data
            save_image_data(artworks)

            return redirect(url_for('home'))

    return render_template('add_image.html')

if __name__ == '__main__':
    app.run(debug=True)
