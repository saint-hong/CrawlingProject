import pandas as pd
import requests
from bs4 import BeautifulSoup

class Hypebeast:
    
    def __init__(self):
        self.basic_url = "https://hypebeast.kr" 
    
    # link를 받아서 content를 추가해주는 함수    
    def get_content(self, link):
        response = requests.get(link)
        dom = BeautifulSoup(response.content, "html.parser")
        return dom.select_one('.row p').text.strip().replace("\xa0", "")
    
    # page 입력 함수    
    def one_page(self, page):
        elements = []
        for page in range(page, page * 20):
            print("Crawling : {} page..".format(page))
            url = "https://hypebeast.kr/page/{}?after=".format(page)
            response = requests.get(url)
            dom = BeautifulSoup(response.content, "html.parser")
            elements = elements + dom.select(".posts>div>.post-box-content-container")
        
        # Css Select로 파싱할 때 해당 html이 없는 경우는 예외 처리 해주는 함수
        datas = []
        for element in elements :
            try:
                category = element.select_one('.post-box-content-categories> a').text
            except:
                category = "-"
            try:
                title = element.select_one('.post-box-content-title > a').text
            except:
                title = "-"
            try:
                summary = element.select_one('.post-box-content-excerpt').text.strip()
            except:
                summary = "-"
            try:
                author = element.select_one('.author-name > a').text
            except:
                author = "-"
            try:
                link = element.select_one('.post-box-content-title > a').get("href")
            except:
                link = "-"
            try:
                date = element.select_one('.time > time').text
            except:
                date = "-"

            data = ({
                "category" : category,
                "title" : title,
                "summary" : summary,
                "author" : author,
                "link" : link,
                "date" : date,
            })
            
            datas.append(data)
    
        hb_df = pd.DataFrame(datas)
        hb_df["content"] = hb_df["link"].apply(self.get_content)
        
        return hb_df
