# For data curation for Cleanlab Studio project
import os
import pandas as pd

def create_metadata(folder_path="faces"):
    """Create a DataFrame with image paths and labels extracted from file names."""
    image_paths = []
    poses = []
    expressions = []
    eyes = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder {folder_path} not found")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png')):
            file_name_without_ext = os.path.splitext(filename)[0]
            parts = file_name_without_ext.split('_')
            if len(parts) >= 4:
                pose = parts[1]
                expression = parts[2]
                eye = parts[3]

            image_paths.append(filename)
            poses.append(pose)
            expressions.append(expression)
            eyes.append(eye)

    df = pd.DataFrame({
        'image': image_paths,
        'pose': poses,
        'expression': expressions,
        'eye': eyes
    })
    
    return df

# Create the dataframe
df = create_metadata()
print(df.head())
df.to_csv('faces//metadata.csv', index=False)