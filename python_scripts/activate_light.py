brightnessLevelDown = data.get('brightnessLevelDown') or None
brightnessLevelUp = data.get('brightnessLevelUp') or None
brightnessPercentage = data.get('brightnessPercentage') or None
colorName = data.get('colorName') or None
lightLocation = data.get('lightLocation') or None

logger.info("Light Location: {}".format(lightLocation))
logger.info("Color Name: {}".format(colorName))
logger.info("Brightness Percentage: {}".format(brightnessPercentage))

entity_ids = []

if lightLocation == 'living room' or lightLocation is None:
  living_room = hass.states.get('group.living_room')
  for entity in living_room.attributes['entity_id']:
    entity_ids.append(entity)
else:
  entity = 'light.' + lightLocation.replace(' ', '_')
  entity_ids.append(entity.lower())
  
logger.info(entity_ids)

temp_service_data = { "entity_id" : entity_ids, 'color_name': colorName, 'brightness_pct': brightnessPercentage }
service_data = {k: v for k, v in temp_service_data.items() if v is not None}

logger.info(temp_service_data)
logger.info(service_data)

hass.services.call('light', 'turn_on', service_data)
