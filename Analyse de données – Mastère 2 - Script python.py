#!/usr/bin/env python
# coding: utf-8

# ## EXAMEN Analyse de donnée avec Python :
# ### Sujet : Scrapper l'ensemble des informations des produits du site open food facts.
# https://fr.openfoodfacts.org
# 
# #### Année : 2020 - 2021

# #### Présenté par :
# | Prénoms       |     Nom         |   
# | ------------- |: -------------: |
# | Aboubacar Sidiki        |        SIDIBE        |
# 
# GROUPE GEMA / IA-SCHOOL

# ### Procédures de scrapping
# 1. Récupérer les url des produits de la page 1
# 2. Récupérer les url des produits sur toutes les pages
# 3. Récupérer pour chaque produits, les informations demandées
# 4. Généralisation ie parcourir l'ensemble des pages pour récupérer les informations demandées

# In[1]:


#### import des modules
import requests
from bs4 import BeautifulSoup
from IPython import get_ipython
import unicodedata
import re
import numpy as np
import time
import traceback
import datetime


# In[2]:


urlOpenFoodFact = "https://fr.openfoodfacts.org" #### lien du site open food facts


# 1. Récupérer les url des produits de la page 1

# In[3]:


#### en-tête html utilisée pour la coordination entre le client (navigateur) et le serveur de open food fact, simule le comportement d'un navigateur
headers = {"Accept": "image/webp,*/*",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
			"Connection": "keep-alive",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
		}


# In[4]:


res = requests.get(urlOpenFoodFact, headers = headers) #### exécute la requêtte get et renvoie la donnée non structuré pour python


# In[5]:


soupOpenFoodFacts = BeautifulSoup(res.text, 'html.parser') #### parsing du text en html à l'aide de BeautifulSOup


# In[6]:


productContent = soupOpenFoodFacts.find_all('div', attrs={'id':'search_results'})[0] #### Récupération du contenu de la balise qui contient la liste des produits


# In[8]:


list_of_produits = productContent.find_all('a', attrs={'class':''}) #### Récupération de la liste des produits


# In[9]:


len(list_of_produits) #### 100 produits récupérés sur la page


# In[10]:


list_of_produits[0] #### prémier élément de la liste des produits


# In[11]:


list_of_produits[0]['href'] #### Premier url associé à la premier balise de la page 1


# In[12]:


list_of_produits[1]['href'] #### Deuxième url associé à la premier balise de la page 2


# In[13]:


#### récupérer les urls des produits de la page 1
#### on concatène la partie générique du site avec l'url de chaque
list_of_urls_product = []
for i in range(len(list_of_produits)): #### Pour chaque élément de 0 à 100 (list_of_produits = 100)
    list_of_urls_product.append(urlOpenFoodFact+list_of_produits[i]['href']) #### ajout de lien du produit dans la liste des urls de produit


# 2. Récupérer les url des produits sur toutes les pages

# a) Récupération du numéro de la dernière page du site

# In[14]:


paginationContent = soupOpenFoodFacts.find_all('ul', attrs={'class':'pagination'})[0] #### Récupération du contenu de la balise qui contient la pagination
num_of_last_page = paginationContent.find_all('a')[-2].text #### Récupération du numéro de la dernière page
num_of_last_page = int(num_of_last_page) #### convertion de la chaine en numérique
num_of_last_page #### nombre de page disponible à l'exécution


# b) Construction de tous les liens de la pagination

# In[15]:


tmps1=time.time()
####

list_of_urls_page = []
list_of_urls_page.append(urlOpenFoodFact) #### Ajout du premier url
for i in range(2, num_of_last_page+1): #### Pour chaque élément de 2 à num_of_last_page
    list_of_urls_page.append(urlOpenFoodFact+"/"+str(i)) #### ajout du lien de la page à la liste des urls des pages
    
####
tmps2=time.time()-tmps1
print("Temps d'execution = %f" %tmps2)


# In[16]:


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%dh %02dmn %02ds" % (hour, minutes, seconds)


# In[17]:


len(list_of_urls_page) #### nombre total de lien trouvé


# c) Construction de tous les liens de tous les produits

# In[17]:


tmps1=time.time()

products_list = [] #### liste vide des liens des produits d'une page
all_products_list = [] #### liste vide de tous les liens de tous les produits de toutes les pages
for i in range(len(list_of_urls_page)): #### Pour chaque élément de 0 au nombre de page
    res = requests.get(list_of_urls_page[i]) #### on exécute la requête pour obtenir les données non structurées
    soupOpenFoodFacts = BeautifulSoup(res.text, 'html.parser') #### on parse le texte en html
    productContent = soupOpenFoodFacts.find_all('div', attrs={'id':'search_results'})[0] #### on isolé le block qui contient les produits
    products_list = productContent.find_all('a', attrs={'class':''}) #### on récupère la liste de tous les produits
    for j in range(len(products_list)): #### pour élément de la liste de produits trouvés
        all_products_list.append(urlOpenFoodFact+products_list[j]['href']) #### on ajoute le lien du produit dans la liste globale

tmps2=time.time()-tmps1
print("Temps d'execution de récupération de tous les liens des produits = "+convert(tmps2))

len(all_products_list) #### le nombre total de produits trouvés


# In[18]:


tmps1=time.time()

#### export en csv des la liste des liens des produits trouvés
import pandas as pd
df = pd.DataFrame(all_products_list, columns=['images_url'])
df.to_csv('images_url.csv', index=False, encoding='utf-8')

####
tmps2=time.time()-tmps1
print("Temps d'execution export dataframe images urls = "+convert(tmps2))


# 3. Récupérer pour chaque produits, les informations demandées

# In[18]:


labels_caracteristic_id = ['denomination_generique',
 'quantite',
 'conditionnement',
 'marques',
 'categories',
 'labels_certifications_recompenses',
 'origine_des_ingredients',
 'lieux_de_fabrication_ou_de_transformation',
 'code_de_tracabilite',
 'lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant',
 'magasins',
 'pays_de_vente'] #### liste les labels des caractéristiques des produits transformés en id

labels_sub_trace_id = ['substances_ou_produits_provoquant_des_allergies_ou_intolerances','traces_eventuelles'] #### liste les labels des Substances ou produits des produits transformés en id
labels_details_analysis = ['additifs', 'vitamines_ajoutees', 'mineraux_ajoutes'] #### liste les labels des Analyse des ingrédients des produits transformés en id


# In[19]:


def index_in_list(a_list, index):
    """
    vérifie si l'index existe dans une liste
    
    :param a_list : la liste
    :type a_list : List
    
    :returns : resultat de la vérification 1 si l'index est trouvé sinon 0.
    :rtype : boolean.
    """
    return index < len(a_list)


# In[20]:


def transform_label_to_id(caracteristic_list):
    """    
    tranforme les labels de liste en un id
    
    :param  caracteristic_list : la liste contenant les labels.
    :type caracteristic_list : List.

    :returns : la liste avec les labels_id.
    :rtype : List.
    """
    for i in range(len(caracteristic_list)):
        caracteristic_list[i][0] = text_to_id(caracteristic_list[i][0])
    return caracteristic_list


# In[21]:


def split_list_with_xa0(list_el):
    """
    Split les chaines de caractères disponibles dans une liste. La valeur du split est '\xa0:'
    
    :param list_el : liste des chaines de caractères
    :type list_el : List
    
    :return : la liste des chaines de caractères splitées
    :rtype : List
    """
    return list(map(lambda x: x.text.split('\xa0:'),list_el))


# In[22]:


def check_string_exist(el, list_el):
    """    
    vérifie si un élément existe dans la liste
    
    :param el : L'element à rechercher dans la liste.
    :type el : String.
    :param list_el : la liste dans liste le recherche doit être effectuée.
    :type list_el : list.

    :returns : le resultat de la recherche sous forme boolean.
    :rtype : Boolean.
    """
    return list_el.count(el) > 0


# In[23]:


def strip_accents(text):
    """
    Supprime les accents dans une chaîne de caractère.

    :param text : La chaîne de caractères d'entrée.
    :type text : Chaîne.

    :returns : La chaîne de caractères traitée.
    :rtype : String.
    """
    try:
        text = unicode(text, 'utf-8') #### chaque caractère est codé par un codepoint UTF-8 représenté par un nombre hexadécimal
    except (TypeError, NameError):
        pass #### on continue si il y une erreur
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore') #### transforme une str en bytes
    text = text.decode("utf-8") #### transforme les bytes en str
    return str(text) #### conversion de la valeur retournée en string


# In[24]:


def text_to_id(text):
    """
    Convertit le texte d'entrée en identifiant.

    :param text : La chaîne de caractères d'entrée.
    :type text : Chaîne.

    :returns : La chaîne de caractères traitée.
    :rtype : String.
    """
    text = strip_accents(text.lower()) #### on supprime les accents
    text = re.sub('[ ]+', '_', text) #### on remplace les espaces par un tiret de 8 (_)
    text = re.sub('[^0-9a-zA-Z_-]', '', text) #### on supprime les valeurs numériques
    return text #### l'identifiant de la chaine est retourné


# In[26]:


def get_label_id_list(label_list):
    """    
    récupère la liste des label_id contenu dans la liste
    
    :param  label_list : la liste contenant les labels_id.
    :type label_list : List.

    :returns : la liste avec les labels_id.
    :rtype : List.
    """
    label_id_list = [] #### on initialise la liste des id
    for i in range(len(label_list)): #### pour chaque élément de la liste
        label_id_list.append(text_to_id(label_list[i][0].strip())) #### on ajoute dans la liste les ids récuperés
    return label_id_list


# In[27]:


def delete_detail_value(list_el):
    """
    Supprime dans la liste l'élément dont la valeur est égale à '_detail_de_lanalyse_des_ingredients__'
    
    :param list_el : liste des éléments
    :type list_el : List
    
    :return : la liste sans la valeur du filtre
    :rtype : List
    """
    index_list = []
    for i in range(len(list_el)): #### pour chaque élément de la liste
        value = str(list_el[i][0])
        if(value == '_detail_de_lanalyse_des_ingredients__' or value == '_detail_de_lanalyse_des_ingredients__nous_avons_besoin_de_votre_aide_' or value == '_si_ce_produit_a_une_liste_dingredients_en_francais_merci_de_lajouter_modifier_la_fiche'): #### on vérifie si le premier élément est égale à '_detail_de_lanalyse_des_ingredients__'
             index_list.append(i) #### on stock l'index du item à supprimer dans la liste
    for j in index_list: del list_el[j] #### on supprime l'élément de la liste à l'index indiqué
    return list_el


# In[28]:


def get_value_from_list(key, list_el):
    """    
    récupère la valeur associée à la clé passée en paramètre dans le dictionnaire
    
    :param  list_el : la liste des valeurs.
    :type list_el : List.
    
    :param  key : la clé.
    :type key : string

    :returns : la valeur associée à la clé du dictionnaire.
    :rtype : String.
    """
    list_el = delete_detail_value(list_el)
    list_el_dict = dict(list_el) #### on convertie la liste en dictionnaire
    return list_el_dict[key].strip() #### on retourne la valeur du dictionnaire donc la clé est 'key'


# In[29]:


def build_caracteritics_product_values(label_id_list,list_el):
    """    
    récupère la liste des label_id contenu dans la liste
    
    :param  label_list : la liste des éléments
    :type label_list : List.
    
    :param  label_id_list : la liste des ids.
    :type label_list : List.

    :returns : la liste avec les labels_id.
    :rtype : List.
    """
    all_caracteristic_list = [] #### on initialise la liste à retourner
    list_el = split_list_with_xa0(list_el) #### on split les contenus de la liste
    list_el = transform_label_to_id(list_el) #### on transforme les labels de la liste en id
    caracteristic_list_id = get_label_id_list(list_el) #### on récupère la liste des labels
    for i in range(len(label_id_list)): #### pour chaque élément de la liste des ids
        if check_string_exist(label_id_list[i], caracteristic_list_id): #### on vérifie si un élément de la label_id_list à la position i se trouve dans la liste id
            all_caracteristic_list.append([label_id_list[i],get_value_from_list(label_id_list[i], list_el)]) #### on ajoute la valeur de la clé trouve dans le dictionnaire
        else: #### sinon
            all_caracteristic_list.append([label_id_list[i],'XXX']) #### on ajoute la valeur 'XXX'
    return dict(all_caracteristic_list)


# In[30]:


def parse_string(value):
    """
    Parse la chaine en supprimant \n \t \r
    
    :param value : la valeur de la chaine à parser
    :type value : String
    
    :return : la chaine parsée
    :rtype : String
    """
    if value is np.nan:
        return value
    else:
        chaine = value.replace('\n', ',')
        chaine = " ".join(chaine.split()).rstrip(',').strip(',').strip()
        return chaine


# In[31]:


def get_ingredient_analysis(content):
    """
    récupère l'analyse des ingrédients à partir du contenu
    
    :param content : le block contenant le resulta de l'analyse
    :type content : list html
    
    :return : 
    """
    if len(content) == 0:
        return {'ingredients_analysis': 'XXX'}
    content_split = split_list_with_xa0(content)
    for el in content_split:
        el[1] = parse_string(el[1])
    return {'ingredients_analysis': el[1]}


# In[32]:


def get_compare_value(label_list, value_list):
    """    
    récupère la comparaison avec les valeurs moyennes des produits de même catégorie
    
    :param  label_list : la liste des labels
    :type label_list : List.
    
    :param  value_list : la liste des valeurs.
    :type value_list : List.

    :returns : la chaine contenant les valeurs moyennes.
    :rtype : String.
    """
    compare_value = ''
    if len(value_list) > len(label_list):
        value_list = value_list[1:0]
    for i in range(len(compare_label_list)):
        compare_value = (compare_label_list[i]+compare_value_list[i]) + ',' + compare_value if len(compare_label_list) and len(compare_value_list) else 'XXX'
    return compare_value if compare_value != '' else 'XXX'


# In[33]:


def get_infos_nutri(tr_table):
    """    
    récupère la table sur les informations nutritionnelles
    
    :param  tr_table : la liste des éléments de la table.
    :type tr_table : List.

    :returns : un dictionnaire de données.
    :rtype : List.
    """
    item = []
    all_items = []
    if len(tr_table) == 0:
            return [['energie_kj', 'XXX'],['energie_kcal', 'XXX'],['energie', 'XXX'],['matieres_grasses__lipides', 'XXX'],['glucides', 'XXX'],['proteines', 'XXX'],['sel', 'XXX'],['score_nutritionnel_-_france', 'XXX']]
    for i in range(len(tr_table)):
        item = []
        item.append(text_to_id(parse_string(tr_table[i].find('td', attrs={'class':'nutriment_label'}).text)))
        item.append(parse_string(tr_table[i].find('td', attrs={'class':'nutriment_value'}).text if tr_table[0].find('td', attrs={'class':'nutriment_value'}) else 'XXX'))
        all_items.append(item)
    return dict(all_items)


# In[34]:


soupProduct = BeautifulSoup(requests.get('https://fr.openfoodfacts.org/produit/3017620422003/nutella-ferrero').text, 'html.parser') #### récupération du html et parsing


# In[35]:


contentInfos = soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})[0] if len(soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})) else soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/DietarySupplement'})[0] if len(soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})[0] if len(soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})) else soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/DietarySupplement'})) else [] #### récupération de la balise qui contient les informations démandées


# In[36]:


#### nova score
contentInfos.find_all('a',href='/nova')[1].find('img')['alt'].split('-')[0].strip() if index_in_list(contentInfos.find_all('a',href='/nova'),1) else 'XXX'


# In[37]:


#### nutriscore
contentInfos.find_all('a',href='/nutriscore')[1].find('img')['alt'].split(':')[1].strip() if index_in_list(contentInfos.find_all('a',href='/nutriscore'),1) else 'XXX'


# In[38]:


#### ecoscore
contentInfos.find_all('a',href='/ecoscore')[2].find('img')['alt'].split(' ')[1].strip() if index_in_list(contentInfos.find_all('a',href='/ecoscore'),1) else 'XXX'


# In[39]:


#### Nom du Produit
contentInfos.find_all('h1', attrs={'property':'food:name'})[0].text


# In[40]:


#### Code-barres (EAN/EAN-13)
contentInfos.find_all('span', attrs={'property':'food:code'})[0].text if index_in_list(contentInfos.find_all('span', attrs={'property':'food:code'}),0) else 'XXX'


# In[41]:


caracteristicsContent = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[0] #### block qui contient les informations sur les caractéristiques d'un produit


# In[43]:


#### caractéristiques des produits
caracteristic_list = caracteristicsContent.findAll('p') #### on récupère le bloc qui contient les caractéristiques des produits
build_caracteritics_product_values(labels_caracteristic_id, caracteristic_list) #### on construit un dictionnaire avec les valeurs trouvées


# In[44]:


ingredientsContent = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[1]


# In[45]:


#### liste des ingrédients
ingredient_list = ingredientsContent.find_all('div', attrs={'property':'food:ingredientListAsText'})[0].text if ingredientsContent.find_all('div', attrs={'property':'food:ingredientListAsText'}) else 'XXX'
ingredient_list


# In[46]:


#### Substances ou produits provoquant des allergies ou intolérances :
sub_trace_list = ingredientsContent.find_all('p', attrs={'class':'', 'id':''})[:2]
build_caracteritics_product_values(labels_sub_trace_id, sub_trace_list)


# In[47]:


#### Analyse des ingrédients :
ingredients_analysis = ingredientsContent.find_all('p', attrs={'id':'ingredients_analysis'})
get_ingredient_analysis(ingredients_analysis)


# In[48]:


#### Détail de l'analyse des ingrédients:
detail_analysis = ingredientsContent.find_all('div', attrs={'class':'columns'})


# In[49]:


build_caracteritics_product_values(labels_details_analysis, detail_analysis)


# In[50]:


nutritionnelle_content = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[2] if len(contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})) != 0 else []


# In[51]:


#### Repères nutritionnels pour 100 g
repere_nutri = parse_string(nutritionnelle_content.find_all('div', attrs={'class':'small-12 xlarge-6 columns'})[1].text).split(',,,,')[1].strip() if index_in_list(nutritionnelle_content.find_all('div', attrs={'class':'small-12 xlarge-6 columns'}),1) and index_in_list((nutritionnelle_content.find_all('div', attrs={'class':'small-12 xlarge-6 columns'})[1].text).split(',,,,'),1) else 'XXX'


# In[52]:


#### Comparaison avec les valeurs moyennes des produits de même catégorie : 
compare_label_list = list(map(lambda x: parse_string(x.text), nutritionnelle_content.find_all('label')))[:-2] if len(nutritionnelle_content) != 0 else [] 


# In[53]:


compare_value_list = list(map(lambda x:x.text.strip(), nutritionnelle_content.find_all('a' , attrs={'title':''}))) if nutritionnelle_content.find_all('a' , attrs={'title':''}) and len(nutritionnelle_content) else []


# In[54]:


get_compare_value(compare_label_list, compare_value_list)


# In[55]:


nutritionnelle_table = nutritionnelle_content.find_all('table', attrs={'id':'nutrition_data_table', 'class':'data_table'})[0] if nutritionnelle_content and nutritionnelle_content.find_all('table', attrs={'id':'nutrition_data_table', 'class':'data_table'}) else []


# In[56]:


tr_table = nutritionnelle_table.find_all('tr', attrs={'class':'nutriment_main'}) if len(nutritionnelle_table) and nutritionnelle_table.find_all('tr', attrs={'class':'nutriment_main'}) else []


# In[57]:


#### Informations nutritionnelles
information_nutritionnelle = get_infos_nutri(tr_table)
information_nutritionnelle


# In[59]:


#### recyclage
recyclage_content = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[3] if len(contentInfos) and contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'}) and index_in_list(contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'}),3) else []


# In[60]:


recyclage = parse_string(recyclage_content.find('p').text) if len(recyclage_content) else 'XXX'
recyclage


# 4. Généralisation ie parcourir l'ensemble des pages pour récupérer les informations demandées

# In[ ]:


import pandas as pd
tmps1=time.time()
for chunk in pd.read_csv("images_url.csv", chunksize=50000):
    tmps1=time.time()
    food_infos = []
    print('chunk start : '+str(chunk.index.start))
    print('chunk end : '+str(chunk.index.stop))
    print('scrapping start ...')
    #### scrapping des
    for j in chunk.index:
        try:
            res = requests.get(str(chunk['images_url'][j]), headers = headers)
            soupProduct = BeautifulSoup(res.text, 'html.parser')
            contentInfos = soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})[0] if len(soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})) else soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/DietarySupplement'})[0] if len(soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})[0] if len(soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/Product'})) else soupProduct.find_all('div', attrs={'itemscope':'', 'itemtype':'https://schema.org/DietarySupplement'})) else [] #### récupération de la balise qui contient les informations démandées
            if len(contentInfos):
                
                #### Nom du Produit
                product_name = contentInfos.find_all('h1', attrs={'property':'food:name'})[0].text

                #### Code-barres (EAN/EAN-13)
                code_barre = contentInfos.find_all('span', attrs={'property':'food:code'})[0].text if index_in_list(contentInfos.find_all('span', attrs={'property':'food:code'}),0) else 'XXX'

                #### nova score
                novascore = contentInfos.find_all('a',href='/nova')[1].find('img')['alt'].split('-')[0].strip() if index_in_list(contentInfos.find_all('a',href='/nova'),1) else 'XXX'

                #### nutriscore
                nutriscore = contentInfos.find_all('a',href='/nutriscore')[1].find('img')['alt'].split(':')[1].strip() if index_in_list(contentInfos.find_all('a',href='/nutriscore'),1) else 'XXX'

                #### ecoscore
                ecoscore = contentInfos.find_all('a',href='/ecoscore')[2].find('img')['alt'].split(' ')[1].strip() if index_in_list(contentInfos.find_all('a',href='/ecoscore'),1) else 'XXX'
                #### caractéristiques des produits
                caracteristicsContent = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[0] #### block qui contient les informations sur les caractéristiques d'un produit
                caracteristic_list_value = caracteristicsContent.findAll('p') #### on récupère le bloc qui contient les caractéristiques des produits
                caracteristics = build_caracteritics_product_values(labels_caracteristic_id, caracteristic_list_value) #### on construit un dictionnaire avec les valeurs trouvées
                denomination_generique = caracteristics['denomination_generique']
                quantite = caracteristics['quantite']
                conditionnement = caracteristics['conditionnement']
                marques = caracteristics['marques']
                categories = caracteristics['categories']
                labels_certifications_recompenses = caracteristics['labels_certifications_recompenses']
                origine_des_ingredients = caracteristics['origine_des_ingredients']
                lieux_de_fabrication_ou_de_transformation = caracteristics['lieux_de_fabrication_ou_de_transformation']
                code_de_tracabilite = caracteristics['code_de_tracabilite']
                lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant = caracteristics['lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant']
                magasins = caracteristics['magasins']
                pays_de_vente = caracteristics['pays_de_vente']

                ingredientsContent = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[1]

                #### Substances ou produits provoquant des allergies ou intolérances :
                sub_trace_list = ingredientsContent.find_all('p', attrs={'class':'', 'id':''})[:2]
                substances_ou_produits_provoquant_des_allergies_ou_intolerances = build_caracteritics_product_values(labels_sub_trace_id, sub_trace_list)['substances_ou_produits_provoquant_des_allergies_ou_intolerances']
                traces_eventuelles = build_caracteritics_product_values(labels_sub_trace_id, sub_trace_list)['traces_eventuelles']

                #### Analyse des ingrédients :
                ingredients_analysis = ingredientsContent.find_all('p', attrs={'id':'ingredients_analysis'})
                ingredients_analysis = get_ingredient_analysis(ingredients_analysis)['ingredients_analysis']

                #### Détail de l'analyse des ingrédients:
                detail_analysis = ingredientsContent.find_all('div', attrs={'class':'columns'})
                additifs = build_caracteritics_product_values(labels_details_analysis, detail_analysis)['additifs']
                vitamines_ajoutees = build_caracteritics_product_values(labels_details_analysis, detail_analysis)['vitamines_ajoutees']
                mineraux_ajoutes = build_caracteritics_product_values(labels_details_analysis, detail_analysis)['mineraux_ajoutes']
                
                #### Repères nutritionnels pour 100 g
                nutritionnelle_content = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[2] if len(contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})) != 0 else []
                reperes_nutritionnels = parse_string(nutritionnelle_content.find_all('div', attrs={'class':'small-12 xlarge-6 columns'})[1].text).split(',,,,')[1].strip() if index_in_list(nutritionnelle_content.find_all('div', attrs={'class':'small-12 xlarge-6 columns'}),1) and index_in_list(parse_string(nutritionnelle_content.find_all('div', attrs={'class':'small-12 xlarge-6 columns'})[1].text).split(',,,,'),1) else 'XXX'        
                
                compare_label_list = list(map(lambda x: parse_string(x.text), nutritionnelle_content.find_all('label')))[:-2] if len(nutritionnelle_content) != 0 else [] 
                compare_value_list = list(map(lambda x:x.text.strip(), nutritionnelle_content.find_all('a' , attrs={'title':''}))) if nutritionnelle_content.find_all('a' , attrs={'title':''}) and len(nutritionnelle_content) else []
                compare_value_mean = get_compare_value(compare_label_list, compare_value_list)

                #### table information nutritionnelle
                nutritionnelle_content = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[2] if len(contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})) != 0 else []
                nutritionnelle_table = nutritionnelle_content.find_all('table', attrs={'id':'nutrition_data_table', 'class':'data_table'})[0] if nutritionnelle_content and nutritionnelle_content.find_all('table', attrs={'id':'nutrition_data_table', 'class':'data_table'}) else []
                tr_table = nutritionnelle_table.find_all('tr', attrs={'class':'nutriment_main'}) if len(nutritionnelle_table) and nutritionnelle_table.find_all('tr', attrs={'class':'nutriment_main'}) else []
                energie_kj = get_infos_nutri(tr_table)['energie_kj'] if 'energie_kj' in get_infos_nutri(tr_table) else 'XXX'
                energie_kcal = get_infos_nutri(tr_table)['energie_kcal'] if 'energie_kcal' in get_infos_nutri(tr_table) else 'XXX'
                energie = get_infos_nutri(tr_table)['energie'] if 'energie' in get_infos_nutri(tr_table) else 'XXX'
                matieres_grasses__lipides = get_infos_nutri(tr_table)['matieres_grasses__lipides'] if energie_kj in get_infos_nutri(tr_table) else 'XXX'
                glucides = get_infos_nutri(tr_table)['glucides'] if 'glucides' in get_infos_nutri(tr_table) else 'XXX'
                proteines = get_infos_nutri(tr_table)['proteines'] if 'proteines' in get_infos_nutri(tr_table) else 'XXX'
                silice = get_infos_nutri(tr_table)['silice'] if 'silice' in get_infos_nutri(tr_table) else 'XXX'
                potassium = get_infos_nutri(tr_table)['potassium'] if 'potassium' in get_infos_nutri(tr_table) else 'XXX'
                chlorure = get_infos_nutri(tr_table)['chlorure'] if 'chlorure' in get_infos_nutri(tr_table) else 'XXX'
                calcium = get_infos_nutri(tr_table)['calcium'] if 'calcium' in get_infos_nutri(tr_table) else 'XXX'
                ph = get_infos_nutri(tr_table)['ph'] if 'ph' in get_infos_nutri(tr_table)else 'XXX'
                sel = get_infos_nutri(tr_table)['sel'] if 'sel' in get_infos_nutri(tr_table) else 'XXX'
                fibres_alimentaires = get_infos_nutri(tr_table)['fibres_alimentaires'] if 'fibres_alimentaires' in get_infos_nutri(tr_table) else 'XXX'
                alcool = get_infos_nutri(tr_table)['alcool'] if 'alcool' in get_infos_nutri(tr_table) else 'XXX'
                bicarbonate = get_infos_nutri(tr_table)['bicarbonate'] if 'bicarbonate' in get_infos_nutri(tr_table) else 'XXX'
                fluorure = get_infos_nutri(tr_table)['fluorure'] if 'fluorure' in get_infos_nutri(tr_table) else 'XXX'
                nitrate = get_infos_nutri(tr_table)['nitrate'] if 'nitrate' in get_infos_nutri(tr_table) else 'XXX'
                sulfate = get_infos_nutri(tr_table)['sulfate'] if 'sulfate' in get_infos_nutri(tr_table) else 'XXX'
                score_nutritionnel_france = get_infos_nutri(tr_table)['score_nutritionnel_-_france'] if 'score_nutritionnel_-_france' in get_infos_nutri(tr_table) else 'XXX'

                #### recyclage
                recyclage_content = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[3] if len(contentInfos) and contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'}) else []
                recyclage = parse_string(recyclage_content.find('p').text) if len(recyclage_content) else 'XXX'

                ingredientsContent = contentInfos.find_all('div', attrs={'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})[1]
                #### liste des ingrédients
                ingredient_list = ingredientsContent.find_all('div', attrs={'property':'food:ingredientListAsText'})[0].text if ingredientsContent.find_all('div', attrs={'property':'food:ingredientListAsText'}) else 'XXX'
                
                food_infos.append([product_name, 
                                  code_barre, 
                                  novascore, 
                                  nutriscore, 
                                  ecoscore,
                                  denomination_generique, 
                                  quantite, 
                                  conditionnement, 
                                  marques, 
                                  categories, 
                                  labels_certifications_recompenses, 
                                  origine_des_ingredients, 
                                  lieux_de_fabrication_ou_de_transformation, 
                                  code_de_tracabilite, 
                                  lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant, 
                                  magasins, 
                                  pays_de_vente, 
                                  substances_ou_produits_provoquant_des_allergies_ou_intolerances, 
                                  traces_eventuelles,
                                  ingredients_analysis, 
                                  additifs, 
                                  vitamines_ajoutees, 
                                  mineraux_ajoutes,
                                  reperes_nutritionnels,
                                  compare_value_mean,
                                  energie_kj, 
                                  energie_kcal, 
                                  energie, 
                                  matieres_grasses__lipides, 
                                  glucides, 
                                  proteines, 
                                  sel,
                                  glucides,
                                  proteines,
                                  silice, 
                                  potassium, 
                                  chlorure, 
                                  calcium, 
                                  ph,
                                  fibres_alimentaires, 
                                  alcool, 
                                  bicarbonate, 
                                  fluorure, 
                                  nitrate, 
                                  sulfate,
                                  score_nutritionnel_france, 
                                  recyclage,
                                  ingredient_list])
            else:
                print("lien "+str(j)+" : "+chunk['images_url'][j])

        except Exception as e:
            print("lien "+str(j)+" : "+chunk['images_url'][j])
            print(e)
            traceback.print_exc()
            tmps2=time.time()-tmps1
            print("Temps d'execution avant l'erreur = "+convert(tmps2))
            continue
    print('scrapping end ...' + str(chunk.index.stop))
    tmps2=time.time()-tmps1
    print("Temps d'execution de scrapping des données des produits = "+convert(tmps2))
    print("Export dataframe to csv ...")
    tmps1=time.time()
    #### export en csv des la liste des liens des produits trouvés
    df = pd.DataFrame(food_infos, columns=['product_name', 
                                      'code_barre', 
                                      'novascore', 
                                      'nutriscore', 
                                      'ecoscore',
                                      'denomination_generique', 
                                      'quantite', 
                                      'conditionnement', 
                                      'marques', 
                                      'categories', 
                                      'labels_certifications_recompenses', 
                                      'origine_des_ingredients', 
                                      'lieux_de_fabrication_ou_de_transformation', 
                                      'code_de_tracabilite', 
                                      'lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant', 
                                      'magasins', 
                                      'pays_de_vente', 
                                      'substances_ou_produits_provoquant_des_allergies_ou_intolerances', 
                                      'traces_eventuelles',
                                      'ingredients_analysis', 
                                      'additifs', 
                                      'vitamines_ajoutees', 
                                      'mineraux_ajoutes',
                                      'compare_value_mean', 
                                      'reperes_nutritionnels', 
                                      'energie_kj', 
                                      'energie_kcal', 
                                      'energie', 
                                      'matieres_grasses__lipides', 
                                      'glucides', 
                                      'proteines', 
                                      'sel',
                                      'glucides',
                                      'proteines',
                                      'silice', 
                                      'potassium', 
                                      'chlorure', 
                                      'calcium', 
                                      'ph',
                                      'fibres_alimentaires', 
                                      'alcool', 
                                      'bicarbonate', 
                                      'fluorure', 
                                      'nitrate', 
                                      'sulfate',
                                      'score_nutritionnel_france', 
                                      'recyclage',
                                      'ingredient_list'
                                      ])
    df.to_csv('DataframeFood'+str(chunk.index.start)+'.csv', index=False, encoding='utf-8')
    tmps2=time.time()-tmps1
    print("Fin export dataframe to csv ...")
    print("Temps d'execution export csv dataframe food = "+convert(tmps2))

tmps2=time.time()-tmps1
print("Temps d'execution de global de l'ensemble = "+convert(tmps2))

