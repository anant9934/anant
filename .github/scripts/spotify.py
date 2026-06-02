import os
import requests
import base64
from io import BytesIO

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN")

def get_access_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        }
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error getting access token:", response.text)
        return None

def get_currently_playing(access_token):
    response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204: # Not playing anything
        return get_recently_played(access_token)
    else:
        return None

def get_recently_played(access_token):
    response = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?limit=1",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if response.status_code == 200:
        items = response.json().get("items")
        if items:
            track = items[0].get("track")
            return {"item": track, "is_playing": False}
    return None

def image_to_base64(url):
    response = requests.get(url)
    if response.status_code == 200:
        encoded = base64.b64encode(response.content).decode()
        return f"data:{response.headers['Content-Type']};base64,{encoded}"
    return ""

def generate_svg(track_data):
    if not track_data or 'item' not in track_data:
        return ""
        
    track = track_data['item']
    is_playing = track_data.get('is_playing', False)
    
    title = track['name']
    artist = ", ".join([a['name'] for a in track['artists']])
    image_url = track['album']['images'][0]['url']
    image_b64 = image_to_base64(image_url)
    
    status = "Listening to Spotify" if is_playing else "Recently Played"
    
    # Beautiful Spotify SVG Template
    svg = f"""<svg width="400" height="130" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="130" rx="10" fill="#181818" />
    <svg x="15" y="15">
        <rect width="100" height="100" rx="5" fill="#282828" />
        <image href="{image_b64}" width="100" height="100" clip-path="inset(0% round 5px)" />
    </svg>
    <text x="135" y="45" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#1DB954">{status}</text>
    <text x="135" y="70" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#FFFFFF">{title}</text>
    <text x="135" y="95" font-family="Arial, sans-serif" font-size="14" fill="#B3B3B3">{artist}</text>
    
    <!-- Sound bars animation if playing -->
    {'''
    <svg x="330" y="55" width="40" height="40">
        <rect x="0" y="15" width="4" height="25" fill="#1DB954">
            <animate attributeName="height" values="25;5;25" dur="1s" repeatCount="indefinite"/>
            <animate attributeName="y" values="15;35;15" dur="1s" repeatCount="indefinite"/>
        </rect>
        <rect x="8" y="5" width="4" height="35" fill="#1DB954">
            <animate attributeName="height" values="35;15;35" dur="0.8s" repeatCount="indefinite"/>
            <animate attributeName="y" values="5;25;5" dur="0.8s" repeatCount="indefinite"/>
        </rect>
        <rect x="16" y="25" width="4" height="15" fill="#1DB954">
            <animate attributeName="height" values="15;30;15" dur="1.2s" repeatCount="indefinite"/>
            <animate attributeName="y" values="25;10;25" dur="1.2s" repeatCount="indefinite"/>
        </rect>
    </svg>
    ''' if is_playing else ''}
</svg>"""
    return svg

def main():
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        print("Missing Spotify credentials in environment variables.")
        return

    access_token = get_access_token()
    if not access_token:
        return
        
    track_data = get_currently_playing(access_token)
    svg = generate_svg(track_data)
    
    if svg:
        with open("spotify-now-playing.svg", "w") as f:
            f.write(svg)
        print("Successfully generated spotify-now-playing.svg")
    else:
        print("No track data found or failed to generate SVG.")

if __name__ == "__main__":
    main()
