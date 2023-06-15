from PIL import Image
import os

def separate_images_in_directory(input_folder, output_folder_name, n):
    # Create the output folder path
    output_folder = os.path.join(os.getcwd(), output_folder_name)
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through each file in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is an image (you can add more image extensions as needed)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Construct the path for the current image
            image_path = os.path.join(input_folder, filename)
            
            # Open the image file
            original_image = Image.open(image_path)
            
            # Get the dimensions of the original image
            width, height = original_image.size
            
            # Calculate the dimensions of each cut image
            cut_width = width // n
            cut_height = height // n
            
            # Loop through each row and column to cut the image
            for i in range(n):
                for j in range(n):
                    # Calculate the coordinates of the current cut
                    left = j * cut_width
                    upper = i * cut_height
                    right = left + cut_width
                    lower = upper + cut_height
                    
                    # Crop the original image to the current cut
                    cut_image = original_image.crop((left, upper, right, lower))
                    
                    # Save the cut image with a modified name
                    cut_image_name = os.path.splitext(filename)[0] + str(i * n + j) + os.path.splitext(filename)[1]
                    cut_image_path = os.path.join(output_folder, cut_image_name)
                    cut_image.save(cut_image_path)
    
    # Print the separation finish message
    print("Separation complete!")


# Example usage
input_folder = "input_folder"  # Replace with the actual input folder path
output_folder_name = "output_folder"  # Replace with the desired output folder name
n = 4  # Number of cuts (e.g., 4x4)

separate_images_in_directory(input_folder, output_folder_name, n)
