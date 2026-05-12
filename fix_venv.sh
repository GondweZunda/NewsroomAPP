#!/bin/bash
# Clean venv reinstall - RECOMMENDED METHOD
# Usage: bash fix_venv.sh

set -e

echo "🔧 Reinstalling NewsroomAPP Virtual Environment (Clean)"
echo ""

VENV_PATH="/home/adminuser/venv"

# Step 1: Remove old venv
echo "🗑️  Step 1: Removing old virtual environment..."
rm -rf "$VENV_PATH"

# Step 2: Create fresh venv
echo "📦 Step 2: Creating fresh virtual environment..."
python3 -m venv "$VENV_PATH"

# Step 3: Activate venv
echo "🔌 Step 3: Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Step 4: Upgrade pip, setuptools, wheel
echo "⬆️  Step 4: Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Step 5: Install required packages
echo "📥 Step 5: Installing required packages..."
pip install streamlit groq textblob

echo ""
echo "✅ Virtual environment setup complete!"
echo ""
echo "🚀 Run the app with:"
echo "   source $VENV_PATH/bin/activate"
echo "   streamlit run app.py"
echo ""
