
# Merge PDF Pages

## Overview
This Python script intelligently maximizes space by merging multiple PDF pages onto a single page. It calculates the best layout to minimize whitespace and ensure that the content of each page is clearly visible. This tool is perfect for consolidating documents or creating summaries where space conservation is crucial.

## Installation

### Prerequisites
- Anaconda or Miniconda installed on your system.

### Setting Up Your Environment
1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/merge_pdf_pages.git
   cd merge_pdf_pages
   ```

2. **Create a Conda environment:**
   ```
   conda create --name pdf_merge_env python=3.8
   ```

3. **Activate the environment:**
   ```
   conda activate pdf_merge_env
   ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

   `requirements.txt` should include:
   ```
   PyMuPDF
   requests
   ```

## Usage
To use the script, run the following command in your terminal:
```
python merge_pdf_pages.py [input.pdf | input_url] [output.pdf] [m] [n] [d1] [d2]
```

Where:
- `input.pdf | input_url` is the path to the PDF file or a URL to download the PDF from.
- `output.pdf` is the optional path where the merged PDF will be saved.
- `m` and `n` are optional parameters specifying the number of rows and columns in the merge layout.
- `d1` and `d2` are optional parameters specifying the spacing between rows and columns, respectively.

## License
This project is licensed under the MIT License - see the LICENSE file for details. You are free to use, modify, and distribute this software according to the terms of the MIT License. Contributions are welcome. Please feel free to fork the repository and submit pull requests.

By using this license, you allow others to use your work freely while still maintaining copyright over your work. You may also consider adding a note about how you'd like to be credited or if you're open to collaborations.
