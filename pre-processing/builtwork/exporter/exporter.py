import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import sys
import os
load_dotenv()

q='query.sql'

#connect to db via .env
conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST'), 
    dbname=os.getenv('POSTGRES_DATABASE'),
    user=os.getenv('POSTGRES_USERNAME'),
    password=os.getenv('POSTGRES_PASSWORD'))

#get all tables
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
dict_cur.execute(open(q).read())

data = dict_cur.fetchall()

f=open('data.tsv', 'w')
#Removed height and material because sansecondo_island_1500 doesn't have it. haven't controller others
#BW_ID	IslandName	Date	Start	End	Name	Function	Start_Function	End_Function	Use	Start_Use	End_Use	Typology	Start_Typology	End_Typology	Material	Architect	Patron	Owner	Start_Owner	End_Owner	Tenant	Start_Tenant	End_Tenant	SHP_Lenght	SHP_Area
cols = ['"BW_ID"', '"geometry"', '"IslandName"','"Date"','"Start"','"End"','"Name"','"Function"','"Start_Function"','"End_Function"','"Use"','"Start_Use"','"End_Use"','"Typology"','"Start_Typology"','"End_Typology"','"Material"','"Architect"','"Patron"','"Owner"','"Start_Owner"','"End_Owner"','"Tenant"','"Start_Tenant"','"End_Tenant"','"SHP_Lenght"','"SHP_Area"']

for tab in data:
    dict_cur.copy_to(f, tab[0], sep='\t', null='', columns=cols)

dict_cur.close()
conn.close()