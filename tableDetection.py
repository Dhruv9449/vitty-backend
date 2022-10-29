"""Importing necessary modules"""

import re


# V1
def fetch_text_timetable(text):
    data, slots = [], []
    slots += re.findall(
        r"[A-Z]{1,3}[0-9]{1,2}[\D]{1}[A-Z]{3,4}[0-9]{3,4}[A-Z]{0,1}[\D]{1}[A-Z]{2,3}[\D]{1}[A-Z]{2,6}[0-9]{2,4}[A-Za-z]{0,1}[\D]{1}[A-Z]{2,4}[0-9]{0,3}",
        text,
    )
    for single_slot in slots:
        slot = re.findall(r"[A-Z]{1,3}[0-9]{1,2}\b", single_slot)[0]
        course_name = re.findall(r"[A-Z]{3,4}[0-9]{3,4}[A-Z]{0,1}\b", single_slot)[0]
        course_code = re.findall(r"[ETH,SS,ELA,LO]{2,3}\b", single_slot)
        course_type = "Lab" if course_code[0] in ("ELA", "LO") else "Theory"
        venue = re.findall(r"[A-Z]{2,6}[0-9]{2,4}[A-Za-z]{0,1}\b", single_slot)[1]
        slot_data = {
            "Parsed_Data": single_slot,
            "Slot": slot,
            "Course_Name": course_name,
            "Course_type": course_type,
            "Venue": venue,
        }
        data.append(slot_data)
    return {"Slots": data}


# V2
def fetch_text_timetable_v2(text):
    text = text.replace("\r", "")
    code_and_name = [
        i[:-1].split(" - ")
        for i in re.findall("[A-Z]{4}[0-9]{3}.+\n|[A-Z]{3}[0-9]{4}.+\n", text)
    ]
    venue = [i[3:-1] for i in re.findall("\n{3}[A-Z]+[0-9]{1,3}.+\n|\n{3}NIL\n", text)]
    slots = [i[:-3].split("+") for i in re.findall(".+\d.+[-]\n|NIL.+[-]\n", text)]
    data = []

    try:
        for i in range(len(slots)):
            if slots[i][0] != "NIL":
                for slot in slots[i]:
                    slot_data = {
                        "Parsed_Data": "NIL",
                        "Slot": slot,
                        "Course_Name": code_and_name[i][0],
                        "Course_Full_Name": code_and_name[i][1],
                        "Venue": venue[i],
                        "Course_type": "Lab" if slot[0] == "L" else "Theory",
                    }
                    data.append(slot_data)

    except IndentationError:
        data = []
    return {"Slots": data}
