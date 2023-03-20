#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gzip
from correctionlib.schemav2 import CorrectionSet,Correction,Category,CategoryItem, Formula, MultiBinning
from itertools import chain


# In[2]:


def getdict(file):
    import yaml
    # opening a file
    with open(file, 'r') as stream:
        try:
            d=yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
    #k={"2018":{"HLT_Photon120": {315257: {1: 49}, 315259: {1: 49}, 315264: {32: 74}, 315265: {4: 74}}}}
    return d


# In[3]:


def dictf(prescale_dict,year,HLT,run,lumi):
    try:
        dd=prescale_dict[year][HLT][run][lumi]
    except:
        dd=-1
    return dd
 


# In[10]:


import copy
def getmultibinning(triggerlumilist):
    triggerlumilist1=copy.deepcopy(triggerlumilist)#.deepcopy()
    if triggerlumilist[0]!=1:
        triggerlumilist1.insert(0, 1)
    tot=len(triggerlumilist1)
    triggerlumilist1.insert(tot, 99999)
    return triggerlumilist1

def prescaletrick(prescalelist,lumilist_):
    if lumilist_[0]!=1:
        prescalelist.insert(0, 1)
    return prescalelist

def getvalue(prescale_dict,year,HLT,run):
    print(year,HLT,run)
    lumilist_= list(set(chain.from_iterable(value.keys() for value in [prescale_dict[year][HLT][run]])))
    print(lumilist_)
    print([dictf(prescale_dict,year,HLT,run,lumi) for lumi in lumilist_])
    print(lumilist_)
    print(getmultibinning(lumilist_))
    print(lumilist_)
    print([dictf(prescale_dict,year,HLT,run,lumi) for lumi in lumilist_])
    print([dictf(prescale_dict,year,HLT,run,lumi) for lumi in lumilist_])
    print(prescaletrick([dictf(prescale_dict,year,HLT,run,lumi) for lumi in lumilist_],lumilist_))
    value=MultiBinning.parse_obj({
        "inputs":["lumi"],
        "nodetype": "multibinning",
        "edges": [
            getmultibinning(lumilist_)
        ],
        "content": prescaletrick([dictf(prescale_dict,year,HLT,run,lumi) for lumi in lumilist_],lumilist_)  ,
        "flow": 'error',
    })
    print(prescaletrick([dictf(prescale_dict,year,HLT,run,lumi) for lumi in lumilist_],lumilist_))
    return value

def getdictpre(years):
    prescale_dict={'2018':getdict("2018_UL/photon_prescales_2018.yaml.txt")}
    
    HLTs = list(set(chain.from_iterable(value.keys() for value in [prescale_dict[year] for year in years])))
    #for year in years:
    #    runs = list(set(chain.from_iterable(value.keys() for value in [prescale_dict[year][HLT] for HLT in HLTs])))
    #for year in years:
    #    for HLT in HLTs:
    #        lumis = list(set(chain.from_iterable(value.keys() for value in [prescale_dict[year][HLT][run] for run in runs])))
    output = Category.parse_obj({
                "nodetype": "category",
                "input": "HLT",
                "content":[
                    CategoryItem.parse_obj({
                        "key": HLT, 
                        "value":Category.parse_obj({
                            "nodetype": "category",
                            "input": "run",
                            "content":[
                                CategoryItem.parse_obj({
                                    "key": run, 
                                    "value": getvalue(prescale_dict,year,HLT,run)
                                })
                                for run in list(set(chain.from_iterable(value.keys() for value in [prescale_dict[year][HLT]])))
                            ],
                        })
                    })
                    for HLT in HLTs
                ],
    })
    return output


# In[ ]:





# In[11]:


years=["2018"]

for year in years:
    corrs=[]
    corr = Correction.parse_obj(
        {
            "version": 2,
            "name": "HLT_prescale",
            "description": f"Testing prescale",
            "inputs": [
                {"name": "year","type": "string", "description": "year/scenario: example 2016preVFP, 2017 etc"},
                {"name": "HLT","type": "string", "description": "HLT name"},
                {"name": "run","type": "int", "description": "run "},
                {"name": "lumi","type": "int"},
            ],
            "output": {"name": "prescale", "type": "real", "description": "value of prescale"},
            "data": Category.parse_obj({
                "nodetype": "category",
                "input": "year",
                "content": [
                CategoryItem.parse_obj({"key":year,
                                        "value": getdictpre([year])})]
            })
        })

    corrs.append(corr)


    #Save JSON
    cset = CorrectionSet(schema_version=2, corrections=corrs,description=f"Trigger prescales- preliminary")
    with open("prescale.json", "w") as fout:
        fout.write(cset.json(exclude_unset=True, indent=4))


# In[ ]:





# In[6]:


from correctionlib import _core

evaluator = _core.CorrectionSet.from_file('prescale.json')


# In[9]:


evaluator["HLT_prescale"].evaluate("2018","HLT_Photon120",317391,10.0)


# In[ ]:


evaluator["HLT_prescale"].evaluate("2018","HLT_Photon120",315257,10.0)


# In[ ]:


evaluator["HLT_prescale"].evaluate("2018","HLT_Photon120",315257,10)


# In[ ]:


2018 HLT_Photon165_R9Id90_HE10_IsoM 321887


# In[ ]:


evaluator["HLT_prescale"].evaluate("2018","HLT_Photon165_R9Id90_HE10_IsoM",321887,99.0)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




