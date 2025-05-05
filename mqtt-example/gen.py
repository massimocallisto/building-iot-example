import json
import random

def random_hex_color():
    return "#{:06X}".format(random.randint(0, 0xFFFFFF))

def generate_simulation_json(num_floors: int) -> dict:
    config = {
        "eventFrequency": 4000,
        "varyEventFrequency": True,
        "repeatWorkflow": True,
        "timeBetweenRepeat": 15000,
        "varyRepeatFrequency": True,
        "steps": []
    }

    for floor in range(1, num_floors + 1):
        pir_id = f"pir{random.randint(10, 99)}"
        light_id = f"light{random.randint(10, 99)}"
        secret_presence = random_hex_color()
        secret_light = random_hex_color()

        config["steps"].append({
            "duration": 0,
            "producerConfig": {
                "mqtt": {
                    "topic": f"building_iot/piano{floor}/device/presence/{pir_id}"
                }
            },
            "config": [
                {
                    "device": pir_id,
                    "tz": "now()",
                    "presence": "integer(0, 1)",
                    "secret" : secret_presence
                }
            ]
        })

        config["steps"].append({
            "duration": 0,
            "producerConfig": {
                "mqtt": {
                    "topic": f"building_iot/piano{floor}/device/light/{light_id}"
                }
            },
            "config": [
                {
                    "device": light_id,
                    "tz": "now()",
                    "light": "boolean()",
                    "secret" : secret_light
                }
            ]
        })

    return config

# ESEMPIO USO
num_piani = 12
simulation = generate_simulation_json(num_piani)

# Salva su file (opzionale)
with open("conf/simple_Building_Workflow.json", "w") as f:
    json.dump(simulation, f, indent=2)

# Stampa in console
print(json.dumps(simulation, indent=2))
