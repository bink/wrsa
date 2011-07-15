init -1 python:
    # Notizzettel
    
    def ui_note_menu():
        
        global notes
        
        exit = 0
        while exit != 1:
            renpy.transition(Dissolve(0.1))
            
            # notizzettel bild
            ui.window(area=(0,0,1024,768),xpadding=0,ypadding=0, background=ImageReference(("item","notizzettel_menu")))
            ui.window(area=(272,96,479,649),background=Solid((0,0,0,0)),clipping=True)
            ui.vbox()
            ui.window(background=Solid((0,0,0,0)),xpadding=0,ypadding=0,area=(0,0,479,546))
            txt = textarea(default=notes,color=(0,0,0,255),size=30,line_spacing=-4)
            txb = ui.button(clicked=ui.returns("save"))
            ui.text("Fertig")
            ui.close()
            
            
            action = ui.interact()
            
            if action == "save":
                notes = txt.get_text()
                exit = 1