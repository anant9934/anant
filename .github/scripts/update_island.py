import re
import os
from datetime import datetime, timedelta, timezone

# IST is UTC+5:30
ist = timezone(timedelta(hours=5, minutes=30))
now = datetime.now(ist)
hour = now.hour

# Choose the GIF based on the time of day in IST
if 6 <= hour < 12:
    # Morning (Sunrise)
    gif_url = "https://i.giphy.com/media/TEILCythSScYyaaEDK/giphy.webp"
elif 12 <= hour < 17:
    # Afternoon (Sunny Island)
    gif_url = "https://i.giphy.com/media/10IEUy0f5V3WLu/giphy.webp"
elif 17 <= hour < 20:
    # Evening (Sunset)
    gif_url = "https://i.giphy.com/media/e0Uiyu70TXQAALdKP9/giphy.webp"
else:
    # Night (Night Space / Stars)
    # Using a starry night pixel art GIF
    gif_url = "https://media.giphy.com/media/3o7TKrEzvLbgzGgJeq/giphy.gif"

print(f"Current IST Time: {now.strftime('%H:%M:%S')}")
print(f"Selected GIF: {gif_url}")

# Read the README
readme_path = "README.md"
with open(readme_path, "r") as f:
    content = f.read()

# Replace the specific dynamic-island image source using regex
pattern = r'(<img id="dynamic-island" src=")([^"]+)(")'
new_content = re.sub(pattern, rf'\g<1>{gif_url}\g<3>', content)

if content != new_content:
    with open(readme_path, "w") as f:
        f.write(new_content)
    print("README.md updated with the new island.")
else:
    print("Island is already up to date.")
