# LZMW Compression Algorithm

A Streamlit application that demonstrates the LZMW (Lempel-Ziv-Miller-Wegman) compression algorithm, a dictionary-based compression technique that extends LZW by adding more complex phrases to the dictionary.

## Overview

This application allows users to compress text using the LZMW algorithm, view compression statistics, explore the compression dictionary, and download compressed data. The app provides a practical demonstration of how dictionary-based compression works and its effectiveness on different types of text data.

## Features

- **Multiple Input Methods**: Enter text directly, upload a text file, or use sample texts
- **Compression Analysis**: View detailed compression statistics, including compression ratio and space saved
- **Dictionary Exploration**: Examine the generated compression dictionary
- **Data Validation**: Verify that decompression correctly restores the original text
- **Downloadable Results**: Save the compressed data to a file

## How to Use

1. **Choose an Input Method**:
   - Enter text directly in the text area
   - Upload a .txt file
   - Select from provided sample texts

2. **Compress the Data**:
   - Click the "Compress" button to process the input

3. **View Results**:
   - **Compression Results tab**:
     - See statistics (original size, compressed size, compression ratio, space saved)
     - Compare original and decompressed text
     - Download the compressed data

   - **Dictionary tab**:
     - Explore the complete compression dictionary
     - Filter to view initial or generated dictionary entries

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/lzmw-compression.git
cd lzmw-compression

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Requirements

- Python 3.6+
- Streamlit
- Pandas

## How LZMW Compression Works

LZMW (Lempel-Ziv-Miller-Wegman) is a dictionary-based compression algorithm that extends the LZW algorithm.

### Compression Process

1. Initialize a dictionary with all possible single characters (0-255)
2. Start with the first character as the current phrase
3. For each subsequent character:
   - If the current phrase + character exists in the dictionary, extend the current phrase
   - Otherwise:
     - Output the code for the current phrase
     - Add the current phrase + first character of the next phrase to the dictionary
     - Set the current phrase to the current character
4. Output the code for any remaining phrase

### Decompression Process

1. Initialize the same dictionary with all possible single characters
2. For each code in the compressed data:
   - Look up the code in the dictionary to get the corresponding phrase
   - Add the phrase to the result
   - Add a new entry to the dictionary (previous phrase + first character of current phrase)

### Performance Factors

- Works best with repetitive data patterns
- The dictionary grows as compression proceeds, capturing longer patterns
- The compression ratio depends on the nature of the input data


## Acknowledgments

This implementation is based on the LZMW compression algorithm, which extends the original LZW algorithm developed by Abraham Lempel, Jacob Ziv, and Terry Welch.