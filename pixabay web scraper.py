import requests
import csv
import concurrent.futures


#getting the cover image url and write it in the file

def download(image_data):
    url = image_data["URL"]
    image_response = requests.get(url)
    with open(f"image_{image_data['id']}.jpg", "wb") as file:
        file.write(image_response.content)
    print(f"Downloaded image {image_data['id']}/{image_data['num_images']}")


#  making function for the pixabay main url and number of images and for the API key

def download_from_pixabay( num_images, api_key):
    base_url = "https://pixabay.com/api/"
    params = {
        "key": api_key,
        "image_type": "cover",
        "numnunm": num_images
    }
# by API we can get response from the site 
# by json we can extract image data 
    response = requests.get(base_url, params=params)
    data = response.json()
    
#  getting information for csv file  

#  making list for the images and their details 

    image_data = []
    for i, image in enumerate(data["hits"]):
        tags = image["tags"]
        creator_name = image["user"]
        image_url = image["largeImageURL"]
        title = image["userImageURL"]
        resolution = f"{image['imageWidth']}x{image['imageHeight']}"
        image_data.append({
            "id": i + 1,
            "num_images": num_images,
            "Tags": tags,
            "Creator": creator_name,
            "URL": image_url,
            "Title": title,
            "Resolution": resolution
        })
        
#          multithreading

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, image_data)
        
#      writing the data in the csv file 

    keys = image_data[0].keys()
    with open("pixabay_image_keys.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(image_data)

    print("images and CSV file are in the data.eater file now ^_^")



num_images = 12
api_key = "41944678-39b6d49cec7fd580a769da914"
download_from_pixabay( num_images, api_key)