# Methodology

Taxplorer was created to collect, aggregate and analyze data from country-by-country reports published by multinationals.
Our approach is based on three pillars:
- Open source: the code is available here (https://github.com/dataforgoodfr/12_taxobservatory/) and our database can be downloaded here (add link to /download-data)
- Collaborative: Reach out (add link to contact page) to contribute or suggest improvements.
- Dynamic: Our database is regularly updated to incorporate new insights and to enhance its accuracy.

# How is the data collected ?

**Search Strategy**
Our methodology revolves around searching for specific PDF documents related to corporate reporting, particularly focusing on tax country-by-country reporting. The following steps outline our search strategy:
1. Google Custom Search API Integration: We utilize the Google Custom Search API to conduct targeted searches for PDF documents. This API allows us to narrow down our search to PDF files related to corporate reporting, enhancing the efficiency of our search process.
2.Query Formulation: Each search query is formulated based on the company name and relevant keywords. The keywords used in the search queries are meticulously chosen to target documents about tax country-by-country reporting, ensuring the retrieval of relevant PDF files.
3. Query Execution: The formulated search queries are sent to the Google Custom Search API, specifying parameters such as the API key, custom search engine (CSE) ID, and file type (PDF). By incorporating these parameters, we focus our search exclusively on PDF documents related to the specified keywords and company names.
4. Iterative Search Process: We conduct an iterative search process, querying the API for each unique company name derived from the provided CSV file. This iterative approach enables comprehensive coverage of relevant documents across multiple companies.
5. URL Caching: To optimize performance and avoid redundant queries, we implement URL caching. Cached URLs are stored locally, allowing us to bypass repeated API queries for previously searched company names and keywords. This caching mechanism significantly reduces query latency during subsequent runs.

**PDF Retrieval and Validation**
Upon identifying relevant PDF documents through the search process, we employ the following methodology for retrieval and validation:
1. PDF Download: Using the URLs obtained from the search results, we proceed to download the corresponding PDF files. Each PDF file is downloaded to a designated directory for further processing.
2. Download Handling: We implement error handling mechanisms to manage download failures and interruptions gracefully. In case of download errors or timeouts, appropriate error messages are logged, and the corresponding PDF file is discarded to maintain data integrity.
3. PDF Integrity Check: Upon successful download, each PDF file undergoes an integrity check to ensure its validity. We utilize the PyPDF2 library to validate the structure and metadata of the downloaded PDF files. Any PDF files found to be corrupted or incomplete are flagged, logged, and subsequently discarded to prevent erroneous data inclusion.
4. Duplicate Detection: Throughout the download process, we employ mechanisms to detect and filter out duplicate PDF files. This prevents redundant downloads of identical documents, optimizing resource utilization and streamlining the data collection process.

**Logging and Monitoring**
Our methodology incorporates robust logging and monitoring mechanisms to facilitate transparency, traceability, and error detection throughout the search and retrieval process. Detailed logs are generated, capturing essential information such as query results, download status, error messages, and system notifications. These logs serve as invaluable assets for troubleshooting, performance analysis, and quality assurance.

**Execution and Configuration**
Our methodology is implemented as a Python script, offering flexibility and configurability to accommodate diverse search requirements and operational environments. Users can specify input parameters such as the CSV file containing company names, Google API credentials, search keywords, destination directory for PDF downloads, timeout thresholds, and debug options. This configurability ensures adaptability to varying use cases and facilitates seamless integration into existing workflows.


# How is the data processed ?

The country-by-country tax report (CbCR) can be provided in a pretty long financial report of a hundred of pages or so. Once the tables of interest are located, the extraction of the figures from the tables in a PDF is not straightforward. These numbers are not necessarily encoded in the PDF code and we need to involve visual processing tools and character recognition (OCR). Finally, the companies indicate their indicators in various ways such that some standardization is required to transform these arbitrary layouts into the target layout of interest. 
Therefore, our processing pipeline involves the following key steps:
- identification of the pages containing the CbCR tables
- localization of the tables in the page and automatic character recognition
- table standardization

**Identification of the relevant pages to process**

Locating the pages of interest is formulated as a binary classification task where we need to decide whether or not a page is relevant. This classification problem is solved with a random forest classifier, trained on a pre-labeled corpus. Input features are extracted from every page and fed into the random forest. The features we extract are the number of countries listed in the page and the number of occurrences of several pre-identified keywords such as “tax”, “countr”, “report”, “revenu”, “incom”, “employ”, etc.. 
At this stage, the pages suggested by the classifier are validated by a human expert.

**Table localization and parsing**

Once the relevant pages are identified, we need to extract the layout of the tables (e.g. column headers) and the content of the cells. Unfortunately, the PDF format has a whole lot of different ways to encode tables and the parsing of these tables is not straightforward. In our pipeline, we tackled the most challenging situation where the tables are inserted as images into the pages. Hence, we need to involve image processing tools to locate the table and parse it. Fortunately, nowadays we have several highly performant algorithms for locating and parsing tables. Within our code, we propose several algorithms implemented in different libraries:
- ExtractTable : https://extracttable.com/ 
- Camelot : https://camelot-py.readthedocs.io/en/master/ 
- LlamaParse : https://github.com/run-llama/llama_parse 
- Unstructured (local or through the API) : https://unstructured-io.github.io/unstructured/core/partition.html 
ExtractTable is a proprietary closed-source solution. It is provided as an API and we do not have any details about its functioning.
 Camelot is open-source and comes in two flavors : stream and lattice. Both involves the text extracted from the PDF with pdfminer (https://pdfminersix.readthedocs.io/en/latest/) which are either aggregated to form tables or combined with the layout extracted with image processing (line, intersection .. detection using OpenCV). 
The last two, LlamaParse and Unstructured, have been developed in the context of the increasing interest in Retrieval Augmented Generation (RAG) applications were a large language model (LLMs) can be plugged onto your own database and generate content that is grounded on your document base. LlamaParse is closed source and can only be accessed through their API. Unstructured provides several algorithms such as cutting edge deep learning algorithms for detecting tables (yolox, detectron2) combined with character recognition (tesseract OCR / PaddlePaddle OCR) as well a private text to image transformer based model called chipper which can be accessed only through the API. 
Our library is modular, allowing us to use any of these algorithms and we performed tests on some reports in order to identify which of these algorithms have the best performance. It turned out that LlamaParse and Unstructured are really competitive. 
This stage may contain errors. For example, OCR is not perfect and there can be typos, for example, in country names. The decimal separator in numbers can also be difficult to catch by these algorithms. Therefore, we implemented some automated checks (e.g. for the juridictions, we can use the Levenshtein distance to fix some errors, the sum of numbers in columns can be compared to the Total if provided in the table) but we also need a human expert to validate this stage. 

**Table standardization**

The layout of the CbCR tables are nothing but standard. The columns can be arbitrarily swapped, the table can be completely transposed, the column headers can be expressed in various different ways, the units and currencies are not always the same. The last step standardizes these tables into a common output format with the key figures always in the same order. To perform this step, instead of handcrafting custom rules for every report, we build on top of the latest developments of Large Language Models (LLMs) and instruct them to extract and reformat the relevant piece of information from the tables we extracted at the previous step. This last step is performed using the LangChain library (https://www.langchain.com/) and the OpenAI GPT-4 LLM.

# Calculations

## Transparency score

We created the transparency score metric to assess how transparent multinationals are in their CbC report, given the CBC report’s format is not standardized yet. 

**This score is calculated for each report and corresponds to the average of two components : one based on the geographical level of reporting (Component I) and the other on the completeness of the financial data provided (Component II).**

**Geographical level of reporting (Component I)**

**Context** : Usually the CBCR has to publish figures country by country (or jurisdiction by jurisdiction). Some multinationals comply with this requirement, but others publish figures by large region, such as Asia or Africa. Some multinationals may also group a certain number of countries together in an "Other" category, in which the multinationals aggregate several countries and may or may not give details of these countries. We wanted here to calculate a score that evaluates the quantity of data reported at a jurisdiction level and would penalize data reported at a more aggregated level than the jurisdiction.

**Calculation behind Component I** : for each financial variable available in the report (transformed into absolute values), we calculate the % attributed to a jurisdiction and then calculate the average of those scores (e.g., if 70% of a company’s profits and 50% of this company’s employees are attributed to a jurisdiction, its geographical score for this report will be 60%)

**Completeness of the financial data provided (Component II)**

**Context** : A full CbCR report should include the following 10 financial data :
- Revenue by Region = Total_Revenue dans le dataset actuel
- Related Party transactions ou relacted Party Revenue by region = Related party revenue
- Pre-tax income by region = Profit before Tax
- Income Tax expense by region = Income Tax accrued
- Cash Taxes paid by region = Tax paid
- Assets or property, plant, and equipment by region = Tangible assets
- Accumulated earnings
- Tangible assets
- Stated capital
- Number of employees by region = Employees 
Yet, some companies do not disclose all variables. We wanted to reflect this in the transparency score.

**Calculation behind Component II** : We calculate the score based on the weighted share of variables available in the report (i.e., for which the company provides at least 1 datapoint). The weight is 2 for Pre-tax profits and Taxes paid, and 1 for other variables (reflecting the importance of the first two for tax behavior analysis)