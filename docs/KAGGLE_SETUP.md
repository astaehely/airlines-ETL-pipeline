# Kaggle API Setup Guide

## 📁 Where to Place Your `kaggle.json` File

### For macOS/Linux:

1. **Create the `.kaggle` directory** (if it doesn't exist):
   ```bash
   mkdir -p ~/.kaggle
   ```

2. **Copy your `kaggle.json` file**:
   ```bash
   cp /path/to/your/kaggle.json ~/.kaggle/kaggle.json
   ```

3. **Set proper permissions** (required for security):
   ```bash
   chmod 600 ~/.kaggle/kaggle.json
   ```

### For Windows:

1. **Place the file at**:
   ```
   C:\Users\<YourUsername>\.kaggle\kaggle.json
   ```

2. **Or create the directory**:
   ```cmd
   mkdir %HOMEPATH%\.kaggle
   copy kaggle.json %HOMEPATH%\.kaggle\kaggle.json
   ```

## 🔑 How to Get Your `kaggle.json` File

If you don't have it yet:

1. Go to **Kaggle**: https://www.kaggle.com/
2. Click on your **profile picture** (top right)
3. Click **Settings**
4. Scroll to **API** section
5. Click **"Create New Token"**
6. This downloads `kaggle.json` to your computer

## ✅ Verify Setup

After placing the file, test it:

```bash
python -c "import kagglehub; print('Kaggle API configured correctly!')"
```

Or run the ETL pipeline with Kaggle:
```bash
python etl_pipeline.py --kaggle
```

## 📋 What Your `kaggle.json` Should Look Like

```json
{
  "username": "your_kaggle_username",
  "key": "your_api_key_here"
}
```

**Important**: Never commit this file to git! It's already in `.gitignore` for your safety.

## 🔒 Security

- ✅ File should have `600` permissions (owner read/write only)
- ✅ Keep it in `~/.kaggle/` directory
- ✅ Never share or commit this file
- ✅ Already protected by `.gitignore` in this project

## 🐛 Troubleshooting

### Error: "Could not find kaggle.json"
- Make sure the file is in `~/.kaggle/kaggle.json`
- Check the filename is exactly `kaggle.json` (lowercase)

### Error: "Permission denied"
```bash
chmod 600 ~/.kaggle/kaggle.json
```

### Error: "Invalid API credentials"
- Generate a new token from Kaggle website
- Replace the old `kaggle.json` file

## 🚀 Quick Setup (macOS/Linux)

If your `kaggle.json` is in your Downloads folder:

```bash
# Create directory
mkdir -p ~/.kaggle

# Move file
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json

# Set permissions
chmod 600 ~/.kaggle/kaggle.json

# Test it
python etl_pipeline.py --kaggle
```

## 📝 Environment Variables (Alternative)

You can also set environment variables instead of using the file:

```bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_key"
```

Add to your `~/.bashrc` or `~/.zshrc` to make permanent.

---

**Need help?** Check the [official Kaggle API docs](https://github.com/Kaggle/kaggle-api#api-credentials)

