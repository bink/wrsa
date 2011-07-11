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

    # Item-Funktionen
    
    def newItem(name,action,image=None):
        items.append(item(name,action,image))
        
    def giveItem(name):
        for i in items:
            if i.name == name:
                inventory.append(i)
                
    def takeItem(name):
        for i in inventory:
            if i.name == name:
                del inventory[inventory.index(i)]
            
    # Haupt-Buttons
    
    def ui_button_menu():
        if show_button_menu == False:
            return
        
        ui.vbox(xpos=1.0,ypos=1.0,xanchor="right",yanchor="bottom")
        ui.textbutton("Inventar",clicked=toggle_ui_inventory)
        ui.textbutton("Kamera",clicked=camera_take_photo)
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
        ui.window(area=(0,0,1024,100),ypadding=0,xpadding=0,clipping=True,background=Solid((0,0,0,128)))
        ui.hbox()
        for i in inventory:
            b_image = im.Scale(i.image,100,100)
            ui.imagebutton(b_image,im.MatrixColor(b_image,im.matrix.brightness(0.2)),clicked=i.action,ymargin=0,ypadding=0)
        ui.close()
    config.window_overlay_functions.append(ui_inventory_menu)

    # Kamera
    
    def ui_camera_menu():
        global show_camera_large_pic
        if show_camera_menu == False:
            return
        ui.image(ImageReference(("item","kamera_menu")))    
        
        #screen
        
        ui.side(('c', 'r'), xpos=171,ypos=221,xanchor='left',yanchor='top')
        ui.window(xmargin=0,ymargin=0,xpadding=0,ypadding=0,background=ImageReference(("item","kamera_menu_bg")))
        cam_vp = ui.viewport(area=(0,0,572,326),mousewheel=True,draggable=True,xmargin=0,ymargin=0)
        ui.window(xmargin=0,ymargin=0,xpadding=6,ypadding=6,background=None)
        picnum = len(photos)
        if picnum == 0:
            ui.window(yfill=True,xmargin=0,ymargin=0,background=Solid((0,0,0,40)))
            ui.text("Keine Fotos",xalign=0.5,yalign=0.5)
            ui.null()
        else:
            if show_camera_large_pic == None:# not showing zoomed, therefore showing grid
                rownum = int(math.ceil(picnum/5.0))
                ui.grid(5,rownum,10)
                phonum = 0
                for i in photos:
                    ui.button(clicked=ui_camera_large_pic(i),ypadding=2,xpadding=2,xmargin=0,ymargin=0)
                    ui.image(im.Scale("pho/"+i+".png",100,75))
                    phonum+=1
                for i in range(0,(5*rownum)-phonum):
                    ui.null()
                ui.close()
                ui.bar(adjustment=cam_vp.yadjustment, style='vscrollbar')
            else: #showing zoomed
                ui.image(im.Scale("pho/"+show_camera_large_pic+".png",418,314,xalign=0.5))
                ui.null()
        
        ui.close()
        #buttons
        ui.fixed(xpos=814,ypos=229)
        ui.imagebutton(Solid((255,255,255,0)),Solid((255,255,255,0)),clicked=ui_camera_zoom_pic,area=(36,54,53,53))
        ui.imagebutton(Solid((255,255,255,0)),Solid((255,255,255,0)),clicked=ui_camera_hide_large_pic,area=(36,130,53,53))
        ui.imagebutton(Solid((255,255,255,0)),Solid((255,255,255,0)),clicked=ui_camera_delete_pic,area=(36,205,53,53))
        ui.close()
    
    config.window_overlay_functions.append(ui_camera_menu)
    
    def _ui_camera_large_pic(p):
        global show_camera_large_pic
        show_camera_large_pic = p
        renpy.restart_interaction()
        
    ui_camera_large_pic = renpy.curry(_ui_camera_large_pic)
    
    def ui_camera_hide_large_pic():
        global show_camera_large_pic
        show_camera_large_pic = None
        renpy.restart_interaction()
    
    def ui_camera_zoom_pic():
        renpy.invoke_in_new_context(_ui_camera_zoom_pic)
    
    def _ui_camera_zoom_pic():
        if show_camera_large_pic == None:
            return None
        ui.window(yfill=True)
        ui.image("pho/"+show_camera_large_pic+".png",xalign=0.5,yalign=0.5)
        ui.saybehavior()
        ui.interact()
    
    def ui_camera_delete_pic():
        if show_camera_large_pic == None:
            return None
        del photos[photos.index(show_camera_large_pic)]
        ui_camera_hide_large_pic()
    
    def toggle_ui_camera():
        global show_camera_menu
        show_camera_menu = not show_camera_menu
        renpy.restart_interaction()
    
    def camera_take_photo():
        newPhoto = renpy.invoke_in_new_context(_camera_take_photo)
        photos.append(newPhoto)
        
    def _camera_take_photo():
        ui.pausebehavior(0.0)
        ui.interact(suppress_overlay=True, suppress_window=True)
        renpy.take_screenshot((800,600))
        photo = renpy.game.interface.get_screenshot()
        photoname = hashlib.md5(photo).hexdigest()
        photodir = config.basedir + "/game/pho/"
        if(os.path.isdir(photodir) == False):
            os.mkdir(photodir)
        f = open(photodir + photoname + ".png","wb")
        f.write(photo)
        f.close()
        return photoname
            
    # Notizen
    
    def toggle_ui_notes():
        pass
        
    # Items
    
    def item_camera():
        # Kamera-Bildschirm auf dem man alle gemachten Fotos anschauen oder neue machen kann.
        toggle_ui_camera()
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
    
label vorstellung:

    scene bg haupteingang with fade
    
    h "Willkommen in der Wilhelm-Raabe-Schule, %(vorname)s!"
    h "Als Geschenk zum Schulanfang, überreiche ich dir dies hier!"
    
    show item kamera:
        xalign 0.5 yalign 0.5
        zoom 0.0
        linear 0.5 zoom 1.0
    
    h "Eine brandneue Digitalkamera!"
    
    show item kamera:
        linear 0.5 zoom 0.0
    
    $ giveItem("kamera")
    
    h "Damit kannst du überall Fotos von Dingen und Orten schießen, die du nicht vergessen willst!"
    
    hide item kamera
    
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