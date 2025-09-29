#!/bin/bash
# Main Launcher for Chatterbox TTS on M1 MacBook Air
# Created by Claude for Michael Koker

clear
echo "🍎 Chatterbox TTS for M1 MacBook Air"
echo "===================================="
echo ""
echo "What would you like to do?"
echo ""
echo "1) 🔧 Install/Setup Chatterbox (first time setup)"
echo "2) 🧪 Run basic examples"
echo "3) 🎭 Try voice cloning"
echo "4) 🌐 Start web server"
echo "5) 📊 Check system status"
echo "6) 🔧 Fix PyTorch issues (torchvision::nms error)"
echo "7) 🧹 Clean up / Reset"
echo "8) ❓ Help"
echo "9) 🚪 Exit"
echo ""

read -p "Enter your choice (1-9): " choice

case $choice in
    1)
        echo ""
        echo "🔧 Starting installation..."
        chmod +x setup_m1.sh
        ./setup_m1.sh
        ;;
    2)
        echo ""
        echo "🧪 Running basic examples..."
        chmod +x run_example.sh
        ./run_example.sh
        ;;
    3)
        echo ""
        echo "🎭 Running voice cloning examples..."
        chmod +x run_voice_cloning.sh
        ./run_voice_cloning.sh
        ;;
    4)
        echo ""
        echo "🌐 Starting web server..."
        echo "💡 Open http://localhost:8000 in your browser after it starts"
        chmod +x start_server.sh
        ./start_server.sh
        ;;
    5)
        echo ""
        echo "📊 System Status Check"
        echo "====================="
        
        # Check conda environment
        if conda env list | grep -q "chatterbox"; then
            echo "✅ Conda environment: Found"
        else
            echo "❌ Conda environment: Not found"
        fi
        
        # Check if in conda environment
        if [[ "$CONDA_DEFAULT_ENV" == "chatterbox" ]]; then
            echo "✅ Currently in chatterbox environment"
            
            # Check Python packages
            python -c "
try:
    import torch
    print('✅ PyTorch:', torch.__version__)
    print('✅ MPS available:', torch.backends.mps.is_available())
except ImportError:
    print('❌ PyTorch not found')

try:
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS: Available')
except ImportError:
    print('❌ Chatterbox TTS: Not installed')

try:
    import fastapi
    print('✅ FastAPI: Available')
except ImportError:
    print('❌ FastAPI: Not installed')

import psutil
memory = psutil.virtual_memory()
print(f'💾 Available memory: {memory.available / 1024**3:.1f} GB')
print(f'🔥 CPU usage: {psutil.cpu_percent()}%')
            "
        else
            echo "⚠️  Not in chatterbox environment"
            echo "💡 Run: conda activate chatterbox"
        fi
        
        # Check reference audio
        ref_files=$(ls reference_audio/*.wav reference_audio/*.mp3 2>/dev/null | wc -l)
        if [ $ref_files -gt 0 ]; then
            echo "✅ Reference audio files: $ref_files found"
        else
            echo "ℹ️  Reference audio files: None (add to reference_audio/ for voice cloning)"
        fi
        
        echo ""
        read -p "Press Enter to continue..."
        ./launch.sh
        ;;
    6)
        echo ""
        echo "🔧 Fixing PyTorch Issues"
        echo "========================"
        echo "This will fix the 'operator torchvision::nms does not exist' error"
        echo ""
        echo "Choose fix method:"
        echo "1) Quick fix (recommended)"
        echo "2) Alternative fix"
        echo "3) View manual instructions"
        echo "4) Back to main menu"
        echo ""
        read -p "Enter choice (1-4): " pytorch_choice
        
        case $pytorch_choice in
            1)
                echo "🔧 Running quick PyTorch fix..."
                chmod +x fix_pytorch.sh
                ./fix_pytorch.sh
                ;;
            2)
                echo "🔄 Running alternative PyTorch fix..."
                chmod +x fix_pytorch_alternative.sh
                ./fix_pytorch_alternative.sh
                ;;
            3)
                echo "📜 Opening manual fix instructions..."
                if command -v cat &> /dev/null; then
                    cat PYTORCH_FIX.md
                else
                    echo "Please open PYTORCH_FIX.md file for manual instructions"
                fi
                ;;
            4)
                ./launch.sh
                ;;
        esac
        echo ""
        read -p "Press Enter to continue..."
        ./launch.sh
        ;;
    7)
        echo ""
        echo "🧹 Cleanup Options"
        echo "=================="
        echo "1) Clear model cache (free memory)"
        echo "2) Remove conda environment"
        echo "3) Clean output files"
        echo "4) Back to main menu"
        echo ""
        read -p "Enter choice (1-4): " clean_choice
        
        case $clean_choice in
            1)
                echo "🧹 Clearing model cache..."
                if command -v curl &> /dev/null; then
                    curl -X POST http://localhost:8000/clear_cache 2>/dev/null || echo "Server not running"
                fi
                echo "✅ Cache clear attempted"
                ;;
            2)
                echo "⚠️  This will remove the entire chatterbox environment!"
                read -p "Are you sure? (y/N): " confirm
                if [[ $confirm == [Yy] ]]; then
                    conda env remove -n chatterbox
                    echo "✅ Environment removed"
                fi
                ;;
            3)
                read -p "Remove all generated audio files? (y/N): " confirm
                if [[ $confirm == [Yy] ]]; then
                    rm -f outputs/*.wav outputs/*.mp3
                    echo "✅ Output files cleaned"
                fi
                ;;
            4)
                ./launch.sh
                ;;
        esac
        ;;
    8)
        echo ""
        echo "❓ Chatterbox TTS Help"
        echo "===================="
        echo ""
        echo "📋 Quick Start:"
        echo "   1. Run option 1 to install everything"
        echo "   2. Try option 2 for basic examples"
        echo "   3. Use option 4 for the web interface"
        echo ""
        echo "🎭 Voice Cloning:"
        echo "   1. Record 10-30 seconds of voice"
        echo "   2. Save as .wav in reference_audio/ folder"
        echo "   3. Run option 3 for voice cloning"
        echo ""
        echo "🌐 Web Interface:"
        echo "   • Start server with option 4"
        echo "   • Open http://localhost:8000"
        echo "   • Upload audio for voice cloning"
        echo "   • Adjust settings and generate"
        echo ""
        echo "🔧 Performance Tips:"
        echo "   • Keep MacBook plugged in"
        echo "   • Close other memory-heavy apps"
        echo "   • Use shorter texts for faster generation"
        echo ""
        echo "📁 Project Structure:"
        echo "   • examples/ - Python example scripts"
        echo "   • reference_audio/ - Voice samples for cloning"
        echo "   • outputs/ - Generated audio files"
        echo "   • static/ - Web interface files"
        echo ""
        echo "🆘 Troubleshooting:"
        echo "   • If MPS fails, it falls back to CPU"
        echo "   • Check system status with option 5"
        echo "   • Restart if memory usage grows too high"
        echo ""
        read -p "Press Enter to continue..."
        ./launch.sh
        ;;
    9)
        echo ""
        echo "👋 Thanks for using Chatterbox TTS!"
        echo "🎙️ Happy voice synthesis!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please try again."
        sleep 2
        ./launch.sh
        ;;
esac