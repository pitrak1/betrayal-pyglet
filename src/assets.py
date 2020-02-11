import pyglet

def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

def load_images():
	pyglet.resource.path = ['assets']
	pyglet.resource.reindex()

	images = {}
	# images['blue_characters'] = pyglet.resource.image('blue_characters.jpg')
	images['brandon_jaspers'] = pyglet.resource.image('brandon_jaspers.png')
	images['brandon_jaspers_selected'] = pyglet.resource.image('brandon_jaspers_selected.png')
	images['darrin_williams'] = pyglet.resource.image('darrin_williams.png')
	entrance = pyglet.resource.image('entrance.jpg')
	images['entrance'] = pyglet.image.ImageGrid(entrance, 1, 3)
	images['event'] = pyglet.resource.image('event.jpg')
	# images['event_cards'] = pyglet.resource.image('event_cards.jpg')
	images['father_rhinehardt'] = pyglet.resource.image('father_rhinehardt.png')
	# images['green_characters'] = pyglet.resource.image('green_characters.jpg')
	images['heather_granville'] = pyglet.resource.image('heather_granville.png')
	images['item'] = pyglet.resource.image('item.jpg')
	# images['item_cards'] = pyglet.resource.image('item_cards.jpg')
	images['jenny_leclerc'] = pyglet.resource.image('jenny_leclerc.png')
	images['madame_zostra'] = pyglet.resource.image('madame_zostra.png')
	images['missy_dubourde'] = pyglet.resource.image('missy_dubourde.png')
	images['omen'] = pyglet.resource.image('omen.jpg')
	# images['omen_cards'] = pyglet.resource.image('omen_cards.jpg')
	images['ox_bellows'] = pyglet.resource.image('ox_bellows.png')
	images['peter_akimoto'] = pyglet.resource.image('peter_akimoto.png')
	images['professor_longfellow'] = pyglet.resource.image('professor_longfellow.png')
	# images['purple_characters'] = pyglet.resource.image('purple_characters.jpg')
	# images['red_characters'] = pyglet.resource.image('red_characters.jpg')
	rooms = pyglet.resource.image('rooms.jpg')
	images['rooms'] = pyglet.image.ImageGrid(rooms, 8, 8)
	rooms_selected = pyglet.resource.image('rooms_selected.png')
	images['rooms_selected'] = pyglet.image.ImageGrid(rooms_selected, 8, 8)
	images['vivian_lopez'] = pyglet.resource.image('vivian_lopez.png')
	# images['white_characters'] = pyglet.resource.image('white_characters.jpg')
	# images['yellow_characters'] = pyglet.resource.image('yellow_characters.jpg')
	images['zoe_ingstrom'] = pyglet.resource.image('zoe_ingstrom.png')

	for key, value in images.items():
		if value.__class__.__name__ == 'ImageGrid':
			for image in value:
				center_image(image)
		else:
			center_image(value)

	return images
