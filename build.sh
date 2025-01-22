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
# Verify system dependencies
ldconfig -p | grep libgstgl-1.0.so.0
ldconfig -p | grep libgstcodecparsers-1.0.so.0
ldconfig -p | grep libavif.so.15
ldconfig -p | grep libenchant-2.so.2
ldconfig -p | grep libsecret-1.so.0
ldconfig -p | grep libmanette-0.2.so.0
ldconfig -p | grep libGLESv2.so.2
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
