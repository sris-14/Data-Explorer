import pandas as pd
from ydata_profiling import ProfileReport
bio_df = pd.read_csv('D:\\Olympics-api\\Olympic_Athlete_Bio.csv')
event_df = pd.read_csv('D:\\Olympics-api\\Olympic_Athlete_Event_Result.csv') 

# Generate reports separately
profile1 = ProfileReport(bio_df, explorative=True)
profile1.to_file("olympics_data1_report.html")

profile2 = ProfileReport(event_df, explorative=True)
profile2.to_file("olympics_data2_report.html")
