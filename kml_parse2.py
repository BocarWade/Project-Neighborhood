from fastkml import kml
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd

INPUT_KML_FILE = "/Users/bocarwade/Documents/Project Neighborhood/Boundaries - Community Areas (current).kml"

df = pd.read_csv('demidecade_scores_kml.csv')
columns = df.columns
print(columns)
for col in columns:
	if col == "Community Area":
		continue
	#BAD with open(INPUT_KML_FILE, 'rt', encoding="utf-8") as myfile:
	data = open(INPUT_KML_FILE, 'rb')
	doc = data.read()
	doc = doc.decode('utf-8').encode('ascii')
	k = kml.KML()
	k.from_string(doc)
	k_tree = k.etree_element()
	for nhood in k_tree.iter('Placemark'):
		nhood_name = nhood[2][5][0].text
		nhood_name = nhood_name.title()
		if nhood_name == 'Ohare':
			nhood_name = "O'Hare"
		if nhood_name == "Mckinley Park":
			nhood_name = "McKinley Park"
		comm = df.loc[df["Community Area"] == nhood_name]
		score = comm[col].values
		print(nhood_name)
		print(comm[col])
		score =  score[0] -0.05
		print(score)
		color = 'neutral'
		if score < -0.05:
			color = "bad"
		if score < -0.15:
			color = 'veryBad'
		if score > 0.05:
			color = 'good'
		if score > 0.15:
			color = 'veryGood'
		color = '#' + color
		nhood[1].text = color
	k_root = k_tree.getroottree()
	filename = 'modified_nhoods_' + col + '.kml'
	k_root.write(open(filename, 'wb'))
		#print(row['Score Caterory (Down Shifted)'])