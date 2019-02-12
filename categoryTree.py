#coding=utf-8

from wikitools import wiki,category,api
import sys
import chardet

def wikipedia_query(query_params,lang='ja'):
	site = wiki.Wiki(url='https://'+lang+'.wikipedia.org/w/api.php')
	request = api.APIRequest(site, query_params)
	result = request.query(False)
	return result[query_params['action']]

def get_category_members(par_category, depth, index, lang='ja'):
    category_name = 'Category:'+par_category
    if depth < 0:
        return 0
    #Begin crawling articles in category
    results_pages = wikipedia_query({'list': 'categorymembers','cmtitle': category_name,'cmtype': 'page','cmlimit': '500','action': 'query'},lang)  
    
    
    # Begin crawling subcategories
    results_cate = wikipedia_query({'list': 'categorymembers',
                                   'cmtitle': category_name,
                                   'cmtype': 'subcat',
                                   'cmlimit': '500',
                                   'action': 'query',
                                   'format': 'json'},lang)
    
    subcategories = []
    pages = []
    if 'categorymembers' in results_cate.keys() and len(results_cate['categorymembers']) > 0:
        for i, category in enumerate(results_cate['categorymembers']):
            cat_title = category['title']
            subcategories.append(cat_title.strip('Category:'))
        subcat= ''.join(cat+'+' for cat in subcategories).strip('+')
    elif 'categorymembers' in results_pages.keys() and len(results_pages['categorymembers']) > 0:
        for i, category in enumerate(results_pages['categorymembers']):
            cat_title = category['title']
            pages.append(cat_title.strip('Category:'))
        subcat= ''.join(cat+'+' for cat in pages).strip('+')
        if subcat !='':
            wp.write(index+':'+subcat.encode("utf-8")+'\n')

    else:
        subcat = ''
    for category in subcategories:
        index_ = index+">"+category.encode("utf-8")
        get_category_members(category.encode("utf-8"),depth-1,index_)

wikisite = "https://ja.wikipedia.org/w/api.php"
par_category = sys.argv[1]
depth =int(sys.argv[2])
cat_tree =sys.argv[3]
wp =open(cat_tree,'w')
total_item=0
index = par_category


get_category_members(par_category,depth,index,'ja')

