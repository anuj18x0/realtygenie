# 🏡 RealtyGenie Pro
## AI-Powered Property Marketing Revolution

Transform raw property images into stunning social media content in seconds with professional AI enhancement, compelling descriptions, and multi-platform social media automation.

![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3.2-purple)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-green)

## ✨ Features

### 🎨 **Professional Image Processing**
- **Advanced AI Enhancement** with 3 intensity levels (Light/Medium/Strong)
- **Smart Resizing** with aspect ratio preservation
- **Intelligent Compression** with quality optimization
- **Real-time Metrics** showing file size reduction and processing stats

### 🤖 **AI-Powered Description Generation**
- **BLIP AI Model** for intelligent image captioning
- **Multiple Description Styles**:
  - 💎 **Luxury Market** - Premium positioning for high-end buyers
  - 👨‍👩‍👧‍👦 **Family-Friendly** - Appeals to growing families  
  - 💰 **Investment** - ROI-focused for investors
  - 📱 **Social Media** - Short, engaging posts with hashtags

### 🌐 **Multi-Platform Social Media Automation**
- **Instagram** - Visual-first with engagement metrics
- **Facebook** - Community-focused content
- **Twitter** - Concise, hashtag-optimized
- **LinkedIn** - Professional real estate networking
- **Copy-to-clipboard** functionality for instant sharing

### 🎨 **Beautiful Bootstrap 5 Interface**
- **Professional Gradient Design** with hover animations
- **Responsive Layout** that looks amazing on all devices
- **Interactive Settings Panel** with real-time updates
- **Before/After Gallery** with download options

## 🚀 Quick Start

### **Local Installation**
```bash
# Clone or download the project
cd reality-genai

# Run the setup script
python setup.py

# Or install manually
pip install -r requirements.txt
```

### **Launch the Application**
```bash
# Local installation:
streamlit run streamlit_app.py

# Docker (automatic startup)
# Access at http://localhost:8501
```

### **Open in Browser & Upload Images**
```
http://localhost:8501
```
Upload property images directly through the web interface - no need for sample images!

## 📋 System Requirements

### **Minimum Requirements:**
- Python 3.8+
- 4GB RAM
- 2GB free disk space

### **Recommended for Best Performance:**
- Python 3.11+
- 8GB+ RAM
- NVIDIA GPU with CUDA support
- 5GB+ free disk space

## 🛠️ Project Structure

```
reality-genai/
├── 🏡 streamlit_app.py          # Main Bootstrap 5 web interface
├── 🎨 image_processor.py        # Advanced image enhancement
├── 🤖 property_descriptions.py  # AI description generation
├── 📱 social_media_automation.py # Multi-platform content
├── 🚀 launch_app.py            # Application launcher
├── ⚙️ setup.py                 # Automated setup script
├── 📦 requirements.txt         # Python dependencies
├── 📁 images/                  # (Optional) Local image storage
├── 📁 processed_images/        # Enhanced images output
├── 📁 descriptions/            # Generated descriptions
└── 📁 outputs/                 # Final content
```

## 🎯 Usage Workflow

### **Step 1: Upload Images**
- Drag and drop 5-6 property images
- Supported formats: JPG, PNG, WebP
- Images are displayed in a beautiful grid

### **Step 2: Configure Settings**
- **Image Quality**: 60-100% (default: 85%)
- **Enhancement Level**: Light/Medium/Strong
- Settings update in real-time

### **Step 3: Process Images**
- Click "🚀 Start Processing"
- Watch real-time progress and status
- AI enhances images and generates content

### **Step 4: Review Results**
- **📸 Before/After Gallery**: Compare original vs enhanced
- **📝 AI Descriptions**: Multiple styles for different audiences
- **🌐 Social Media Content**: Platform-specific posts

### **Step 5: Download & Share**
- Download enhanced images
- Copy social media content
- Share across platforms


## �🔧 Advanced Configuration

### **GPU Acceleration**
```python
# Automatic GPU detection
# CUDA support for faster processing
device = "cuda" if torch.cuda.is_available() else "cpu"
```

### **Custom Enhancement Settings**
```python
# Modify in image_processor.py
enhancement_profiles = {
    'light': {'brightness': 1.05, 'contrast': 1.08},
    'medium': {'brightness': 1.1, 'contrast': 1.15},
    'strong': {'brightness': 1.15, 'contrast': 1.25}
}
```

## 📊 Performance Metrics

- **Processing Speed**: 2-5 seconds per image
- **File Size Reduction**: 20-60% average
- **Description Generation**: 1-2 seconds per style
- **Social Content**: Instant generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

Having issues? Check these common solutions:

### **Installation Issues**
```bash
# Update pip
python -m pip install --upgrade pip

# Install specific torch version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### **Memory Issues**
- Reduce image quality setting
- Use CPU instead of GPU
- Process fewer images at once

### **GPU Not Detected**
- Install CUDA toolkit
- Update GPU drivers
- Restart application

## 🌟 What's Next?

- 🔄 **Batch Processing**: Handle hundreds of images
- 🌍 **Multi-language Support**: Global real estate markets
- 📈 **Analytics Dashboard**: Track engagement metrics
- 🤖 **Advanced AI Models**: Even better descriptions
- 📱 **Mobile App**: iOS/Android companion