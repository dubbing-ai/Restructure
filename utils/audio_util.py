from pathlib import Path
from tqdm import tqdm
import subprocess
import numpy as np
import os

import torch
import torchaudio

from pydub import AudioSegment

from speechbrain.pretrained import SepformerSeparation as separator

from TTS.bin.resample import resample_files
from TTS.utils.vad import get_vad_model_and_utils, remove_silence

def validate_wav_files(directory_path):
    """
    Ensure all WAV files in a directory are valid by re-encoding them with pcm_mulaw.
    
    Args:
        directory_path (str): Path to directory containing WAV files
        
    Returns:
        int: Number of processed files
    """
    # Convert to Path object
    directory = Path(directory_path)
    
    # Find all .wav files recursively
    wav_files = list(directory.glob("**/*.wav"))
    
    print(f"Found {len(wav_files)} WAV files to validate")
    
    # Process each file
    processed_count = 0
    for wav_file in tqdm(wav_files, desc="Validating WAV files"):
        try:
            # Create temporary filename
            temp_file = wav_file.with_suffix(".tmp.wav")
            
            # Run ffmpeg to convert to pcm_mulaw
            subprocess.run([
                "ffmpeg", 
                "-i", str(wav_file), 
                "-c:a", "pcm_mulaw", 
                str(temp_file),
                "-y"  # Overwrite if exists
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Replace original with the temp file
            temp_file.replace(wav_file)
            
            processed_count += 1
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing {wav_file}: {e}")
        except Exception as e:
            print(f"Unexpected error with {wav_file}: {e}")
    
    print(f"Successfully validated {processed_count} WAV files")
    return processed_count

def convert_wav_to_flac(src_path: str, dst_path: str) -> bool:
    """
    Convert WAV file to FLAC format.
    
    Args:
        src_path: Source WAV file path
        dst_path: Destination FLAC file path
        
    Returns:
        bool: True if conversion successful, False otherwise
        
    Example:
        success = convert_wav_to_flac("input.wav", "output.flac")
    """
    try:
        # Ensure source file exists
        if not os.path.isfile(src_path):
            print(f"Source file not found: {src_path}")
            return False
        
        # Construct FFmpeg command for direct conversion with no processing
        # -c:a flac = use FLAC codec
        # -ac 1 = mono audio
        # -compression_level 0 = no compression
        # -y = overwrite output file if it exists
        command = [
            "ffmpeg",
            "-i", src_path,
            "-c:a", "flac",
            "-ac", "1",
            "-compression_level", "0",
            "-y",
            dst_path
        ]
        
        # Execute FFmpeg command and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Check if process was successful
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error converting {src_path}: {str(e)}")
        return False

def convert_mp3_to_flac(src_path: str, dst_path: str) -> bool:
    """
    Convert MP3 file to FLAC format using FFmpeg
    
    Args:
        src_path: Source MP3 file path
        dst_path: Destination FLAC file path
    
    Returns:
        bool: True if conversion successful, False otherwise

    Example:
        success = convert_mp3_to_flac("input.mp3", "output.flac")
    """
    try:
        # Ensure source file exists
        if not os.path.isfile(src_path):
            print(f"Source file not found: {src_path}")
            return False
        
        # Construct FFmpeg command
        # -c:a flac = use FLAC codec
        # -ac 1 = mono audio
        # -compression_level 0 = no compression
        # -y = overwrite output file if it exists
        command = [
            "ffmpeg",
            "-i", src_path,
            "-c:a", "flac",
            "-ac", "1",
            "-compression_level", "0",
            "-y",
            dst_path
        ]

        # Execute FFmpeg command and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if process was successful
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
        return True

    except Exception as e:
        print(f"Error converting {src_path}: {str(e)}")
        return False

def convert_mp3_to_wav(src_path: str, dst_path: str) -> bool:
    """
    Convert MP3 file to WAV format using pydub
    
    Args:
        src_path: Source MP3 file path
        dst_path: Destination WAV file path
    
    Returns:
        bool: True if conversion successful, False otherwise

    Example:
        success = convert_mp3_to_wav("input.mp3", "output.wav")
    """
    try:
        # Ensure source file exists
        if not os.path.isfile(src_path):
            print(f"Source file not found: {src_path}")
            return False
        
        # Construct FFmpeg command
        # -ac 1 = mono audio
        command = [
            "ffmpeg",
            "-i", src_path,
            "-ac", "1",
            "-y",
            dst_path
        ]

        # Execute FFmpeg command and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if process was successful
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error converting {src_path}: {e}")
        return False

def resample_audios(input_folders: str, file_ext: str, sample_rate: float = 16000, n_jobs: int = 4):
    """
    Resample audio files to specified sample rate.
    
    Args:
        input_folders: Path to input directory
        file_ext: File extension to process (e.g., 'flac', 'wav')
        sample_rate: Target sample rate in Hz (default: 16000)
        n_jobs: Number of parallel jobs (default: 4)
        
    Example:
        resample_audios("path/to/audio", "wav", sample_rate=22050, n_jobs=8)
    """
    resample_files(input_folders, sample_rate, file_ext=file_ext, n_jobs=n_jobs)

def trim_silence_with_vad(input_folder: str, file_extension: str, model_and_utils=None):
    """
    Trim silence from audio files using Voice Activity Detection.
    
    Args:
        input_folder: Path to input directory
        file_extension: File extension to process (e.g., 'flac', 'wav')
        model_and_utils: Optional pre-loaded VAD model and utilities
        
    Returns:
        List of paths where no speech was detected

    Example:
        trim_silence_with_vad("path/to/audio", "flac")
    """
    input_folder = Path(input_folder)
    
    # Load VAD model if not provided
    if model_and_utils is None:
        model_and_utils = get_vad_model_and_utils(
            use_cuda=torch.cuda.is_available(), 
            use_onnx=False
        )
    
    # Get all matching files recursively
    audio_files = list(input_folder.glob(f'**/*.{file_extension}'))
    total_files = len(audio_files)
    print(f"Found {total_files} .{file_extension} files to process")
    
    # Track files with no speech
    no_speech_files = []
    
    for input_path in tqdm(audio_files, desc="Processing files"):
        # Preserve directory structure
        relative_path = input_path.relative_to(input_folder)
        output_path = input_folder / relative_path
        
        # Create subdirectories
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            output_path, is_speech = remove_silence(
                model_and_utils,
                str(input_path),
                str(output_path),
                trim_just_beginning_and_end=True,
                use_cuda=torch.cuda.is_available()
            )
            if not is_speech:
                no_speech_files.append(str(output_path))
        except Exception as e:
            print(f"Error processing {relative_path}: {str(e)}")
    
    print("\nProcessing complete")
    
    # Write list of files with no speech
    if no_speech_files:
        log_path = input_folder.parent / "no_speech_files.txt"
        with open(log_path, "w", encoding="utf-8") as f:
            for file in no_speech_files:
                f.write(f"{file}\n")
        print(f"\nFound {len(no_speech_files)} files with no speech. List saved to {log_path}")

def normalize_audio_files(input_dir, extensions="flac,wav", target_db=-27, sample_rate=16000):
    """
    Normalize audio files using ffmpeg-normalize with RMS normalization.
    Supports both FLAC and WAV formats.
    
    Args:
        input_dir (str): Path to input directory
        extensions (str): Comma-separated extensions (e.g., "flac,wav")
        target_db (float): Target RMS level in dB
        sample_rate (int): Output sample rate in Hz
    """
    input_dir = Path(input_dir)
    
    # Process extensions string
    extensions_list = [f".{ext.strip().lstrip('.')}" for ext in extensions.split(',')]
    
    # Find all audio files
    audio_files = []
    for ext in extensions_list:
        audio_files.extend(list(input_dir.rglob(f"*{ext}")))
    
    for audio_file in tqdm(audio_files, desc="Normalizing audio files"):
        try:
            # Determine codec based on extension
            output_ext = audio_file.suffix.lower()
            codec = "flac" if output_ext == ".flac" else "pcm_s16le"
            
            cmd = [
                "ffmpeg-normalize",
                str(audio_file),
                "-nt", "rms",            # RMS normalization
                "-t", str(target_db),    # Target RMS level
                "-o", str(audio_file),   # Output to same file
                "-ar", str(sample_rate), # Set sample rate
                "-f",                    # Force overwrite
                "-ext", output_ext.lstrip('.'),  # Keep original extension
                "-c:a", codec,          # Codec based on format
                "--progress"             # Show progress
            ]
            
            # Run ffmpeg-normalize
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing {audio_file}: {e}")
            continue

def init_enhancement_model(model_path="speechbrain/sepformer-wham16k-enhancement", savedir='pretrained_models/sepformer-wham16k-enhancement'):
    """
    Initialize the SpeechBrain SepformerSeparation model for audio enhancement.
    
    Args:
        model_path (str): Path to the model or HuggingFace model identifier
        savedir (str): Directory to save the downloaded model
        
    Returns:
        model: Initialized SepformerSeparation model
    """
    print("Loading SepformerSeparation model...")
    model = separator.from_hparams(
        source=model_path, 
        savedir=savedir,
        run_opts={"device":"cuda"}
    )
    return model

def enhance_audio_directory(
    input_dir, 
    enhancement_model=None,
    extensions=["wav", "flac", "mp3"], 
    recursive=True, 
    sample_rate=16000
):
    """
    Enhance all audio files in a directory using SpeechBrain's SepformerSeparation model,
    replacing the original files with enhanced versions.
    
    Args:
        input_dir (str): Path to directory containing audio files
        enhancement_model: Pre-initialized SepformerSeparation model (will initialize if None)
        extensions (list, optional): List of audio file extensions to process
        recursive (bool, optional): Whether to process subdirectories
        sample_rate (int, optional): Sample rate for the output audio files
        
    Returns:
        list: Paths to enhanced audio files
    """
    # Convert input_dir to Path object
    input_dir = Path(input_dir)
    
    # Initialize model if not provided
    model_initialized_internally = False
    if enhancement_model is None:
        enhancement_model = init_enhancement_model()
        model_initialized_internally = True
    
    # Find all audio files
    audio_files = []
    for ext in extensions:
        if recursive:
            audio_files.extend(list(input_dir.rglob(f"*.{ext}")))
        else:
            audio_files.extend(list(input_dir.glob(f"*.{ext}")))
    
    if not audio_files:
        print(f"No audio files found in {input_dir} with extensions {extensions}")
        return []
    
    print(f"Found {len(audio_files)} audio files to enhance")
    
    # Process each file
    enhanced_files = []
    for audio_file in tqdm(audio_files, desc="Enhancing audio files"):
        try:
            # Create a temporary path for the enhanced file
            temp_enhanced_path = audio_file.with_suffix(".enhanced.wav")
            
            # Enhance audio file
            est_sources = enhancement_model.separate_file(str(audio_file))
            
            # Save enhanced audio to temporary file
            torchaudio.save(
                str(temp_enhanced_path),
                est_sources[:, :, 0].detach().cpu(),
                sample_rate
            )
            
            # Replace original file with enhanced version
            temp_enhanced_path.replace(audio_file)
            
            enhanced_files.append(str(audio_file))
            
        except Exception as e:
            print(f"Error enhancing {audio_file}: {str(e)}")
    
    print(f"\nEnhancement complete. Enhanced {len(enhanced_files)} files.")
    return enhanced_files