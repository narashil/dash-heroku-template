import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.io as pio
pio.renderers.default = "vscode"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import warnings
warnings.filterwarnings('ignore')


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",\
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',\
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

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


markdown_text = '''
The [General Social Survey](http://www.gss.norc.org/About-The-GS) (GSS) is a nationally representative survey conducted in United States for adults.\
     It collects data about people's behaviors, opionions and attitudes. It helps in doing trend analysis of th edata since this survey is being conducted sicne 1972. 

Gender wage gap still holds true today, women get paid lesser than men. Teh data in GSS 2019 helps us explore the same. In general women earn only 83 cents for every dolalr men earn.\
    Though pay discriminaion is illegal in the United States, data tells us that women are still not earning the same.\
    source: [American Assication of Univeristy Women](https://www.aauw.org/resources/research/simple-truth). 
'''

gss_1 = gss_clean[['income','sex','job_prestige','socioeconomic_index','education']]
gss_1_g = gss_1.groupby('sex').agg({'mean'}).round(2)
gss_1_g.columns=['mean_income','mean_occupational_prstg','mean_socioecon_index','mean_educ_years']
gss_1_g = gss_1_g.reset_index()
table = ff.create_table(gss_1_g)

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

gss_3 = gss_clean[['job_prestige','income','sex','education','socioeconomic_index']]
fig2 = px.scatter(gss_3, x='job_prestige', y='income',color='sex', 
                 trendline='ols',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig2.update(layout=dict(title=dict(x=0.5)))

gss_4 = gss_clean[['job_prestige','income','sex']]
fig3 = px.box(gss_4, y='sex', x = 'income', color = 'sex',
                   labels={'income':'Income','sex':''})
fig3.update(layout=dict(title=dict(x=0.5),showlegend=False))
fig3.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))

fig4 = px.box(gss_4, y='sex', x= 'job_prestige', color = 'sex',
                   labels={'job_prestige':'Occupational Prestige','sex':' '})
fig4.update(layout=dict(title=dict(x=0.5),showlegend=False))
fig4.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))

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


gs_columns = ['satjob','relationship','male_breadwinner','men_bettersuited','child_suffer','men_overwork'] 
cat_columns = ['sex','region','educ_grp'] 


gss_dash_df = gss_clean[['satjob','relationship','male_breadwinner','men_bettersuited','child_suffer','men_overwork','sex','region','education']]
gss_dash_df['educ_grp'] = pd.cut(gss_dash_df.education,4).astype('str')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
    app.run_server(debug=True, port=8051)


