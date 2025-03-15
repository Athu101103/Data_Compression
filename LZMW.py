import streamlit as st
import pandas as pd
import io

def lzmw_compress(text):
    """
    Compress a string using the LZMW algorithm.
    
    Args:
        text: String to compress
        
    Returns:
        list: List of integers representing the compressed data
    """
    if not text:
        return []
    
    # Initialize dictionary with all possible single characters
    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    
    compressed_data = []
    current_phrase = text[0]
    
    for char in text[1:]:
        next_phrase = current_phrase + char
        
        # If the next phrase exists in the dictionary, update current phrase
        if next_phrase in dictionary:
            current_phrase = next_phrase
        else:
            # Output the code for current phrase
            compressed_data.append(dictionary[current_phrase])
            
            # Add the new phrase to the dictionary
            dictionary[next_phrase] = dict_size
            dict_size += 1
            
            # Reset current phrase to the current character
            current_phrase = char
    
    # Don't forget to output code for the last phrase
    if current_phrase:
        compressed_data.append(dictionary[current_phrase])
    
    return compressed_data, dictionary

def lzmw_decompress(compressed_data):
    """
    Decompress data that was compressed using the LZMW algorithm.
    
    Args:
        compressed_data: List of integers representing the compressed data
        
    Returns:
        str: The decompressed string
    """
    if not compressed_data:
        return ""
    
    # Initialize dictionary with all possible single characters
    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256
    
    # First code is always a character
    result = dictionary[compressed_data[0]]
    previous = result
    
    for code in compressed_data[1:]:
        if code in dictionary:
            current = dictionary[code]
        else:
            # Special case: if the code is not in the dictionary,
            # it must be the first character of the previous string + the previous string
            current = previous + previous[0]
        
        # Append to result
        result += current
        
        # Add new entry to dictionary
        dictionary[dict_size] = previous + current[0]
        dict_size += 1
        
        previous = current
    
    return result, dictionary

def calculate_compression_stats(original, compressed):
    """
    Calculate various compression statistics.
    
    Args:
        original: Original string
        compressed: Compressed data
        
    Returns:
        dict: Dictionary of compression statistics
    """
    # Original size in bytes (assuming ASCII/UTF-8 where each character is 1 byte)
    original_size = len(original)
    
    # Compressed size in bytes (each code could be variable size based on value)
    compressed_size = sum(1 if code < 256 else
                          2 if code < 65536 else
                          3 if code < 16777216 else
                          4 for code in compressed)
    
    compression_ratio = original_size / compressed_size if compressed_size > 0 else float('inf')
    space_saved_percent = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
    
    return {
        "Original Size (bytes)": original_size,
        "Compressed Size (bytes)": compressed_size,
        "Compression Ratio": compression_ratio,
        "Space Saved (%)": space_saved_percent
    }

# Streamlit app
st.title("LZMW Compression Algorithm")
st.write("""
This app demonstrates the LZMW (Lempel-Ziv-Miller-Wegman) compression algorithm, 
a dictionary-based compression technique that extends LZW by adding more complex phrases to the dictionary.
""")

# Input section
st.header("Input Text")
input_method = st.radio(
    "Choose input method:",
    ("Enter text", "Upload file", "Use sample text"),
    key="input_method_radio"
)

if input_method == "Enter text":
    input_text = st.text_area("Enter text to compress:", height=150, key="input_text_area")
elif input_method == "Upload file":
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"], key="file_uploader")
    if uploaded_file is not None:
        input_text = uploaded_file.getvalue().decode("utf-8")
    else:
        input_text = ""
else:  # Use sample text
    sample_option = st.selectbox(
        "Select sample text:",
        ("Simple repeating pattern", "Repeated sentence", "Lorem ipsum"),
        key="sample_text_select"
    )
    
    if sample_option == "Simple repeating pattern":
        input_text = "abcabcabcabcabcabcabcabc"
    elif sample_option == "Repeated sentence":
        input_text = "The quick brown fox jumps over the lazy dog. " * 10
    else:  # Lorem ipsum
        input_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
        ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
        in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat 
        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""" * 5

# Only process if there is input text
if input_text:
    if st.button("Compress", key="compress_button"):
        # Compress the input
        compressed_data, compression_dict = lzmw_compress(input_text)
        
        # Decompress back
        decompressed_text, decompression_dict = lzmw_decompress(compressed_data)
        
        # Calculate stats
        stats = calculate_compression_stats(input_text, compressed_data)
        
        # Display results in tabs
        tab1, tab2 = st.tabs(["Compression Results", "Dictionary"])
        
        with tab1:
            st.header("Compression Results")
            
            # Show statistics
            st.subheader("Statistics")
            stats_df = pd.DataFrame([stats])
            st.dataframe(stats_df, use_container_width=True)
            
            # Original vs Compressed vs Decompressed
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Text")
                st.text_area(
                    label="",
                    value=input_text[:1000] + ("..." if len(input_text) > 1000 else ""), 
                    height=150,
                    disabled=True,
                    key="original_text_area"
                )
                
                st.subheader("Decompressed Text")
                st.text_area(
                    label="",
                    value=decompressed_text[:1000] + ("..." if len(decompressed_text) > 1000 else ""), 
                    height=150,
                    disabled=True,
                    key="decompressed_text_area"
                )
                
                # Validation
                if input_text == decompressed_text:
                    st.success("✓ Decompression successful! The decompressed text matches the original.")
                else:
                    st.error("✗ Decompression failed. The decompressed text doesn't match the original.")
            
            with col2:
                st.subheader("Compressed Data")
                st.text_area(
                    label="", 
                    value=str(compressed_data[:100]) + ("..." if len(compressed_data) > 100 else ""), 
                    height=150,
                    disabled=True,
                    key="compressed_text_area"
                )
                
                # Provide download options
                compressed_bytes = io.BytesIO()
                for code in compressed_data:
                    if code < 256:
                        compressed_bytes.write(code.to_bytes(1, byteorder='big'))
                    elif code < 65536:
                        compressed_bytes.write(code.to_bytes(2, byteorder='big'))
                    else:
                        compressed_bytes.write(code.to_bytes(4, byteorder='big'))
                
                compressed_bytes.seek(0)
                st.download_button(
                    label="Download Compressed Data",
                    data=compressed_bytes,
                    file_name="compressed.lzmw",
                    mime="application/octet-stream",
                    key="download_button"
                )
        
        with tab2:
            st.header("Dictionary Exploration")
            
            # Filter options
            st.subheader("Dictionary Filter")
            dict_filter = st.radio(
                "Show dictionary entries:", 
                ("All", "Initial (0-255)", "Generated (>255)"),
                key="dict_filter_radio"
            )
            
            # Create dataframe from dictionary
            dict_df = pd.DataFrame([(k, v) for k, v in compression_dict.items()], 
                                   columns=["Phrase", "Code"])
            
            if dict_filter == "Initial (0-255)":
                filtered_df = dict_df[dict_df["Code"] <= 255]
            elif dict_filter == "Generated (>255)":
                filtered_df = dict_df[dict_df["Code"] > 255]
            else:
                filtered_df = dict_df
            
            # Display sorted by code
            sorted_df = filtered_df.sort_values("Code")
            st.dataframe(sorted_df, use_container_width=True)
            
            st.text(f"Total Dictionary Size: {len(compression_dict)} entries")
        
    # Add explanation section at the bottom
    with st.expander("How LZMW Compression Works", expanded=False):
        st.write("""
        ## LZMW Algorithm Explanation
        
        LZMW (Lempel-Ziv-Miller-Wegman) is a dictionary-based compression algorithm that extends the LZW algorithm.
        
        ### Compression Process:
        1. Initialize a dictionary with all possible single characters (0-255)
        2. Start with the first character as the current phrase
        3. For each subsequent character:
           - If the current phrase + character exists in the dictionary, extend the current phrase
           - Otherwise:
             - Output the code for the current phrase
             - Add the current phrase + first character of the next phrase to the dictionary
             - Set the current phrase to the current character
        4. Output the code for any remaining phrase
        
        ### Decompression Process:
        1. Initialize the same dictionary with all possible single characters
        2. For each code in the compressed data:
           - Look up the code in the dictionary to get the corresponding phrase
           - Add the phrase to the result
           - Add a new entry to the dictionary (previous phrase + first character of current phrase)
           
        ### Performance Factors:
        - Works best with repetitive data patterns
        - The dictionary grows as compression proceeds, capturing longer patterns
        - The compression ratio depends on the nature of the input data
        """)
        
else:
    st.info("Enter some text or upload a file to compress.")