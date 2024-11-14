# %%
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

def pegar_estados():
  u = 'https://cartorios.info/'
  r = requests.get(u)
  soup = BeautifulSoup(r.text, 'html.parser')
  ul = soup.find('ul', {'id': 'Menu'})
  links = ul.find_all('a')
  lst = []
  for l in links:
    lst.append([l['href'], l.text])
  # transform into pandas df
  df = pd.DataFrame(lst, columns=['link', 'text'])
  df = df[df['link'] != 'https://cartorios.info/']
  df = df[df['link'] != 'javascript:void(0);']
  return df


# %%
def pegar_cidades(link_uf):
  # link_uf = df[df['text'] == 'AC - Cartórios no Acre']['link'].values[0]
  r = requests.get(link_uf)
  soup = BeautifulSoup(r.text, 'html.parser')
  divs = soup.find_all('div', {'class': 'cidades'})
  links = [d.find('a') for d in divs]
  lst = []
  for l in links:
    lst.append(['https://cartorios.info/' + l['href'], l.text])
  df = pd.DataFrame(lst, columns=['link', 'text'])
  return df

# %%
df = pegar_estados()
todos_links = [pegar_cidades(link) for link in df['link'].values]
df_todos_links = pd.concat(todos_links)

# %%

def baixar_cidade(link_cidade, path):
  # path is a folder path.
  # create folder if it doesn't exist
  if not os.path.exists(path):
    os.makedirs(path)
  r = requests.get(link_cidade)
  # create file name from link_cidade and path
  path_file = os.path.join(path, link_cidade.split('/')[-1])
  # write file
  with open(path_file, 'wb') as f:
    f.write(r.content)

# %%

for i in range(len(df_todos_links)):
  print(f'baixando {i} de {len(df_todos_links)}...')
  link_cidade = df_todos_links['link'].values[i]
  baixar_cidade(link_cidade, 'data/raw')


# %%

files = [os.path.join('data/raw', f) for f in os.listdir('data/raw')]
files[0]

# %%

with open(files[0]) as f:
  soup = BeautifulSoup(f, 'html.parser')

print(files[0])



# break by br, remove empty strings and create a 'name' and 'value' columns
# using a colon : as separator





# transform into pandas df




# %%

def parse_file(file):
  #file = 'data/raw/cartorios-de-pindoba-al.html'
  with open(file) as f:
    soup = BeautifulSoup(f, 'html.parser')
  x = soup.find_all('div', id = re.compile('vara-|judici'))
  df_lst = []
  if (len(x) > 0):
    for i in range(len(x)):
      lst = re.split(r'\n|☏|Respons', x[i].text)
      lst = [l for l in lst if l != '']
      lst = [l.split(':', 1) for l in lst]
      lst = [l for l in lst if len(l) == 2]
      df = pd.DataFrame(lst, columns=['name', 'value'])
      df['file'] = file
      df['id'] = i
      df_lst.append(df)
    df = pd.concat(df_lst)
  else:
    df = pd.DataFrame()
  return df
# %%
df_full = pd.DataFrame()

for file in files:
  print(f'parsing {file}...')
  df = parse_file(file)
  df_full = pd.concat([df_full, df])

# %%

df_full
# %%
# create dir
if not os.path.exists('data/tidy'):
  os.makedirs('data/tidy')
df_full.to_csv('data/tidy/cartorios.csv', index=False)
# %%
