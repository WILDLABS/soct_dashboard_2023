#import and load packages
import pandas as pd
import streamlit as st
import numpy as np
from plotnine import ggplot, aes, geom_bar, geom_text, coord_flip, ggtitle, theme, element_text, labs, scale_fill_manual, theme_minimal, geom_point, geom_line, position_stack
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import matplotlib.patches as mpatches
from streamlit_extras.dataframe_explorer import dataframe_explorer

#import the data
demographics = pd.read_excel('Input files/demographics.xlsx')
proficiency = pd.read_excel('Input files/proficiency.xlsx')
proficiency_pivot = pd.read_excel('Input files/proficiency_pivot.xlsx')
uconst = pd.read_excel('Input files/uconst.xlsx')
dconst = pd.read_excel('Input files/dconst.xlsx')
chal = pd.read_excel('Input files/chal.xlsx')

########################
st.image('Input files/cover.jpg')

st.header(':blue[About the research]')

st.markdown('As global environmental challenges continue to escalate, understanding how to most effectively leverage modern technology innovations for conservation impact becomes increasingly critical. Each year, **WILD**LABS surveys the global conservation tech community to find out what you all are working on, what challenges you\'re facing, what support you need, and what you foresee on the horizon. Our aims in this research are to build an evidence base to share back with and support the community, to use the insights produced to create more informed and effective **WILD**LABS programmes, and to communicate shared priorities to influence policy and funding decisions that will benefit our sector as a whole.\
            \
            For the State of Conservation Technology 2023 report, we\'ve built on our 2021 results to coduct a three-year trends analysis,  bringing you insights for the first time into how dynamics have been evolving across the community over time. By highlighting shifting opinions as well as stabilizing trends in technology usage, user and developer challenges, opportunities for growth, and more, we aimed to illuminate the most useful information for advancing the sector together in a more effective and inclusive way. As always, our hope with this research is to amplify a united voice to drive progress toward impactful solutions for the planet.')

st.divider()

st.subheader(':blue[What is WILDLABS?]')

st.markdown('**WILD**LABS is the central hub for conservation technology online, connecting 6,000+ conservationists, researchers, field biologists, engineers, developers, and conservation technology experts from around the world. Our rapidly developing research program harnesses rich insights from this global community to inform effective technology development and capacity building, break down barriers and empower technologists and conservationists alike to transform the conservation landscape. With collaboration and innovation at the heart of our work, **WILD**LABS is the launching pad for meeting conservation’s biggest challenges with conservation technology’s boldest solutions. Visit our platform and [YouTube channel](https://www.youtube.com/channel/UCrxw8iiyFalKHFNAhZYCAYA/videos) to learn more about the community, and follow us on X [@WILDLABSNET](https://twitter.com/WILDLABSNET) and Instagram [@wildlabsnet](https://www.instagram.com/wildlabsnet/).')

st.divider()

st.subheader(':blue[Who did we hear from?]')

st.markdown('We heard from 630 people across three years of surveys - for this report, we included responses from 222 people in 2020, 233 people in 2021, and 175 people in 2022*. About half of respondents said they were active **WILD**LABS members. Across the years, roughly one-third of respondents identified as female (34%), two-thirds identified as male (66%), and a few identified as 3rd gender or non-binary (<1%).')
st.caption('*\*Note: incomplete answers below a certain threshold were filtered out in each year*.')


############################################################
### Gender plot
############################################################
# Filter the DataFrame by gender values of 1 and 0
filtered_df = demographics[demographics['sc_gender'].isin(['Male', 'Female'])]

# Calculate the percentage of each gender value per year
df_summary = filtered_df.groupby(['year', 'sc_gender']).size().reset_index(name='count')
df_summary['percentage'] = df_summary.groupby('year')['count'].transform(lambda x: x / x.sum() * 100).round(1)
df_summary['percentage2'] = df_summary['percentage'].astype(str) + '%'

genderplot = (ggplot(df_summary, aes(y='percentage', x='factor(year)', fill='factor(sc_gender)')) +
              geom_bar(stat='identity', width=0.5) +
              geom_text(aes(label='percentage2'), position=position_stack(vjust=0.5), color='white') +
              coord_flip() +
              ggtitle('Gender Identity') +
              theme(plot_title=element_text(size=18, face="bold")) +
              labs(x='', y='Percentage of respondents', fill='Gender') +
              scale_fill_manual(values=['#DD7E3B', '#0E87BE']) +
              theme_minimal())

st.pyplot(ggplot.draw(genderplot))

st.markdown('Regarding geographic reach, most respondents indicated residing in the United States, the United Kingdom, or other European countries across years. Alongside **WILD**LABS’ efforts to more effectively engagage regional communities, the reach of the survey improved incrementally over time, with the percentage of respondents in North America and Europe dropping from 63% in 2020 to 57% in 2022. The below graph illustrates the geographical expansion of the survey over the last three years by highlighting the first year a country appeared in the responses.')

############################################################
### Map plot
############################################################

# Read the Natural Earth dataset for countries
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Define the custom colors for each region
color_mapping = {
    2020: '#68BDE4',
    2021: '#0E87BE',
    2022: '#04425F',
    'Other': 'lightgray'
}

# Merge the world map with DataFrame based on the country column
merged_data = world.merge(demographics, left_on='name', right_on='sc_country', how='left')

# Fill NaN values in the sc_region column with a default region (e.g., 'Other')
merged_data['sc_count_novel'].fillna('Other', inplace=True)

# Plot the world map with colored countries based on the region using the custom colors
fig, ax = plt.subplots(figsize=(10, 6))
plt.rcParams['font.family'] = 'sans serif'
merged_data.plot(column='sc_count_novel', linewidth=0.4, ax=ax, edgecolor='0.8', legend=True, color=[color_mapping.get(region, 'lightgrey') for region in merged_data['sc_count_novel']])


# Add the first legend for the color mapping
legend_colors = [mpatches.Patch(color=color_mapping[region], label=region) for region in color_mapping]
ax.legend(handles=legend_colors, title='First app.')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='both', which='both', length=0)

ax.set_xticks([])
ax.set_yticks([])



# Set plot title
ax.set_title('Expansion of countries from 2020 to 2022', fontsize=18)

# Display the plot using Streamlit
st.pyplot(fig)

st.markdown('For all years, survey participants most frequently reported working at conservation NGOs, followed by Universities or research institutes. Most of these individuals identified their primary role as either a conservation practitioner or a researcher, but a significant share of them (18%) identified their primary role as technologist. Technology companies were the next most highly represented organization type across all years.')

############################################################
### Org plot
############################################################
#Per year
# Filter the DataFrame by the specified years
years = demographics['year'].unique()

# Create an empty DataFrame to store the org counts
org_counts = pd.DataFrame(index=demographics['sc_organization'].unique(), columns=years)


# Calculate the counts of unique values in 'sc_organisation' column for each year
for year in years:
    year_df = demographics[demographics['year'] == year]
    counts = year_df['sc_organization'].value_counts()
    org_counts[year] = counts

orgs = ['Conservation NGO', 'University/Research Inst.', 'Tech company',
        'Private (non-tech)', 'Government agency', 'Other']
org_counts = org_counts.loc[orgs]

colors = ['#DD7E3B', '#EC7825', '#D22A00']
    
# Set the figure size
fig, ax = plt.subplots(figsize=(12, 6))
plt.rcParams['font.family'] = 'sans serif'

# Plot the circles for each year
x_coords = range(len(years))
for i, year in enumerate(years):
    counts = org_counts[year]
    orgs = counts.index
    sizes = counts.values

    if not orgs.empty:
        plt.scatter([i] * len(orgs), orgs, s=sizes * 350, alpha=0.7, color=colors[i])

        # Add text inside each circle
        for orgs, size in zip(orgs, sizes):
            plt.text(i, orgs, str(int(size)), ha='center', va='center', color='white', weight='bold', fontsize = 14)

# Set x-axis tick labels as year values
plt.xticks(x_coords, years, fontsize=14)
ax.margins(x=0.1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='both', which='both', length=0)


# Set y-axis tick labels
plt.yticks( fontsize=12)

# Set plot title
plt.title('Most respondents worked at Conservation NGOs\nOrganisations by year (count)', fontsize=22)

# Adjust the figure layout to prevent label cutoff
plt.tight_layout()

# Display the plot

st.pyplot(fig)

############################################################
### Role plot
############################################################

# Create an empty DataFrame to store the org counts
role_counts = pd.DataFrame(index=demographics['sc_primary_role'].unique(), columns=years)


# Calculate the counts of unique values in 'sc_organisation' column for each year
for year in years:
    year_df = demographics[demographics['year'] == year]
    counts = year_df['sc_primary_role'].value_counts()
    role_counts[year] = counts

roles = ['Conservation practitioner','Academic or researcher','Technologist', 'Investor or funder','Policymaker']
role_counts = role_counts.loc[roles]

# Replace NaN values with 0 in the specified columns
role_counts[[2020,2021,2022]] = role_counts[[2020,2021,2022]].fillna(0)

colors = ['#4CAF50', 'green', 'darkgreen']
    
# Set the figure size
fig, ax = plt.subplots(figsize=(12, 6))
plt.rcParams['font.family'] = 'sans serif'

# Plot the circles for each year
x_coords = range(len(years))
for i, year in enumerate(years):
    counts = role_counts[year]
    roles = counts.index
    sizes = counts.values

    if not roles.empty:
        plt.scatter([i] * len(roles), roles, s=sizes * 350, alpha=0.7, color=colors[i])

        # Add text inside each circle
        for roles, size in zip(roles, sizes):
            plt.text(i, roles, str(int(size)), ha='center', va='center', color='white', weight='bold', fontsize=14)

# Set x-axis tick labels as year values
plt.xticks(x_coords, years, fontsize=14)
ax.margins(x=0.1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='both', which='both', length=0)

# Set y-axis label
plt.yticks( fontsize=12)

# Adjust the figure layout to prevent label cutoff
plt.tight_layout()

# Set plot title
plt.title('Respondents were mostly conservationsist, researchers or technologists\n', fontsize=22, loc='left')
ax.set_xlabel('Roles by year (count)', fontsize=18, loc='left')
ax.xaxis.set_label_position('top')


# Display the plot
st.pyplot(fig)
st.divider()


####################

st.markdown('The main conservation issues respondents report focusing on in their work remain unchanged in both years we’ve collected opinions on them: ecological monitoring is the most widespread, followed by species protection and protected area management and planning.')

st.image('Input files/workchallenge.jpg')

st.caption('*Note: order based on number of times challenge indicated by respondents; for 2021 and 2022 only*')

st.divider()

######################################################

st.header(':blue[Current Tools: How are they performing?]')

st.markdown('*The tools respondents work with most haven\'t changed substantially since 2020, but people\'s views on the relative potential of these tools to advance conservation have shifted over time.*')

st.subheader(':blue[Usage and proficiency]')

st.markdown('For all years investigated, most survey respondents indicated that they frequently engage with one or more of 11 core conservation technology groups. Notably, almost all respondents reported engaging with more than one technology type (92%), and the vast majority said they engage with more than two (79%). Out of these groups, Camera Traps, GIS and remote sensing, and AI tools were the most widely used. The average self-reported level of expertise was similar across these tools with the exception of eDNA and genomics, which had the smallest sample size and lower average level of expertise than other tools.')

############################################################
### Proficiency plot
############################################################

profplot = (ggplot(proficiency, aes(x='reorder(technology, percentage)', y='percentage')) +
                    geom_bar(stat='identity', fill='#0E87BE') +
                    geom_point(aes(y='average_proficiency2'), color='#3B3838') +
                    geom_line(aes(y='average_proficiency2', group=1), color='#3B3838') +
                    labs(x='', y='Percentage of respondents') +
                    geom_text(aes(label='percentage2'), position=position_stack(vjust=0.5), color='white', size=10) +
                    theme_minimal() +
                    coord_flip() +
                    ggtitle(f'Technology usage and proficiency') +
                    theme(axis_text=element_text(size=12), plot_title=element_text(size=18)) +
                    scale_fill_manual(values=['#0E87BE', '#DD7E3B'], guide=False))

st.pyplot(ggplot.draw(profplot))

st.markdown('Explore what percentage of respondents used these technologies yearly, and what the average corresponding proficiency levels were, by utilizing the filters on the below table.')

############################################################
### Proficiency yearly pivot
############################################################

dataframe = proficiency_pivot

filtered_df = dataframe_explorer(dataframe, case=False)
st.dataframe(filtered_df, use_container_width=True)

# year = proficiency_pivot['Year'].drop_duplicates()
# year_choice = st.sidebar.selectbox('Select Year:', year)

st.subheader(':blue[Performance versus potential]')

st.markdown('To understand how current tools are perceived more broadly, we asked people to rate the conservation technologies they use in terms of both current performance and potential capacity to advance conservation. In 2020, GIS and remote sensing, Drones, and Mobile Apps were rated as the best performing technologies, while AI tools, eDNA and genomics, and Networked sensors were the ones seen as having the highest potential capacity to advance the field.')

st.image('Input files/potential2020.jpg')

st.markdown('The landscape is somewhat different in 2022: while GIS and remote sensing is still the highest performing technology group, protected area management tools and bioacoustics have replaced drones and mobile apps as the othertop-rated groups. Regarding potential to advance conservation, eDNA and genomics moved from the top of the list to nearly the bottom, replaced by Biologgers alongside Networked sensors and AI tools.')

st.markdown('Keep in mind that, while interesting, changes like this in the perceived potential of emerging technologies are not particularly surprising. As reflected in the technology hype cycle, a framework for understanding evolving interest in technologies over time, it’s common for initial excitement to spike when a new tool emerges, which can then take a dramatic hit with early adoption challenges, and then usually grows to a productive place of iterative learning and effective application.')

st.image('Input files/potential2022.jpg')

st.caption('*Note: The above two graphs show the ranking of the mean scores of survey responses for each technology. Respondents rated technologies on both fronts on scales from 1-5, with 1 being the least positive and 5 being the most.*')

st.divider()
st.header(':blue[Constraints: What’s preventing progress?]')

st.markdown('*Small shifts were noted from year to year, but overall, conservation technologists reported fairly consistent challenges and constraints over the last three years.*')

st.subheader(':blue[Challenges for the ecosystem]')

st.markdown('Regarding challenges facing the conservation technology ecosystem as a whole, competition for limited funding and duplication of efforts are the main challenges respondetns reported for all years of the survey.')

############################################################
### challenges
############################################################

# Define custom order and color mapping

color_values = ['#9F2A00', '#D32A00', '#F42A00', '#969696', '#A0A0A0', '#B0B0B0', '#B9B9B9', '#C7C7C7', '#E1E1E1']
ranking_order = chal['ranking'].unique().tolist()

color_map = {ranking: color for ranking, color in zip(ranking_order, color_values)}

plots = {}  # Dictionary to store the plots

for year in [2020, 2021, 2022]:
    # Filter data for the current year
    filtered_data = chal[chal['year'] == year]
    chal_order = filtered_data['chal'].tolist()

    # Create the bar chart
    fig = px.bar(filtered_data,
                 x='percentage',
                 y='chal',
                 color='ranking',
                 orientation='h',
                 category_orders={"chal": chal_order},
                 color_continuous_scale="GnBu_r")

    # Update layout
    fig.update_layout(
        showlegend=True,
        legend_title_text='Ranking',
        xaxis_title='',
        yaxis_title='',
        font=dict(size=16),
        xaxis=dict(
            tickvals=list(range(0, 101, 20)),
            ticktext=[f"{i}%" for i in range(0, 101, 20)],
            range=[0, 100],
            title_standoff=12,
            tickfont=dict(size=10)
        ),
        yaxis=dict(tickfont=dict(size=12)),
        title=f'Ecosystem challenges for {year}',
        title_x=0.39  # This centers the title
    )

    # Store the plot to the dictionary with the key 'year'
    plots[f'challenges{year}'] = fig


# Callback
selected_year = st.radio('Year:', [' 2020', ' 2021', ' 2022'], index=0)



if selected_year == ' 2020':
    st.write('In 2020, funding competition, duplication of efforts and adoption capacity were the most significant challenges.')
    
    st.plotly_chart(plots['challenges2020'])
        
elif selected_year == ' 2021':
    st.write('In the 2021 survey we introcued the category \'matching technology to conservation\', which became the second most reported challenge. Funding competition and duplication of efforts are still the other two significant challenges.')
    
    st.plotly_chart(plots['challenges2021'])
    
    
else:
    st.write('The 2022 landscape of challenges is very similar to the 2021 one with no notable changes.')
    st.plotly_chart(plots['challenges2022'])

st.subheader(':blue[User constrainsts]')

st.markdown('Regarding specific constraints affecting engagement by conservation tech end-users and developers, a key finding is that location matters: both users and developers in countries with developing economies were more likely to report multiple significant constraints. Additionally, gender and professional role are also potentially influential factors.')

st.markdown('End-users in developing countries were 1.5x more likely to report being significantly constrained by  maintenance costs, 2.5x more likely to be constrained by upfront costs, as well as access to training, advice, and mentoring, and 5x more likely to be constrained by local access to technology suppliers.')

st.markdown('When looking at end user constraints year by year, upfront costs are the main constrainst in every year, but the other constrainst have been shifting over the years: maintenance cost and time required seem to be more significant constraints, while technical skills slightly less so.')

st.caption('*Note: Likelihood figures are rounded.*')


############################################################
### User constrainst
############################################################

# Define custom order and color mapping

color_values = ['#9F2A00', '#D32A00', '#F42A00', '#D9D9D9', '#F2F2F2']
ranking_order = uconst['ranking'].unique().tolist()

color_map = {ranking: color for ranking, color in zip(ranking_order, color_values)}

plots = {}  # Dictionary to store the plots

for year in [2020, 2021, 2022]:
    # Filter data for the current year
    filtered_data = uconst[uconst['year'] == year]
    uconst_order = filtered_data['uconst'].tolist()

    # Create the bar chart
    fig = px.bar(filtered_data,
                 x='percentage',
                 y='uconst',
                 color='ranking',
                 orientation='h',
                 category_orders={"uconst": uconst_order},
                 color_discrete_map=color_map)

    # Update layout
    fig.update_layout(
        showlegend=True,
        legend_title_text='Ranking',
        xaxis_title='',
        yaxis_title='',
        font=dict(size=16),
        xaxis=dict(
            tickvals=list(range(0, 101, 20)),
            ticktext=[f"{i}%" for i in range(0, 101, 20)],
            range=[0, 100],
            title_standoff=12,
            tickfont=dict(size=10)
        ),
        yaxis=dict(tickfont=dict(size=12)),
        title=f'User Constraints for {year}',
        title_x=0.39  # This centers the title
    )

    # Store the plot to the dictionary with the key 'year'
    plots[f'constraints{year}'] = fig


# Callback
selected_year = st.radio('Year:', ['2020', '2021', '2022'], index=0)



if selected_year == '2020':
    st.write('In 2020, upfront costs, technical skills and time required were the most significant constraints.')
    
    st.plotly_chart(plots['constraints2020'])
        
elif selected_year == '2021':
    st.write('Compared to 2020, upfront costs is still the most significant constraint, but maintenance cost shifted from fourth place to become the second most pressing issue, while the newly introduced local access to suppliers is the thirs most pressing constraint.')
    
    st.plotly_chart(plots['constraints2021'])
    
    
else:
    st.write('Compared to 2021, upfront costs is still the most significant constraint, but local access to suppliers shifted from third place to become the second most pressing issue, while time required shifted from fifth to third place.')
    st.plotly_chart(plots['constraints2022'])
    
         
st.subheader(':blue[Developer constrainsts]')


############################################################
### Dev constrainst
############################################################

st.markdown('Tech developers in developing countries were also more likely to report significant constraints compared to their deveopled country counterparts. They were 3.5x as likely to rate  sourcing supplies and testing sites, and 2.5x as likely to rate securing seed funding as primary constraints.')

st.markdown('Female tech developers were also 2x more likely than male developers to report significant constraints regarding user data concerns,  2.5x as likely regarding both securing  continued funding and data access, and 3.5x as likely regarding accessing testing sites.')

st.markdown('When looking at developer constraints year by year, continued funding and seed funding are the two typically most significant constraints, but their order changes across the years. ')

st.caption('*Note: Likelihood figures are rounded.*')


# Define custom order and color mapping

color_values2 = ['#9F2A00', '#D32A00', '#F42A00', '#D9D9D9', '#F2F2F2']
ranking_order2 = dconst['ranking'].unique().tolist()

color_map2 = {ranking: color for ranking, color in zip(ranking_order2, color_values2)}

plots2 = {}  # Dictionary to store the plots

for year in [2020, 2021, 2022]:
    # Filter data for the current year
    filtered_data2 = dconst[dconst['year'] == year]
    dconst_order2 = filtered_data2['dconst'].tolist()

    # Create the bar chart
    fig = px.bar(filtered_data2,
                 x='percentage',
                 y='dconst',
                 color='ranking',
                 orientation='h',
                 category_orders={"dconst": dconst_order2},
                 color_discrete_map=color_map2)

    # Update layout
    fig.update_layout(
        showlegend=True,
        legend_title_text='Ranking',
        xaxis_title='',
        yaxis_title='',
        font=dict(size=16),
        xaxis=dict(
            tickvals=list(range(0, 101, 20)),
            ticktext=[f"{i}%" for i in range(0, 101, 20)],
            range=[0, 100],
            title_standoff=12,
            tickfont=dict(size=10)
        ),
        yaxis=dict(tickfont=dict(size=12)),
        title=f'Developer Constraints for {year}',
        title_x=0.39  # This centers the title
    )

    # Store the plot to the dictionary with the key 'year'
    plots2[f'constraints{year}'] = fig


# Callback
selected_year = st.radio('Year:', ['2020 ', '2021 ', '2022 ' ], index=0)



if selected_year == '2020 ':
    st.write('In 2020, continued funding and seed funding were similarily significant constraints for most developers, followed by understanding landscape.')
    
    st.plotly_chart(plots2['constraints2020'])
        
elif selected_year == '2021 ':
    st.write('There were no changes in the top 3 constraints in 2022 compared to 2021.')
    st.plotly_chart(plots2['constraints2021'])
    
    
else:
    st.write('In 2022')
    st.plotly_chart(plots2['constraints2022'])

st.divider()
st.header(':blue[Opportunities: What’s needed?]')

st.markdown('*Despite these challenges the community has remarkable hope for the future that only improved over time, and largely agrees on what needs to be done.*')

st.markdown('Almost two-thirds of survey respondents (63%) reported feeling more optimistic about the future of conservation technology relative to 12 months prior. This improves on results from both 2021 and 2020: in both years, about 52% indicated being optimistic. When asked to rank potential reasons for optimism, people indicated that the rate at which the field is evolving, the increasing accessibility of conservation technologies, and growing support most important, with 73%, 73%, and 43% respectively ranking them in their top three. In earlier years, collaborative culture was typically rated as the third reason for optimism.')

st.image('Input files/optimism.jpg')

st.markdown('When thinking about the opportunities the future brings, ...')

st.image('Input files/opportunities.jpg')

st.divider()
st.header(':blue[Moving forward]')

st.markdown('Future.. + quotes')

st.markdown('People look for advice -> online sources and other individuals -> WILDLABS -> we have a measurable impact')

st.image('Input files/wildlabs.jpg')

st.markdown('Some input from survey quotes, WILDLABS future plans')