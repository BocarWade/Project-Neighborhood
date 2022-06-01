from fastkml import kml
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd

INPUT_KML_FILE = "/Users/bocarwade/Documents/Project Neighborhood/Boundaries - Community Areas (current).kml"


#BAD with open(INPUT_KML_FILE, 'rt', encoding="utf-8") as myfile:
data = open(INPUT_KML_FILE, 'rb')
doc = data.read()
doc = doc.decode('utf-8').encode('ascii')
k = kml.KML()
k.from_string(doc)
features = list(k.features())

#print(features[0].get_style_by_url('#defaultStyle').to_string())
#print(features[0].append_style())
f2 = list(features[0].features())
#print(f2[0])
nhoods = list(f2[0].features())
# print(nhoods)
df = pd.read_csv('total_scores_kml.csv')
rows = set()
k_tree = k.etree_element()
for nhood in k_tree.iter('Placemark'):
	nhood_name = nhood[2][5][0].text
	nhood_name = nhood_name.title()
	if nhood_name == 'Ohare':
		nhood_name = "O'Hare"
	if nhood_name == "Mckinley Park":
		nhood_name = "McKinley Park"
	row = df.loc[df["Community Area"] == nhood_name]
	color = row['Score Caterory (Down Shifted)']
	print(nhood_name)
	color = color.values[0]
	print(color)
	if color == 'very good':
		color = 'veryGood'
	if color == 'very bad':
		color = 'veryBad'
	color = '#' + color
	nhood[1].text = color
k_root = k_tree.getroottree()
k_root.write(open('modified_nhoods.kml', 'wb'))
	#print(row['Score Caterory (Down Shifted)'])