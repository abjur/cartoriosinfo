# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os

driver = webdriver.Firefox()
# %%

driver.get('https://cartorios.info')

# %%

# df_todos_links

for i in range(len(df_todos_links)):
  print(f'baixando {i} de {len(df_todos_links)}...')
  link_cidade = df_todos_links['link'].values[i]
  path_file = os.path.join('data/raw_selenium', link_cidade.split('/')[-1])
  if not os.path.exists(path_file):
    driver.get(link_cidade)
    # write to file
    with open(path_file, 'w') as f:
      f.write(driver.page_source)

# %%
