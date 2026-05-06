import json
from datetime import datetime

# All laptop data from Excel
laptops_data = [
    {"user": "KeyAns", "system": "SKLA-001", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 12gb Ram, 240SSD", "serial": "G20Z432", "location": "Office 1", "year": "2014", "condition": "Working"},
    {"user": "Dead in office 2", "system": "SKLA-002", "model": "Lattitude 3440", "config": "Intel I3 4th gen 12gb Ram, 240SSD", "serial": "430Z432", "location": "Office 2", "year": "2014", "condition": ""},
    {"user": "Sivarathri Narendra", "system": "SKLA-003", "model": "Lattitude 3440", "config": "Intel I3 4th, 12gb Ram, 240SSD", "serial": "Not Available", "location": "Office 2", "year": "2014", "condition": "In Stock(working condition)"},
    {"user": "nikhil prasad for automation", "system": "SKLA-004", "model": "Dell Inspiron 15-3567", "config": "Intel I5 7th gen, 16gb Ram, 240SSD", "serial": "GFCWZN2", "location": "Office 2", "year": "2018", "condition": "In Stock(working condition)"},
    {"user": "Sheetal mam (kalpesh Sir took)", "system": "SKLA-005", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 8gb Ram, 240SSD", "serial": "J20Z432", "location": "Office 1", "year": "2014", "condition": ""},
    {"user": "Golla Devraju (in stock)", "system": "SKLA-006", "model": "Latitude E6430", "config": "Intel I7,8GB RAM,500HDD", "serial": "JFFMSW1", "location": "Office 2", "year": "2013", "condition": "In Stock( Not working condition)"},
    {"user": "Siva kabilan banglore", "system": "SKLA-007", "model": "Vostro 3590", "config": "Intel I5 10th gen,12gb Ram, 240SSD,1TB HDD", "serial": "832CP63", "location": "Bangalore", "year": "2020", "condition": "Working"},
    {"user": "Lavanya M", "system": "SKLA-008", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 8gb Ram, 240SSD", "serial": "B30Z432", "location": "Office 1", "year": "2014", "condition": "Working"},
    {"user": "Amit Kumar Gupta", "system": "SKLA-009", "model": "Dell Inspiron 15-3567", "config": "Intel I5 7th gen,,16gb RAM, 240SSD", "serial": "3Z1F3L2", "location": "Office 2", "year": "2018", "condition": "Working"},
    {"user": "Nagalakshmi k", "system": "SKLA-010", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 12gb Ram, 240SSD", "serial": "D20Z432", "location": "Office 1", "year": "2014", "condition": "Working"},
    {"user": "Testing intune", "system": "SKLA-011", "model": "Dell vostro 1450", "config": "Intel I3, 12gb Ram, 240SSD", "serial": "2LGLNP1", "location": "Office 2", "year": "2011", "condition": "In Stock( Not working condition)"},
    {"user": "Sowjanya", "system": "SKLA-012", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 12gb Ram, 240SSD", "serial": "Not Available", "location": "Office 2", "year": "2014", "condition": "Working"},
    {"user": "Keyans Tally", "system": "SKLA-013", "model": "Latitude 3450", "config": "Intel I5 5th gen,12GB RAM,240SSD", "serial": "G3SQG22", "location": "Office 1", "year": "2016", "condition": ""},
    {"user": "Naveen old machine", "system": "SKLA-014", "model": "Dell Inspiron 15-3567", "config": "IIntel I5 7th gen,8GB RAM,240SSD", "serial": "JP04MJ2", "location": "Office 2", "year": "2018", "condition": "In Stock(working condition)"},
    {"user": "Rudra Patel (old system) bangalore office", "system": "SKLA-015", "model": "Lattitude 3440", "config": "Intel I3 4th gen 8gb Ram, 240SSD", "serial": "330Z432", "location": "Bangalore", "year": "2014", "condition": ""},
    {"user": "Prashanth m", "system": "SKLA-016", "model": "Lenovo 81SY", "config": "Intel I7 9th,16gb Ram, 240SSD,1TB HDD", "serial": "PF2LPQXL", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Keyans Gayithri", "system": "SKLA-017", "model": "Dell vostro 1450", "config": "Intel I3, 12gb Ram, 240SSD", "serial": "HKGLNP1", "location": "Office 1", "year": "2011", "condition": ""},
    {"user": "Dead in office 2", "system": "SKLA-018", "model": "Dell vostro 1450", "config": "Intel I3, 12gb Ram, 240SSD", "serial": "JKGLNP1", "location": "Office 2", "year": "2011", "condition": "In Stock( Not working condition)"},
    {"user": "Puneeth Narayana(Display Issuse)", "system": "SKLA-019", "model": "Latttude 3590", "config": "Intel I5 8th gen ,8gb Ram, 240SSD,1TB HDD", "serial": "CP18YQ2", "location": "Office 2", "year": "2018", "condition": "In Stock( Not working condition)"},
    {"user": "Darshan PK", "system": "SKLA-020", "model": "Lattitude 3440", "config": "Intel I3 4th gen 12gb Ram, 240SSD", "serial": "D30Z432", "location": "Office 2", "year": "2014", "condition": "Working"},
    {"user": "Shaik Peer Basha", "system": "SKLA-021", "model": "Dell Inspiron 15-3567", "config": "Intel I5 7th gen,8gb Ram ,256gb ssd", "serial": "PF2TWWY", "location": "Office 2", "year": "2018", "condition": "Working"},
    {"user": "Abubakar", "system": "SKLA-022", "model": "Lattitude 3440", "config": "Intel I3 4th, 12gb Ram, 240SSD", "serial": "830Z432", "location": "Office 2", "year": "2014", "condition": "In Stock(working condition)"},
    {"user": "Mohammad Arshad", "system": "SKLA-023", "model": "dell latitude 3590", "config": "Intel I5 8th gen ,8GB RAM,240SSD", "serial": "4C18YQ2", "location": "Office 1", "year": "2018", "condition": "Working"},
    {"user": "ABUBAKAR", "system": "SKLA-024", "model": "Inspiron 15-3567", "config": "Intel I5 7th gen,12GB RAM,240SSD", "serial": "2WTJ4F2", "location": "Office 1", "year": "2018", "condition": "Working"},
    {"user": "mamatha m (in office 1)", "system": "SKLA-025", "model": "Dell vostro 1450", "config": "Intel I3, 12gb Ram, 240SSD", "serial": "4LGLNP1", "location": "Office 1", "year": "2011", "condition": ""},
    {"user": "Dead", "system": "SKLA-026", "model": "Dell vostro 1450", "config": "Intel I3, 12gb Ram, 240SSD", "serial": "3LGLNP1", "location": "Office 1", "year": "2011", "condition": ""},
    {"user": "chandan in (office 1)", "system": "SKLA-027", "model": "Latitude E6430", "config": "Intel I7,8GB RAM,240SSD", "serial": "H5CT9Y1", "location": "Office 1", "year": "2013", "condition": ""},
    {"user": "Deekshith", "system": "SKLA-028", "model": "Dell Latitude 3450", "config": "Intel I5 5th gen,12GB RAM,240SSD", "serial": "45SQG22", "location": "Office 2", "year": "2016", "condition": "Working"},
    {"user": "Aashish N hansbavi", "system": "SKLA-029", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 12gb Ram, 240SSD", "serial": "630Z432", "location": "Office 2", "year": "2014", "condition": "Working"},
    {"user": "Arshiya Siddiqa(old)", "system": "SKLA-030", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 8gb Ram, 240SSD", "serial": "F20Z432", "location": "Office 2", "year": "2014", "condition": "Working"},
    {"user": "Nikhil Prasad", "system": "SKLA-031", "model": "Vostro 3590", "config": "Intel I5 10th gen,16gb Ram, 240SSD,1TB HDD", "serial": "C32CP36", "location": "Office 2", "year": "2020", "condition": "Working"},
    {"user": "In office 1 old dual core laptop", "system": "SKLA-032", "model": "Hp", "config": "Dualcore", "serial": "Not Available", "location": "Office 1", "year": "", "condition": ""},
    {"user": "Vinay T", "system": "SKLA-033", "model": "Vostro 3590", "config": "Intel I5 10th gen,8gb Ram, 240SSD,1TB HDD", "serial": "G32CP63", "location": "Office 2", "year": "2020", "condition": "Working"},
    {"user": "Arshiya Siddiqa", "system": "SKLA-034", "model": "Vostro 3590", "config": "Intel I5 10th gen,12gb Ram, 240SSD,1TB HDD", "serial": "932CP63", "location": "Office 2", "year": "2020", "condition": "Working"},
    {"user": "Vijay sir(Nistha Kalpesh sir daughter)", "system": "SKLA-035", "model": "Inspiron 15-3567", "config": "Intel I5 7th gen,8gb Ram, 240SSD", "serial": "H84R5L2", "location": "Office 1", "year": "2018", "condition": "Working"},
    {"user": "macbook old", "system": "SKLA-036", "model": "Apple macbook", "config": "I7 Processor,16gb RAM,240SSD", "serial": "", "location": "Office 2", "year": "", "condition": "In Stock( Not working condition)"},
    {"user": "Swathi Pradeep", "system": "SKLA-037", "model": "Lattitude 3440", "config": "Intel I3 4th gen 12gb Ram, 240SSD", "serial": "130Z432", "location": "Office 1", "year": "2014", "condition": "working"},
    {"user": "Tejana Patel", "system": "SKLA-038", "model": "", "config": "", "serial": "0XD9DCG", "location": "Not available", "year": "", "condition": ""},
    {"user": "With Saleem for Repair", "system": "SKLA-039", "model": "", "config": "", "serial": "Not Available", "location": "Not available", "year": "", "condition": ""},
    {"user": "Sanjana V", "system": "SKLA-040", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 12gb Ram, 240SSD", "serial": "730Z432", "location": "Office 1", "year": "2014", "condition": "Working"},
    {"user": "Harsha (laptop missing)", "system": "SKLA-041", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 8gb Ram, 240SSD", "serial": "Not Available", "location": "Not available", "year": "2014", "condition": ""},
    {"user": "Monika JM", "system": "SKLA-042", "model": "Latitude 3490", "config": "Intel I5, 16gb Ram, 240SSD", "serial": "9GS8DQ2", "location": "", "year": "2018", "condition": "Working"},
    {"user": "Karthik S", "system": "SKLA-043", "model": "dell Inspiron 15-3567", "config": "Intel i5 7thgen ,12GB,240SSD", "serial": "6DYDYN2", "location": "Office 2", "year": "2018", "condition": "Working"},
    {"user": "Abhijith", "system": "SKLA-044", "model": "Vostro 3590", "config": "Intel I5 10th gen,8gb Ram, 240SSD,", "serial": "632CP63", "location": "Office 2", "year": "2020", "condition": "Working"},
    {"user": "Dead in office 2", "system": "SKLA-045", "model": "Lattitude 3440", "config": "Intel I3 4th gen, 8gb Ram, 240SSD", "serial": "BQJ4832", "location": "Office 2", "year": "2014", "condition": ""},
    {"user": "Kowshik S", "system": "SKLA-046", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,12GB Ram,512 SSD", "serial": "PF2TJC75", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Rishab Jain", "system": "SKLA-047", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,20GB Ram,512 SSD", "serial": "PF2TK1DS", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Prince", "system": "SKLA-048", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,8GB Ram,512 SSD", "serial": "PF2THVG9", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Kaliya krishna", "system": "SKLA-049", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,20GB Ram,512 SSD", "serial": "PF2TW32V", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Prithviraj Patil", "system": "SKLA-050", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,12GB Ram,512 SSD", "serial": "PF2TJX7R", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Bharath Kumar Y N", "system": "SKLA-051", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,8GB Ram,512 SSD", "serial": "PF2TJGYX", "location": "Bangalore", "year": "2021", "condition": "Working"},
    {"user": "Tilak Pednekar", "system": "SKLA-052", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,8GB Ram,512 SSD", "serial": "PF2TJVK3", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Ravi Teja S", "system": "SKLA-053", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,12GB Ram,512 SSD", "serial": "PF2VS6V6", "location": "Bangalore", "year": "2021", "condition": "Working"},
    {"user": "jayram", "system": "SKLA-054", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,8GB Ram,512 SSD", "serial": "PF2TJTFC", "location": "Bangalore", "year": "2021", "condition": "Working"},
    {"user": "Aamir Zahir", "system": "SKLA-055", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,20GB Ram,512 SSD", "serial": "PF2TJRQA", "location": "London(uk)", "year": "2021", "condition": ""},
    {"user": "Monika V D", "system": "SKLA-056", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,8GB Ram,512 SSD", "serial": "PF3V65FA", "location": "Office 1", "year": "2021", "condition": "Working"},
    {"user": "Akash s Ishwarappa", "system": "SKLA-057", "model": "Lenovo 82H7", "config": "Intel I3,11th gen,12GB Ram,512 SSD", "serial": "PF2VR32P", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "NiraV Langrojana", "system": "SKLA-058", "model": "Vostro 3590", "config": "Intel I5 10th gen,8gb Ram, 240SSD,1TB HDD", "serial": "B32CP63", "location": "Bangalore", "year": "2020", "condition": "Working"},
    {"user": "Golla Devraju", "system": "SKLA-059", "model": "Vostro 3590", "config": "Intel I5 10th gen8gb Ram, 240SSD,1TB HDD", "serial": "D32CPC3", "location": "Office 2", "year": "2020", "condition": "Working"},
    {"user": "Nithin GD", "system": "SKLA-060", "model": "Vostro 3590", "config": "Intel I5 10th gen,8gb Ram, 240SSD,1TB HDD", "serial": "532CP63", "location": "Bangalore", "year": "2020", "condition": "Working"},
    {"user": "Shaloom Calvin", "system": "SKLA-061", "model": "Vostro 3590", "config": "Intel I5 10th gen,20gb Ram, 240SSD,1TB HDD", "serial": "F32CP63", "location": "Office 2", "year": "2020", "condition": "Working"},
    {"user": "Chettati sai kiran", "system": "SKLA-062", "model": "Vostro 3590", "config": "Intel I5 10th gen,16gb Ram, 240SSD,1TB HDD", "serial": "732CP63", "location": "Office 2", "year": "2020", "condition": "Working"},
    {"user": "Anuj sir", "system": "SKLA-063", "model": "Lenovo T490s", "config": "(Core i5-8265U),16gb Ram,512 SSD", "serial": "MJ0DC65K", "location": "Office 2", "year": "2021", "condition": ""},
    {"user": "Kalpesh sir", "system": "SKLA-064", "model": "Lenovo S340-14IIL-81VV", "config": "Core i5-1035G1,8gb ram,240ssd,1tb hdd", "serial": "MP1WXTBL", "location": "Office 2", "year": "2021", "condition": ""},
    {"user": "Pakruthi V mail campign", "system": "SKLA-065", "model": "Lenovo S340-14IIL-81VV", "config": "Core i5-1035G1,8gb ram,240ssd,1tb hdd", "serial": "MP1WXLT5", "location": "Office 1", "year": "2021", "condition": "Working"},
    {"user": "Sheetal Mam", "system": "SKLA-066", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen,8gb RAM,512 Nvme", "serial": "PF36CSZ5", "location": "Office 1", "year": "2021", "condition": "Working"},
    {"user": "Subramanya s", "system": "SKLA-067", "model": "Lenovo Think pad P14s Gen 2", "config": "Intel I7  1165G7 gen ,20gb RAM,512 Nvme", "serial": "PF3DWVEJ", "location": "Office 2", "year": "2022", "condition": "Working"},
    {"user": "Stalin k paul", "system": "SKLA-068", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen,12gb RAM,512 Nvme", "serial": "PF35YLNK", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Puneeth Narayana", "system": "SKLA-069", "model": "Lenovo Think pad P14s Gen 2", "config": "Intel  I7 1165G7 gen ,20gb RAM,512 Nvme", "serial": "PF3DBLXY", "location": "Office 2", "year": "2022", "condition": "Working"},
    {"user": "Poorvik Gowda", "system": "SKLA-070", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen,12gb RAM,512 Nvme", "serial": "PF34RK75", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Sudha nerale", "system": "SKLA-071", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen ,8gb RAM,512 Nvme", "serial": "PF36CVAC", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Sree Kumar sir", "system": "SKLA-072", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen ,20gb RAM,512 Nvme", "serial": "PF34QYMA", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Naveen Kumar", "system": "SKLA-073", "model": "Lenovo Think pad P14s Gen 2", "config": "Intel I7  1165G7 gen ,20gb RAM,512 Nvme", "serial": "PF3EAK4F", "location": "Office 2", "year": "2022", "condition": "Working"},
    {"user": "Rudra Patel", "system": "SKLA-074", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen,12gb RAM,512 Nvme", "serial": "PF35YLNX", "location": "Bangalore", "year": "2021", "condition": "Working"},
    {"user": "Vijay sir", "system": "SKLA-075", "model": "Dell Latitude 7390", "config": "i7 8th gen  8gb ram  256 nvme", "serial": "GVYKVT2", "location": "Office 1", "year": "2019", "condition": "Working"},
    {"user": "Pouli Sharon Dsilva", "system": "SKLA-076", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen,12gb RAM,512 Nvme", "serial": "PF31ANJL", "location": "Office 2", "year": "2021", "condition": "Working"},
    {"user": "Poojashree L", "system": "SKLA-077", "model": "lenovo ideapad 3-15ITL6 -82H8", "config": "Intel I3 11th gen,8gb RAM,512 Nvme", "serial": "PF2YFDPA", "location": "Office 2", "year": "2021", "condition": "Working"},
]

# Generate JSON assets
assets = []
base_timestamp = 1735564800000

for idx, laptop in enumerate(laptops_data):
    # Determine status based on condition
    condition = laptop["condition"].lower()
    if "working" in condition and "not" not in condition:
        status = "assigned" if laptop["user"] and laptop["user"] not in ["Dead", "Dead in office 2"] else "available"
    elif "not working" in condition or "dead" in laptop["user"].lower():
        status = "retired"
    elif "stock" in condition:
        status = "available"
    else:
        status = "assigned" if laptop["user"] else "available"
    
    asset = {
        "id": base_timestamp + idx,
        "type": "laptop",
        "assetId": laptop["system"],
        "model": laptop["model"],
        "serialNumber": laptop["serial"],
        "configuration": laptop["config"],
        "officeLocation": laptop["location"],
        "year": laptop["year"],
        "currentCondition": laptop["condition"],
        "currentUser": laptop["user"],
        "lastUser": "",
        "status": status,
        "dateAdded": datetime.now().isoformat(),
        "accessories": {
            "mouse": "",
            "headphone": "",
            "charger": "",
            "monitor": ""
        }
    }
    assets.append(asset)

# Write to JSON file
with open('assets_data.json', 'w') as f:
    json.dump(assets, f, indent=2)

print(f"Successfully generated {len(assets)} laptop records!")
print("Data saved to assets_data.json")
