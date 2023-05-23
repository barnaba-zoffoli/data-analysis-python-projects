#!/usr/bin/env python
# coding: utf-8


## Import necessary libraries



import numpy as np
import pandas as pd
import seaborn as sns
import datetime as dt
import os
import matplotlib.pyplot as plt



## Create the dataframe that will host data from merged datasets. 
## Datasets were previously downloaded from the open data website of Municipality of Rome >> https://dati.comune.roma.it/catalog/dataset?q=incidenti&groups=sicurezza-urbana&sort=score+desc%2C+metadata_modified+desc 



incidenti_roma_raw = pd.DataFrame([])



os.chdir("C:\\Users\\test\\path/folder-path/")



files=os.listdir()



## csv files downloaded were not UTF-8, so it was necessary to find the encoding type using **chardet library



from chardet import detect
def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']



get_encoding_type("C:\\Users\\test\\path/folder-path/")



##Use for cycle to concatenate the different csv for each month of each year and include them within the dataframe created previously



for f in files: 
    f_csv = pd.read_csv(f, encoding='ISO-8859-1',sep=';')
    mkp_tmp=pd.DataFrame(f_csv)
    incidenti_roma_raw = pd.concat([incidenti_roma_raw, mkp_tmp])



##Now begins the exploratory analysis of data and the cleaning process



incidenti_roma_raw.info()



incidenti_roma_raw.head()



##Some unnecessary columns for the aim of the analysis were singled out and removed



incidenti_roma=incidenti_roma_raw.drop(["Latitude", "Longitude", "Unnamed: 37","Segnaletica","Confermato","Progressivo","NUM_RISERVATA","TipoStrada","Traffico","Visibilita","TipoVeicolo","Tipolesione","Deceduto","DecedutoDopo","CinturaCascoUtilizzato","Airbag","Sesso","TipoPersona","StatoVeicolo"],axis=1)



incidenti_roma.info()



##The column "Protocollo" includes the id of every car accidents, but each id was duplicated for each car/person involved in the accident. I order to clean the dataframe and to have the correct number of accidents ids, duplicates were removed.



incidenti_roma.drop_duplicates(subset="Protocollo", inplace=True)



incidenti_roma.info()



##Creating new separated columns for date and hours allowed to bring forward more precise analysis about timing of the accidents



incidenti_roma[["Data_new", "Orario_completo"]] = incidenti_roma["DataOraIncidente"].str.split(" ", expand = True)



incidenti_roma["Data_new"]=pd.to_datetime(incidenti_roma["Data_new"], format = "%d/%m/%Y")



incidenti_roma[["Ora","Minuti","Secondi"]]=incidenti_roma["Orario_completo"].str.split(":", expand = True)



incidenti_roma=incidenti_roma.drop(["Minuti","Secondi"], axis=1)



incidenti_roma.info()



incidenti_roma["Ora"]=incidenti_roma["Ora"].astype("float")



incidenti_roma["Anno"]=incidenti_roma["Data_new"].dt.year
incidenti_roma["Mese"]=incidenti_roma["Data_new"].dt.month


##Quick graph was created to have a grasp of how many accidents there were in each year



sns.countplot(x="Anno", data=incidenti_roma, color="c")



incidenti_roma.info()



incidenti_roma=incidenti_roma.reset_index(drop=True)



##The column "Natura incidente" included some type of accidents which could be aggregated.



incidenti_roma.groupby(["NaturaIncidente"],as_index=False)["Protocollo"].count()



x=incidenti_roma.loc[incidenti_roma["NaturaIncidente"].str.contains("altezza civico",na=False)]
x[["NaturaIncidente","STRADA1","Localizzazione2","STRADA2","Strada02","Chilometrica","DaSpecificare","Illuminazione","CondizioneAtmosferica","Pavimentazione","FondoStradale","particolaritastrade"]]



incidenti_roma["NaturaIncidente"]=incidenti_roma["NaturaIncidente"].str.replace("altezza civico 19", "Scontro frontale/laterale SX fra veicoli in marcia")



incidenti_roma["particolaritastrade"]=incidenti_roma["particolaritastrade"].str.replace("Scontro frontale/laterale SX fra veicoli in marcia", "altezza civico 19")



incidenti_roma["NaturaIncidente"]=incidenti_roma["NaturaIncidente"].str.replace("Scontro frontale/laterale SX fra veicoli in marcia", "Scontro frontale/laterale SX fra veicoli in marcia")



incidenti_roma = incidenti_roma.drop(labels=[49859], axis=0)
incidenti_roma=incidenti_roma.reset_index(drop=True)



incidenti_roma.groupby("NaturaIncidente",as_index=False)["Protocollo"].count()



incidenti_roma["NaturaIncidente"]=incidenti_roma["NaturaIncidente"].str.replace("Veicoli in marcia contro veicolo fermo", "Veicolo in marcia contro veicolo fermo")
incidenti_roma["NaturaIncidente"]=incidenti_roma["NaturaIncidente"].str.replace("Veicoli in marcia contro veicoli fermi", "Veicolo in marcia contro veicolo fermo")
incidenti_roma["NaturaIncidente"]=incidenti_roma["NaturaIncidente"].str.replace("Veicolo in marcia contro veicoli fermi", "Veicolo in marcia contro veicolo fermo")
incidenti_roma["NaturaIncidente"]=incidenti_roma["NaturaIncidente"].str.replace("Veicolo in marcia contro veicoli in sosta", "Veicolo in marcia contro veicolo in sosta")
incidenti_roma["NaturaIncidente"]=incidenti_roma["NaturaIncidente"].str.replace("Veicolo in marcia contro veicolo arresto", "Veicolo in marcia contro veicoli in arresto")
incidenti_roma.groupby("NaturaIncidente",as_index=False)["Protocollo"].count()



##In order get complete and clean addresses to use in geographical analysis and locate each accidents, a new column was created combinining main info included in other columns such as "STRADA1","STRADA2","Chilometrica".



indirizzi_incidenti=incidenti_roma[["STRADA1","STRADA2","Chilometrica"]].fillna("")



incidenti_roma["Indirizzo_completo"]=indirizzi_incidenti["STRADA1"]+","+indirizzi_incidenti["STRADA2"]+","+indirizzi_incidenti["Chilometrica"]+ ",Rome,Italy"

incidenti_roma


incidenti_roma["Indirizzo_completo"] = incidenti_roma["Indirizzo_completo"].str.replace(',,,', ',')
incidenti_roma["Indirizzo_completo"] = incidenti_roma["Indirizzo_completo"].str.replace(',,', ',')



incidenti_roma.tail(5)


incidenti_roma.info()


##Final dataset was converted in csv file to be used in Tableau for data visualization


incidenti_roma.to_csv("C:\\Users\\test\\path/folder-path/incidenti_roma_cleaned.csv")

