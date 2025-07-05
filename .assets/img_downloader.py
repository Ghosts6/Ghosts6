import os
import requests
import re
from urllib.parse import urlparse

# Create .assets directory
os.makedirs(".assets", exist_ok=True)

# Full HTML block with all image tags
html = '''
<img src="https://img.shields.io/static/v1?message=Instagram&logo=instagram&label=&color=E4405F&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="instagram logo" />
<img src="https://img.shields.io/static/v1?message=Twitch&logo=twitch&label=&color=9146FF&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="twitch logo" />
<img src="https://img.shields.io/static/v1?message=Discord&logo=discord&label=&color=7289DA&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="discord logo" />
<img src="https://img.shields.io/static/v1?message=Telegram&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="telegram logo" />
<img src="https://img.shields.io/static/v1?message=Youtube&logo=youtube&label=&color=FF0000&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="youtube logo" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="30" alt="flask logo" />
<img src="https://img.shields.io/static/v1?message=LeetCode&logo=leetcode&label=&color=FFA116&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="leetcode logo" />
'''

# Find all image src URLs
img_urls = re.findall(r'src="(https?://[^"]+)"', html)

# Map to track replacements
replacements = {}

print(f"Found {len(img_urls)} images. Starting download...\n")

for url in img_urls:
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)

    # Fallback filename for weird URLs (like icons8)
    if not filename or "." not in filename:
        filename = re.sub(r'\W+', '_', url.split('/')[-1]) + ".png"

    local_path = f".assets/{filename}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(response.content)
        print(f"✔ Downloaded: {url} → {local_path}")
        replacements[url] = local_path
    except Exception as e:
        print(f"✖ Failed to download {url}: {e}")

# Replace URLs in HTML
for old_url, local_path in replacements.items():
    html = html.replace(old_url, local_path)

# Write updated HTML to file
with open("updated_icons_block.html", "w") as f:
    f.write(html)

print("\n✅ All done! Updated HTML saved to 'updated_icons_block.html'.")