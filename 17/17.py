ex = [[20, 30], [-10, -5]]
inp = [[244, 303], [-91, -54]]
area = inp

ans = 0
D = {}

vel_x = 0
vel_y = 0
x = 0
y = 0
xy = True
vels = []

for vel_x in range(1, area[0][1] + 1):
    for vel_y in range(area[1][0] - 1, 100):
        vel_x_step = vel_x
        vel_y_step = vel_y
        max_y = 0

        for step in range(1000):
            x += vel_x_step
            y += vel_y_step
            max_y = max(max_y, y)
            if x in range(area[0][0], area[0][1] + 1) and y in range(area[1][0], area[1][1] + 1):
                ans = max(ans, max_y)
                vels.append((vel_x, vel_y))
                break
            vel_x_step = max(vel_x_step - 1, 0)
            vel_y_step -= 1

            if y < area[1][0] or x > area[0][1]:
                break
        y = 0
        x = 0

print(f'{ans=}')
print(f'{len(vels)=}')
