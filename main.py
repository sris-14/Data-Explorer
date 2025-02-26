from fastapi import FastAPI
import pandas as pd

app = FastAPI()


# datasets
bio_df = pd.read_csv('Olympic_Athlete_Bio.csv')
event_df = pd.read_csv('Olympic_Athlete_Event_Result.csv')




# print(bio_df.columns)
print(bio_df[['country_noc']].head())  # Print first few rows


@app.get('/')
def home():
    return {'message':'Welcome to the Olympics Data API'}

@app.get('/athletes')
def get_atheletes(country: str):
    print(f"Received country: {country}") 
    res = bio_df[bio_df['country_noc']== country][['name','gender','born','description','special_notes']]
    print(f"Filtered Data:\n{res}")
    if res.empty:
        return {'error': 'No athletes found for the given country'}
    return {'athletes':res.to_dict(orient='records')}

@app.get('/medals')
def get_medals(year: int):
    filtered_df = event_df[event_df['year'] == year]
    medal_count = filtered_df.groupby(['country_noc','medal']).size().reset_index(name='count')
    return {'medal_data': medal_count.to_dict(orient='records')}

@app.get('/athlete/{athlete_id}')
def get_athelete(athlete_id : int):
    result = bio_df[bio_df['athlete_id']== athlete_id]
    if result.empty:
        return {'error':'Athlete not found'}
    return result.to_dict(orient='records')[0]