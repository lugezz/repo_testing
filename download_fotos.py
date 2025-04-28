import requests


def download_jpgs(base_url, start, end):
    for i in range(start, end + 1):
        filename = f"malvinas{i:03}.jpg"
        url = f"{base_url}/{filename}"

        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}. Status code: {response.status_code}")


base_url = "https://cbarun.com.ar/wp-content/uploads/2025/04/"
download_jpgs(base_url, 2, 900)
