label vorstellung:

    $ freund = 0 # beziehung zum freund
    $ lehrer = 0 # beziehung zum lehrer

    scene bg haupteingang with fade

    h "Willkommen in der Wilhelm-Raabe-Schule, [vorname]!"
    
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
    
    scene bg schulhof with wipeleft
    show x neutral at left with dissolve
    
    h "Dies ist der Schulhof."
    h "Er wurde erst vor ein paar Wochen fertiggestellt."
    h "Vorher glich er einer staubigen Wüste, die sich im Herbst in einen Sumpf verwandelte, haha!"
    h "Sehen wir uns mal das Gebäude von innen an! Folge mir!"
    
    scene bg gymnastikhalle with fade # foto von vor der halle
    
    show x neutral at left with dissolve
    
    h "Hier befindet sich unsere schöne Gymnastikhalle."
    h "Sie ist so alt wie das Gebäude und wenn sie abbrennen würde sicherlich nicht gesundheitsfördernd, aber egal!"
    h "Das da vorne ist eine Treppe in den ersten Stock."
    h "Gehen wir nun über diesen langen Flur in die Eingangshalle."
    
    scene bg eingangshalle_doppeltuer with fade
    show x neutral at left with dissolve
    
    h "Sieh dir diese beeindruckende Halle an!"
    
    with None
    show bg eingangshalle_schulhoftuer
    show x neutral at right
    with dissolve
    
    h "Über diese Flügeltür geht es wieder auf den Schulhof."
    
    with None
    show bg eingangshalle_treppe
    show x neutral at left
    with dissolve
    
    h "Folgst du dieser Treppe, gelangst du in den ersten Stock."
    
    show x neutral at center with move
    
    h "So, nun muss ich aber wieder an die Arbeit!"
    h "In so einer Schule hat man viel zu tun."
    h "Wenn du mich brauchst, such mich einfach. {w}Ich bin immer irgendwo hier."
    h "Und bevor ich es vergesse..."
    h "Du solltest dich eventuell im Sekretariat melden. Da erfährst du dann auch in welche Klasse du musst."
    
    # hausmeister verschwindet
    
    hide x with dissolve
    
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
    scene bg gang_links_eg
    with fade
    "Ob es hier wirklich zum Sekretariat geht?"
    "Sieht irgendwie nicht so aus."
    "Ich hätte wohl besser jemanden fragen sollen."
    $ freund += 5
    # hier folgt das treffen mit freund oder freundin
    # entsprechend wird aufgespalten
    if geschlecht == "Männlich":
        # bild freund
        "Typ" "Hast dich wohl verlaufen, was?"
        "Wer ist der denn? {w}Und wieso labert der mich so von der Seite an?"
        "Typ" "Bist du neu hier?"
        "Typ" "Hab dich noch nie hier gesehen."
        # erste frage
        menu:
            "Ja, heute ist mein erster Schultag.":
                p "Ja, heute ist mein erster Schultag."
                "Typ" "War ja klar."
                "Typ" "Die neuen verlaufen sich dauernd hier."
                "Typ" "Dabei stehen extra überall Schilder... {w}aber lesen kannste wohl nicht."
                menu:
                    "Haha! Sehr witzig!":
                        p "Haha! Sehr witzig!"
                        p "Du hälst dich wohl für besonders lustig, was?"
                        "Typ" "Hey... man darf doch wohl mal einen Witz machen..."
                    "Nein... das hab ich nie gelernt.":
                        p "Nein... das hab ich nie gelernt."
                        "Typ" "W-Was?"
                        "Typ" "Echt nicht?"
                        p "Das war ein Witz."
                        "Typ" "..."
                        "Typ" "Ich weiß..."
            "Nein, ich bin schon lange hier.":
                p "Nein, ich bin schon lange hier."
                "Typ" "Ja klar."
                "Typ" "Dann kannst du mir sicher sagen, wo es hier zum Sekretariat geht, oder?"
                p "..."
                "Typ" "Dachte ich mir doch!"
                "Typ" "Du bist sehr wohl neu!"
                p "Ja."
                "Typ" "Das merkt man sofort."
            "Das geht dich gar nichts an!":
                p "Das geht dich gar nichts an!"
                "Typ" "Reg dich nicht gleich so auf."
                "Typ" "Wollte ja nur helfen."
        # zweite frage
        $ antworten = [] # Wird gesetzt um herauszufinden ob der Spieler bereits alle wichtigen Infos hat
        while not 1 in antworten:
            menu:
                "Kannst du mir sagen, wie ich zum Sekretariat komme?":
                    p "Kannst du mir sagen, wie ich zum Sekretariat komme?"
                    p "Ich soll mich da melden aber hab keine Ahnung wo es ist."
                    "Typ" "Klar kann ich das."
                    "Typ" "Du gehst zurück in die Eingangshalle und dann die Treppe nach oben."
                    "Typ" "Da siehst du es dann schon."
                    "Typ" "Alles klar?"
                    p "Glaub schon."
                    p "Danke für die Hilfe."
                    "Typ" "Hey, warte mal!"
                    p "Was denn?"
                    "Typ" "Ich bin [freundvorname]."
                    f "Wie heißt du?"
                    p "[vorname]."
                    f "Alles klar, [vorname]."
                    f "Man sieht sich!"
                    # verschwindet
                    "Komischer Typ."
                    $ antworten.append(1) # alle infos erhalten, weiter
                "Wer bist du überhaupt?" if not 2 in antworten: 
                    p "Wer bist du überhaupt?"
                    "Typ" "Ich bin [freundvorname]."
                    f "Und du?"
                    p "[vorname]."
                    f "Freut mich, [vorname]."
                    $ antworten.append(2) # antwort bereits gewählt
                "Tschüss!":
                    p "Tschüss!"
                    "Typ" "Hey! Warte doch mal!"
                    "Typ" "Du kennst dich doch überhaupt nicht hier aus, oder?"
                    "Typ" "Wohin willst du denn?"
                    p "Zum Sekretariat."
                    "Typ" "Kein Problem!"
                    "Typ" "Einfach die Treppe in der Eingangshalle nach oben und schon siehst du es."
                    "Typ" "Verstanden?"
                    p "Denke schon."
                    p "Danke für die Hilfe."
                    "Typ" "Wie heißt du überhaupt?"
                    p "[vorname]."
                    "Typ" "Freut mich, [vorname]."
                    "Typ" "Ich bin [freundvorname]."
                    f "Also dann... {w}wir laufen uns bestimmt nochmal über den Weg, wenn du jetzt hier zur Schule gehst."
                    f "Bis dann!"
                    # verschwindet
                    "Komischer Typ."
                    $ antworten.append(1) # alle infos erhalten, weiter
        "Also muss ich doch nach oben."
        "Dann mal los..."
    elif geschlecht == "Weiblich":
        "Dialog für Freundin fehlt."
    # nach dem gespräch gehts oben weiter, es muss also passend enden
    jump tag_eins_oben
    
label tag_eins_rechts:
    # hier folgt das gespräch mit lehrerin oder lehrer
    "Gespräch mit Lehrer fehlt."
    # nach dem gespräch gehts oben weiter, es muss also passend enden
    jump tag_eins_oben
    
label tag_eins_oben:
    # der spieler kommt oben an
    "Puh, hier ist ja alles voller Türen."
    "Welche führt denn nun zum Sekretariat?"
    menu:
        "Was mach ich nur?"
        "Ich sollte einen Schüler fragen.":
            jump tag_eins_schueler_fragen
        "Ich probier einfach eine Tür aus.":
            "Ach, was solls!"
            "Ich nehm einfach diese Tür hier!"
            $ rand = renpy.random.randint(1,3)
            $ print rand
            if rand == 1:
                # bild vom sek
                "Tatsache, hier stehts sogar dran."
                "Volltreffer!"
                jump tag_eins_sekretariat
            elif rand == 2:
                # bild vom direktorzimmer
                "Dann klopf ich mal hier."
                # klopfgeräusch
                "..."
                # klopfgeräusch
                "Macht keiner auf."
                jump tag_eins_schueler_fragen
            elif rand == 3:
                # bild vom koordinatorenzimmer
                "Hier steht Koordinatoren dran."
                "Ob ich klopfen soll?"
                "Ich horche lieber mal an der Tür..."
                "..."
                "..."
                "Stille."
                "Nein, hier arbeitet bestimmt nie jemand."
                "Aber ich weiss immer noch nicht, wo das Sekretariat ist."
                jump tag_eins_schueler_fragen
                
label tag_eins_schueler_fragen:
    "Ich frag einfach mal jemanden, der vorbeikommt."
    "Ah, da ist ja jemand."
    p "Entschuldigung!"
    r "Hä?"
    p "Kannst du mir vielleicht sagen, wo das Sekretariat ist?"
    p "Ich bin neu hier und kenne mich nicht aus."
    r "Äh..."
    r "Da hinten?"
    p "...ok."
    "Scheint als wären die hier nicht besonders gesprächig."
    "Immerhin weiss ich jetzt, wo das Sekretariat ist, also schau ich mal dort vorbei."
    # bild vom sek
    "Das hier muss es sein."
    jump tag_eins_sekretariat
    
label tag_eins_sekretariat:
    "Dann klopf ich mal an..."
    # klopf ton
    "Hm..."
    "Macht keiner auf?"
    # klopf ton
    "..."
    "Oh, hier hängt ein Zettel."
    "”Öffnungszeiten: 8-10 Uhr und 11-14 Uhr\nBei dringenen Fragen bitte im Lehrerzimmer melden.”"
    "Von 10 bis 11 ist also Mittagspause?"
    "Super, es ist eine Minute nach Zehn!"
    "Dann muss ich wohl zum Lehrerzimmer."
    jump tag_eins_lehrerzimmer

label tag_eins_lehrerzimmer:
    # hier wird das lehrerzimmer belauscht
    "Ich würde mal behaupten, dass es hinter dieser Tür ist."
    "Nanu?"
    "Die steht ja offen?"
    "Gut, dann muss ich ja gar nicht klopfen."
    "Ich werd einfach mal fragen."
    "Oh, da redet grad jemand."
    # bild vom lehrerzimmer innen
    # zwei lehrer und "der unbekannte"
    # ein spalt durch den man die szene sieht
    u "Das bedarf aber noch einiger Vorbereitungen."
    u "Wir dürfen uns keinerlei Fehler leisten."
    "Großer Lehrer" "Das Stimmt."
    "Großer Lehrer" "Wenn das schiefgehen sollte dann... (undeutliches Gemurmel)"
    "Kleine, dicke Lehrerin" "Aber wir müssen sehr vorsichtig sein."
    "Kleine, dicke Lehrerin" "In der Tat brauchen wir noch viel Zeit und Vorbereitungen."
    "Kleine, dicke Lehrerin" "Aber die Schüler dürfen auf keinen Fall etwas davon mitbekommen."
    u "Richtig. {w}Wir müssen schnell, effizient und unauffällig handeln."
    u "Nicht auszudenken, was sonst passieren würde."
    u "Unser Plan (genuschel) hinfällig und (laute Nebengeräusche) Massenpanik!"
    "Kleine, dicke Lehrerin" "Zum Glück hat mit der Lieferung (lautes Niesen) geklappt."
    "Kleine, dicke Lehrerin" "Und (geräuschvolles Naseputzen) ist gut versteckt."
    "Großer Lehrer" "Wo denn, wenn man fragen darf?"
    "Großer Lehrer" "Man weiß ja nie. {w}Am besten wir wissen alle wo..."
    "Kleine, dicke Lehrerin" "(Jemand fängt an laut und ausgiebig mit Papier zu rascheln)... Tür."
    "Kleine, dicke Lehrerin" "Der Schlüssel bleibt allerdings (Kaffeemaschine röchelt)... nur zur Sicherheit."
    u "Gut. {w}Und zur Sicherheit sollten wir diese Besprechung ein anderes Mal fortsetzen und das Lehrerzimmer wieder öffnen."
    u "So, die nächste Dienstbesprechung findet dann wie verabredet statt."
    u "Ach ja, und da der Kollege (XY) immer noch krank ist, muss eine Dauervertretung für seine 8. Klasse organisiert werden."
    u "Ich muss jetzt jedenfalls noch ein paar Atlanten holen."
    "Oh, oh."
    "Sie kommen raus."
    "Ich gehe besser."
    
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
    jump tag_eins_endlich_sekretariat
    
label tag_eins_gespräch_freund:
    # labern mit dem freund
    "Gespräch mit dem Freund fehlt."
    jump tag_eins_endlich_sekretariat
    
label tag_eins_endlich_sekretariat:
    # hier erhält man den raumplan
    "Gespräch im Sekretariat fehlt."
    "Demo vorbei!"