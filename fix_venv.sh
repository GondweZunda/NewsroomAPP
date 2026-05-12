#!/bin/bash
# Fix venv permissions and reinstall packages
# Usage: bash fix_venv.sh

set -e

echo "🔧 Fixing NewsroomAPP Virtual Environment..."
echo ""

VENV_PATH="/home/adminuser/venv"
PYTHON_VERSION="3.13"

# Step 1: Fix permissions
echo "📝 Step 1: Fixing permissions on site-packages..."
sudo chown -R $USER "$VENV_PATH/lib/python$PYTHON_VERSION/site-packages" 2>/dev/null || {
    echo "⚠️  Could not fix permissions with chown. Trying alternative method..."
    sudo chmod -R u+w "$VENV_PATH/lib/python$PYTHON_VERSION/site-packages"
}

# Step 2: Activate venv and upgrade pip
echo "📦 Step 2: Upgrading pip..."
source "$VENV_PATH/bin/activate"
python3 -m pip install --upgrade pip setuptools wheel --quiet

# Step 3: Install required packages
echo "📥 Step 3: Installing required packages..."
python3 -m pip install groq textblob --no-cache-dir

echo ""
echo "✅ Virtual environment fixed successfully!"
echo ""
echo "🚀 You can now run the app with:"
echo "   source $VENV_PATH/bin/activate"
echo "   streamlit run app.py"
