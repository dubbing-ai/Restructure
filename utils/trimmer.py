#!/usr/bin/env python3
import os
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import detect_leading_silence
import argparse
from tqdm import tqdm
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def trim_silence(audio):
    """
    Trim silence from the beginning and end of an audio segment.
    
    Args:
        audio (AudioSegment): The audio segment to trim
        
    Returns:
        AudioSegment: Trimmed audio segment
    """
    def detect_trailing_silence(audio_segment):
        return detect_leading_silence(audio_segment.reverse())

    start_trim = detect_leading_silence(audio)
    end_trim = detect_trailing_silence(audio)

    duration = len(audio)
    trimmed_audio = audio[start_trim:duration-end_trim]
    return trimmed_audio

def process_audio_file(args):
    """
    Process a single audio file by trimming silence and saving in specified format.
    
    Args:
        args (tuple): Tuple containing (input_path, output_path, output_format)
    Returns:
        bool: True if processing was successful, False otherwise
    """
    input_path, output_path, output_format = args
    try:
        # Load audio file (pydub can handle various formats)
        audio = AudioSegment.from_file(str(input_path))
        
        # Trim silence
        trimmed_audio = trim_silence(audio)
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Export in specified format
        trimmed_audio.export(str(output_path), format=output_format)
        return True
        
    except Exception as e:
        tqdm.write(f"Error processing {input_path}: {str(e)}")
        return False

def process_directory(input_dir, output_format='wav', num_threads=None):
    """
    Process all audio files in a directory recursively using multiple threads.
    
    Args:
        input_dir (str): Path to input directory
        output_format (str): Output audio format ('wav' or 'flac')
        num_threads (int, optional): Number of threads to use. Defaults to CPU count.
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise ValueError(f"Input directory does not exist: {input_dir}")
    
    # Create output directory name by appending '_silence_trimmed'
    output_base = input_path.parent / f"{input_path.name}_silence_trimmed"
    
    # Clean output directory if it exists
    if output_base.exists():
        print("Clearing existing output directory...")
        shutil.rmtree(output_base)
    
    # Supported audio formats
    audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.wma'}
    
    # First, collect all audio files
    audio_files = [f for f in input_path.rglob('*') if f.suffix.lower() in audio_extensions]
    
    # Prepare work items
    work_items = []
    for audio_file in audio_files:
        rel_path = audio_file.relative_to(input_path)
        output_path = output_base / rel_path.with_suffix(f'.{output_format}')
        work_items.append((audio_file, output_path, output_format))
    
    # Initialize counters
    successful = 0
    failed = 0
    
    # Use CPU count if num_threads not specified
    if num_threads is None:
        num_threads = multiprocessing.cpu_count()
    
    # Process files using thread pool
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_audio_file, item): item[0] 
            for item in work_items
        }
        
        # Process results with progress bar
        with tqdm(total=len(work_items), desc=f"Processing files ({num_threads} threads)", unit="file") as pbar:
            for future in as_completed(future_to_file):
                if future.result():
                    successful += 1
                else:
                    failed += 1
                pbar.update(1)
    
    return successful, failed

def main():
    parser = argparse.ArgumentParser(description='Trim silence from audio files in a directory.')
    parser.add_argument('input_dir', help='Input directory containing audio files')
    parser.add_argument('--format', choices=['wav', 'flac'], default='wav',
                      help='Output audio format (default: wav)')
    parser.add_argument('--threads', type=int, help='Number of threads to use (default: CPU count)')
    args = parser.parse_args()
    
    try:
        successful, failed = process_directory(args.input_dir, args.format, args.threads)
        tqdm.write(f"\nProcessing completed!")
        tqdm.write(f"Successfully processed: {successful} files")
        if failed > 0:
            tqdm.write(f"Failed to process: {failed} files")
        return 0 if failed == 0 else 1
    
    except Exception as e:
        tqdm.write(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())