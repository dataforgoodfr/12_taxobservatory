import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import humanize

# TODO add viz comment
# Viz 1 -
def number_of_tracked_reports(df):
    number_of_tracked_reports = len(df.groupby(["year", "mnc"])["mnc"])
    return number_of_tracked_reports

# TODO add viz comment
def number_of_tracked_reports_company(df_selected_company):
    number_of_tracked_reports_company = len(
        df_selected_company.groupby(["year"])["year"]
    )
    return number_of_tracked_reports_company

# TODO add viz comment
def number_of_tracked_reports_sector(df_selected_sector):
    number_of_tracked_reports_sector = len(
            df_selected_sector.groupby(["year", "mnc"])["year"]
        )
    return number_of_tracked_reports_sector

# TODO add viz comment
def number_of_tracked_reports_country(df_selected_country):    
    number_of_tracked_reports_country = len(
        df_selected_country.groupby(["year", "mnc"])["year"]
    )
    return number_of_tracked_reports_country

# TODO add viz comment
# Viz 2 - Number of tracked reports over time
def number_of_tracked_reports_over_time(df):
    df_count = df.groupby(["year"])["mnc"].nunique().reset_index()
    return df_count

# TODO add viz comment
def number_of_tracked_reports_over_time_company(df_selected_company):
    df_count_company = (
        df_selected_company.groupby(["year"])["mnc"].nunique().reset_index()
    )    
    # df_count_all_company = df.groupby(["year"])["mnc"].nunique().reset_index()

    # row[3].line_chart(df_count_all_company, x="year", y="mnc")

    # row[4].write("selected sector")
    # row[4].write(
    #     "df_selected_sector.groupby(['year'])['mnc'].nunique().reset_index()"
    # )
    return df_count_company

# TODO add viz comment
def number_of_tracked_reports_over_time_sector(df_selected_sector):
    df_count_sector = (
        df_selected_sector.groupby(["year"])["mnc"].nunique().reset_index()
    )

    # df_count_all_sector = (
    #     df.groupby(["year", "sector"])["mnc"].nunique().reset_index()
    # )

    # row[4].line_chart(df_count_all_sector, x="year", y="mnc", color="sector")

    # row[5].write("selected country")
    # row[5].write(
    #     "df_selected_country.groupby(['year'])['mnc'].nunique().reset_index()"
    # )
    return df_count_sector

# TODO add viz comment
def number_of_tracked_reports_over_time_country(df_selected_country):
    df_count_country = (
        df_selected_country.groupby(["year"])["mnc"].nunique().reset_index()
    )
    # df_count_all_country = (
    #     df.groupby(["year", "jur_name"])["mnc"].nunique().reset_index()
    # )

    # row[5].line_chart(df_count_all_country, x="year", y="mnc", color="jur_name")
    return df_count_country

# Viz 19
# what are the tax havens being used by the company
# to test but could be a table with one row per jurisdiction (filtering on TH) with
# % profit
# % employee
# profit per employee
# % related party revenue
#  for domestic vs tax havens vs. non havens
def tax_haven_used_by_company(df_selected_company):
    company_upe_code = df_selected_company['upe_code'].unique()[0]
    pc_list = ['employees', 'profit_before_tax', 'related_revenues']
    # grouper = df_selected_company.groupby('jur_name')

    df_domestic_company = df_selected_company[df_selected_company['jur_code']==company_upe_code]
    df_selected_company_th = df_selected_company[df_selected_company['jur_tax_haven'] != 'not.TH']
    df_selected_company_nth = df_selected_company[df_selected_company['jur_tax_haven'] == 'not.TH']


    for col in pc_list:
        df_selected_company[col + '_domestic_sum'] = df_domestic_company[col].sum()
        df_selected_company[col + '_th_sum'] = df_selected_company_th[col].sum()
        df_selected_company[col + '_nth_sum'] = df_selected_company_nth[col].sum()

        df_selected_company[col+'_sum'] = df_selected_company[col].sum()
        df_selected_company[col + '_pc'] = 100 * df_selected_company[col] / df_selected_company[col+'_sum']



    df_selected_company_th = df_selected_company[df_selected_company['jur_tax_haven'] != 'not.TH']
    df_selected_company_th_agg = df_selected_company_th.groupby(['mnc', 'jur_name']).agg(
        profit_before_tax=('profit_before_tax', 'sum'),
        profit_before_tax_pc=('profit_before_tax_pc', 'sum'),
        employees_pc=('employees_pc', 'sum'),
        employees=('employees', 'sum'),
        related_revenues_pc=('related_revenues_pc', 'sum')
    )
    df_selected_company_th_agg = df_selected_company_th_agg.reset_index()
    df_selected_company_th_agg['profit per employee'] =\
        df_selected_company_th_agg['profit_before_tax']/df_selected_company_th_agg['employees']
    df_selected_company_th_agg['profit per employee'] = df_selected_company_th_agg['profit per employee'].replace([np.inf, -np.inf], None)

    return df_selected_company, df_selected_company_th_agg

# TODO add viz comment
# complete table table showing for all jurisdictions revenues, profits, employees, taxes with % of total for each (color code for tax havens)
def company_table(df_selected_company):
    company_upe_code = df_selected_company['upe_code'].unique()[0]
    pc_list = ['employees', 'profit_before_tax', 'unrelated_revenues', 'related_revenues', 'total_revenues', 'tax_paid']
    # grouper = df_selected_company.groupby('jur_name')

    # df_domestic_company = df_selected_company[df_selected_company['jur_code'] == company_upe_code]
    # df_selected_company_th = df_selected_company[df_selected_company['jur_tax_haven'] != 'not.TH']
    # df_selected_company_nth = df_selected_company[df_selected_company['jur_tax_haven'] == 'not.TH']

    for col in pc_list:
        # df_selected_company[col + '_domestic_sum'] = df_domestic_company[col].sum()
        # df_selected_company[col + '_th_sum'] = df_selected_company_th[col].sum()
        # df_selected_company[col + '_nth_sum'] = df_selected_company_nth[col].sum()

        df_selected_company[col + '_sum'] = df_selected_company[col].sum()
        df_selected_company[col + '_pc'] = 100 * df_selected_company[col] / df_selected_company[col + '_sum']

    # complete table table showing for all jurisdictions revenues, profits, employees, taxes with % of total for each (color code for tax havens)
    df_selected_company_by_jur = df_selected_company.groupby(['mnc', 'jur_name']).agg(
        related_revenues_pc=('related_revenues_pc', 'sum'),
        unrelated_revenues=('unrelated_revenues', 'sum'),
        total_revenues=('total_revenues', 'sum'),
        profit_before_tax=('profit_before_tax', 'sum'),
        employees_pc=('employees_pc', 'sum'),
        tax_paid=('tax_paid', 'sum'),
        tax_paid_pc=('tax_paid_pc', 'sum'),
    )
    return df_selected_company_by_jur.reset_index()



# Viz 4 - Breakdown of reports by sector (pie chart)
def breakdown_of_reports_by_sector(df):

    #Dataframe called df
    df_reports_per_sector_year = df.groupby(['sector', 'year'])['mnc'].nunique().reset_index(name='unique_company_count')

    # Aggregate the counts of unique companies across all years for each sector
    df_reports_per_sector = df_reports_per_sector_year.groupby('sector')['unique_company_count'].sum().reset_index()

    # Calculate the total count of unique companies across all sectors
    total_companies = df_reports_per_sector['unique_company_count'].sum()

    # Calculate the percentage of each sector's count relative to the total count and round to 2 decimals
    df_reports_per_sector['percent'] = ((df_reports_per_sector['unique_company_count'] / total_companies) * 100).round(2)

    # Sort the DataFrame by the count of unique companies in ascending order
    df_reports_per_sector = df_reports_per_sector.sort_values(by='unique_company_count', ascending=True)

    return df_reports_per_sector

def breakdown_of_reports_by_sector_viz(df_reports_per_sector):
    # Plotting the horizontal bar chart with Plotly Express
    fig = px.bar(df_reports_per_sector, y='sector', x='percent',
                orientation='h',  # Horizontal orientation
                title='Breakdown of Reports by Sector (All Years)',
                labels={'percent': 'Percentage of Companies (%)', 'sector': 'Sector'},
                text='percent',  # Show the percentage as text label
                hover_data={'unique_company_count': True, 'percent': ':.2f%'},  # Add tooltip for count and rounded percentage
                )

    # Update layout to display the title above the chart
    fig.update_layout(title='Breakdown of Reports by Sector',
                    title_x=0.5, title_y=0.9,  # Adjust position
                    title_font_size=20)  # Adjust font size

    # Show the horizontal bar chart
    return go.Figure(fig)


# Viz 5 - Breakdown of reports by HQ country (pie chart)
def breakdown_of_reports_by_hq_country(df):
    # Group the DataFrame by 'upe_name' (HQ country) and 'year' and count the number of unique companies for each HQ country and year
    df_reports_per_country_year = df.groupby(['upe_name', 'year'])['mnc'].nunique().reset_index(
        name='unique_company_count')

    # Aggregate the counts of unique companies across all years for each HQ country
    df_reports_per_country = df_reports_per_country_year.groupby('upe_name')['unique_company_count'].sum().reset_index()

    # Calculate the total count of unique companies across all HQ countries
    total_companies = df_reports_per_country['unique_company_count'].sum()

    # Calculate the percentage of each HQ country's count relative to the total count and round to 2 decimals
    df_reports_per_country['percent'] = (
                (df_reports_per_country['unique_company_count'] / total_companies) * 100).round(2)

    # Sort the DataFrame by the count of unique companies in ascending order
    df_reports_per_country = df_reports_per_country.sort_values(by='unique_company_count', ascending=True)

    return df_reports_per_country

def breakdown_of_reports_by_hq_country_viz(df_reports_per_country):
    # Plotting the horizontal bar chart with Plotly Express
    fig = px.bar(df_reports_per_country, y='upe_name', x='percent',
                 orientation='h',  # Horizontal orientation
                 title='Breakdown of Reports by HQ Country over Time',
                 labels={'percent': 'Percentage of Companies (%)', 'upe_name': 'HQ Country'},
                 text='percent',  # Show the percentage as text label
                 hover_data={'unique_company_count': True, 'percent': ':.2f%'},
                 # Add tooltip for count and rounded percentage
                 )

    # Update layout to display the title above the chart
    fig.update_layout(title='Breakdown of Reports by HQ Country over Time',
                      title_x=0.5, title_y=0.95,  # Adjust position
                      title_font_size=20)  # Adjust font size

    # Show the horizontal bar chart
    # fig.show()
    return go.Figure(fig)

## Viz 6 - Breakdown of reports by sector over time (bar chart)

import plotly.express as px
def breakdown_of_reports_by_sector_over_time(df):
    df_reports_per_sector_over_time = df
    # return df_reports_per_sector_over_time

    # Step 1: Determine the top 10 sectors that released reports
    top_10_sectors = df['sector'].value_counts().nlargest(10).index.tolist()

    # Step 2: Group all other sectors as "Others"
    df['Sectors'] = df['sector'].apply(lambda x: x if x in top_10_sectors else 'Others')

    # Step 3: Group the DataFrame by 'year', 'Sectors', and count the number of unique companies for each year and sector
    df_reports_per_year_sector = df.groupby(['year', 'Sectors'])['mnc'].nunique().reset_index(name='unique_company_count')

    # Sort sectors alphabetically
    df_reports_per_year_sector = df_reports_per_year_sector.sort_values(by='Sectors', ascending=False)

    return df_reports_per_year_sector, top_10_sectors
def breakdown_of_reports_by_sector_over_time_viz(df_reports_per_year_sector, top_10_sectors):


    # Define the order of sectors for the stacked bar chart and legend, reversed
    chart_order = ['Others'] + top_10_sectors[::-1]
    legend_order = ['Others'] + top_10_sectors[::-1]

    # Plotting the bar chart using Plotly Express
    fig = px.bar(df_reports_per_year_sector, x='year', y='unique_company_count', color='Sectors',
                 title='Breakdown of Reports by Sector over Time',
                 labels={'unique_company_count': 'Number of Companies Reporting', 'year': 'Year'},
                 barmode='stack',
                 category_orders={'Sectors': chart_order})

    # Reverse the order of legend items
    fig.update_layout(legend=dict(traceorder='reversed'))

    # Adjusting the legend order and formatting the legend labels
    for i, trace in enumerate(fig.data):
        trace.name = legend_order[i]
        # Change color of the "Others" bar to grey
        if trace.name == 'Others':
            trace.marker.color = 'grey'

    # Show the plot
    # fig.show()
    return go.Figure(fig)






## Viz 7 - Breakdown of reports by HQ country over time (bar chart)
# TODO add code

## Viz 8 - Breakdown of MNC by sector (pie chart - changed to bar chart for more visibility)
# TODO add code

## Viz 9 - Breakdown of MNC by HQ country (pie chart - changed to bar chart for more visibility)
# TODO add code

## Viz 10/11 - Breakdown of MNC by sector
# TODO add code

## Viz 11 - Breakdown of MNC by HQ country
# TODO add code

# Viz 12 - available reports by company
def compute_company_available_reports(df: pd.DataFrame, company: str) -> dict:
    """Compute the number of reports tracked for a specific company and the
    available fiscal years.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): company name.

    Returns:
        dict: numbers of reports and fiscal years.
    """
    available_years = df.loc[df['mnc'] == company, 'year'].unique()
    n_reports = len(available_years)

    # Convert type of items from 'int' to 'str' in available years list
    years_string_list = [str(year) for year in available_years]

    # Summarize all available years in one string
    if len(years_string_list) == 1:
        years_string = years_string_list[0]
    elif len(years_string_list) > 1:
        years_string = ', '.join(years_string_list[:-1])
        years_string += ' and ' + years_string_list[-1]

    # Create a dictionnary with the results
    data = {
        'Company': company,
        'Reports': n_reports,
        'Fiscal year(s) available': years_string
    }

    return data

def display_company_available_reports(
        df: pd.DataFrame, company: str, hide_company: bool = True) -> pd.DataFrame:
    """Display the number of reports tracked for a specific company and the
    available fiscal years.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): company name.
        hide_company (bool, optional): hide company name in final table. Defaults to True.

    Returns:
        pd.DataFrame: numbers of reports and fiscal years.
    """

    # Compute data
    data = compute_company_available_reports(df=df, company=company)

    # Create the table
    df = pd.DataFrame.from_dict(data=data, orient='index')

    if hide_company:
        return df[1:].style.hide(axis='columns')

    return df.style.hide(axis='columns')


# Viz 13 - company key financials kpis
def compute_company_key_financials_kpis(
        df: pd.DataFrame,
        company: str,
        year: int = None) -> dict:
    """Compute key financial KPIs for a company.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int, optional): fiscal year to filter the results with. Defaults to None.

    Returns:
        dict: company key financial KPIs.
    """

    kpis_list = ['total_revenues', 'unrelated_revenues', 'related_revenues',
                 'profit_before_tax', 'tax_paid', 'employees']

    years_list = df.loc[df['mnc'] == company, 'year'].unique()

    # Compute sum of kpis
    if not year or year not in years_list:
        df = (df.loc[df['mnc'] == company]
              .groupby(['year', 'upe_name'], as_index=False)[kpis_list]
              .sum()
              )
    else:
        df = (df.loc[(df['mnc'] == company) & (df['year'] == year)]
              .groupby(['year', 'upe_name'], as_index=False)[kpis_list]
              .sum())

    df = df.set_index('year')

    # Make financial numbers easily readable with 'humanize' package
    for column in df.columns:
        if column not in ['employees', 'upe_name']:
            df[column] = df[column].apply(
                lambda x: humanize.intword(x) if isinstance(x, (int, float)) else x)
            df[column] = '€ ' + df[column]
        elif column == 'employees':
            df[column] = df[column].astype(int)

    # Clean columns string
    df = df.rename(columns={'upe_name': 'headquarter'})
    df.columns = df.columns.str.replace('_', ' ').str.capitalize()

    # Create a dictionnary with the results
    data = df.to_dict(orient='index')

    return data
def display_company_key_financials_kpis(
        df: pd.DataFrame, company: str, year: int = None) -> pd.DataFrame:
    """Display key financial KPIs for a company.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int, optional): fiscal year to filter the results with. Defaults to None.

    Returns:
        pd.DataFrame: company key financial KPIs.
    """

    # Compute data
    data = compute_company_key_financials_kpis(df=df, company=company, year=year)

    # Create the table
    df = pd.DataFrame.from_dict(data)

    return df

# Viz 14
def compute_top_jurisdictions_revenue(
        df: pd.DataFrame, company: str, year: int) -> dict:
    """Rank jurisdictions on their percentage of total revenues in a top 10.
    When there are more than 10 jurisdictions, the tenth represent all
    jurisdictions below 9.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int): fiscal year.

    Returns:
        dict: Top 10 jurisdictions for percentage of total revenues.
    """

    df = df.loc[
        (df['mnc'] == company) & (df['year'] == year),
        ['jur_name', 'related_revenues', 'unrelated_revenues', 'total_revenues']
    ]

    # Calculate missing values in 'total_revenues' if 'related_revenues' and
    # 'unrelated_revenues' are available
    df.loc[
        df['related_revenues'].notna()
        & df['unrelated_revenues'].notna()
        & df['total_revenues'].isna(),
        'total_revenues'
    ] = df['related_revenues'] + df['unrelated_revenues']

    # Subset DataFrame
    df = df[['jur_name', 'total_revenues']]

    # Remove rows where 'total_revenues' is missing
    df = df.dropna(subset=['total_revenues'])

    # Group same 'jur_name' (sometimes several 'Other')
    # e.g. SWISS LIFE, 2021
    df = df.groupby('jur_name', as_index=False).sum()

    # Filter the top 10 'jur_name' for 'total_revenues'
    if len(df) > 10:
        # Check if 'Other' already in 'jur_name' and add the revenues
        # of the 'jur_name' below top 10 to its value
        if 'Other' in df['jur_name'].values:
            top = df.nlargest(10, 'total_revenues')
            below_top_revenues = df.loc[
                ~df['jur_name'].isin(top['jur_name']), 'total_revenues'].sum()
            top.loc[top['jur_name'] == 'Other', 'total_revenues'] += below_top_revenues
            top = top.reset_index(drop=True)
        else:
            # Keep top 9 and group all revenues of the rest in 'Others'
            top = df.nlargest(9, 'total_revenues')
            below_top_revenues = df.loc[
                ~df['jur_name'].isin(top['jur_name']), 'total_revenues'].sum()
            top = top.reset_index(drop=True)
            top.loc[9] = ['Others', below_top_revenues]
    else:
        top = df

    # Rename 'Other' to 'Others'
    top.loc[top['jur_name'] == 'Other', 'jur_name'] = 'Others'

    # Compute percentage of revenue
    top['total_revenues_%'] = top['total_revenues'] / top['total_revenues'].sum()

    # Convert DataFrame to dictionnary
    data = top.to_dict()

    # Create DataFrame
    df = pd.DataFrame.from_dict(data)
    df = df.sort_values(by='total_revenues_%')

    return df


def display_jurisdictions_top_revenue(df: pd.DataFrame, company: str, year: int):
    """Display top 10 jurisdictions for percentage of total revenues in an
    horizontal bar chart.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int): fiscal year.
    """

    # Compute data
    data = compute_top_jurisdictions_revenue(df=df, company=company, year=year)

    # Create DataFrame
    df = pd.DataFrame.from_dict(data)
    df = df.sort_values(by='total_revenues_%')

    # Create figure
    fig = px.bar(df,
                 x='total_revenues_%',
                 y='jur_name',
                 orientation='h',
                 title='Top jurisdictions for revenue',
                 text_auto='.1%')

    # Update layout settings
    fig.update_layout(
        xaxis=dict(
            title='Percentage of total revenue',
            tickformat='.0%'
        ),
        yaxis_title=None,
        plot_bgcolor='white',
        # width=800,
        # height=480
    )

    # Define position of text values
    values_positions = [
        'outside' if value <= 0.05 else 'inside' for value in df['total_revenues_%']]

    fig.update_traces(
        textangle=0,
        textposition=values_positions,
        selector=dict(name='')
    )

    # Define style of hover on bars
    fig.update_traces(hovertemplate='%{y}: %{x: .3%}')
    # fig.show()
    return go.Figure(fig)


# Viz 15
def compute_pretax_profit_and_employees_rank(
        df: pd.DataFrame, company: str, year: int) -> dict:
    """Compute jurisdictions percentage of profit before tax and percentage
    of employees and rank by percentage of profit.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int): fiscal year.

    Returns:
        dict: rank of jurisdictions with percentage of profit before and percentage
        of employees.
    """

    # Filter rows with selected company/year and subset with necessary features
    features = ['jur_name', 'profit_before_tax', 'employees']
    df = df.loc[(df['mnc'] == company) & (df['year'] == year), features]

    # Keep only profitable jurisdictions
    df = df.loc[df['profit_before_tax'] >= 0]

    # Sort jurisdictions by profits
    df = df.sort_values(by='profit_before_tax').reset_index(drop=True)

    # Calculate percentages
    df['profit_before_tax_%'] = df['profit_before_tax'] / df['profit_before_tax'].sum()
    df['employees_%'] = df['employees'] / df['employees'].sum()
    df = df.drop(columns=['profit_before_tax', 'employees'])

    # data = df.to_dict()

    return df


def display_pretax_profit_and_employees_rank(
        df: pd.DataFrame, company: str, year: int):
    """Display rank of jurisdictions by percentage of profit before and percentage
        of employees.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int): fiscal year.
    """

    # Compute data
    data = compute_pretax_profit_and_employees_rank(df=df, company=company, year=year)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Rename columns
    df = df.rename(columns={
        'profit_before_tax_%': 'Percentage of pre-tax profit',
        'employees_%': 'Percentage of employees'
    })

    # Create figure
    fig = px.bar(
        df,
        x=['Percentage of employees', 'Percentage of pre-tax profit'],
        y='jur_name',
        barmode='group',
        orientation='h',
        text_auto='.1%'
    )

    # Set figure height (min. 480) depending on the number of jurisdictions
    fig_height = max(480, (48 * len(df['jur_name'])))

    # Set maximum value for x axis
    if not df[['Percentage of pre-tax profit', 'Percentage of employees']].isna().all().all():
        max_x_value = max(df[['Percentage of pre-tax profit', 'Percentage of employees']].max(axis='columns')) + 0.1
    else:
        max_x_value = 1

    # Update layout settings
    fig.update_layout(
        title='Profitables jurisdictions pre-tax profit & employees',
        xaxis=dict(
            title=None,
            tickformat='.0%',
            range=[0, max_x_value]
        ),
        yaxis_title=None,
        legend=dict(
            title=dict(text=''),
            orientation='h'
        ),
        plot_bgcolor='white',
        width=800,
        height=fig_height
    )

    # Add annotations for NaN values where there should have been a bar
    for index, row in df.iterrows():
        if pd.isna(row['Percentage of employees']):
            fig.add_annotation(
                xanchor='left',
                x=0.001,
                y=df.index[index],
                yshift=-10,
                text='Information not provided',
                showarrow=False,
                font=dict(size=12)
            )
        if pd.isna(row['Percentage of pre-tax profit']):
            fig.add_annotation(
                xanchor='left',
                x=0.001,
                y=df.index[index],
                yshift=10,
                text='Information not provided',
                showarrow=False,
                font=dict(size=12)
            )

    # Loop through each bar trace and hide the text if the value is NaN
    for trace in fig.data:
        values = df[trace.name]
        text_position = ['outside' if not np.isnan(value) else 'none' for value in values]
        trace.textposition = text_position

    # fig.show()
    return go.Figure(fig)


# Viz 18

def compute_related_and_unrelated_revenues_breakdown(
        df: pd.DataFrame, company: str, year: int) -> dict:
    """Compute related and unrelated revenues in tax heaven, non tax heaven and
    domestic jusrisdictions.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int): fiscal year to filter the results with.

    Returns:
        dict: revenues percentage for different type of jurisdictions.
    """

    # Filter rows with selected company/year and subset with necessary features
    features = ['upe_code', 'jur_code', 'jur_name', 'jur_tax_haven',
                'unrelated_revenues', 'related_revenues']

    df = df.loc[(df['mnc'] == company) & (df['year'] == year), features]

    # Drop rows where either unrelated or related revenues are missing
    df = df.dropna(subset=['unrelated_revenues', 'related_revenues'])

    # 'total_revenues' is recreated using related and unrelated revenues since the one
    # reported by companies is not always reliable
    df['total_revenues'] = df['unrelated_revenues'] + df['related_revenues']

    # Create a column to check if 'jur_code' is the domestic country
    df['domestic'] = df.apply(lambda row: row['jur_code'] == row['upe_code'], axis='columns')

    # Compute kpis in a new DataFrame
    data = pd.DataFrame()
    data['tax_haven'] = df.loc[df['jur_tax_haven'] == True, ['unrelated_revenues', 'related_revenues']].sum()
    data['non_tax_haven'] = df.loc[df['jur_tax_haven'] == False, ['unrelated_revenues', 'related_revenues']].sum()
    data['domestic'] = df.loc[df['domestic'] == True, ['unrelated_revenues', 'related_revenues']].sum()

    # Replace values with share (%) of 'unrelated/related revenues'
    data = data.div(data.sum(axis='rows'), axis='columns')

    # Rename indexes
    data = data.rename(index={
        'unrelated_revenues': 'unrelated_revenues_percentage',
        'related_revenues': 'related_revenues_percentage'
    })

    # Convert DataFrame to dictionnary
    data = data.to_dict()

    return data


def display_related_and_unrelated_revenues_breakdown(df: pd.DataFrame, company: str, year: int):
    """Display related and unrelated revenues in tax heaven, non tax heaven and
    domestic jusrisdictions.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
        year (int): fiscal year to filter the results with.
    """

    # Compute data
    data = compute_related_and_unrelated_revenues_breakdown(df=df, company=company, year=year)

    # Create DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')

    # Rename columns and indexes
    df.columns = df.columns.str.replace('_', ' ').str.capitalize()
    df.index = df.index.str.replace('_', ' ').str.capitalize()

    # Create figure
    fig = px.bar(
        df,
        x=['Unrelated revenues percentage', 'Related revenues percentage'],
        y=df.index,
        orientation='h',
        text_auto='.0%'
    )

    # Update layout settings
    fig.update_layout(
        title='Breakdown of revenue',
        xaxis=dict(
            title=None,
            tickformat='.0%'
        ),
        yaxis_title=None,
        legend=dict(
            title=dict(text=''),
            orientation='h'
        ),
        plot_bgcolor='white',
        width=800,
        height=480
    )

    # Define position of text values
    for col in ['Unrelated revenues percentage', 'Related revenues percentage']:
        values_positions = ['outside' if value <= 0.05 else 'inside' for value in df[col]]

        fig.update_traces(
            textangle=0,
            textposition=values_positions,
            selector=dict(name=col)
        )

    # Add annotation if no values are availables (no bar displayed)
    for i, index in enumerate(df.index):
        if df.loc[index].isna().all():
            fig.add_annotation(
                x=0.5,
                y=df.index[i],
                text='No information to display',
                showarrow=False,
                font=dict(size=13)
            )

    # fig.show()
    return go.Figure(fig)
    
# Viz 21 - evolution of tax havens use over time : % profit vs % employees in TH over time
def compute_tax_havens_use_evolution(df: pd.DataFrame, company: str) -> dict:
    """Compute the evolution of tax havens use by company over time.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name

    Returns:
        dict: tax havens percentage of profits and employees for each year.
    """

    # Filter rows with selected company and subset with necessary features
    features = ['jur_code', 'year', 'jur_tax_haven', 'profit_before_tax', 'employees']
    df = df.loc[(df['mnc'] == company), features]

    # Keep jurisdictions with profitable or missing revenues
    df = df.loc[(df['profit_before_tax'] >= 0) | (df['profit_before_tax'].isna())]

    # For all sum calculations below :
    # - Result NA : all jurisdictions values were NA ;
    # - Result 0 : at least one jurisdiction was reported as 0.

    # Calculate total profit and employees by year and tax haven status
    df = df.groupby(['year', 'jur_tax_haven'], as_index=False)[['profit_before_tax', 'employees']].sum(min_count=1)

    # Calculate total profits and employees for each year
    for year in df['year'].unique():
        df.loc[df['year'] == year, 'total_profit'] = df.loc[df['year'] == year, 'profit_before_tax'].sum(min_count=1)
        df.loc[df['year'] == year, 'total_employees'] = df.loc[df['year'] == year, 'employees'].sum(min_count=1)

    # Remove non tax haven jurisdictions
    df = df.loc[df['jur_tax_haven'] == True].reset_index()

    # Calculate percentages
    df['tax_havens_profit_%'] = df['profit_before_tax'] / df['total_profit']
    df['tax_havens_employees_%'] = df['employees'] / df['total_employees']

    # Convert necessary data to dictionnary
    data = df[['year', 'tax_havens_profit_%', 'tax_havens_employees_%']].to_dict()

    return data


def display_tax_havens_use_evolution(df: pd.DataFrame, company: str):
    """Display the evolution of tax havens use by company over time.

    Args:
        df (pd.DataFrame): CbCRs database.
        company (str): Company name
    """

    # Compute data
    data = compute_tax_havens_use_evolution(df=df, company=company)

    # Create DataFrame
    df = pd.DataFrame.from_dict(data)

    # Rename columns
    df = df.rename(columns={
        'tax_havens_profit_%': 'Percentage of profits in tax havens',
        'tax_havens_employees_%': 'Percentage of employees in tax havens'
    })

    # Create figure
    fig = px.bar(
        df,
        x='year',
        y=['Percentage of profits in tax havens', 'Percentage of employees in tax havens'],
        barmode='group',
        text_auto='.1%'
    )

    # Update layout settings
    fig.update_layout(
        title='Tax havens use in profitables jurisdictions',
        xaxis_title=None,
        yaxis_title=None,
        yaxis_tickformat='.0%',
        legend=dict(
            title=dict(text=''),
            orientation='h'
        ),
        plot_bgcolor='white',
        width=800,
        height=480
    )

    # fig.show()
    return go.Figure(fig)


# Viz 24
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def viz_24_compute_data(df):
    # Drop duplicates to ensure each MNC appears only once per year
    df_unique_mnc = df.drop_duplicates(subset=['year', 'mnc'])

    # Group the DataFrame by 'mnc' and count the number of reports for each MNC
    df_reports_per_mnc = df_unique_mnc.groupby('mnc').size().reset_index(name='report_count')

    # Convert the DataFrame to a dictionary where MNCs are keys and report counts are values
    mnc_report_count = dict(zip(df_reports_per_mnc['mnc'], df_reports_per_mnc['report_count']))

    return mnc_report_count

def viz_24_viz(mnc_report_count):
    # Generate the word cloud using the report counts as weights
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(mnc_report_count)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    fig = px.imshow(wordcloud)
    # plt.imshow(wordcloud, interpolation='bilinear')
    return fig