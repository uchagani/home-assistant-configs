brightnessLevelDown = data.get('brightnessLevelDown') or None
brightnessLevelUp = data.get('brightnessLevelUp') or None
colorName = data.get('colorName') or None
lightLocation = data.get('lightLocation') or None
brightnessPercentage = data.get('brightnessPercentage') or None
domain = data.get('domain') or None

logger.info("Color Name: {}".format(colorName))
logger.info("Light Location: {}".format(lightLocation))
logger.info("Brightness Percentage: {}".format(brightnessPercentage))
logger.info("Domain: {}".format(domain))

if (domain == "light") or (domain == "lights"):
    entity_ids = []
    if lightLocation == 'living room':
        # If a group is (living room) is passed in, act on only that group.
        living_room = hass.states.get('group.living_room')
        for entity in living_room.attributes['entity_id']:
            entity_ids.append(entity)
    elif lightLocation == "" or lightLocation is None:
        # If no lightLocation is passed in, check if any lights are currently on and act on those.
        lights = hass.states.entity_ids('light')

        for light in lights:
            if hass.states.is_state(light, 'on'):
                entity_ids.append(light)

        #If no lights are currently 'on', assume we mean to interact with all lights
        if len(entity_ids) == 0:
            lights = hass.states.entity_ids('light')
            for light in lights:
                entity_ids.append(light)
    else:
        # A specific light location was passed in
        entity = 'light.' + lightLocation.replace(' ', '_')
        entity_ids.append(entity.lower())

    service_datas = []

    for entity in entity_ids:
        if brightnessPercentage == "" or brightnessPercentage is None:
            # If no brightnessPercentage is passed in, get the current/brightnessPercentage for each entity
            entity_state = hass.states.get(entity)
            if hass.states.is_state(entity, 'on'):
                state_attributes = hass.states.get(entity).attributes
                temp_service_data = {"entity_id": entity, 'color_name': colorName, 
                                     'brightness': state_attributes['brightness']}
                service_datas.append(temp_service_data)
            else:
                # The lights we want to interact with are not yet turned on so we'll handle it later
                temp_service_data = {"entity_id": entity, 'color_name': colorName, 
                                     'brightness_pct': brightnessPercentage}
                service_datas.append(temp_service_data)
        else:
            temp_service_data = {"entity_id": entity, 'color_name': colorName, 
                                 'brightness_pct': brightnessPercentage}
            service_datas.append(temp_service_data)

    for service_data in service_datas:        
        data = {k: v for k, v in service_data.items() if v is not None}    
        data['power'] = True

        if data.get('brightness_pct') is None and data.get('brightness') is None:
            if hass.states.is_state(data.get('entity_id'), 'off'):               
                # The light we want to interact with is off and no brightness percentage was passed in
                # So turn the light on, get the current brightness, then interact with it.
                temp_service_data = {"entity_id": entity_ids, "power": True, "transition": 0}
                hass.services.call('light', 'lifx_set_state', temp_service_data)
                
                # Wait until the light turns on or else no brightness attribute will exist
                logger.info("Waiting for lights to turn on to get the brightness level...")
                timeout = time.time() + 2
                while time.time() < timeout:
                    if hass.states.get(data['entity_id']).attributes.get('brightness') is not None: break
                    time.sleep(.1)

                brightness = hass.states.get(data['entity_id']).attributes.get('brightness')
                data['brightness'] = brightness
                data['transition'] = 1 # Gracefully transition to the new brightness (if applicable)


        hass.services.call('light', 'lifx_set_state', data) #Finally turn on/transition to the new light color/brightness
else:
    logger.info("No domain found.")
