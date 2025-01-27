import PySimpleGUIQt as g
import sys
import json

def get_layout(config, name, content):
    if 'darwin' in sys.platform:
        NTB = False
    else:
        NTB = config.no_titlebar
    if NTB:   
        layout = [
            [g.T(name, font=('Arial', int(config.title_size)), justification='center')],
            ]
    else:
        layout = []
    layout.extend([
            [g.Multiline(content, size=(None, int(config.height)), key='content')],
            [g.B('Close'), g.B('Delete'), g.B('Save')]
            ])
    return layout, NTB

def open_note(name, config):
    g.SetOptions(background_color=config.background_color, text_color=config.text_color,
                 input_elements_background_color=config.background_color, input_text_color=config.text_color,
                 button_color=(config.text_color, config.background_color), border_width=config.border_width, font=('Arial', int(config.font_size)))
    with open(config.notes_path, 'r+') as notes:
        note_obj = json.load(notes)
        match = False
        content = ''
    for k, v in note_obj.items():
        if name == k:
            match = True
            content = v
    if match == False:
        print('No Note Found With That Name')
        exit(1)

    layout, NTB = get_layout(config, name, content)
    window = g.Window(name, resizable=True, no_titlebar=NTB, keep_on_top=True, grab_anywhere=True, layout=layout, alpha_channel=float(config.alpha))
    
    while True:
        try:
            event, value = window.Read()
            # print(event,value)
            if event == 'Close' or event == None or event == 'Save':
                note_obj[name] = value['content']
                with open(config.notes_path, 'r+') as notes:
                    notes.seek(0)
                    notes.truncate()
                    json.dump(note_obj, notes, indent=4)
                if event == 'Close' or event == None:
                    window.Close()
                    break
            elif event == 'Delete':
                new_layout = [
                    [g.T('Are you sure you want to delete {}?'.format(name), justification='center')],
                    [g.B('No'), g.B('Yes')]
                ]
                confirm_window = g.Window('', no_titlebar=NTB, keep_on_top=True, grab_anywhere=True, layout=new_layout)
                while True:
                    event1, value1 = confirm_window.Read()
                    if event1 == 'Yes':
                        note_obj.pop(name, [])
                        with open(config.notes_path, 'r+') as notes:
                            notes.seek(0)
                            notes.truncate()
                            json.dump(note_obj, notes, indent=4)
                        confirm_window.Close()
                        break
                    else:
                        confirm_window.Close()
                        break
                window.Close()
                break
        except Exception as exc:
            print(exc)
            pass
                
def create_note(name, config):
    g.SetOptions(background_color=config.background_color, text_color=config.text_color,
                 input_elements_background_color=config.background_color, input_text_color=config.text_color,
                 button_color=(config.text_color, config.background_color), border_width=config.border_width, font=('Arial', int(config.font_size)))

    layout, NTB = get_layout(config, name, content="")
    window = g.Window(name, no_titlebar=NTB, auto_size_text=True, keep_on_top=True, grab_anywhere=True, layout=layout, alpha_channel=float(config.alpha))
    while True:
        try:
            event, value = window.Read()
            # print(event,value)
            if event == 'Close' or event == None or event == 'Save':
                with open(config.notes_path, 'r+') as notes:
                    note_obj = json.load(notes)
                    note_obj.update({
                        name: value['content']
                    })
                    notes.seek(0)
                    notes.truncate()
                    json.dump(note_obj, notes, indent=4)
                if event == 'Close' or event == None:
                    window.Close()
                    break
        except:
            pass
        
def list_notes(config):
    with open(config.notes_path, 'r+') as json_file:
        obj = json.load(json_file)
        print('Available Notes:\n')
        for k, v in obj.items():
            print(k)
def delete_note(name, config):
    with open(config.notes_path, "r+") as json_file:
        obj = json.load(json_file)
    try:
        del obj[name]
        print('Deleted note "{}".'.format(name))
    except KeyError:
        print('No note found with name "{}"'.format(name))

    with open(config.notes_path, "w") as json_file:
        json_file.write(json.dumps(obj, indent=4))
