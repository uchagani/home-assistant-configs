lightLocation = data.get('lightLocation') or None

logger.info("Light Location: {}".format(lightLocation))

entity_ids = []

if lightLocation == 'living room':
  living_room = hass.states.get('group.living_room')
  for entity in living_room.attributes['entity_id']:
    entity_ids.append(entity)
elif lightLocation == 'kitchen':
  living_room = hass.states.get('group.kitchen')
  for entity in living_room.attributes['entity_id']:
    entity_ids.append(entity)
elif lightLocation == 'bar':
  living_room = hass.states.get('group.bar')
  for entity in living_room.attributes['entity_id']:
    entity_ids.append(entity)
elif lightLocation == "" or lightLocation is None:
  #Assume we want to turn off all the lights
  lights = hass.states.entity_ids('light')
  for light in lights:
    entity_ids.append(light)
else:
  entity = 'light.' + lightLocation.replace(' ', '_')
  entity_ids.append(entity.lower())
  
logger.info(entity_ids)

service_data = { "entity_id" : entity_ids }

logger.info(service_data)

hass.services.call('light', 'turn_off', service_data)
