# GigaSpeech Dataset Structure (Processed)

## Dataset Splits

The dataset is organized into three primary splits:

- **Train**: divided into subsets: XS, S, M, L, XL
- **Validation**: 6,750 samples
- **Test**: 25,619 samples

## Features

Each dataset entry contains the following fields:

| Feature             | Description |
|---------------------|-------------|
| `segment_id`       | Unique identifier for the audio segment |
| `speaker`          | Speaker ID associated with the segment |
| `text`             | Transcribed text of the audio |
| `audio`            | Audio file data |
| `begin_time`       | Start time of the segment in the full audio file |
| `end_time`         | End time of the segment in the full audio file |
| `audio_id`         | Identifier of the original audio file |
| `title`            | Title of the source audio content |
| `url`              | URL of the original source |
| `source`           | Source name (e.g., podcast, audiobook, etc.) |
| `category`         | Category label (e.g., news, conversation, lecture, etc.) |
| `original_full_path` | Path to the original full-length audio |

## Directory Layout

```plaintext
GigaSpeech/
├── data/                     # Main dataset folder
│   ├── audio/                # Audio data
│   │   ├── dev_files/
│   │   ├── l_files_additional/
│   │   ├── m_files_additional/
│   │   ├── s_files_additional/
│   │   ├── test_files/
│   │   ├── xl_files_additional/
│   │   ├── xs_files/
│   ├── metadata/             # Metadata for different splits
│   │   ├── dev_metadata/
│   │   ├── l_metadata_additional/
│   │   ├── m_metadata_additional/
│   │   ├── s_metadata_additional/
│   │   ├── test_metadata/
│   │   ├── xl_metadata_additional/
│   │   ├── xs_metadata/
│   ├── dev_n_archives.txt
│   ├── l_n_archives_additional.txt
│   ├── m_n_archives_additional.txt
│   ├── s_n_archives_additional.txt
│   ├── test_n_archives.txt
│   ├── xl_n_archives_additional.txt
│   ├── xs_n_archives.txt
├── .gitattributes
├── README.md
├── gigaspeech.py
```