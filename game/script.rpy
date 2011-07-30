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
define h = Character('Hausmeister')

image bg black = Solid((0,0,0,255))
image bg white = Solid((255,255,255,255))

# Hier startet das eigentliche Spiel
label start:
    
    $ photos = [ ]
    $ inventory = [ ]
    
    jump vorstellung
    
    scene bg black with fade
    
    "Oh, das Anmeldeformular von der Schule ist da."
    
    # bild vom formular
    
    "Na dann werde ich das mal ausfüllen..."
    
    jump formular
    
label formular:
    "Zuerst den Vornamen."
    $ vorname = renpy.input("Vorname:","Max",length=50)
    "OK, jetzt den Nachnamen."
    $ nachname = renpy.input("Nachname:",u"Musterschüler",length=50)    
    "Nun noch das Alter..."

label altersinput:
    $ alter = renpy.input("Alter:","14",length=3,allow="0123456789")
    python:
        try:
            alter = int(alter)
        except:
            alter = 14
    "Und das Geschlecht."
    menu:
        "Geschlecht:"
        "Männlich":
            $ geschlecht = u"Männlich"
        "Weiblich":
            $ geschlecht = u"Weiblich"
    "So, schon fertig!"
    "Stimmt das nun auch alles?"
    menu:
        "Name: %(vorname)s %(nachname)s. %(geschlecht)s. %(alter)s Jahre alt."
        "Stimmt!":
            "Super, stimmt alles!"
            "Dann ab damit zur Post..."
            
            $ renpy.pause(1.0)
            
            "Kurze Zeit später..."
            
            # herzlichen glückwunsch, sie wurden angenommen!
            jump vorstellung
        "Nein, warte...":
            "Ups, das stimmt ja gar nicht!"
            "Also nochmal..."
            jump formular