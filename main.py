import flet as ft
import fidsmod
import datetime as dt
import GlerModule

def main(page: ft.Page):
     page.title = "Schengen Appið"
     fids = fidsmod.CallFIDS()
     #print(fids.columns)
     GlerData = GlerModule.DATA
     GateGroup = ["E2"]

     def soft_Refresh():
          btnHlið.text = btnHlið.text = GateGroup[btnHlið.data]
          btnHlið.update()
          ddStillaGler.options = GlerData[GateGroup[btnHlið.data]]["GlerValm"]
          ddStillaGler.update()
          Column_of_Cards.controls.clear()
          Column_of_Cards.controls=List_of_Cards(fids)
          page.update()

     def event_Hlið(e):
          if e.control.value == False:
               for g in e.control.data: GateGroup.remove(g)
          else:
               GateGroup.extend(e.control.data)
          GateGroup.sort()
          btnHlið.data = 0
          if len(GateGroup) > 0: 
               soft_Refresh()
          else: 
               btnHlið.text = ""
               ddStillaGler.options = []
               btnHlið.update()
               ddStillaGler.update()

     cbE2 = ft.Checkbox(label="E2", value=True, on_change=event_Hlið, data=["E2"])
     cb15 = ft.Checkbox(label="15", value=False, on_change=event_Hlið, data=["15"])
     cb20 = ft.Checkbox(label="20", value=False, on_change=event_Hlið, data=["21","22","23"])
     cb30 = ft.Checkbox(label="30", value=False, on_change=event_Hlið, data=["32","34","35"])
     cb2427 = ft.Checkbox(label="24-27", value=False, on_change=event_Hlið, data=["2427"])
     cb2829 = ft.Checkbox(label="28-29", value=False, on_change=event_Hlið, data=["2829"])
     cb3133 = ft.Checkbox(label="31-33", value=False, on_change=event_Hlið, data=["3133"])
     

     def event_PrevGate(e):
          if len(GateGroup) > 0:
               if btnHlið.data == 0:
                    btnHlið.data = len(GateGroup)-1
               else: btnHlið.data -= 1
               soft_Refresh()
     def event_NextGate(e):
          if len(GateGroup) > 0:
               if btnHlið.data == len(GateGroup)-1:
                    btnHlið.data = 0
               else: btnHlið.data += 1
               soft_Refresh()
     btnPrevGate = ft.OutlinedButton(icon=ft.icons.ARROW_BACK, on_click=event_PrevGate)
     btnNextGate = ft.OutlinedButton(icon=ft.icons.ARROW_FORWARD, on_click=event_NextGate)

     def event_Gler(e):
          GlerData[GateGroup[btnHlið.data]]["GlerStaða"] = ddStillaGler.value
          print(GlerData[GateGroup[btnHlið.data]]["GlerStaða"])
          soft_Refresh()
     ddStillaGler = ft.Dropdown(options=GlerData["E2"]["GlerValm"],
                                value=GlerData["E2"]["GlerValm"][0],
                                on_change=event_Gler,
                                data=0)
     
     btnHlið = ft.OutlinedButton(text="E2", data=0)

     def event_Staða(e):
          if swStaða.value: swStaða.data = "Almennt"
          else: swStaða.data = "Annað"
          soft_Refresh()
     swStaða = ft.Switch(label="Almennt", 
                         value=True,
                         data="Almennt", 
                         on_change=event_Staða)

     def event_Horizon(e):
          soft_Refresh()
     rbHorizon = ft.RadioGroup(on_change=event_Horizon,
                               content=ft.Column([
          ft.Radio(label="Enginn", value="Enginn", toggleable=False),
          ft.Radio(label="2", value=2, toggleable=False),
          ft.Radio(label="4", value=4, toggleable=False),
          ft.Radio(label="6", value=6, toggleable=False),
          ft.Radio(label="8", value=8, toggleable=False)
     ]))
     rbHorizon.value = "Enginn"

     def hard_refresh(e):
          fids = fidsmod.CallFIDS()
          """ btnHlið.text = btnHlið.text = GateGroup[btnHlið.data]
          btnHlið.update()
          ddStillaGler.options = GlerData[GateGroup[btnHlið.data]]["GlerValm"]
          ddStillaGler.update() """
          Column_of_Cards.controls.clear()
          Column_of_Cards.controls=List_of_Cards(fids)
          page.update()
          #soft_Refresh()
     btnFIDS = ft.OutlinedButton(text="Ný gögn", on_click=hard_refresh) 

     leftdrawer = ft.NavigationDrawer(
          position=ft.NavigationDrawerPosition.START,
          controls=[ft.Text("Staða flugs:"),
                    swStaða,
                    ft.Text("Hlið:"),
                    cbE2,cb15,cb20,cb30,cb2427,cb2829,cb3133,
                    ft.Text("Tímarammi:"),
                    rbHorizon])

     def Card_Design(fids,i):
          cpGateKB = ft.Chip(label=ft.Text(fids["Gate"].iloc[i] + " " + fids["KomaBrottför"].iloc[i]))
          Titill2 = ft.Row(controls=[
               #ft.Text(fids["~Time(Date)Byrja"].iloc[i]),
               cpGateKB,
               #ft.Text(fids["~Time(Date)Enda"].iloc[i])
          ])
          if fids["KomaBrottför"].iloc[i] == "Brottför":
               cpGateKB.color = ft.colors.YELLOW
               Titill2.controls.insert(0, ft.Text("--:-- (--/--/--)"))
               Titill2.controls.extend([ft.Text(fids["~Time(Date)Enda"].iloc[i])])
          elif fids["KomaBrottför"].iloc[i] == "Koma":
               Titill2.controls.insert(0,ft.Text(fids["~Time(Date)Byrja"].iloc[i]))
               Titill2.controls.extend([ft.Text("--:-- (--/--/--)")])
          Lina1 = ft.Text(fids["Status"].iloc[i] + " / Stæði " + fids["Stand"].iloc[i] + " / " + fids["OriginDest"].iloc[i])
          Lina2 = ft.Text(fids["Airline"].iloc[i] + " / " + fids["No"].iloc[i] + " / " + fids["Aircraft"].iloc[i])
          Lina3 = ft.Text(fids["FullCDKB"].iloc[i] + " - " + GlerData[GateGroup[btnHlið.data]]["GlerStaða"])
          cpPassStat = ft.Chip(ft.Text(fids["FullCDKB"].iloc[i]))
          cpGlerStat = ft.Chip(ft.Text(GlerData[GateGroup[btnHlið.data]]["GlerStaða"]))
          if (fids["FullCDKB"].iloc[i] == GlerData[GateGroup[btnHlið.data]]["GlerStaða"]):
               icnAction = ft.Icon(name=ft.icons.DONE_ROUNDED, color=ft.colors.GREEN)
          else: 
               icnAction = ft.Icon(name=ft.icons.STOP_CIRCLE, color=ft.colors.RED)
          Lina3 = ft.Row([cpPassStat, icnAction, cpGlerStat])
          Card_Design = ft.Card(
               width=400,
               elevation=20,
               content=ft.Container(
                    content=ft.Column(
                         controls=[
                              Titill2, Lina1, Lina2, Lina3
                         ])))
          return Card_Design

     def List_of_Cards(fids):
          List_of_Cards = []
          for i in fids.index:
               skilyrdi = ((fids["StatusGroup"].iloc[i] == swStaða.data) 
                           & (fids["Hlið"].iloc[i] == GateGroup[btnHlið.data]))
               if rbHorizon.value != "Enginn":
                    skilyrdi = skilyrdi & (fids["Horizon"].iloc[i] < dt.timedelta(hours=int(rbHorizon.value)))
               if skilyrdi:
                    List_of_Cards.append(Card_Design(fids,i))
          return List_of_Cards
     Column_of_Cards = ft.Column(controls=List_of_Cards(fids))

     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

     page.add(
          ft.Row(
               controls=[
                    ft.ElevatedButton("Síur", on_click=lambda e: page.open(leftdrawer)),
                    ]))
     page.add(ft.Row([btnFIDS,ddStillaGler],alignment=ft.MainAxisAlignment.CENTER),
              ft.Row([btnPrevGate,btnHlið,btnNextGate],alignment=ft.MainAxisAlignment.CENTER),
              Column_of_Cards)
     

ft.app(target=main)

"""      dctFilter = {
          "Hlið": "E2",
          "Staða": ["Landed","Estimated","On time","Boarding","Go to Gate", "Final Call"],
          "Tímarammi": "Enginn"
          }

# INITIAL VALUES
     dct_GateGroups = {"E2": ["E2"],
                       "15-20-30": ["15","21","22","23","2427","2829","32","34","35"],
                       "Annað": ["33","31","A11","A13","D22B","C","C2","D","E"]}
     lst_Selected_Gate_Group = dct_GateGroups["E2"]
     dctFilter["Hlið"] = lst_Selected_Gate_Group[0]

     

# DATA REFRESH
     def event_refresh(e):
          fids = fidsmod.CallFIDS()
          Column_of_Cards.controls.clear()
          Column_of_Cards.controls=List_of_Cards(fids)
          page.update()
     btnFIDS = ft.OutlinedButton(text="Ný gögn", on_click=event_refresh) 

     def soft_refresh(GateGroup):
          dctFilter["Hlið"] = GateGroup[btnCurrentGate.data]
          # Update Gate Text
          btnCurrentGate.text = f"Hlið {GateGroup[btnCurrentGate.data]}"
          btnCurrentGate.update()
          Column_of_Cards.controls.clear()
          Column_of_Cards.controls=List_of_Cards(fids)
          page.update()

     def event_Change_GateGroup(e):
          # Update Gate Group
          lst_Selected_Gate_Group = dct_GateGroups[list(sgbMainHlið.selected)[0]]
          # Reset Current Gate
          btnCurrentGate.data = 0
          soft_refresh(lst_Selected_Gate_Group)
     
     sgbMainHlið = ft.SegmentedButton(
          on_change=event_Change_GateGroup,
          selected={"E2"},
          allow_empty_selection=False,
          allow_multiple_selection=False,
          segments=[
               ft.Segment(label=ft.Text("E2"), value="E2"),
               ft.Segment(label=ft.Text("15-20-30"), value="15-20-30"),
               ft.Segment(label=ft.Text("Annað"), value="Annað")
          ]
     )

     def event_Prev_Gate(e):
          # If index at the end, reset to zero
          lst_Selected_Gate_Group = dct_GateGroups[list(sgbMainHlið.selected)[0]]
          if len(lst_Selected_Gate_Group) > 1:
               if btnCurrentGate.data == 0:
                    btnCurrentGate.data = (len(lst_Selected_Gate_Group)-1)
               else: # Else increment
                    btnCurrentGate.data -= 1
               soft_refresh(lst_Selected_Gate_Group)
          
     def event_Next_Gate(e):
          # If index at the end, reset to zero
          lst_Selected_Gate_Group = dct_GateGroups[list(sgbMainHlið.selected)[0]]
          if len(lst_Selected_Gate_Group) > 1:
               if btnCurrentGate.data == (len(lst_Selected_Gate_Group)-1):
                    btnCurrentGate.data = 0
               else: # Else increment
                    btnCurrentGate.data += 1
               soft_refresh(lst_Selected_Gate_Group)

     
     btnCurrentGate = ft.OutlinedButton(text=f"Hlið {lst_Selected_Gate_Group[0]}", 
                                        on_click=event_Prev_Gate, data=0)
     
     def event_Change_Status(e):
          if btnStatus.value == "Almennt":
               dctFilter["Staða"] = ["Landed","Estimated","On time","Boarding","Go to Gate", "Final Call"]
          elif btnStatus.value == "Annað":
               dctFilter["Staða"] = ["Cancelled", "Departed", "Gate Closed", "All Bags on Belt"]
          soft_refresh(dct_GateGroups[list(sgbMainHlið.selected)[0]])

     btnStatus = ft.Dropdown(
          width=200,
          label="Staða flugs",
          options=[
               ft.dropdown.Option("Almennt"),
               ft.dropdown.Option("Annað")
          ],
          on_change=event_Change_Status
     )

     dctGLER = {
          "15": " - ",
          "21": " - ",
          "22": " - ",
          "23": " - ",
          "32": " - ",
          "34": " - ",
          "35": " - ",
          "2427": " - ",
          "2829": " - "
          }

     def event_GLER(e):
          dctGLER[e.control.label] = e.control.value
          print(dctGLER)

     def event_HORIZON(e):
          dctFilter["Tímarammi"] = ddHorizon.value
          soft_refresh(dct_GateGroups[list(sgbMainHlið.selected)[0]])
          print(dctFilter["Tímarammi"])

     

     
     rightdrawer = ft.NavigationDrawer(
          position=ft.NavigationDrawerPosition.END,
          controls=[
               
               ])

     

     page.add(
          sgbMainHlið,
          ft.Row([btnPrevGate,btnCurrentGate,btnNextGate]),
          Column_of_Cards) """