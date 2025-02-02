# Tsync2 Dataset Structure

## Directory Layout

```plaintext
Tsync2/
├── wrd_ph/                     # Text transcriptions
│   ├── tsync2_noon_0_250.txt        
│   │   
│   └── ...
├── wav/                        # Audio files at different sampling rates (16/32/48 kHz)
    ├── tsync2_noon_0_250.wav                
    └── ...

```

## File Formats

### Text Files (*.txt)

- One utterance per file
- UTF-8 encoded plain text
- Contains the transcription text, transcription text with space, phonetic Representation
- Filename format: tsync2_noon_[Group]_[Number_in_group].txt

### Audio Files (*.wav)

- 44kHz sampling rate
- 16-bit PCM encoding
- Mono channel
- Filename format: tsync2_noon_[Group]_[Number_in_group].wav

## Naming Convention

- Files: tsync2_noon_[Group]_[Number_in_group].[extension]
  - Example: tsync2_noon_0_250.wav, tsync2_noon_0_250.txt