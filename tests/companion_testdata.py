DEFAULT_COMMANDER = {
    "alive": True,
    "capabilities": {
        "AllowCobraMkIV": False,
        "Horizons": True
    },
    "credits": 1337,
    "currentShipId": 8,
    "debt": 0,
    "docked": True,  # Set this in your usages
    "id": 123456,
    "name": "EDMCTEST",
    "rank": {
        "combat": 1,
        "cqc": 2,
        "crime": 3,
        "empire": 4,
        "explore": 5,
        "federation": 6,
        "power": 7,
        "service": 0,
        "trade": 8
    }
}

DOCKED = {
    "commander": DEFAULT_COMMANDER.update({"Docked": True}),
    "lastStarport": {
        
    }
}