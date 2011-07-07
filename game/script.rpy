# -*- coding: utf-8 -*-

# Init-Abschnitt
# Definiert alle wichtigen Funktionen, Styles, etc.

init -1 python:

    # Variablen

    show_button_menu = True
    show_inventory_menu = False
    photos = []

init python:

    import os,hashlib

    # Alle Bilder laden
    imagepath = config.basedir + "/game/img/"    
    for path, dirs, files in os.walk(imagepath):
        for file in files:
            if file[-4:] not in [".jpg",".png"]: continue #nur png und jpg
            filename = path[len(imagepath):]+"/"+file
            nametuple = tuple(filename[:-4].split("/"))
            renpy.image(nametuple,"img/"+filename)
            
    # Haupt-Buttons
    
    def ui_button_menu():
        if show_button_menu == False:
            return
        
        ui.vbox(xpos=1.0,ypos=1.0,xanchor="right",yanchor="bottom")
        ui.textbutton("Inventar",clicked=toggle_ui_inventory)
        ui.textbutton("Kamera",clicked=toggle_ui_camera)
        ui.textbutton("Notizen",clicked=toggle_ui_notes)
        ui.close()
        
    config.window_overlay_functions.append(ui_button_menu)
    
    # Inventar
        
    def toggle_ui_inventory():
        global show_inventory_menu
        show_inventory_menu = not show_inventory_menu
        renpy.restart_interaction()
        
    def ui_inventory_menu():     
        if show_inventory_menu == False:
            return
        ui.window(xpos=0.0,xanchor="left",ypos=0.0,yanchor="top",ymaximum=100,background=Solid((0,0,0,128)))
        ui.hbox()
        # write items here
        ui.close()
            
    config.window_overlay_functions.append(ui_inventory_menu)
        
    # Kamera
    
    def toggle_ui_camera():
        renpy.invoke_in_new_context(camera_take_photo)
        pass
        
    def camera_take_photo():
        ui.pausebehavior(0.01)
        ui.interact(suppress_overlay=True, suppress_window=True)
        renpy.take_screenshot((800,600))
        photo = renpy.game.interface.get_screenshot()
        photoname = hashlib.md5(photo).hexdigest()
        f = open(config.basedir + "/game/pho/" + photoname + ".png","w")
        f.write(photo)
        f.close()
        return photoname
    
    # Notizen
    
    def toggle_ui_notes():
        pass

# Definitionen
define h = Character('Hausmeister')

image bg black = Solid((0,0,0,255))
image bg white = Solid((255,255,255,255))

# Hier startet das eigentliche Spiel
label start:

    #$ result = renpy.imagemap("bg haupteingang",im.MatrixColor(ImageReference("bg haupteingang"),im.matrix.contrast(1.5)),[(350,377,468,555,"keks"),(598,377,735,555,"keks")])
    
    #$ print result
    
    scene bg black with fade
    
    "Oh, das Anmeldeformular von der Schule ist da."
    
    # bild vom formular
    
    "Na dann werde ich das mal ausfüllen..."
    
    jump formular
    
label formular:
    "Zuerst den Vornamen."
    $ vorname = renpy.input("Vorname:","",length=50)
    "OK, jetzt den Nachnamen."
    $ nachname = renpy.input("Nachname:","",length=50)
    "Nun noch das Alter..."
    $ alter = int(renpy.input("Alter:","",length=3,allow="0123456789"))
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
    
label vorstellung:
    scene bg haupteingang with fade
    
    h "Willkommen in der Wilhelm-Raabe-Schule, %(vorname)s!"
    h "Bevor dein Schulalltag beginnt, möchte ich dir die Schule etwas näher vorstellen."
    h "Bist du bereit?"
    menu:
        "Ja!":
            h "Okay!"
        "Nein!":
            h "Red keinen Unsinn, du kommst mit!"
    
    h "Dies ist der Haupteingang dieses altehrwürdigen Gebäudes."
    h "Der damalige Stadtbausmeister Richard Kampf ließ es von 1906-1908 errichten."
    h "Dieser alte Gebäudeteil enthält zwei Hauptflügel und..."
    
    scene bg turm_aussen with wipedown
    
    h "...einen Turm!"
    
    scene bg neubau_aussen with fade
    
    h "1970 wurde dieser Neubau errichtet, in dem die naturwissenschaftlichen Räume untergebracht sind."
    h "Von 2006-2008 wurden die Fachräume renoviert und neue Klassenräume im Erdgeschoss eingerichtet."
    
    scene bg schulhof with wipeleft
    
    h "Dies ist der Schulhof."
    h "Er wurde erst vor ein paar Wochen fertiggestellt."
    h "Vorher glich er einer staubigen Wüste, die sich im Herbst in einen Sumpf verwandelte, haha!"
    h "Sehen wir uns mal das Gebäude von innen an! Folge mir!"
    
    scene bg black with fade # foto von vor der halle
    
    h "Hier befindet sich unsere schöne Gymnastikhalle."
    h "Sie ist so alt wie das Gebäude und wenn sie abbrennen würde sicherlich nicht gesundheitsfördernd, aber egal!"
    h "Das da vorne ist eine Treppe in den ersten Stock."
    h "Gehen wir nun über diesen langen Flur in die Eingangshalle."
    
    # eingangshalle
    
    h "Sieh dir diese beeindruckende Halle an!"
    h "Über diese Flügeltür geht es wieder auf den Schulhof."
    h "Folgst du dieser Treppe, gelangst du in den ersten Stock."
    