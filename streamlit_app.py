import streamlit as st
import os
import json
import time
import tempfile
import shutil
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import zipfile
import io
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64

from image_processor import PropertyImageProcessor
from property_descriptions import PropertyDescriptionGenerator
from social_media_automation import SocialMediaGenerator

# Page configuration
st.set_page_config(
    page_title="RealtyGenie Pro - AI Property Marketing",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bootstrap 5 + Custom styling
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global font */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Custom gradients */
    .gradient-primary {
        background: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);
        color: white;
    }
    
    .gradient-success {
        background: linear-gradient(135deg, #198754 0%, #20c997 100%);
        color: white;
    }
    
    .gradient-info {
        background: linear-gradient(135deg, #0dcaf0 0%, #6f42c1 100%);
        color: white;
    }
    
    .gradient-warning {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
    }
    
    .text-gradient {
        background: linear-gradient(135deg, #0d6efd, #6610f2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Enhanced card animations */
    .card {
        transition: all 0.3s ease;
        border: none !important;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid #dee2e6;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0d6efd, #6610f2);
        color: white !important;
        border: 1px solid #0d6efd;
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Button enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #0d6efd, #6610f2);
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(13, 110, 253, 0.3);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #198754, #20c997);
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(25, 135, 84, 0.3);
    }
    
    /* Floating animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0d6efd, #6610f2);
        border-radius: 10px;
    }
    
    /* Alert styling */
    .alert {
        border-radius: 12px;
        border: none;
        font-weight: 500;
    }
    
    /* Copy button styling */
    button[onclick*="clipboard"] {
        transition: all 0.2s ease;
    }
    
    button[onclick*="clipboard"]:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    defaults = {
        'uploaded_files': [],
        'processing_complete': False,
        'results': {},
        'temp_dir': None,
        'processing_history': [],
        'user_preferences': {
            'image_quality': 85,
            'target_width': 1080,
            'target_height': 810,
            'enhancement_level': 'medium'
        },
        'last_settings': {
            'image_quality': 85,
            'enhancement_level': 'medium'
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    current_quality = st.session_state.user_preferences['image_quality']
    current_enhancement = st.session_state.user_preferences['enhancement_level']
    last_quality = st.session_state.last_settings['image_quality']
    last_enhancement = st.session_state.last_settings['enhancement_level']
    
    if current_quality != last_quality or current_enhancement != last_enhancement:
        st.session_state.processing_complete = False
        st.session_state.results = {}
        st.session_state.last_settings['image_quality'] = current_quality
        st.session_state.last_settings['enhancement_level'] = current_enhancement

def create_hero_header():
    st.markdown("""
    <div class="container-fluid mb-5">
        <div class="row">
            <div class="col-12">
                <div class="card gradient-primary rounded-4 shadow-lg">
                    <div class="card-body text-center p-5">
                        <h1 class="display-3 fw-bold mb-3">
                            <i class="bi bi-house-heart"></i> RealtyGenie Pro
                        </h1>
                        <p class="lead fs-3 mb-4">AI-Powered Property Marketing Revolution</p>
                        <p class="fs-5 mb-4">Transform raw property images into stunning social media content in seconds</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="text-center">
            <i class="bi bi-lightning-charge text-primary" style="font-size: 4rem;"></i>
            <h5 class="mt-2">Lightning Fast</h5>
            <p class="text-primary">Process images in seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="text-center">
            <i class="bi bi-robot text-success" style="font-size: 4rem;"></i>
            <h5 class="mt-2">AI Powered</h5>
            <p class="text-success">Smart image enhancement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="text-center">
            <i class="bi bi-share text-info" style="font-size: 4rem;"></i>
            <h5 class="mt-2">Social Ready</h5>
            <p class="text-info">Multi-platform content</p>
        </div>
        """, unsafe_allow_html=True)

def create_upload_section():
    st.markdown("""
    <div class="container mb-4">
        <div class="row">
            <div class="col-12">
                <div class="card shadow-sm rounded-4">
                    <div class="card-body p-4">
                        <h3 class="card-title text-center mb-3">
                            <i class="bi bi-camera text-gradient"></i> Upload Your Property Images
                        </h3>
                        <p class="text-center text-muted">Drag and drop your high-quality property photos to get started</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose property images",
        type=['png', 'jpg', 'jpeg', 'webp'],
        accept_multiple_files=True,
        key="property_images",
        help="Upload up to 10 high-quality property images"
    )
    
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        
        st.markdown("""
        <div class="container mt-4">
            <div class="row">
                <div class="col-12">
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <i class="bi bi-check-circle-fill me-2"></i>
                        <div>Successfully uploaded {} image(s)!</div>
                    </div>
                </div>
            </div>
        </div>
        """.format(len(uploaded_files)), unsafe_allow_html=True)
        
        # Show image grid
        cols = st.columns(min(4, len(uploaded_files)))
        for idx, file in enumerate(uploaded_files):
            with cols[idx % 4]:
                image = Image.open(file)
                st.image(image, caption=file.name, width='stretch')
                image = Image.open(file)
                st.image(image, caption=file.name, width='stretch')
    
    return uploaded_files

def create_processing_section():
    if not st.session_state.uploaded_files:
        return
    
    settings_changed = (
        st.session_state.user_preferences['image_quality'] != st.session_state.last_settings['image_quality'] or
        st.session_state.user_preferences['enhancement_level'] != st.session_state.last_settings['enhancement_level']
    )
    
    if settings_changed:
        st.warning("⚠️ Settings have changed. Click 'Start Processing' to apply new settings.")
    
    st.markdown("""
    <div class="container mb-4">
        <div class="row">
            <div class="col-12">
                <div class="card gradient-info shadow-sm rounded-4">
                    <div class="card-body text-center p-4">
                        <h3 class="card-title">
                            <i class="bi bi-gear-fill"></i> Process Your Images
                        </h3>
                        <p class="mb-4">Click below to enhance images, generate descriptions, and create social media content</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col2:
        button_text = "Reprocess with New Settings" if settings_changed else "🚀 Start Processing"
        if st.button(button_text, type="primary", width='stretch'):
            process_images()

def process_images():
    try:
        # Display current settings for debugging
        current_quality = st.session_state.user_preferences['image_quality']
        current_enhancement = st.session_state.user_preferences['enhancement_level']
        
        st.info(f"Processing with: Quality={current_quality}%, Enhancement={current_enhancement.title()}")
        
        with st.spinner("🔄 Processing your property images with AI..."):
            temp_dir = tempfile.mkdtemp()
            st.session_state.temp_dir = temp_dir
            
            image_processor = PropertyImageProcessor(
                target_size=(1080, 810), 
                quality=st.session_state.user_preferences['image_quality']
            )
            desc_generator = PropertyDescriptionGenerator()
            social_generator = SocialMediaGenerator()
            
            results = {}
            total_files = len(st.session_state.uploaded_files)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, uploaded_file in enumerate(st.session_state.uploaded_files):
                current_file = f"Processing {idx + 1}/{total_files}: {uploaded_file.name}"
                status_text.text(current_file)
                
                try:
                    original_path = os.path.join(temp_dir, f"original_{uploaded_file.name}")
                    with open(original_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    enhancement_level = st.session_state.user_preferences['enhancement_level'].lower()
                    processing_metadata = image_processor.process_image(
                        original_path, 
                        enhancement_level=enhancement_level
                    )
                    
                    if processing_metadata['status'] != 'success':
                        raise Exception(f"Image processing failed: {processing_metadata.get('error', 'Unknown error')}")
                    
                    processed_path = processing_metadata['output_path']
                    
                    descriptions = desc_generator.generate_description(processed_path, style='luxury')
                    
                    if 'error' in descriptions:
                        st.warning(f"⚠️ Description generation failed for {uploaded_file.name}: {descriptions['error']}")
                        descriptions = {
                            'luxury': f"Beautiful property featuring stunning architecture and modern amenities.",
                            'family': f"Perfect family home with spacious rooms and comfortable living areas.",
                            'investment': f"Excellent investment opportunity in a prime location.",
                            'social': f"🏡 STUNNING PROPERTY! Beautiful home with modern features. #RealEstate #DreamHome",
                            'basic': "Property image"
                        }
                    
                    social_posts = {}
                    platforms = ['instagram', 'facebook', 'twitter', 'linkedin']
                    
                    for platform in platforms:
                        try:
                            post_data = social_generator.generate_post(
                                descriptions.get('luxury', 'Beautiful property'), 
                                uploaded_file.name, 
                                platform
                            )
                            social_posts[platform] = post_data
                        except Exception as e:
                            st.warning(f"Social media generation failed for {platform}: {str(e)}")
                            social_posts[platform] = {
                                'content': f"🏡 Beautiful property! Contact us for details. #RealEstate",
                                'platform': platform,
                                'error': str(e)
                            }
                    
                    results[uploaded_file.name] = {
                        'original_path': original_path,
                        'processed_path': processed_path,
                        'processing_metadata': processing_metadata,
                        'descriptions': descriptions,
                        'social_posts': social_posts,
                        'processing_time': datetime.now().isoformat(),
                        'enhancement_level': enhancement_level,
                        'file_size_reduction': processing_metadata.get('compression_ratio', 'N/A'),
                        'status': 'success'
                    }
                    
                except Exception as e:
                    st.error(f"Failed to process {uploaded_file.name}: {str(e)}")
                    results[uploaded_file.name] = {
                        'original_path': original_path if 'original_path' in locals() else None,
                        'processed_path': None,
                        'descriptions': {'error': str(e)},
                        'social_posts': {'error': str(e)},
                        'processing_time': datetime.now().isoformat(),
                        'status': 'error',
                        'error_message': str(e)
                    }
                
                progress_bar.progress((idx + 1) / total_files)
            
            successful_count = sum(1 for r in results.values() if r.get('status') == 'success')
            st.session_state.results = results
            st.session_state.processing_complete = True
            
            status_text.empty()
            
            if successful_count == total_files:
                st.markdown(f"""
                <div class="container mt-4">
                    <div class="row">
                        <div class="col-12">
                            <div class="alert alert-success d-flex align-items-center" role="alert">
                                <i class="bi bi-check-circle-fill me-2"></i>
                                <div>
                                    <strong>Processing Complete!</strong><br>
                                    Successfully processed all {total_files} images with AI enhancement, 
                                    description generation, and social media content creation!
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                failed_count = total_files - successful_count
                st.markdown(f"""
                <div class="container mt-4">
                    <div class="row">
                        <div class="col-12">
                            <div class="alert alert-warning d-flex align-items-center" role="alert">
                                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                                <div>
                                    <strong>Partial Success</strong><br>
                                    Processed {successful_count}/{total_files} images successfully. 
                                    {failed_count} files had processing errors.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Critical processing error: {str(e)}")
        st.markdown("""
        <div class="container mt-4">
            <div class="row">
                <div class="col-12">
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        <i class="bi bi-x-circle-fill me-2"></i>
                        <div>
                            <strong>Processing Failed</strong><br>
                            Please check your images and try again. If the problem persists, 
                            contact support.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_results_section():
    if not st.session_state.processing_complete:
        return
    
    st.markdown("""
    <div class="container mb-5">
        <div class="row">
            <div class="col-12">
                <div class="card gradient-success shadow-lg rounded-4 border-0">
                    <div class="card-body text-center p-5">
                        <h2 class="card-title text-white fw-bold mb-3">
                            <i class="bi bi-trophy-fill me-3"></i> Results Dashboard
                        </h2>
                        <p class="text-white fs-5 mb-0">Your processed images and generated content are ready!</p>
                        <div class="row mt-4">
                            <div class="col-md-4">
                                <div class="text-white">
                                    <i class="bi bi-images fs-1"></i>
                                    <div class="fw-bold">Enhanced Images</div>
                                    <small>Professional quality processing</small>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="text-white">
                                    <i class="bi bi-robot fs-1"></i>
                                    <div class="fw-bold">AI Descriptions</div>
                                    <small>Multiple target audiences</small>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="text-white">
                                    <i class="bi bi-share-fill fs-1"></i>
                                    <div class="fw-bold">Social Content</div>
                                    <small>Ready for all platforms</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs([
        "📸 Before/After Gallery", 
        "📝 AI Descriptions", 
        "🌐 Social Media Content"
    ])
    
    with tab1:
        create_gallery_view()
    
    with tab2:
        create_descriptions_view()
    
    with tab3:
        create_social_view()

def create_gallery_view():
    for filename, result in st.session_state.results.items():
        if result.get('status') == 'error':
            st.markdown(f"""
            <div class="container mb-4">
                <div class="row">
                    <div class="col-12">
                        <div class="alert alert-danger d-flex align-items-center" role="alert">
                            <i class="bi bi-x-circle-fill me-2"></i>
                            <div>
                                <strong>Failed to process {filename}</strong><br>
                                {result.get('error_message', 'Unknown error occurred')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            continue
        
        processing_metadata = result.get('processing_metadata', {})
        
        st.markdown(f"""
        <div class="container mb-5">
            <div class="row">
                <div class="col-12">
                    <div class="card shadow-lg rounded-4 border-0">
                        <div class="card-header gradient-success py-3">
                            <h5 class="mb-0 text-white fw-bold">
                                <i class="bi bi-image-fill me-2"></i> Enhanced Gallery: {filename}
                            </h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original Image")
            if result.get('original_path') and os.path.exists(result['original_path']):
                original_img = Image.open(result['original_path'])
                st.image(original_img, width='stretch')
                
                original_size = os.path.getsize(result['original_path'])
                st.markdown(f"""
                <div class="card bg-light">
                    <div class="card-body p-2">
                        <small>
                            <strong>Original:</strong> {original_img.size[0]}×{original_img.size[1]} | 
                            {original_size / (1024*1024):.1f} MB
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Enhanced Image")
            if result.get('processed_path') and os.path.exists(result['processed_path']):
                processed_img = Image.open(result['processed_path'])
                st.image(processed_img, width='stretch')
                
                processed_size = os.path.getsize(result['processed_path'])
                compression_ratio = processing_metadata.get('compression_ratio', 'N/A')
                
                st.markdown(f"""
                <div class="card bg-success text-white">
                    <div class="card-body p-2">
                        <small>
                            <strong>Enhanced:</strong> {processed_img.size[0]}×{processed_img.size[1]} | 
                            {processed_size / (1024*1024):.1f} MB | 
                            {compression_ratio} savings
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with open(result['processed_path'], "rb") as file:
                    btn = st.download_button(
                        label="💾 Download Enhanced Image",
                        data=file.read(),
                        file_name=f"enhanced_{filename}",
                        mime="image/jpeg",
                        width='stretch'
                    )
        
        if processing_metadata:
            st.markdown("### 📊 Processing Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Enhancement Level", 
                    result.get('enhancement_level', 'N/A').title(),
                    delta=None
                )
            
            with col2:
                quality = processing_metadata.get('quality_setting', 'N/A')
                st.metric("JPEG Quality", f"{quality}%", delta=None)
            
            with col3:
                original_dims = processing_metadata.get('original_dimensions', (0, 0))
                final_dims = processing_metadata.get('final_dimensions', (0, 0))
                if original_dims != final_dims:
                    st.metric("Resolution", f"{final_dims[0]}×{final_dims[1]}", delta="Optimized")
                else:
                    st.metric("Resolution", f"{final_dims[0]}×{final_dims[1]}", delta=None)
            
            with col4:
                compression = processing_metadata.get('compression_ratio', 'N/A')
                if compression != 'N/A' and compression.endswith('%'):
                    compression_val = compression.replace('%', '')
                    st.metric("File Size Reduction", compression, delta=f"-{compression_val}%")
                else:
                    st.metric("File Size Reduction", compression, delta=None)

def create_descriptions_view():
    for filename, result in st.session_state.results.items():
        if result.get('status') == 'error':
            st.markdown(f"""
            <div class="container mb-4">
                <div class="row">
                    <div class="col-12">
                        <div class="alert alert-danger d-flex align-items-center" role="alert">
                            <i class="bi bi-x-circle-fill me-2"></i>
                            <div>
                                <strong>Error processing {filename}</strong><br>
                                {result.get('error_message', 'Unknown error occurred')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            continue
        
        descriptions = result.get('descriptions', {})
        
        st.markdown(f"""
        <div class="container mb-4">
            <div class="row">
                <div class="col-12">
                    <div class="card shadow-lg rounded-4 border-0">
                        <div class="card-header gradient-info py-3">
                            <h5 class="mb-0 text-white fw-bold">
                                <i class="bi bi-chat-text-fill me-2"></i> AI-Generated Descriptions for {filename}
                            </h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "💎 Luxury", "👨‍👩‍👧‍👦 Family", "💰 Investment", "📱 Social Media"
        ])
        
        with tab1:
            luxury_desc = descriptions.get('luxury', 'No luxury description available')
            escaped_luxury = luxury_desc.replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <div class="card gradient-warning shadow-lg rounded-4 border-0 mb-3">
                <div class="card-body p-4">
                    <h6 class="card-title text-white fw-bold mb-3">
                        <i class="bi bi-gem me-2"></i> Luxury Market Description
                    </h6>
                    <p class="card-text text-white fs-6 lh-base">{luxury_desc}</p>
                    <div class="d-flex justify-content-end mt-3">
                        <button class="btn btn-light btn-sm" onclick="navigator.clipboard.writeText('{escaped_luxury}')">
                            <i class="bi bi-clipboard me-1"></i> Copy
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            family_desc = descriptions.get('family', 'No family description available')
            escaped_family = family_desc.replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <div class="card bg-success shadow-lg rounded-4 border-0 mb-3">
                <div class="card-body p-4">
                    <h6 class="card-title text-white fw-bold mb-3">
                        <i class="bi bi-house-heart-fill me-2"></i> Family-Friendly Description
                    </h6>
                    <p class="card-text text-white fs-6 lh-base">{family_desc}</p>
                    <div class="d-flex justify-content-end mt-3">
                        <button class="btn btn-light btn-sm" onclick="navigator.clipboard.writeText('{escaped_family}')">
                            <i class="bi bi-clipboard me-1"></i> Copy
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            investment_desc = descriptions.get('investment', 'No investment description available')
            escaped_investment = investment_desc.replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <div class="card bg-primary shadow-lg rounded-4 border-0 mb-3">
                <div class="card-body p-4">
                    <h6 class="card-title text-white fw-bold mb-3">
                        <i class="bi bi-graph-up-arrow me-2"></i> Investment Opportunity
                    </h6>
                    <p class="card-text text-white fs-6 lh-base">{investment_desc}</p>
                    <div class="d-flex justify-content-end mt-3">
                        <button class="btn btn-light btn-sm" onclick="navigator.clipboard.writeText('{escaped_investment}')">
                            <i class="bi bi-clipboard me-1"></i> Copy
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tab4:
            social_desc = descriptions.get('social', 'No social media description available')
            escaped_social = social_desc.replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <div class="card bg-info shadow-lg rounded-4 border-0 mb-3">
                <div class="card-body p-4">
                    <h6 class="card-title text-white fw-bold mb-3">
                        <i class="bi bi-share-fill me-2"></i> Social Media Ready
                    </h6>
                    <p class="card-text text-white fs-6 lh-base">{social_desc}</p>
                    <div class="d-flex justify-content-end mt-3">
                        <button class="btn btn-light btn-sm" onclick="navigator.clipboard.writeText('{escaped_social}')">
                            <i class="bi bi-clipboard me-1"></i> Copy
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_social_view():
    for filename, result in st.session_state.results.items():
        if result.get('status') == 'error':
            continue
            
        st.markdown(f"""
        <div class="container mb-4">
            <div class="row">
                <div class="col-12">
                    <h4 class="text-gradient">
                        <i class="bi bi-share"></i> Social Media Content for {filename}
                    </h4>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        social_posts = result.get('social_posts', {})
        
        platform_configs = {
            'instagram': {'color': '#E4405F', 'icon': 'instagram', 'name': 'Instagram'},
            'facebook': {'color': '#1877F2', 'icon': 'facebook', 'name': 'Facebook'}, 
            'twitter': {'color': '#1DA1F2', 'icon': 'twitter', 'name': 'Twitter'},
            'linkedin': {'color': '#0A66C2', 'icon': 'linkedin', 'name': 'LinkedIn'}
        }
        
        cols = st.columns(2)
        
        for idx, (platform, post_data) in enumerate(social_posts.items()):
            col = cols[idx % 2]
            
            if platform in platform_configs:
                config = platform_configs[platform]
                
                with col:
                    if isinstance(post_data, dict):
                        content = post_data.get('content', 'No content available')
                        engagement = post_data.get('estimated_engagement', 'N/A')
                        char_count = post_data.get('character_count', len(content))
                        
                        engagement_color = {
                            'High': 'success',
                            'Medium-High': 'warning', 
                            'Medium': 'info',
                            'Low-Medium': 'secondary'
                        }.get(engagement, 'secondary')
                        
                        escaped_content = content.replace("'", "\\'").replace('"', '\\"')
                        
                        st.markdown(f"""
                        <div class="card shadow-sm rounded-3 mb-3">
                            <div class="card-header d-flex justify-content-between align-items-center" 
                                 style="background-color: {config['color']}; color: white;">
                                <div>
                                    <i class="bi bi-{config['icon']}"></i> {config['name']}
                                </div>
                                <div>
                                    <span class="badge bg-light text-dark">{char_count} chars</span>
                                </div>
                            </div>
                            <div class="card-body">
                                <div class="mb-3">
                                    <p class="card-text">{content}</p>
                                </div>
                                <div class="d-flex justify-content-between align-items-center">
                                    <span class="badge bg-{engagement_color}">
                                        📊 {engagement} Engagement
                                    </span>
                                    <button class="btn btn-outline-primary btn-sm" onclick="navigator.clipboard.writeText('{escaped_content}')">
                                        <i class="bi bi-clipboard"></i> Copy
                                    </button>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        content = str(post_data) if post_data else 'No content available'
                        escaped_content = content.replace("'", "\\'").replace('"', '\\"')
                        
                        st.markdown(f"""
                        <div class="card shadow-sm rounded-3 mb-3">
                            <div class="card-header" style="background-color: {config['color']}; color: white;">
                                <h6 class="mb-0"><i class="bi bi-{config['icon']}"></i> {config['name']}</h6>
                            </div>
                            <div class="card-body">
                                <p class="card-text">{content}</p>
                                <button class="btn btn-outline-primary btn-sm" onclick="navigator.clipboard.writeText('{escaped_content}')">
                                    <i class="bi bi-clipboard"></i> Copy
                                </button>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

def create_sidebar():
    """Bootstrap-styled sidebar with live settings"""
    st.sidebar.markdown("""
    <div class="text-center mb-4">
        <h3 class="text-gradient">⚙️ Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### Image Processing")
    quality = st.sidebar.slider("Image Quality", 60, 100, 85, key="quality_slider")
    enhancement = st.sidebar.selectbox("Enhancement Level", ["light", "medium", "strong"], index=1, key="enhancement_select")
    
    st.session_state.user_preferences['image_quality'] = quality
    st.session_state.user_preferences['enhancement_level'] = enhancement
    
    st.sidebar.markdown(f"""
    <div class="alert alert-info">
        <small>
            <strong>Active Settings:</strong><br>
            Quality: {quality}% {"🔄" if quality != 85 else "✅"}<br>
            Enhancement: {enhancement.title()} {"🔄" if enhancement != "medium" else "✅"}
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a clear cache button for debugging
    if st.sidebar.button("Apply New Settings", help="Click after changing settings to ensure they're applied"):
        st.session_state.processing_complete = False
        st.rerun()
    
    # Platform stats
    st.sidebar.markdown("### Supported Platforms")

# Main App
def main():
    # Initialize session state
    init_session_state()
    
    create_sidebar()
    
    create_hero_header()
    
    uploaded_files = create_upload_section()
    
    if uploaded_files:
        create_processing_section()
    
    if st.session_state.processing_complete:
        create_results_section()
    
if __name__ == "__main__":
    main()