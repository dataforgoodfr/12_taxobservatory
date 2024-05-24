# All the viz that we need

### 1. Number of tracked reports

- Global valule
    raw figure (aka scorecard)

    ```
    def number_of_tracked_reports(df):
        number_of_tracked_reports = len(df.groupby(["year", "mnc"])["mnc"])
        return number_of_tracked_reports
    ```  
    **Number of tracked reports : <|{tracked_reports}|>**

- For a specific company
    
    <|{selected_company}|selector|lov={selector_company}|on_change=on_change_company|dropdown|label=Company|>  

    ```
    def number_of_tracked_reports_company(df_selected_company):
        number_of_tracked_reports_company = len(
            df_selected_company.groupby(["year"])["year"]
        )
    ```   
    Number of tracked reports for company <|{selected_company}|> : **<|{tracked_reports_company}|>**

- For a specific sector

    <|{selected_sector}|selector|lov={selector_sector}|on_change=on_change_sector|dropdown|label=Sector|>

    ```
    def number_of_tracked_reports_sector(df_selected_sector):
        number_of_tracked_reports_sector = len(
                df_selected_sector.groupby(["year", "mnc"])["year"]
            )
    ```   
    Number of tracked reports for sector <|{selected_sector}|> : **<|{tracked_reports_sector}|>**

- For a specific country
    <|{selected_country}|selector|lov={selector_country}|on_change=on_change_country|dropdown|label=Country|>

    ```
    def number_of_tracked_reports_country(df_selected_country):    
        number_of_tracked_reports_country = len(
            df_selected_country.groupby(["year", "mnc"])["year"]
        )
    ```  
    Number of tracked reports for country <|{selected_country}|> : **<|{tracked_reports_counrty}|>**

### 2. Number of tracked reports over time

bar chart / line chart
dsfsdqqfsd
- Global valule
    ```
    code:
    df_count = df.groupby(["year"])["mnc"].nunique().reset_index()
    ```

<|layout|columns=1 1 1|

<|{df_count}|number_format=%.2f|page_size=50|table|>

<|{df_count}|chart|mode=lines|x=year|y[1]=mnc|line[1]=dash|>

<|{df_count}|chart|type=bar|x=year|y[1]=mnc|>

|>

- For a specific company : {selected_company}
    ```
    code:
    df_count_company = (
    df_selected_company.groupby(["year"])["mnc"].nunique().reset_index()
    )
    ```

<|layout|columns=1 1 1|

<|{df_count_company}|number_format=%.2f|page_size=50|table|>

<|{df_count_company}|chart|mode=lines|x=year|y[1]=mnc|line[1]=dash|>

<|{df_count_company}|chart|type=bar|x=year|y[1]=mnc|>

|>

- For a specific sector
    ```
    code:
    df_count_sector = (
    df_selected_sector.groupby(["year"])["mnc"].nunique().reset_index()
    )
    ```
<|layout|columns=1 1 1|

<|{df_count_sector}|number_format=%.2f|page_size=50|table|>

<|{df_count_sector}|chart|mode=lines|x=year|y[1]=mnc|line[1]=dash|>

<|{df_count_sector}|chart|type=bar|x=year|y[1]=mnc|line[1]=dash|>

|>

- For a specific country
    ```
    code:
    df_count_counrty = (
    df_selected_counrty.groupby(["year"])["mnc"].nunique().reset_index()
    )
    ```
<|layout|columns=1 1 1|

<|{df_count_country}|number_format=%.2f|page_size=50|table|>

<|{df_count_country}|chart|mode=lines|x=year|y[1]=mnc|line[1]=dash|>

<|{df_count_country}|chart|type=bar|x=year|y[1]=mnc|line[1]=dash|>

|>

## Viz 4 - Breakdown of reports by sector (pie chart)
[//]: # (<|{df_reports_per_sector_year}|chart|x=percent|y=sector|title=Breakdown of Reports by Sector &#40;All Years&#41;|type[1]=bar|orientation=h|>)
<|chart|figure={breakdown_of_reports_by_sector_fig}|>

## Viz 5 - Breakdown of reports by HQ country (pie chart)
<|chart|figure={df_reports_per_country_fig}|>

## Viz 6 - Breakdown of reports by sector over time (bar chart)

## Viz 7 - Breakdown of reports by HQ country over time (bar chart)

## Viz 8 - Breakdown of MNC by sector (pie chart - changed to bar chart for more visibility)

## Viz 9 - Breakdown of MNC by HQ country (pie chart - changed to bar chart for more visibility)

## Viz 10/11 - Breakdown of MNC by sector / HQ country

## 19 what are the tax havens being used by the company 

### computed data
<|{df_company_info}|number_format=%.2f|page_size=50|table|>

### table result
<|{df_tax_haven_company}|number_format=%.2f|page_size=50|table|>

## 20 complete table table showing for all jurisdictions revenues, profits, employees, taxes with % of total for each (color code for tax havens)
<|{df_company_table}|number_format=%.2f|page_size=50|table|>