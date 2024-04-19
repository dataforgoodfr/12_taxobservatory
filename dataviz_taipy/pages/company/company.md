
<header||layout|columns=1  1|class_name=p4 fr header|

<headerleft|part|

<|part|class_name=h1 fr align-columns-center|
Pick a company to dive into their report
|>

<|{selected_company}|selector|lov={selector_company}|on_change=on_change_company|dropdown|label=Company|>

<|part|
Can’t find a company ?   
We might have missed out in its report,  
Reach with this contact form if you found it  
|>

|headerleft>

<headerright|part|

<|{header_right_image_path}|image|>

|headerright>

|header>

<generalinfo|part|

<|part|class_name=h2|
<|{selected_company}|>
|>

<firstrow|layout|columns=1 1 1 1|class_name=p4 align-columns-center align-columns-stretch|
<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz1.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz1.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz1.sub_title}|>
|sub_title>
<data_viz|part|
<|{viz1.data}|>
|data_viz>
|viz_card>
<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz2.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz2.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz2.sub_title}|>
|sub_title>
<data_viz|part|
<|{viz2.data}|>
|data_viz>
|viz_card>
<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz3.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz3.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz3.sub_title}|>
|sub_title>
<data_viz|part|class_name=round|
<|{viz3.data}|>
|data_viz>
|viz_card>
<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz4.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz4.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz4.sub_title}|>
|sub_title>
<data_viz|part|class_name=round|
<|{viz4.data}|>
|data_viz>
|viz_card>
|firstrow>

|generalinfo>

<cntent1|part|

[//]: # (###########################################")
[//]: # (Financial Reporting Overview)
[//]: # (###########################################")
<header|layout|columns=1fr 1|clas_name=p4 align-columns-center|
<|part|class_name=h2|
Financial Reporting Overview
|>
<|{selected_year}|selector|lov={selector_year}|on_change=on_change_year|dropdown|label=Fiscal Year|>
|header>

[//]: # (###########################################")
[//]: # (Tax transparency)
<header|part|class_name=h3|
Tax transparency
|header>

<datarow|layout|columns=1 1fr|clas_name=p4 align-columns-center|

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz5.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz5.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz5.sub_title}|>
|sub_title>
<data_viz|part|class_name=round|
<|{viz5.data}|>
|data_viz>
|viz_card>

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz6.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz6.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz6.sub_title}|>
|sub_title>
<data_viz|part|class_name=round|
<|{viz6.data}|>
|data_viz>
|viz_card>

|datarow>

<blabla|part|
- Transparency vary from one multinational to another in terms 
of the financial variables disclosed and the extent of 
geographical disaggregation.  

- We evaluate the reports transparency considering two 
features: the geographical disaggregation and the presence 
of of the different recommended variables. The more 
detailed the geographical disaggregation and the higher 
the number of variables published the higher the 
transparency score.  

- It is important to note that the availability of different 
variables will be essential to calculate the indicators 
below. When the variables are not available it will not be 
possible to calculate all of the indicators.
|blabla>

[//]: # (###########################################")
[//]: # (Financial profile)
<header|part|class_name=h3|
Financial profile
|header>

<datarow|layout|columns=1 1|class_name=p4 align-columns-center align-columns-stretch|

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_13_key_metric.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_13_key_metric.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_13_key_metric.sub_title}|>
|sub_title>
<data_viz|part||
<|{viz_13_key_metric.data}|table|>
|data_viz>
|viz_card>

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_14.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_14.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_14.sub_title}|>
|sub_title>
<data_viz|part|
<|{viz_14.data}|chart|orientation=h|type=bar|x=total_revenues_%|y=jur_name|>
|data_viz>
|viz_card>

|datarow>

[//]: # (###########################################")
[//]: # (Distribution of profits vs. employees)
<header|part|class_name=h3|
Distribution of profits vs. employees
|header>

<datarow|layout|columns=1 1|class_name=p4 align-columns-center|

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_15.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_15.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_15.sub_title}|>
|sub_title>
<data_viz|part|
[//]: # (<|{viz_15.data}|chart|orientation=h|type=bar|x[1]=employees_%|x[2]=profit_before_tax_%|y=jur_name|>)
<|{viz_15.data}|chart|type=bar|properties={properties}|>
|data_viz>
|viz_card>

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_16.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_16.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_16.sub_title}|>
|sub_title>
<data_viz|part|class_name=round|
<|{viz_16.data}|>
|data_viz>
|viz_card>
|datarow>

<blabla|part|
This chart plots the percentage of total positive profits 
and the percentage of total employees reported in each 
jurisdiction where the multinational is active. Comparing 
the amount of physical production factors like employees 
with the amount of profit can give an indication of profit 
shifting activities where strong misalignment are observed. 
|blabla>

|cntent1>



[//]: # (###########################################")
[//]: # (Use of tax havens)
[//]: # (###########################################")
<cntent2|layout|columns=1=|gap=4rem|clas_name=p4 align-columns-center|

<header|layout|columns=1fr 1|clas_name=p4 align-columns-center|
<|part|class_name=h2|
Use of tax havens
|>
<|{selected_year}|selector|lov={selector_year}|on_change=on_change_year|dropdown|label=Fiscal Year|>
|header>

<blabla|part|
(change text) Tax havens are countries where low effective 
tax rates are observed, in this section, we rely on official 
lists of tax havens (see methodology)
|blabla>

<datarow|layout|columns=1 1|gap=5rem|clas_name=p4 align-columns-center|

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_17.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_17.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_17.sub_title}|>
|sub_title>
<data_viz|part|
<|{viz_17.data}|table|>
|data_viz>
<blabla|part|
This charts shows the percentage of profits booked in each 
jurisdiction (horizontal axis and bubble size) and contrast 
it with the amount of profit per employee reported in the 
jurisdiction. Tax havens are XXX color while other countries 
are in XXX color.
|blabla>
|viz_card>

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_18.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_18.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_18.sub_title}|>
|sub_title>
<data_viz|part|
[//]: # (<|{viz_18.data}|table|>)
<|{viz_18.data}|chart|type=bar|x=index|y[1]=unrelated_revenues_percentage|y[2]=related_revenues_percentage|layout={layout}|>
|data_viz>
<blabla|part|
Related party revenues arise when the company trades 
internally. These revenues, in contrast with unrelated party 
revenues that arise from trade with external partners, 
present a risk of profit shifting as could entail transfer 
pricing manipulations.
|blabla>
|viz_card>

|datarow>

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_19.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_19.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_19.sub_title}|>
|sub_title>
<data_viz|part|
<|{viz_19.data}|table|page_size=8|>
|data_viz>
|viz_card>

<viz_card|part|class_name=viz|
<headers|layout|columns=2fr 1|
<title|part|
<|{viz_21.title}|>
|title>
<download_button|part|
<|{download_icon_path}|image|class_name=download_button|on_action={viz_21.on_action}|>
|download_button>
|headers>
<sub_title|
<|{viz_21.sub_title}|>
|sub_title>
<data_viz|part|
<|{viz_21.data}|chart|mode=lines|x=year|y[1]=tax_havens_profit_%|y[2]=tax_havens_employees_%|line[1]=dash|>
|data_viz>
|viz_card>

|cntent2>






























<cntent3|layout|columns=1=|gap=4rem|clas_name=blue_sectionp4 align-columns-center|

<button|part|
<|button|active|label=Download data|>
|button>

<blabla|part|class_name=h1 align-columns-center|
Would you like to learn more?
|blabla>


<layoutcard|layout|columns=1 1 1|class_name=p4|gap=5rem|
  <|card|
  <|part|class_name=h1
  Publication trends
  |>
  Visualize how tax reporting practices from the world's 
  largest corporations are evolving across industries, 
  regions and over time through interactive charts and 
  analysis.

  <|button|active|label=Publication trends ->|>
  |>    

  <|card|
  <|part|class_name=h1
  Methodology
  |>
  text

  <|button|active|label=Our methodology ->|>
  |>   
  <|card|
  <|part|class_name=h1
  Key stories
  |>
  Access our ongoing research examining multinational tax 
  behavior based on this country-by-country data, including 
  case studies, risk scoring and more.

  <|button|active|label=Key stories ->|>
  |>
|layoutcard>
[//]: <> (end layout card)

|cntent3>


