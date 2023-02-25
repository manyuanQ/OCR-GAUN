# Weekly Update Log

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

## Week of 02/22-26

### Completed tasks:

- Write a function to extract information from column A to J and M, K L can be obtained outside the function, N cannot be recognized by text whether this file is scanned or not. However each file has a slightly difference between each other, there are many bugs in this function, need to be improved by testing with different files.


