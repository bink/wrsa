init -1 python:
    # Kamera
    
    def ui_camera_menu():
        global show_camera_large_pic
        global show_camera_delete_prompt
        
        exit = 0
        flash = 0
        while exit != 1:
            if flash == 0:
                renpy.transition(Dissolve(0.1))
            
            # kamera bild
            ui.window(area=(0,0,1024,768),xpadding=0,ypadding=0, background=ImageReference(("item","kamera_menu")))
            
            # bildschirm
            ui.window(area=(172,221,583,326),background=ImageReference(("item","kamera_menu_bg")))
            ui.hbox(xfill=True,yfill=True) # horizontal angeordnet
            
            cam_vp = ui.viewport(area=(0,0,434,326),mousewheel=True,draggable=True,xmargin=0,ymargin=0)
            ui.window(background=None,xpadding=0,ypadding=0,xfill=False,) # inhalt des viewports
            picnum = len(photos)
            rowmax = 4.0
            if picnum <= 0: # keine Fotos oder weniger als keine
                ui.window(yfill=True,background=Solid((0,0,0,40)))
                ui.text("Keine Fotos",xalign=0.5,yalign=0.5)
            else: # es gibt fotos
                if show_camera_large_pic == None: # alle fotos anzeigen
                    rownum = int(math.ceil(picnum/rowmax))
                    ui.grid(int(rowmax),rownum,5) # grid bauen
                    phonum = 0
                    for i in photos: # grid füllen
                        ui.button(clicked=ui_camera_large_pic(i),ypadding=1,xpadding=1,xmargin=0,ymargin=0,background=Solid((100,100,100,200)),hover_background=Solid((200,200,200,200)))
                        ui.image(im.Scale("pho/"+i+".png",100,75))
                        phonum+=1
                    for i in range(0,(rowmax*rownum)-phonum):
                        ui.null()
                    ui.close() # close grid
                else: # zoom foto anzeigen
                    ui.fixed(xfill=False,background=Solid((0,0,0,100)))
                    pho = im.Scale("pho/"+show_camera_large_pic+".png",400,300)
                    ui.imagebutton(pho,pho,xalign=0.5,yalign=0.5,clicked=ui_camera_zoom_pic)
                    if show_camera_delete_prompt == True:
                        ui.fixed()
                        ui.window(xfill=True,yfill=True,xmargin=40,ymargin=40,ypadding=50,background=Solid((0,0,0,200)))
                        ui.vbox(xalign=0.5)
                        ui.text("Dieses Bild wirklich löschen?",xalign=0.5,yalign=0.5)
                        ui.null(1,70)
                        ui.hbox(xalign=0.5)
                        ui.textbutton("Ja",clicked=ui_camera_delete_pic,xminimum=100)
                        ui.null(70,1)
                        ui.textbutton("Nein",clicked=ui_camera_hide_delete_prompt,xminimum=100)
                        ui.close()
                        ui.close()
                        ui.close()
                    ui.close()
           
            ui.bar(adjustment=cam_vp.yadjustment,style="vscrollbar",yfill=True,unscrollable="hide")

            ui.vbox(yalign=0.5) # buttons
            b = "img/item/kamera_button_"
            ui.imagebutton(im.Recolor(b+"power.png",255,255,255,100),b+"power.png",clicked=ui.returns("exit"),xalign=0.5)
            if show_camera_large_pic != None:
                ui.imagebutton(im.Recolor(b+"zoom.png",255,255,255,100),b+"zoom.png",clicked=ui_camera_zoom_pic,xalign=0.5)
                ui.imagebutton(im.Recolor(b+"gallery.png",255,255,255,100),b+"gallery.png",clicked=ui_camera_hide_large_pic,xalign=0.5)
                ui.imagebutton(im.Recolor(b+"delete.png",255,255,255,100),b+"delete.png",clicked=ui_camera_show_delete_prompt,xalign=0.5)
            else:
                ui.null(76,76)
                ui.null(76,76)
                ui.null(76,76)
            
            ui.close() # close vbox
            ui.close() # close hbox
            
            ui.fixed(xpos=790,ypos=110)
            ui.imagebutton(ImageReference(("item","kamera_button_up")),Solid((0,0,0,0)),area=(0,0,90,50),clicked=camera_take_photo)
            ui.close()
            
            action = ui.interact()
            
            if action == "exit":
                exit = 1
            if action == "photo_taken":
                flash = 1
            else:
                flash = 0
    
    #config.window_overlay_functions.append(ui_camera_menu)
    
    def _ui_camera_large_pic(p):
        global show_camera_large_pic
        show_camera_large_pic = p
        return 0
        
    ui_camera_large_pic = renpy.curry(_ui_camera_large_pic)
    
    def ui_camera_hide_large_pic():
        global show_camera_large_pic
        show_camera_large_pic = None
        return 0
    
    def ui_camera_zoom_pic():
        renpy.invoke_in_new_context(_ui_camera_zoom_pic)
    
    def _ui_camera_zoom_pic():
        if show_camera_large_pic == None:
            return None
        renpy.transition(Dissolve(0.3))
        ui.window(yfill=True)
        ui.image("pho/"+show_camera_large_pic+".png",xalign=0.5,yalign=0.5)
        ui.saybehavior()
        ui.interact()
    
    def ui_camera_show_delete_prompt():
        global show_camera_delete_prompt
        show_camera_delete_prompt = True
        return 0
        
    def ui_camera_hide_delete_prompt():
        global show_camera_delete_prompt
        show_camera_delete_prompt = False
        return 0
    
    def ui_camera_delete_pic():
        if show_camera_large_pic == None:
            return None
        del photos[photos.index(show_camera_large_pic)]
        ui_camera_hide_delete_prompt()
        return ui_camera_hide_large_pic()
        
    
    def toggle_ui_camera():
        global show_camera_menu
        show_camera_menu = not show_camera_menu
        renpy.restart_interaction()
    
    def camera_take_photo():
        newPhoto = renpy.invoke_in_new_context(_camera_take_photo)
        renpy.transition(Fade(0,0,0.5,color=(255,255,255,255)))
        photos.append(newPhoto)
        return "photo_taken"
        
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