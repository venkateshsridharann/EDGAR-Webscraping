# Mutual Funds Holding Report Webscraping from EDGAR

## Overview

This Python script parses fund holdings pulled from EDGAR, given a ticker or CIK, and writes a .tsv file saved to the output folder.
Requests is used to get HTML and XML content from the website
BeautifulSoup is used to parse the HTML and XML.
Python i/o operations are used to write the tsv file.

## Set up

Use the following command to install dependencies

`pip install -r requirements.txt`

## Usage

Run the following command

`python scrape.py`

You will see an input prompt like this

`Enter the CIK for the Company's report`

Enter a valid CIK. You will see a successfull message like this

`Successfully created file in outputs/<cik>.tsv`

Enter an invalid CIK and you will see the following message.

`CIK entered is not valid. Please try a different value!`

## Assumptions

1. The reports in the table are arranged most recent report first, if the order changes the code breaks.


## Accessing older reports

The code only parses the latest report. It can be modified to accesss any previous report by inputting the year, month and comparing the current year, month to loop through and find the corresponding report.