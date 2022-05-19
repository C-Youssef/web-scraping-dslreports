
## Extracting review data from dslreports.com

In this project, we used [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to extract review data of multiple Canadian ISPs from [dslreports.com](https://www.dslreports.com/), save the resulting dataset to a csv file, and generate charts from it usingn [Matplotlib](https://matplotlib.org).

In the first notebook named [extracting_Bell_internet_review_data.ipynb](https://github.com/C-Youssef/web-scraping-dslreports/blob/main/extracting_Bell_internet_review_data.ipynb), we showed step by step how to build a function that scans a single DSL reports web page and extract review ratings and other data from it. This function was then used to extrat all Bell Internet review data and chart reviewer's ratings.

In the second notebook named [extracting_Canadian_ISPs_review_data.ipynb](https://github.com/C-Youssef/web-scraping-dslreports/blob/main/extracting_Canadian_ISPs_review_data.ipynb), we extended the work done in the first notebook to include all Canadian ISPs that are reviewed on dslreports.com.

We also used Matplotlib to generate, from the extracted data, charts that show the reviewers' satisfaction levels with major Canadian ISPs for the last two decades.

The aim from this notebook is educational. It is to demonstrate how meaningful data can be extracted from semi-structred data on the web and visualized or saved in a tabular format for future analysis.

As a future work and a good charting practice, the extracted data can be used for spatial data visualization. We have the locations of the reviewers along with their ISP ratings. Drawing these ratings on a map can be quite interesting. 
