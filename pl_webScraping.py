# -*- coding: utf-8 -*-
"""
Created on Sun May 21 02:35:43 2023

@author: LENOVO
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from matplotlib import pyplot as plt
import seaborn as sns



position=[]
title=[]
season=[]
games_played=[]
wins=[]
draws=[]
losses=[]
goals_for=[]
goals_against=[]
goals_diff=[]
points=[]

root="https://www.espn.com/soccer/standings/_/league/ENG.1/season/"
path="C:/Users/LENOVO/Downloads/chromedriver"
driver=webdriver.Chrome(path)

start_season=2022

for i in range(0,21):
    
    
    website=f"https://www.espn.com/soccer/standings/_/league/ENG.1/season/{start_season}"
    
    driver.get(website)
    
    rows1=driver.find_elements(By.XPATH,"//div[@class='flex']/table/tbody/tr")
    rows2=driver.find_elements(By.XPATH,"//div[@class='Table__Scroller']/table/tbody/tr")
    
    
    
    
    for row in rows1:
        position.append(row.find_element(By.XPATH,".//td/div/span[1]").text)
        title.append(row.find_element(By.XPATH,".//td/div/span[4]/a").text)
        #img=row.find_element(By.XPATH,".//td/div/span[2]/a/img")
        #image.append(img.get_attribute("src"))
        season.append(driver.find_element(By.XPATH,"//div[@class='flex']/table/thead/tr/th/span").text)
        
        
   
    
    for row in rows2:
        
        games_played.append(row.find_element(By.XPATH,".//td[1]/span").text)
        wins.append(row.find_element(By.XPATH,".//td[2]/span").text)
        draws.append(row.find_element(By.XPATH,".//td[3]/span").text)
        losses.append(row.find_element(By.XPATH,".//td[4]/span").text)
        goals_for.append(row.find_element(By.XPATH,".//td[5]/span").text)
        goals_against.append(row.find_element(By.XPATH,".//td[6]/span").text)
        goals_diff.append(row.find_element(By.XPATH,".//td[7]/span").text)
        points.append(row.find_element(By.XPATH,".//td[8]/span").text)
    
    
    start_season=start_season-1
            
   
    
print(position)
print(title)
print(season)    
print(games_played)
print(wins)
print(draws)
print(losses)
print(goals_for)
print(goals_against)
print(goals_diff)
print(points)
    

df_dict={"position":position,"title":title,"season":season,
         "games_played":games_played,"wins":wins
         ,"draws":draws,"losses":losses,"goals_for":goals_for,"goals_against":goals_against,
         "goals_diff":goals_diff,"points":points
         }

df=pd.DataFrame(df_dict)

df.to_csv("pl_stats.csv",index=False)