# Weekly Update Log

## Week of 03/07-03/11:

### Completed tasks:

- Divided extract.ipynb into extract_column.py, main.py, and test.ipynb.
- Resolved the issue of multi-line extraction for single country sessions.
- Reviewed the 1994 version and removed the footnote preceding the country list.

### Questions and Plans:

- The extraction of footnotes before the country list is not yet entirely functional.
- Continue testing the functions and fixing any errors that occur.
- Hopefully let 1995 version done in next week.

## Week of 02/27-03/02:

### Completed tasks:

- Divided the extract function into smaller parts to handle each column efficiently.
- Optimized helper functions and regular expressions to improve the accuracy and speed of the extraction process.
- Conducted testing with five different PDF file formats.

### Questions and Plans:

- I have observed some differences in the file formats for each year, such as variations in the body text, footnotes, and council sections. Thus, I plan to adjust the extract functions by year to ensure greater accuracy.
- There is one bug remaining in the body text of the 1994 file, which I will fix in the next update. Error case: both country and body text are countries' names.


## Week of 02/22-26

### Completed tasks:

- Developed a function to extract information from new version files (columns A to J and M), while columns K and L can be obtained outside the function. However, the presence of column N cannot be recognized by text, whether the file is scanned or not. While the function has a few bugs, I am currently testing it with different files to improve its accuracy.
- Although it is challenging to extract footnotes precisely, the function has a good level of accuracy for other columns.
- The processing time for 30 files, on average, is approximately 6 minutes.

### Questions and Plans:
- I will seek the agreement of Prof. Yang to begin extracting new version files.
- I plan to consider specific preprocessing for old version files in the upcoming week.


## Week of 02/14-19

### Completed tasks:

- Downloaded all data from Dropbox
- Ran a simple comparison between scanned (<1990) and non-scanned (>1990) files.
- Compared extracted text with real document content
- Experimented with several OCR engines and decided to use Tesseract due to its ease of use in Python and its active online community.
- For more detailed progress, please look into file "[extract_example.ipynb](https://github.com/manyuanQ/OCR-GAUN/blob/main/extract_example.ipynb)".

### Questions and plans:

- Verify that there are 161,649 PDF files in total
- Consider applying image denoising to scanned files to increase accuracy
- Estimate a more precise time frame for extracting text from non-scanned files and organizing into CSV files

### Request for Prof. Yang:

- Could you please review the file "[Afghanistan1956-3865163_extract_text.pdf](https://github.com/manyuanQ/OCR-GAUN/blob/main/Afghanistan1956-3865163_extract_text.pdf)" to look into the possible errors during the OCR process? I have labeled the error in red, but it's worth noting that in some cases the result may be even worse. For instance, the date may not be extracted correctly.
- Please let me know if you think the level of correctness is acceptable, as this may affect similar scanned files. For example, last time it could not recognize dates correctly.
- Additionally, do you know the proportion of scanned and non-scanned files? This information will help me understand how many files require attention in order to improve accuracy.
- My suggested solution is to prioritize processing non-scanned (>1990) files first, and then focus on improving accuracy of scanned files. 
