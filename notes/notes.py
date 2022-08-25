import csv


notes = []


def write_note(note: str):
    notes_in_fun = notes

    # заметка выглядит так: <текст заметки> <вермя> <приоритет>
    note = note.split(" ")
    notes_in_fun.append(note)

    notes_in_fun = sorted(notes_in_fun, key=lambda nt: (-int(nt[2])))

    with open("notes/notes.csv", "w", encoding="utf8") as note:
        writer = csv.writer(note)
        writer.writerows(notes_in_fun)

    return "Ваша заметка была вписана"


def del_note_by_text(text: str):
    notes_in_fun = notes
    for nt in range(len(notes_in_fun)):
        if nt[0] == text:
            del notes_in_fun[nt]
            return "Ваша заметка была удалена"
    else:
        return "Увы, но такой заметки нет. Мне жаль."


def del_note_by_time(time: str):
    notes_in_fun = notes

    for nt in range(len(notes_in_fun)):
        if nt[1] == time:
            del notes_in_fun[nt]
            return "Ваша заметка была удалена"
    else:
        return "Увы, но такой заметки с таким временем нет. Мне жаль."
