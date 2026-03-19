"""
AI Agent Tools - Function implementations for LLM tool calling.

This module contains 4 tools that can be provided to LLMs:
1. get_current_time - Returns current timestamp
2. get_weather_from_ip - Fetches weather based on IP geolocation
3. write_txt_file - Writes content to text files
4. generate_qr_code - Generates QR codes with optional logo embedding

AI 智能体工具模块
包含4个可供LLM调用的工具函数
"""

import requests
from datetime import datetime
from pathlib import Path
from typing import Optional

import qrcode
from qrcode.image.styledpil import StyledPilImage

from config import Config


# ========================================
# Tool 1: Current Time
# ========================================

def get_current_time() -> dict:
    """
    Returns the current time.

    返回当前时间。

    Returns:
        dict: Current time in HH:MM:SS format
    """
    return {"current_time": datetime.now().strftime("%H:%M:%S")}


# ========================================
# Tool 2: Weather Information
# ========================================

def get_weather_from_ip() -> dict:
    """
    Retrieves current, high, and low temperatures for the user's location
    based on their IP address.

    基于用户的IP地址获取当前位置的温度信息（当前温度、最高温、最低温）。

    Returns:
        dict: Weather information with temperature data

    Examples:
        >>> get_weather_from_ip()
        {"status": "success", "temperature": {"current": 72.5, "high": 78.0, "low": 65.2, "unit": "°F"}}
    """
    try:
        # Get geographic coordinates from IP address
        location_response = requests.get(Config.IPINFO_URL, timeout=10)
        location_response.raise_for_status()
        lat, lon = location_response.json()['loc'].split(',')

        # Set up weather API parameters
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m",
            "daily": "temperature_2m_max,temperature_2m_min",
            "temperature_unit": Config.TEMPERATURE_UNIT,
            "timezone": Config.DEFAULT_TIMEZONE
        }

        # Fetch weather data
        weather_response = requests.get(Config.WEATHER_API_URL, params=params, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Format and return weather information
        unit_symbol = "°F" if Config.TEMPERATURE_UNIT == "fahrenheit" else "°C"
        current_temp = weather_data['current']['temperature_2m']
        high_temp = weather_data['daily']['temperature_2m_max'][0]
        low_temp = weather_data['daily']['temperature_2m_min'][0]

        return {
            "status": "success",
            "temperature": {
                "current": current_temp,
                "high": high_temp,
                "low": low_temp,
                "unit": unit_symbol
            },
            "location": {
                "latitude": lat,
                "longitude": lon
            }
        }

    except requests.RequestException as e:
        return {
            "status": "error",
            "error_type": "network_error",
            "message": str(e)
        }
    except (KeyError, ValueError) as e:
        return {
            "status": "error",
            "error_type": "parsing_error",
            "message": str(e)
        }


# ========================================
# Tool 3: File Writing
# ========================================

def write_txt_file(file_path: str, content: str) -> dict:
    """
    Writes a string to a .txt file, creating or overwriting as needed.

    将字符串写入文本文件，如果文件已存在则覆盖。

    Args:
        file_path (str): Destination file path (can be relative or absolute)
        content (str): Text content to write

    Returns:
        dict: Result with file information

    Examples:
        >>> write_txt_file("reminder.txt", "Call Daniel at 7pm")
        {"status": "success", "file_path": "E:\\...\\reminder.txt", "file_name": "reminder.txt"}
    """
    try:
        # Convert to Path object for better handling
        path = Path(file_path)

        # If path is relative, make it relative to project root
        if not path.is_absolute():
            path = Config.PROJECT_ROOT / path

        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        path.write_text(content, encoding="utf-8")

        return {
            "status": "success",
            "file_path": str(path.absolute()),
            "file_name": path.name,
            "content_length": len(content)
        }

    except Exception as e:
        return {
            "status": "error",
            "error_type": "file_error",
            "file_path": file_path,
            "message": str(e)
        }


# ========================================
# Tool 4: QR Code Generation
# ========================================

def generate_qr_code(data: str, filename: str, image_path: Optional[str] = None) -> dict:
    """
    Generates a QR code image with optional embedded logo.

    生成二维码图片，可选嵌入Logo图片。

    Args:
        data (str): Text or URL to encode in the QR code
        filename (str): Output filename (without extension)
        image_path (str, optional): Path to logo image to embed in center

    Returns:
        dict: Result with QR code information

    Examples:
        >>> generate_qr_code("https://deeplearning.ai", "dl_qr", "assets/dl_logo.jpg")
        {"status": "success", "qr_code_path": "output/dl_qr.png", "encoded_data": "https://deeplearning.ai"}
    """
    try:
        # Create QR code with high error correction for logo embedding
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)

        has_logo = False
        logo_used = None

        # Generate image with optional embedded logo
        if image_path:
            logo_path = Path(image_path)
            if not logo_path.is_absolute():
                logo_path = Config.ASSETS_DIR / image_path

            if logo_path.exists():
                img = qr.make_image(image_factory=StyledPilImage, embedded_image_path=str(logo_path))
                has_logo = True
                logo_used = str(logo_path)
            else:
                print(f"⚠️  Warning: Image {logo_path} not found. Generating QR code without logo.")
                img = qr.make_image()
        else:
            img = qr.make_image()

        # Save to output directory
        output_path = Config.OUTPUT_DIR / f"{filename}.png"
        img.save(output_path)

        return {
            "status": "success",
            "qr_code_path": str(output_path),
            "file_name": f"{filename}.png",
            "encoded_data": data,
            "has_logo": has_logo,
            "logo_path": logo_used
        }

    except Exception as e:
        return {
            "status": "error",
            "error_type": "qr_generation_error",
            "filename": filename,
            "message": str(e)
        }


# ========================================
# Tool Registry
# ========================================

# List of all available tools for easy import
ALL_TOOLS = [
    get_current_time,
    get_weather_from_ip,
    write_txt_file,
    generate_qr_code
]


# ========================================
# Module Test
# ========================================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing AI Agent Tools")
    print("=" * 60)

    print("\n1. Testing get_current_time():")
    print(f"   {get_current_time()}")

    print("\n2. Testing get_weather_from_ip():")
    print(f"   {get_weather_from_ip()}")

    print("\n3. Testing write_txt_file():")
    print(f"   {write_txt_file('test_output.txt', 'This is a test file.')}")

    print("\n4. Testing generate_qr_code():")
    print(f"   {generate_qr_code('https://deeplearning.ai', 'test_qr')}")

    print("\n" + "=" * 60)
    print("✅ All tools loaded successfully!")
    print("=" * 60)
