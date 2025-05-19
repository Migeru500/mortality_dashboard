import plotly.express as px
import pandas as pd
import requests
import unicodedata

class GraphManager:
    def __init__(self):
        self.mortality_df = pd.read_csv("./../../data/NoFetal2019.csv")
        self.codes_df = pd.read_csv("./../../data/CodigosDeMuerte.csv")
        self.divipola_df = pd.read_csv("./../../data/Divipola.csv")

    def generate_deaths_by_month_line_graph(self):
        mortality_df = self.mortality_df.copy(deep=True)
        deaths_by_month = (
            mortality_df
            .groupby('MES')
            .size()
            .reset_index(name='TOTAL_MUERTES')
        )

        months = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        deaths_by_month['MES_NOMBRE'] = deaths_by_month['MES'].map(months)

        deaths_by_month = deaths_by_month.sort_values('MES')

        fig = px.line(
            deaths_by_month,
            x='MES_NOMBRE',
            y='TOTAL_MUERTES',
            title='Total de Muertes por Mes en Colombia (2019)',
            labels={
                'MES_NOMBRE': 'Mes',
                'TOTAL_MUERTES': 'Número de Muertes'
            }
        )

        fig.update_layout(
            xaxis_title='Mes',
            yaxis_title='Total de Muertes',
            xaxis_tickangle=-45
        )

        return fig
    
    def generate_most_violent_cities_bar_graph(self):
        mortality_df = self.mortality_df.copy(deep=True)
        divipola_df = self.divipola_df.copy(deep=True)
        homicide_codes = ['X93', 'X94', 'X95', 'Y09']
        df_homicidios = mortality_df[
            mortality_df['COD_MUERTE'].str[:3].isin(homicide_codes)
        ]

        homicides_by_municipalities = (
            df_homicidios
            .groupby(['COD_DEPARTAMENTO', 'COD_MUNICIPIO'])
            .size()
            .reset_index(name='TOTAL_HOMICIDIOS')
        )

        homicides_by_municipalities = homicides_by_municipalities.merge(
            divipola_df[['COD_DEPARTAMENTO', 'COD_MUNICIPIO', 'DEPARTAMENTO', 'MUNICIPIO']],
            on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'],
            how='left'
        )

        top5_cities = homicides_by_municipalities.sort_values(
            'TOTAL_HOMICIDIOS', ascending=False
        ).head(5)

        fig = px.bar(
            top5_cities,
            x='MUNICIPIO',
            y='TOTAL_HOMICIDIOS',
            color='MUNICIPIO',
            title='Top 5 Ciudades con Más Homicidios en Colombia (2019)',
            labels={
                'MUNICIPIO': 'Ciudad',
                'TOTAL_HOMICIDIOS': 'Número de Homicidios',
                'DEPARTAMENTO': 'Departamento'
            }
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            legend_title_text='Ciudad'
        )

        return fig
    
    def generate_least_mortality_cities_circle_graph(self):
        mortality_df = self.mortality_df.copy(deep=True)
        divipola_df = self.divipola_df.copy(deep=True)
        deaths_by_municipalities = (
            mortality_df
            .groupby(['COD_DEPARTAMENTO', 'COD_MUNICIPIO'])
            .size()
            .reset_index(name='TOTAL_MUERTES')
        )

        deaths_by_municipalities = deaths_by_municipalities.merge(
            divipola_df[['COD_DEPARTAMENTO', 'COD_MUNICIPIO', 'MUNICIPIO']],
            on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'],
            how='left'
        )

        deaths_by_municipalities = deaths_by_municipalities.dropna(subset=['MUNICIPIO'])

        bottom10 = deaths_by_municipalities.sort_values('TOTAL_MUERTES', ascending=True).head(10)

        fig = px.pie(
            bottom10,
            names='MUNICIPIO',
            values='TOTAL_MUERTES',
            title='10 Ciudades con Menor Número de Muertes en Colombia (2019)',
            hole=0.3
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            legend_title_text='Ciudad',
            margin=dict(t=50, b=0, l=0, r=0)
        )

        return fig
    
    def generate_principal_death_reasons_table(self):
        mortality_df = self.mortality_df.copy(deep=True)
        codes_df = self.codes_df.copy(deep=True)
        mortality_df['COD_MUERTE'] = mortality_df['COD_MUERTE'].where(
        mortality_df['COD_MUERTE'].str.len() != 3,
        mortality_df['COD_MUERTE'] + 'X')

        counter = (
            mortality_df
            .groupby('COD_MUERTE')
            .size()
            .reset_index(name='TOTAL_CASOS')
        )

        top10 = (
            counter
            .merge(codes_df, on='COD_MUERTE', how='left')
            .sort_values('TOTAL_CASOS', ascending=False)
            .head(10)
            .reset_index(drop=True)
        )

        return top10
    
    def set_quinquenio(self, codigo):
        if 0 <= codigo <= 8:
            return '0-4'
        if codigo == 9:
            return '5-9'
        if codigo == 10:
            return '10-14'
        if codigo == 11:
            return '15-19'
        if codigo == 12:
            return '20-24'
        if codigo == 13:
            return '25-29'
        if codigo == 14:
            return '30-34'
        if codigo == 15:
            return '35-39'
        if codigo == 16:
            return '40-44'
        if codigo == 17:
            return '45-49'
        if codigo == 18:
            return '50-54'
        if codigo == 19:
            return '55-59'
        if codigo == 20:
            return '60-64'
        if codigo == 21:
            return '65-69'
        if codigo == 22:
            return '70-74'
        if codigo == 23:
            return '75-79'
        if codigo == 24:
            return '80-84'
        if 25 <= codigo <= 28:
            return '85+'
        return None
    
    def generate_age_histogram_graph(self):
        mortality_df = self.mortality_df.copy(deep=True)
        mortality_df['EDAD_GRUPO'] = mortality_df['GRUPO_EDAD1'].apply(self.set_quinquenio)

        mortality_df = mortality_df.dropna(subset=['EDAD_GRUPO'])

        counter = (
            mortality_df
            .groupby('EDAD_GRUPO')
            .size()
            .reset_index(name='TOTAL_MUERTES')
        )

        orden = ['0-4','5-9','10-14','15-19','20-24','25-29',
                '30-34','35-39','40-44','45-49','50-54','55-59',
                '60-64','65-69','70-74','75-79','80-84','85+']
        counter['EDAD_GRUPO'] = pd.Categorical(counter['EDAD_GRUPO'], categories=orden, ordered=True)
        counter = counter.sort_values('EDAD_GRUPO')

        fig = px.bar(
            counter,
            x='EDAD_GRUPO',
            y='TOTAL_MUERTES',
            title='Distribución de Muertes por Rango de Edad Quinquenal (Colombia, 2019)',
            labels={'EDAD_GRUPO': 'Rango de Edad (años)', 'TOTAL_MUERTES': 'Número de Muertes'},
            text='TOTAL_MUERTES'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickangle=-45, bargap=0.2)
        return fig
    
    def generate_gender_stacked_bar_graph(self):
        mortality_df = self.mortality_df.copy(deep=True)
        divipola_df = self.divipola_df.copy(deep=True)
        gender_map = {
            1: 'Masculino',
            2: 'Femenino',
            3: 'Indeterminado'
        }
        mortality_df['SEXO_LABEL'] = mortality_df['SEXO'].map(gender_map)

        counter = (
            mortality_df
            .groupby(['COD_DEPARTAMENTO', 'SEXO_LABEL'])
            .size()
            .reset_index(name='TOTAL_MUERTES')
        )

        counter = counter.merge(
            divipola_df[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates(),
            on='COD_DEPARTAMENTO',
            how='left'
        )
        
        counter['DEPARTAMENTO'] = pd.Categorical(
            counter['DEPARTAMENTO'],
            categories=sorted(counter['DEPARTAMENTO'].unique()),
            ordered=True
        )

        fig = px.bar(
            counter,
            x='DEPARTAMENTO',
            y='TOTAL_MUERTES',
            color='SEXO_LABEL',
            title='Comparación del Total de Muertes por Sexo y Departamento (Colombia, 2019)',
            labels={
                'DEPARTAMENTO': 'Departamento',
                'TOTAL_MUERTES': 'Número de Muertes',
                'SEXO_LABEL': 'Sexo'
            },
            category_orders={'SEXO_LABEL': ['Masculino', 'Femenino', 'Indeterminado']}
        )

        fig.update_layout(
            barmode='stack',
            xaxis_tickangle=-45,
            legend_title_text='Sexo',
            margin=dict(t=50, b=100, l=50, r=50)
        )

        return fig
    
    def change_tildes(self, text):
        return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    def generate_deaths_by_department_map_graph(self):
        mortality_df = self.mortality_df.copy(deep=True)
        divipola_df = self.divipola_df.copy(deep=True)

        divipola_df['DEPARTAMENTO'] = divipola_df['DEPARTAMENTO'].replace({'BOGOTÁ, D.C.': 'SANTAFE DE BOGOTA D.C'})
        divipola_df['DEPARTAMENTO'] = divipola_df['DEPARTAMENTO'].apply(self.change_tildes)
        divipola_df['DEPARTAMENTO'] = divipola_df['DEPARTAMENTO'].replace({'NARINO': 'NARIÑO'})

        deaths_by_department = (
            mortality_df
            .groupby('COD_DEPARTAMENTO')
            .size()
            .reset_index(name='TOTAL_MUERTES')
        )

        deaths_by_department = deaths_by_department.merge(
            divipola_df,
            on='COD_DEPARTAMENTO',
            how='left'
        )

        url_geojson = (
            'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
        )
        
        geojson_dpto = requests.get(url_geojson).json()

        fig = px.choropleth(
            deaths_by_department,
            geojson=geojson_dpto,
            locations='DEPARTAMENTO',
            featureidkey='properties.NOMBRE_DPT',
            color='TOTAL_MUERTES',
            color_continuous_scale='Viridis',
            projection='mercator',
            title='Distribución Total de Muertes por Departamento (Colombia, 2019)',
            labels={'TOTAL_MUERTES':'Número de Muertes'}
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

        return fig
