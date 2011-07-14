init -1 python:
    
    import pygame
    from renpy.ui import Wrapper
    from renpy.display.behavior import map_event
    
    class Textarea(renpy.display.text.Text):
        """
        This is a Displayable that takes multiple lines of text as input.
        """
    
        changed = None
        prefix = ""
        suffix = ""
        
        def __init__(self,
                     default="",
                     length=None,
                     cols=None,
                     rows=None,
                     style='input',
                     allow=None,
                     exclude=None,
                     prefix="",
                     suffix="",
                     changed=None,
                     button=None,
                     replaces=None,
                     **properties):
    
            super(Textarea, self).__init__("", style=style, replaces=replaces, **properties)
    
            self.content = unicode(default)
            self.length = length
            self.cols = cols
            self.rows = rows
    
            self.allow = allow
            self.exclude = exclude
            self.prefix = prefix
            self.suffix = suffix
    
            self.changed = changed
    
            self.editable = True
            
            self.caret_pos = len(self.content)
    
            caretprops = { 'color' : None}
            for i in properties:
                if i.endswith("color"):
                    caretprops[i] = properties[i]
    
            self.caret = renpy.display.image.Solid(xmaximum=1, style=style, **caretprops)
    
            if button:
                self.editable = False
                button.hovered = HoveredProxy(self.enable, button.hovered)
                button.unhovered = HoveredProxy(self.disable, button.unhovered)
    
            if isinstance(replaces, Input):
                self.content = replaces.content
                self.editable = replaces.editable
    
            self.update_text(self.content, self.editable)
    
    
        def update_text(self, content, editable):
    
            if content != self.content or editable != self.editable:
                renpy.display.render.redraw(self, 0)
                                                
            if content != self.content:
                self.content = content
    
                if self.changed:
                    self.changed(content)
                    
            self.editable = editable
            
            content = content.replace("{", "{{")
                                                
            if editable:
                self.set_text([self.prefix, content[:self.caret_pos], self.caret, content[self.caret_pos:], self.suffix])
            else:
                self.set_text([self.prefix, content, self.suffix ])
    
        def get_text(self):
            return self.content
    
        def enable(self):
            self.update_text(self.content, True)
    
        def disable(self):
            self.update_text(self.content, False)
                
        def event(self, ev, x, y, st):
    
            content = self.content
    
            if not self.editable:
                return None
            
            if map_event(ev, "input_backspace"):
    
                if self.content:
                    content = self.content[:self.caret_pos-1] + self.content[self.caret_pos:]
                    self.caret_pos -= 1
                    self.update_text(content, self.editable)
                                                
                renpy.display.render.redraw(self, 0)
    
            elif map_event(ev, "input_enter"):
                content = self.content[:self.caret_pos] + "\n" + self.content[self.caret_pos:]
                self.caret_pos += 1
                self.update_text(content, self.editable)
                #if not self.changed:
                #    return self.content
    
            elif ev.type == pygame.KEYDOWN and ev.unicode and ev.key not in [pygame.K_LEFT,pygame.K_RIGHT]:
                if ord(ev.unicode[0]) < 32:
                    return None
                    
                if self.length and len(self.content) >= self.length:
                    raise renpy.display.core.IgnoreEvent()
    
                if self.allow and ev.unicode not in self.allow:
                    raise renpy.display.core.IgnoreEvent()
    
                if self.exclude and ev.unicode in self.exclude:
                    raise renpy.display.core.IgnoreEvent()
    
                content = self.content[:self.caret_pos] + ev.unicode + self.content[self.caret_pos:]
                self.caret_pos += 1
    
                self.update_text(content, self.editable)
    
                raise renpy.display.core.IgnoreEvent()
                
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    self.caret_pos -= 1
                    if self.caret_pos < 0:
                        self.caret_pos = 0
                    self.update_text(content,True)
                elif ev.key == pygame.K_RIGHT:
                    self.caret_pos += 1
                    if self.caret_pos > len(content):
                        self.caret_pos = len(content)
                    self.update_text(content,True)
                    
    textarea = Wrapper(Textarea, exclude='{}', style="input", replaces=True)