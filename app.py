# %% [markdown]
# # Lab Assignment 12: Interactive Visualizations
# ## DS 6001: Practice and Application of Data Science
# 
# ### Instructions
# Please answer the following questions as completely as possible using text, code, and the results of code as needed. Format your answers in a Jupyter notebook. To receive full credit, make sure you address every part of the problem, and make sure your document is formatted in a clean and professional way.

# %% [markdown]
# ## Problem 0
# Import the following libraries:

# %%
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import plotly.io as pio
pio.renderers.default = "vscode"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# For this lab, we will be working with the 2019 General Social Survey one last time.


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

# %% [markdown]
# Here is code that cleans the data and gets it ready to be used for data visualizations:

# %%
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

# %% [markdown]
# The `gss_clean` dataframe now contains the following features:
# 
# * `id` - a numeric unique ID for each person who responded to the survey
# * `weight` - survey sample weights
# * `sex` - male or female
# * `education` - years of formal education
# * `region` - region of the country where the respondent lives
# * `age` - age
# * `income` - the respondent's personal annual income
# * `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
# * `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
# * `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
# * `socioeconomic_index` - an index measuring the respondent's socioeconomic status
# * `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
# * `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
# * `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
# * `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
# * `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
# * `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."

# %% [markdown]
# ## Problem 1
# Our goal in this lab is to build a dashboard that presents our findings from the GSS. A dashboard is meant to be shared with an audience, whether that audience is a manager, a client, a potential employer, or the general public. So we need to provide context for our results. One way to provide context is to write text using markdown code.
# 
# Find one or two websites that discuss the gender wage gap, and write a short paragraph in markdown code summarizing what these sources tell us. Include hyperlinks to these websites. Then write another short paragraph describing what the GSS is, what the data contain, how it was collected, and/or other information that you think your audience ought to know. A good starting point for information about the GSS is here: http://www.gss.norc.org/About-The-GSS
# 
# Then save the text as a Python string so that you can use the markdown code in your dashboard later.
# 
# It should go without saying, but no plagiarization! If you summarize a website, make sure you put the summary in your own words. Anything that is copied and pasted from the GSS webpage, Wikipedia, or another website without attribution will receive no credit.
# 
# (Don't spend too much time on this, and you might want to skip it during the Zoom session and return to it later so that you can focus on working on code with your classmates.) [1 point]

# %%
markdown_text = '''
The [General Social Survey](http://www.gss.norc.org/About-The-GS) (GSS) is a nationally representative survey conducted in United States for adults.\
     It collects data about people's behaviors, opionions and attitudes. It helps in doing trend analysis of th edata since this survey is being conducted sicne 1972. 

Gender wage gap still holds true today, women get paid lesser than men. Teh data in GSS 2019 helps us explore the same. In general women earn only 83 cents for every dolalr men earn.\
    Though pay discriminaion is illegal in the United States, data tells us that women are still not earning the same.\
    source: [American Assication of Univeristy Women](https://www.aauw.org/resources/research/simple-truth). 
'''

# %% [markdown]
# ## Problem 2
# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

# %%
gss_1 = gss_clean[['income','sex','job_prestige','socioeconomic_index','education']]
gss_1_g = gss_1.groupby('sex').agg({'mean'}).round(2)
gss_1_g.columns=['mean_income','mean_occupational_prstg','mean_socioecon_index','mean_educ_years']
gss_1_g = gss_1_g.reset_index()
table = ff.create_table(gss_1_g)
# table.show()

# %% [markdown]
# ## Problem 3
# Create an interactive barplot that shows the number of men and women who respond with each level of agreement to `male_breadwinner`. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# %%
gss_2 = gss_clean.groupby(['sex','male_breadwinner'])['male_breadwinner'].size()
gss_2 = pd.DataFrame(gss_2)
gss_2.columns=['Response Count']
gss_2 = gss_2.reset_index()
fig1 = px.bar(gss_2, x='male_breadwinner', y='Response Count',color='sex',
            labels={'male_breadwinner':'Male Breadwinner'},
            #title = 'Male Breadwinner Response Counts by Sex',
            hover_data = ['sex', 'Response Count'],
            text='Response Count',barmode = 'group')
fig1.update_layout(showlegend=True)
fig1.update(layout=dict(title=dict(x=0.5)))
# fig1.show()

# %% [markdown]
# ## Problem 4
# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# %%
gss_3 = gss_clean[['job_prestige','income','sex','education','socioeconomic_index']]
fig2 = px.scatter(gss_3, x='job_prestige', y='income',color='sex', 
                 trendline='ols',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig2.update(layout=dict(title=dict(x=0.5)))
# fig2.show()

# %% [markdown]
# ## Problem 5
# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]

# %%
gss_4 = gss_clean[['job_prestige','income','sex']]
fig3 = px.box(gss_4, y='sex', x = 'income', color = 'sex',
                   labels={'income':'Income','sex':''})
fig3.update(layout=dict(title=dict(x=0.5),showlegend=False))
fig3.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))
# fig3.show()

# %%
fig4 = px.box(gss_4, y='sex', x= 'job_prestige', color = 'sex',
                   labels={'job_prestige':'Occupational Prestige','sex':' '})
fig4.update(layout=dict(title=dict(x=0.5),showlegend=False))
fig4.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))
# fig4.show()

# %% [markdown]
# ## Problem 6
# Create a new dataframe that contains only `income`, `sex`, and `job_prestige`. Then create a new feature in this dataframe that breaks `job_prestige` into six categories with equally sized ranges. Finally, drop all rows with any missing values in this dataframe.
# 
# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories. 
# 
# (If you want men to be represented by blue and women by red, you can include `color_discrete_map = {'male':'blue', 'female':'red'}` in your plotting function. Or use different colors if you want!) [3 points]

# %%
gss_5 = gss_clean[['job_prestige','income','sex']]
gss_5['job_prestige_grp'] = pd.cut(gss_5.job_prestige,6).astype(str)
gss_5 = gss_5.dropna().sort_values(by='job_prestige_grp')
fig5 = px.box(gss_5, x='sex', y='income', facet_col='job_prestige_grp', color='sex',
                 hover_data=['job_prestige_grp', 'sex', 'income'],facet_col_wrap=2,
                 #olor_discrete_map = {'male':'blue','female':'red'},
                 labels={'job_prestige_grp':'Occupational Prestige Groups'},
                 title = 'Incoem Distribution by Sex and Occupational Prestige',
                 width=1000, height=2000)
fig5.update(layout=dict(title=dict(x=0.5)))
fig5.update_layout(showlegend=False)
fig5.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))
# fig5.show()



# %% [markdown]
# ## Extra Credit (up to 10 bonus points)
# Dashboards are all about good design, functionality, and accessability. For this extra credit problem, create another version of the dashboard you built for problem 7, but take extra steps to improve the appearance of the dashboard, add user-inputs, and host it on the internet with its own URL.
# 
# **Challenge 1**: Be creative and use a layout that significantly departs from the one used for the ANES data in the module 12 notebook. A good place to look for inspiration is the [Dash gallery](https://dash-gallery.plotly.host/Portal/). We will award up to 3 bonus points for creativity, novelty, and style.
# 
# **Challenge 2**: Alter the barplot from problem 3 to include user inputs. Create two dropdown menus on the dashboard. The first one should allow a user to display bars for the categories of `satjob`, `relationship`, `male_breadwinner`, `men_bettersuited`, `child_suffer`, or `men_overwork`. The second one should allow a user to group the bars by `sex`, `region`, or `education`. After choosing a feature for the bars and one for the grouping, program the barplot to update automatically to display the user-inputted features. One bonus point will be awarded for a good effort, and 3 bonus points will be awarded for a working user-input barplot in the dashboard.
# 
# **Challenge 3**: Follow the steps listed in the module notebook to deploy your dashboard on Heroku. 1 bonus point will be awarded for a Heroku link to an app that isn't working. 4 bonus points will be awarded for a working Heroku link.

# %% [markdown]
# ## Challenge 2:
# **Grouping by years of eduation did not make sense aesthetically. Tehrefore created a years of education group variable instead. Figure 3 (bar plot) is moved to the end to add input features.**

# %%
gs_columns = ['satjob','relationship','male_breadwinner','men_bettersuited','child_suffer','men_overwork'] 
cat_columns = ['sex','region','educ_grp'] 

# %%
gss_dash_df = gss_clean[['satjob','relationship','male_breadwinner','men_bettersuited','child_suffer','men_overwork','sex','region','education']]
gss_dash_df['educ_grp'] = pd.cut(gss_dash_df.education,4).astype('str')
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Exploring the 2019 General Social Survey"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Comparing mean income, occupational prestige, socioeconomic index, years of education by Sex"),
        
        dcc.Graph(figure=table),

        html.Div([
            html.H2("Relationship between income and occupational prestige by Sex"),
        
                dcc.Graph(figure=fig2),

        ],style={'width': '70%', 'display': 'inline'}),
        
        html.Div([
            
            html.H2("Distribution of income by Sex"),
            
            dcc.Graph(figure=fig3)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Distribution of occupational prestige by Sex"),
            
            dcc.Graph(figure=fig4)
            
        ], style = {'width':'48%', 'float':'right'}),

           
        html.H2("Distribution of income by sex and occupational prestige groups"),
                
            dcc.Graph(figure=fig5),
        html.Div([
            html.H2("x-axis feature"),
                
                    dcc.Dropdown(id='x-axis',
                        options=[{'label': i, 'value': i} for i in gs_columns],value='male_breadwinner'),
                            
                html.H3("colors"),
                
                    dcc.Dropdown(id='colors',
                        options=[{'label': i, 'value': i} for i in cat_columns],value='sex'),

            ], style={'width': '25%', 'height':'100%', 'float': 'left'}),
            
            
            html.Div([
            html.H2("Men vs Women Responses - It is much better for everyone if man is breadwinner?"),
            
            dcc.Graph(id='dash_bar'),

            ],style={'width': '70%', 'float': 'right'})
    ]
)
@app.callback(Output(component_id="dash_bar",component_property="figure"), 
             [Input(component_id='x-axis',component_property="value"),
              Input(component_id='colors',component_property="value")])

def make_figure(x, colors):
    gss_dash = gss_dash_df.groupby([colors,x])[x].size()
    gss_dash = pd.DataFrame(gss_dash)
    gss_dash.columns=['Response Count']
    gss_dash = gss_dash.reset_index().sort_values(by=colors)
    fig = px.bar(gss_dash, x=x, y='Response Count',color=colors,
            hover_data = [colors, 'Response Count'],
            text='Response Count',barmode = 'group', 
            labels={'male_breadwinner':'Male Breadwinner',
                'child_suffer':'child Suffer', 'men_bettersuited':'Men Bettersuited', 
                'men_overwork': 'Men Overwork','educ_grp': 'Years of Education Groups', 
                })
    fig.update_layout(legend_title_text=colors)
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace(colors+"=", colors)))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')


