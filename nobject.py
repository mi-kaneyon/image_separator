from PIL import Image
import os

def delete_black_images(input_folder):
    # Get the absolute path of the input folder
    input_folder_path = os.path.abspath(input_folder)
    
    # Loop through each file in the input folder
    for filename in os.listdir(input_folder_path):
        # Construct the file path
        file_path = os.path.join(input_folder_path, filename)
        
        # Check if the file is an image (you can add more image extensions as needed)
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Open the image file
            image = Image.open(file_path)
            
            # Convert the image to grayscale
            grayscale_image = image.convert('L')
            
            # Calculate the histogram of pixel values
            histogram = grayscale_image.histogram()
            
            # Check if the image contains any non-black pixels (excluding noise)
            has_non_black_pixels = any(histogram[1:])
            
            # If the image is entirely black or contains only noise, delete it
            if not has_non_black_pixels:
                os.remove(file_path)
                print(f"Deleted: {filename}")
    
    # Print the deletion finish message
    print("Deletion complete!")


# Example usage
input_folder = "ouput_folder"  # Replace with the actual input folder path

delete_black_images(input_folder)
