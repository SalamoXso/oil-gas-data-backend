#!/bin/bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libavif15 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
