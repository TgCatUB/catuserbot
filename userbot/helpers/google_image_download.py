import html
import os
import random
import re
import time
import urllib.parse

import httpx
from googleapiclient.discovery import build
from PIL import Image

try:
    from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
except ImportError:
    BingImageCrawler, GoogleImageCrawler = None, None


def create_directories(main_directory, dir_name):
    # make a search keyword directory
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
    return os.path.join(main_directory, dir_name)


def google_crawl_images(query, num_images=3):
    clean_name = re.sub(r"[^a-zA-Z0-9_-]", "_", query)[:30]
    sub_dir = f"{clean_name}_{random.randint(1000, 9999)}"
    sub_directory = create_directories("downloads", sub_dir)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    image_urls = []
    # 1. Primary: Bing Image Search async endpoint
    try:
        q_enc = urllib.parse.quote_plus(query)
        url = f"https://www.bing.com/images/async?q={q_enc}&first=0"
        with httpx.Client(headers=headers, timeout=12, follow_redirects=True) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                raw_text = html.unescape(resp.text)
                image_urls.extend(re.findall(r'\"murl\":\"(https?://[^\"]+)\"', raw_text))
    except Exception:
        pass

    # 2. Secondary fallback: Yandex Image Search
    if len(image_urls) < num_images:
        try:
            url = "https://yandex.com/images/search"
            with httpx.Client(headers=headers, timeout=12, follow_redirects=True) as client:
                resp = client.get(url, params={"text": query})
                if resp.status_code == 200:
                    y_urls = re.findall(r"img_url=(https?%3A%2F%2F[^&]+)", resp.text)
                    for u in y_urls:
                        image_urls.append(urllib.parse.unquote(u))
        except Exception:
            pass

    downloaded = []
    with httpx.Client(headers=headers, timeout=10, follow_redirects=True) as client:
        # Check candidates (up to 4x requested number or at least 15)
        candidates = image_urls[:max(num_images * 4, 15)]
        for img_url in candidates:
            if len(downloaded) >= num_images:
                break
            try:
                res = client.get(img_url)
                if res.status_code == 200 and len(res.content) > 1024:
                    raw_file = os.path.join(sub_directory, f"temp_{len(downloaded)+1}")
                    with open(raw_file, "wb") as f:
                        f.write(res.content)

                    # Validate with PIL and normalize format
                    try:
                        with Image.open(raw_file) as im:
                            ext = ".jpg"
                            if im.format == "PNG":
                                ext = ".png"
                            elif im.format == "GIF":
                                ext = ".gif"
                            else:
                                # Convert webp or other formats to JPEG for guaranteed Telegram preview
                                im = im.convert("RGB")

                            dest_file = os.path.join(sub_directory, f"img_{len(downloaded)+1}{ext}")
                            im.save(dest_file)
                            downloaded.append(dest_file)
                    except Exception:
                        pass
                    finally:
                        if os.path.exists(raw_file):
                            os.remove(raw_file)
            except Exception:
                continue

    return downloaded


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

    clean_name = re.sub(r"[^a-zA-Z0-9_-]", "_", query)[:30]
    sub_dir = f"{clean_name}_{random.randint(1000, 9999)}"

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
                dest = f"{sub_directory}/image_{i+1}{file_extension}"
                with open(dest, "wb") as file:
                    file.write(response.content)
                download_paths.append(dest)
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
