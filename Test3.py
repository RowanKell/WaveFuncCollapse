radius = 4
screen_width = 800
screen_height = 600
center_of_tile_radius = radius * 2
odds = [0] * radius
dimensions = [[(0, 0) for x in range(radius)] for x in range(radius)]
for i in range(len(odds)):
    odds[i] = 2 * i + 1
for i in range(radius):
    for j in range(radius):
        dimensions[i][j] = (screen_width * odds[i] / radius, screen_height * odds[j] / center_of_tile_radius)
tileset = [["tile%d" % x for x in range(radius)] for x in range(radius)]
print(tileset)
