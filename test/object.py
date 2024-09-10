prediction = {
    "predictions": [
        {
            "x": 0,
            "y": 200,
            "width": 1200,
            "height": 600,
            "confidence": 0.663,
            "class": "sea",
            "class_id": 1,
        },
        {
            "x": 210,
            "y": 210,
            "width": 20,
            "height": 20,
            "confidence": 0.515,
            "class": "person_in_water",
            "class_id": 1,
        },
        {
            "x": 320,
            "y": 210,
            "width": 20,
            "height": 20,
            "confidence": 0.515,
            "class": "person_in_water",
            "class_id": 1,
        },
        {
            "x": 620,
            "y": 260,
            "width": 20,
            "height": 20,
            "confidence": 0.515,
            "class": "person_in_water",
            "class_id": 1,
        },
        {
            "x": 920,
            "y": 270,
            "width": 20,
            "height": 20,
            "confidence": 0.515,
            "class": "person_in_water",
            "class_id": 1,
        },
        {
            "x": 400,
            "y": 550,
            "width": 20,
            "height": 20,
            "confidence": 0.515,
            "class": "person_in_water",
            "class_id": 1,
        },
        {
            "x": 900,
            "y": 250,
            "width": 20,
            "height": 20,
            "confidence": 0.515,
            "class": "boat",
            "class_id": 1,
        },
    ]
}

# if swimmer in danger zone then alert
zoneRed = [[1100, 250, 50, 50], [900, 250, 200, 200]]

# if swimmer in danger zone and no full sea then alert
zoneOrange = [[200, 200, 100, 50], [300, 200, 50, 50]]

# if water and swimmer then alert
zoneGreen = [[600, 250, 100, 100], [500, 250, 50, 50]]
