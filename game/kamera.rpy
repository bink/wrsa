init -1 python:
    # Kamera
    
    def ui_camera_menu():
        global show_camera_large_pic
        #if show_camera_menu == False:
        #    return
        ui.window(area=(0,0,1024,768))
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
        
        ui.interact()
    
    #config.window_overlay_functions.append(ui_camera_menu)
    
    def _ui_camera_large_pic(p):
        global show_camera_large_pic
        print "lol"
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