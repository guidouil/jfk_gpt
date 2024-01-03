# Make a JFK Archives GPT

## TL;DR

Use the GPTs : <https://chat.openai.com/g/g-10Lsb6YMz-jfk-gov-archives-analyst>

## Mission

Getting all pdf from the [JFK Assassination Records](https://www.archives.gov/research/jfk) to train a GPT to be an expert on this case.

## Requirements

First clone this repo and install dependancies

```sh
pip install --upgrade pip
pip install pandas requests openpyxl  pymupdf pytesseract

brew install tesseract
```

## Download PDFs

They are listed in the jfk.xls file

`python3 download.py`

## Extract PDFs

Once all PDF are collected, start Tesseract to extract text from PDF into 1 Mb txt files (openai doesn't like larger txt files)

`python3 extract.py`

## Notes

All the code was written (after many try) with the help of [GPT4](https://chat.openai.com/)
