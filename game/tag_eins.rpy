label vorstellung:

    $ freund = 0 # beziehung zum freund
    $ lehrer = 0 # beziehung zum lehrer

    scene bg haupteingang with fade

    h "Willkommen in der Wilhelm-Raabe-Schule, %(vorname)s!"
    
    "Nanu?"
    "Wer ist da?"
    
    show x neutral:
        yanchor 0.0 ypos 1.0 xalign 0.5
        
        ease 0.5 yanchor 1.0
        
    h "Ich! Der Hausmeister!"
    
    h "Als Geschenk zum Schulanfang, überreiche ich dir dies hier!"
    
    $ giveItem("kamera","Du hast eine Digitalkamera erhalten!\nMit ihr kannst du Fotos machen und so Eindrücke festhalten, die du niemals vergessen willst!")
    
    h "Damit kannst du überall Fotos von Dingen und Orten schießen, die du nicht vergessen willst!"
    
    h "Bevor dein Schulalltag beginnt, möchte ich dir die Schule etwas näher vorstellen."    
    h "Bist du bereit?"
    menu:
        "Ja!":
            h "Okay!"
        "Nein!":
            h "Red keinen Unsinn, du kommst mit!"
            
    show x neutral at left with move
            
    h "Dies ist der Haupteingang dieses altehrwürdigen Gebäudes."
    h "Der damalige Stadtbausmeister Richard Kampf ließ es von 1906-1908 errichten."
    h "Dieser alte Gebäudeteil enthält zwei Hauptflügel und..."
    
    scene bg turm_aussen with wipedown
    
    h "...einen Turm!"
    
    scene bg neubau_aussen with fade
    
    h "1970 wurde dieser Neubau errichtet, in dem die naturwissenschaftlichen Räume untergebracht sind."
    h "Von 2006-2008 wurden die Fachräume renoviert und neue Klassenräume im Erdgeschoss eingerichtet."
    
    scene bg schulhof
    show x neutral at left with wipeleft
    
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
    
    h "So, nun muss ich aber wieder an die Arbeit!"
    h "In so einer Schule hat man viel zu tun."
    h "Wenn du mich brauchst, such mich einfach. {w}Ich bin immer irgendwo hier."
    h "Und bevor ich es vergesse..."
    h "Du solltest dich eventuell im Sekretariat melden. Da erfährst du dann auch in welche Klasse du musst."
    
    # hausmeister verschwindet
    
    "Also zum Sekretariat."
    "Wo finde ich das nur?"
    
    $ draussen = False
    while True:
        menu:
            "Ich glaube links.":
                "Ich gehe wohl mal nach links."
                jump tag_eins_links
            "Vielleicht rechts?":
                "Ich schaue besser mal rechts nach."
                jump tag_eins_rechts
            "Mit Sicherheit oben!":
                "Alles klar!"
                "Ab nach oben!"
                jump tag_eins_oben
            "Ich weiß! Es ist draußen!" if draussen == False:
                $ draussen = True
                "Ich will aber nicht raus."
                "Vielleicht ist es ja doch drinnen?"
                
label tag_eins_links:
    # hier folgt das treffen mit freund oder freundin
    "Gespräch mit Freund fehlt."
    # nach dem gespräch gehts oben weiter, es muss also passend enden
    jump tag_eins_oben
    
label tag_eins_rechts:
    # hier folgt das gespräch mit lehrerin oder lehrer
    "Gespräch mit Lehrer fehlt."
    # nach dem gespräch gehts oben weiter, es muss also passend enden
    jump tag_eins_oben
    
label tag_eins_oben:
    # der spieler kommt oben an
    "Szene für oben fehlt."
    jump tag_eins_lehrerzimmer
    
label tag_eins_lehrerzimmer:
    # hier wird das lehrerzimmer belauscht
    "Szene für Lehrerzimmer fehlt."
    # dann kommen freund oder lehrer
    if freund > 0:
        jump tag_eins_abholen_freund
    else:
        jump tag_eins_abholen_lehrer
    
label tag_eins_abholen_freund:
    # hier holt der freund einen zur ersten stunde ab
    "Szene fürs abholen durch den Freund fehlt."
    jump tag_eins_erste_stunde

label tag_eins_abholen_lehrer:
    # hier holt der lehrer einen zur ersten stunde ab
    "Szene fürs abholen durch den Lehrer fehlt."
    jump tag_eins_erste_stunde

label tag_eins_erste_stunde:
    # erste unterrichtsstunde
    "Erste Unterrichtsstunde fehlt."
    jump tag_eins_nach_dem_unterricht
    
label tag_eins_nach_dem_unterricht:
    # kurzer abschnitt nach dem unterricht
    "Abschnitt nach dem Unterricht fehlt."
    if freund > 0:
        jump tag_eins_gespräch_lehrer
    else:
        jump tag_eins_gespräch_freund
        
label tag_eins_gespräch_lehrer:
    # labern mit dem lehrer
    "Gespräch mit dem Lehrer fehlt."
    jump tag_eins_sekretariat
    
label tag_eins_gespräch_freund:
    # labern mit dem freund
    "Gespräch mit dem Freund fehlt."
    jump tag_eins_sekretariat
    
label tag_eins_sekretariat:
    # hier erhält man den raumplan
    "Gespräch im Sekretariat fehlt."
    "Demo vorbei!"