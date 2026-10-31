import os
import random
import time

import httpx
from googleapiclient.discovery import build
from icrawler.builtin import GoogleImageCrawler


def create_directories(main_directory, dir_name):
    # make a search keyword  directory
    try:
        if not os.path.exists(main_directory):
            os.makedirs(main_directory)
            time.sleep(0.15)
        path = dir_name
        sub_directory = os.path.join(main_directory, path)
        if not os.path.exists(sub_directory):
            os.makedirs(sub_directory)

        return sub_directory
    except OSError as e:
        if e.errno != 17:
            raise
    return


def google_crawl_images(query, num_images=3):
    sub_dir = f"{query.replace(' ','_')}_{random.randint(1000,9999)}"

    sub_directory = create_directories("downloads", sub_dir)

    google_crawler = GoogleImageCrawler(storage={"root_dir": sub_directory})

    google_crawler.crawl(keyword=query, max_num=num_images)

    files = os.listdir(sub_directory)

    return list(map(lambda path: os.path.join(sub_directory, path), files))


def search_and_download_images(query, api_key, cse_id, num_images=3):
    service = build("customsearch", "v1", developerKey=api_key)

    try:
        res = service.cse().list(q=query, cx=cse_id, searchType="image", num=num_images).execute()
    except Exception as e:
        print(f"An error occurred while searching: {e}")
        return

    if "items" not in res:
        print("No image results found.")
        return

    sub_dir = f"{query.replace(' ', '_')}_{random.randint(1000,9999)}"

    # Create a directory for the images
    sub_directory = create_directories("downloads", sub_dir)

    errors = []
    download_paths = []

    for i, item in enumerate(res["items"]):
        try:
            # Get the image URL
            image_url = item["link"]

            # Download the image
            response = httpx.get(image_url, follow_redirects=True, timeout=60)

            # Check if the request was successful
            if response.status_code == 200:
                # Get the file extension
                file_extension = os.path.splitext(image_url)[1]
                if file_extension == "":
                    file_extension = ".jpg"  # Default to .jpg if no extension found

                # Save the image
                with open(f"{sub_directory}/image_{i+1}{file_extension}", "wb") as file:
                    file.write(response.content)
                download_paths.append(f"{sub_directory}/image_{i+1}{file_extension}")
                print(f"Downloaded: image_{i+1}{file_extension}")
            else:
                print(f"Failed to download image {i+1}")

        except Exception as e:
            errors.append(f"An error occurred while downloading image {i+1}: {e}")

    return {
        "download_path": download_paths,
        "folder": sub_directory,
        "errors": errors,
    }


# ------------- Main Program -------------#
def main():
    google_crawl_images("catuserbot")


if __name__ == "__main__":
    main()
