import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def number_of_tracked_reports(df):
    number_of_tracked_reports = len(df.groupby(["year", "mnc"])["mnc"])
    return number_of_tracked_reports

def number_of_tracked_reports_company(df_selected_company):
    number_of_tracked_reports_company = len(
        df_selected_company.groupby(["year"])["year"]
    )
    return number_of_tracked_reports_company

def number_of_tracked_reports_sector(df_selected_sector):
    number_of_tracked_reports_sector = len(
            df_selected_sector.groupby(["year", "mnc"])["year"]
        )
    return number_of_tracked_reports_sector

def number_of_tracked_reports_country(df_selected_country):    
    number_of_tracked_reports_country = len(
        df_selected_country.groupby(["year", "mnc"])["year"]
    )
    return number_of_tracked_reports_country

def number_of_tracked_reports_over_time(df):
    df_count = df.groupby(["year"])["mnc"].nunique().reset_index()
    return df_count

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

def number_of_tracked_reports_over_time_country(df_selected_country):
    df_count_country = (
        df_selected_country.groupby(["year"])["mnc"].nunique().reset_index()
    )
    # df_count_all_country = (
    #     df.groupby(["year", "jur_name"])["mnc"].nunique().reset_index()
    # )

    # row[5].line_chart(df_count_all_country, x="year", y="mnc", color="jur_name")
    return df_count_country

    
    
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

    print (df_selected_company_th_agg.reset_index())
    return df_selected_company, df_selected_company_th_agg


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