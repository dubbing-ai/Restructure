from pathlib import Path
from tqdm import tqdm
import torch
from pydub import AudioSegment

from TTS.bin.resample import resample_files
from TTS.utils.vad import get_vad_model_and_utils, remove_silence

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
        # Load WAV file
        audio = AudioSegment.from_file(src_path, format="wav")
        
        # Export as FLAC"
        audio.export(
            dst_path,
            format="flac",
            parameters=[
                "-ac", "1",  # mono audio
                "-ar", "32000",  # 32kHz sample rate
                "-compression_level", "8"  # highest compression
            ]
        )
    except Exception as e:
        print(f"Error converting {src_path}: {str(e)}")
        return False
    return True

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