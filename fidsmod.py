import pandas as pd
import datetime as dt

def CallFIDS():
                        
        # Hlaða inn og sameina
        import requests
        response = requests.get('https://www.innanlandsflugvellir.is/fids/departures.aspx')
        Departures_List = response.json()["Items"]
        response = requests.get('https://www.innanlandsflugvellir.is/fids/arrivals.aspx')
        Arrivals_List = response.json()["Items"]
        FIDS = pd.concat([pd.DataFrame(Departures_List), 
                        pd.DataFrame(Arrivals_List)])
        del([response, Departures_List, Arrivals_List])
        FIDS = FIDS.reset_index(drop=True)

        # Engin auð hlið eða tvöföld skráning
        FIDS = FIDS[FIDS["Gate"] != ""]
        FIDS = FIDS.drop_duplicates(subset="No", keep="last")

        # DagsTími
        SerActual = FIDS["Actual"][FIDS["Actual"].notna()]
        SerEstimated = FIDS["Estimated"][FIDS["Actual"].isna() & FIDS["Estimated"].notna()]
        SerScheduled = FIDS["Scheduled"][FIDS["Actual"].isna() & FIDS["Estimated"].isna() & FIDS["Scheduled"].notna()]
        FIDS = FIDS.assign(DagsTimi = pd.concat([SerActual, SerEstimated, SerScheduled]))
        del([SerActual, SerEstimated, SerScheduled])
        FIDS["DagsTimi"] = pd.to_datetime(FIDS["DagsTimi"], utc=True)

        # Styttri Dags og Tími
        SerArr = FIDS["DagsTimi"][~FIDS["Departure"]] + dt.timedelta(minutes=15)
        SerDep = FIDS["DagsTimi"][FIDS["Departure"]] - dt.timedelta(minutes=45)
        #SerArr = "--/--/--"
        #SerDep = "--/--/--"
        FIDS["DTStart"] = pd.concat([FIDS["DagsTimi"][~FIDS["Departure"]], SerDep])
        FIDS["DTEnd"] =  pd.concat([FIDS["DagsTimi"][FIDS["Departure"]], SerArr])
        del([SerArr, SerDep])
        FIDS["Byrja"] = FIDS["DTStart"].dt.strftime("%m-%d-%H:%M")
        FIDS["Enda"] = FIDS["DTEnd"].dt.strftime("%m-%d-%H:%M")
        FIDS["DateOnlyByrja"] = FIDS["DTStart"].dt.strftime("%m-%d")
        FIDS["DateOnlyEnda"] = FIDS["DTEnd"].dt.strftime("%m-%d")
        FIDS["TimeOnlyByrja"] = FIDS["DTStart"].dt.strftime("%H:%M")
        FIDS["TimeOnlyEnda"] = FIDS["DTEnd"].dt.strftime("%H:%M")
        FIDS["Time(Date)Byrja"] = FIDS["DTStart"].dt.strftime("%H:%M (%d/%m)")
        FIDS["Time(Date)Enda"] = FIDS["DTEnd"].dt.strftime("%H:%M (%d/%m)")

        # Tímarammi
        FIDS["Horizon"] = FIDS["DTStart"]-pd.Timestamp.now(tz=dt.timezone.utc)

        # Hlið
        FIDS["Hlið"] = FIDS["Gate"]
        FIDS["Hlið"] = FIDS["Hlið"].replace({
                "A15": "15", 
                "D15": "15", 
                "C21": "21",
                "D21": "21",
                "C22": "22",
                "D22": "22",
                "C23": "23",
                "D23": "23",
                "C24": "2427",
                "D24": "2427",
                "C25": "2427",
                "D25": "2427",
                "C26": "2427",
                "D26": "2427",
                "C27": "2427",
                "D27": "2427",
                "C28": "2829",
                "D28": "2829",
                "C29": "2829",
                "D29": "2829",
                "C31": "3133",
                "D31": "3133",
                "C32": "32",
                "D32": "32",
                "C33": "333",
                "D33": "3133",
                "C34": "34",
                "D34": "34",
                "C35": "35",
                "D35": "35"
                })
        FIDS["Hlið"] = FIDS["Hlið"].astype("string")
        

        # Schengen / Non-Schengen
        FIDS["CD"] = FIDS["Gate"].str.slice(0,1)
        FIDS["CD"] = FIDS["CD"].replace({"A": "C"})
        FIDS["KB"] = FIDS["Departure"].replace({True: "B", False: "K"})
        FIDS["CDKB"] = FIDS["CD"] + FIDS["KB"]
        FIDS["Schengen"] = FIDS["CD"].replace({"C": "Schengen", "D": "Non-Schengen"})
        FIDS["KomaBrottför"] = FIDS["KB"].replace({"K": "Koma", "B": "Brottför"})
        FIDS["FullCDKB"] = FIDS["Schengen"] + " " + FIDS["KomaBrottför"]
        FIDS["FullCDKB"] = FIDS["FullCDKB"].astype("string")

        FIDS["~Time(Date)Byrja"] = FIDS["KB"].replace({"K": "", "B": "~"}) + FIDS["Time(Date)Byrja"]
        FIDS["~Time(Date)Enda"] = FIDS["KB"].replace({"K": "~", "B": ""}) + FIDS["Time(Date)Enda"]
        FIDS["Status"] = FIDS["Status"].astype("string")
        FIDS["StatusGroup"] = FIDS["Status"].replace({"Landed": "Almennt",
                                                      "Estimated": "Almennt",
                                                      "On time": "Almennt",
                                                      "Boarding": "Almennt",
                                                      "Go to Gate": "Almennt", 
                                                      "Final Call": "Almennt",
                                                      "Cancelled": "Annað", 
                                                      "Departed": "Annað", 
                                                      "Gate Closed": "Annað", 
                                                      "All Bags on Belt": "Annað"})
        
        Dalkar = ["FullCDKB","~Time(Date)Byrja","~Time(Date)Enda","Time(Date)Byrja","Time(Date)Enda","Status","StatusGroup","No", 
                        "DagsTimi","DTStart","DTEnd","Horizon",
                        "Byrja","DateOnlyByrja","TimeOnlyByrja",
                        "KB","CD","CDKB","Schengen", "KomaBrottför",
                        "Enda","DateOnlyEnda","TimeOnlyEnda", 
                        "Aircraft","Airline", "OriginDest","Gate","Hlið","Stand"]
        

        FIDS = pd.DataFrame(FIDS, columns=Dalkar)
        FIDS = FIDS.sort_values(by=["Hlið","DTStart"])

        FIDS = FIDS.reset_index(drop=True)

        return FIDS