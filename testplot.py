import matplotlib.pyplot as plt
import numpy as np

# Generate swell data
# num_points = 100
# swells = np.random.uniform(-100, 10, num_points)
# swells[np.random.choice(num_points, 20, replace=False)] = -99  # Set some random points to -99

# Calculate offsets for longitudes and latitudes
x_offset = (100 - 66) / 10  # Each X_Node (width of each rectangle)
y_offset = (24 - 4) / 10    # Each Y_Node (height of each rectangle)

minLongitude = 66  # x1
maxLongitude = 100  # x2

minLatitude = 24  # y1
maxLatitude = 4  # y2

longitudes = []
latitudes = []

# Generate longitudes and latitudes with the same length
y = minLatitude
while y > maxLatitude:
    x = minLongitude
    while x <= maxLongitude:
        longitudes.append(x)
        latitudes.append(y)
        x += x_offset
    y -= y_offset

# Ensure that the number of swells matches the number of points (adjust if necessary)
# if len(swells) != len(longitudes):
#     swells = np.random.uniform(-100, 10, len(longitudes))

def plot_swell_data_rectangles(longitudes, latitudes, swells, x_offset, y_offset):
    # Create a figure
    plt.figure(figsize=(12, 8))

    # Normalize the swell values for color mapping
    norm = plt.Normalize(vmin=-100, vmax=10)
    cmap = plt.cm.coolwarm

    # Create the plot by drawing rectangles
    for lon, lat, swell in zip(longitudes, latitudes, swells):
        if swell == -99:
            color = 'brown'
        else:
            # print(f"swell :   {swell}")
            color = 'blue'
        # color = cmap(norm(swell))  # Use normalized swell to get color from cmap
        rect = plt.Rectangle((lon, lat - y_offset), x_offset, y_offset, color=color, edgecolor='black')
        plt.gca().add_patch(rect)

    # Add colorbar by creating a ScalarMappable object
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # This is necessary to link it to the colorbar
    # cbar = plt.colorbar(sm)
    # cbar.set_label('Swell Value')

    # Set labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Swell Data Plot (Rectangles)')

    # Set axis limits
    plt.xlim(66, 100)
    plt.ylim(4, 24)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)

    # Show plot
    plt.show()

# Call the function with rectangle drawing

swells = []
content = ""
with open("./wavesData/day1_waves_data.csv", "r") as file:
    content = file.read()

count= 0
for row in content.split("\n"):
    data = row.split(",")
    try:
        if data[1] == "00":
            print(f"{count} : {data[7]}")
            count += 1
            swells.append(float(data[7]))
    except:
        continue

# swells = [float(swell) for swell in swells]
# print(swells)
# print(swells[709])
plot_swell_data_rectangles(longitudes, latitudes, swells, x_offset, y_offset)
