# -*- coding: utf-8 -*-

# Init-Abschnitt
# Definiert alle wichtigen Funktionen, Styles, etc.

init -1 python:
   
    import os,hashlib,math

    # Variablen

    show_button_menu = True
    show_inventory_menu = False
    show_camera_menu = False
    show_camera_large_pic = None
    show_camera_delete_prompt = False
    items = []

    # Alle Bilder laden
    imagepath = config.basedir + "/game/img/"    
    for path, dirs, files in os.walk(imagepath):
        for file in files:
            if file[-4:] not in [".jpg",".png"]: continue #nur png und jpg
            filename = path[len(imagepath):]+"/"+file
            nametuple = tuple(filename[:-4].split("/"))
            renpy.image(nametuple,"img/"+filename)
    
    # Klassen
    
    class item:
        """
        item(name,action,image=None)
        
        Defines an item that can be carried by the player.
        
        name - String. The name of the item.
        action - Callable. The function to call when the item is clicked.
        image - Displayable to use as the item picture. If none, name is used to load one.
        """
        
        def __init__(self,name,action,image=None):
            self.name = name
            self.action = action
            if image != None:
                self.image = image
            else:
                self.image = ImageReference(("item",name))

init python:

    # Tolle Funktionen
    
    def popupMessage(message,image=None,sound=None,time=None,transition=None):
        if transition:
            renpy.transition(transition)
        else:
            renpy.transition(dissolve)
        ui.window(xalign=0.5,yalign=0.5,xfill=False,background=Solid((0,0,0,100)))
        ui.vbox(xalign=0.5)
        if image:
            ui.image(image,xalign=0.5)
        ui.text(message,xalign=0.5,xmaximum=500,text_align=0.5)
        ui.close()
        if time:
            ui.pausebehavior(time)
        else:
            ui.saybehavior()
        ui.interact()
        renpy.transition(Dissolve(0.1))

    # Item-Funktionen
    
    def newItem(name,action,image=None):
        items.append(item(name,action,image))
        
    def giveItem(name,message=None):
        for i in items:
            if i.name == name:
                inventory.append(i)
                if message:
                    renpy.invoke_in_new_context(give_item_message,i,message)
            
    def give_item_message(item,message):
        popupMessage(message,item.image)
                
    def takeItem(name):
        for i in inventory:
            if i.name == name:
                del inventory[inventory.index(i)]
                
    def hasItem(name):
        for i in inventory:
            if i.name == name:
                return True
        return False
            
    # Haupt-Buttons
    
    def ui_button_menu():
        if show_button_menu == False:
            return
        
        ui.vbox(xpos=1.0,ypos=1.0,xanchor="right",yanchor="bottom")
        ui.textbutton("Inventar",clicked=toggle_ui_inventory)
        if (hasItem("kamera")):
            ui.textbutton("Kamera",clicked=camera_take_photo)
        if (hasItem("notizzettel")):
            ui.textbutton("Notizen",clicked=toggle_ui_notes)
        ui.close()
        
    config.window_overlay_functions.append(ui_button_menu)
    
    # Inventar
        
    def toggle_ui_inventory():
        global show_inventory_menu
        if show_inventory_menu == True:
            renpy.transition(CropMove(.3,"custom",(0,0,1.0,0.2),(0,0),(0,0,1.0,0.0),(0,0),topnew=False))
        else:
            renpy.transition(CropMove(.3,"custom",(0,0,1.0,0.0),(0,0),(0,0,1.0,0.2),(0,0),topnew=True))
        show_inventory_menu = not show_inventory_menu
        renpy.restart_interaction()
        
    def ui_inventory_menu():     
        if show_inventory_menu == False:
            return
        ui.window(area=(0,0,1024,100),ypadding=0,xpadding=0,clipping=True,background=Solid((0,0,0,128)))
        ui.hbox()
        for i in inventory:
            b_image = im.Scale(i.image,100,100)
            ui.imagebutton(b_image,im.MatrixColor(b_image,im.matrix.brightness(0.2)),clicked=i.action,ymargin=0,ypadding=0)
        ui.close()
    config.window_overlay_functions.append(ui_inventory_menu)
            
    # Notizen
    
    def toggle_ui_notes():
        pass
        
    # Items
    
    def item_camera():
        # Kamera-Bildschirm auf dem man alle gemachten Fotos anschauen oder neue machen kann.
        renpy.invoke_in_new_context(ui_camera_menu)
        return
    
    newItem("kamera",item_camera)
        
# Definitionen
define p = DynamicCharacter('vorname')
define h = Character('Hausmeister')
define f = Character('<FREUND NAME?>')
define r = Character('Schüler')
define u = Character('???')

image bg black = Solid((0,0,0,255))
image bg white = Solid((255,255,255,255))

# Hier startet das eigentliche Spiel
label start:
    
    $ photos = [ ]
    $ inventory = [ ]
    
    menu:
        "Formular überspringen?"
        "Ja":
            python:
                vorname = "Max"
                nachname = "Musterschüler"
                alter = 14
                geschlecht = "Männlich" 
            jump vorstellung
        "Nein":
            "OK"
            
    scene bg black with fade
    
    "Oh, das Anmeldeformular von der Schule ist da."
    
    # bild vom formular
    
    "Na dann werde ich das mal ausfüllen..."
    
    jump formular

label formular:
    python:
        vorname = ""
        nachname = ""
        alter = ""
        geschlecht = ""
        
        input_valid = False
        while input_valid == False:
            ui.window(area=(0,0,1024,768),background=Solid((0,0,0,255)))
            ui.vbox()
            
            ui.hbox()
            ui.window(style="ui_window",size_group="labels")
            ui.text("Vorname: ",xalign=1.0)
            ui.window(style="ui_window",size_group="inputs",xminimum=200)
            ui.text(vorname)
            ui.textbutton("Edit",clicked=ui.returns("edit_firstname"))
            ui.close()
            
            ui.hbox()
            ui.window(style="ui_window",size_group="labels")
            ui.text("Nachname: ",xalign=1.0)
            ui.window(style="ui_window",size_group="inputs",xminimum=200)
            ui.text(nachname)
            ui.textbutton("Edit",clicked=ui.returns("edit_lastname"))
            ui.close()
            
            ui.hbox()
            ui.window(style="ui_window",size_group="labels")
            ui.text("Alter: ",xalign=1.0)
            ui.window(style="ui_window",size_group="inputs",xminimum=200)
            ui.text("%s" % alter)
            ui.textbutton("Edit",clicked=ui.returns("edit_age"))
            ui.close()
            
            ui.hbox()
            ui.window(style="ui_window",size_group="labels")
            ui.text("Geschlecht: ")
            ui.window(style="ui_window",size_group="inputs",xminimum=200)
            ui.text("%s" % geschlecht)
            ui.textbutton("Edit",clicked=ui.returns("edit_gender"))
            ui.close()
            ui.textbutton("Absenden",clicked=ui.returns("done"))
            ui.close()
            
            result = ui.interact()
            
            if result == "edit_firstname":
                ui.window(style="ui_window",xalign=0.5,yalign=0.5,background=Solid((0,0,0,150)))
                ui.vbox()
                ui.text("Gib deinen Vornamen ein:",xalign=0.5)
                ui.input(vorname,xalign=0.5)
                ui.close()
                vorname = ui.interact()
            elif result == "edit_lastname":
                ui.window(style="ui_window",xalign=0.5,yalign=0.5,background=Solid((0,0,0,150)))
                ui.vbox()
                ui.text("Gib deinen Nachnamen ein:",xalign=0.5)
                ui.input(nachname,xalign=0.5)
                ui.close()
                nachname = ui.interact()
            elif result == "edit_age":
                ui.window(style="ui_window",xalign=0.5,yalign=0.5,background=Solid((0,0,0,150)))
                ui.vbox()
                ui.text("Gib dein Alter ein:",xalign=0.5)
                ui.input(str(alter),xalign=0.5,allow="0123456789",length=3)
                ui.close()
                alter = int(ui.interact())
            elif result == "edit_gender":  
                ui.window(style="ui_window",xalign=0.5,yalign=0.5,background=Solid((0,0,0,150)))
                ui.vbox()
                ui.text("Gib dein Geschlecht an:",xalign=0.5)
                ui.textbutton("Männlich",size_group="gender_buttons",clicked=ui.returns("Männlich"),xalign=0.5)
                ui.textbutton("Weiblich",size_group="gender_buttons",clicked=ui.returns("Weiblich"),xalign=0.5)
                ui.close()
                geschlecht = ui.interact()
            elif result == "done":
                if vorname != "" and nachname != "" and alter != "" and geschlecht != "":
                    input_valid = True
    
    "So, das wäre geschafft!"
    "Jetzt ab zum Briefkasten damit."
    
    $ renpy.pause(2.0)
    
    "Kurze Zeit später..."
    
    # bild mit "Du wurdest angenommen" usw.   
    jump vorstellung