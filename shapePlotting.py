import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Polygon
import numpy as np
import os


def plotGeo(shapefile_path,outer_file,ids=None,ax = None, reload=False):
    global gdf_shapefile, df_outer, tri_fill, tri_border
    if not reload:
        gdf_shapefile = gpd.read_file(shapefile_path)

    if not reload:
        df_outer = pd.read_csv(outer_file,delimiter=";")

    df_filtered = df_outer
    if ids is not None:
        df_filtered = df_outer[df_outer['id'].isin(ids)]

    polygons = []
    for polygon_str in df_filtered['geometry']:
        polygon_coords = [tuple(map(float, point.split())) for point in polygon_str.replace('POLYGON ((', '').replace('))', '').split(', ')]
        polygon = Polygon(polygon_coords)
        polygons.append(polygon)

    gdf_custom = gpd.GeoDataFrame(df_filtered, geometry=polygons)

    if ax is None:
        fig, ax = plt.subplots()

    if reload:
        ax.clear()

    gdf_shapefile.plot(ax=ax, color='grey', edgecolor='black')


    gdf_custom.plot(ax=ax, color='grey',alpha=0.3)
    gdf_custom.boundary.plot(ax=ax, color='red', linewidth=0.3,alpha=0.3)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Geodata')
    if ax is None:
        plt.axis('off')
        plt.show()


def plotInteractive(fig,ax_scatter, ax_geo, solution_file,shape_file,outer_file):
    global highlighted_point 
    highlighted_point = None
    df = pd.read_csv(solution_file, delimiter=",")


    # Add the weight of the {s,t} edge for osterloh, as it is not included in the solution .csv.
    if "osterloh" in solution_file:
        df["area"] += 37399

    extreme = df[df["extreme"] == True][["area","perimeter"]]
    nonextreme = df[df["extreme"] == False][["area","perimeter"]]

    ax_scatter.scatter(nonextreme["area"], nonextreme["perimeter"], c='lightblue', label='nonextreme PO solution',s=3,alpha=0.5)
    ax_scatter.scatter(extreme["area"], extreme["perimeter"], c='orange', label='extreme PO solution',marker='s',s=3*6,alpha=1)

    ax_scatter.legend()

    ax_scatter.set_xlabel('Area')
    ax_scatter.set_ylabel('Perimeter')


    data = df.to_numpy()
    for i in range(len(data)):
        data[i,2] = np.fromstring(data[i,2][1:-1],dtype=int,sep=",")
    
    def clear_highlight():
        global highlighted_point 
        if highlighted_point is not None: 
            highlighted_point.remove()
            highlighted_point = None

    def find_closest_point(x, y, data, ratio):
        distances = ((data[:, 0] - x) * ratio) ** 2 + (data[:, 1] - y) ** 2
    
        closest_index = np.argmin(distances)

        return data[closest_index]



    def on_scroll(event):
        if event.inaxes != ax_scatter or event.button != 'up' and event.button != 'down':
            return
        x_mouse = event.xdata
        y_mouse = event.ydata
        x_range_old = ax_scatter.get_xlim()[1] - ax_scatter.get_xlim()[0]
        y_range_old = ax_scatter.get_ylim()[1] - ax_scatter.get_ylim()[0]
        if event.button == 'up':
            scale_factor = 0.7
        elif event.button == 'down':
            scale_factor = 1.3
        new_x_range = x_range_old * scale_factor
        new_y_range = y_range_old * scale_factor
        x_new_min = x_mouse - (x_mouse - ax_scatter.get_xlim()[0]) * (new_x_range / x_range_old)
        x_new_max = x_new_min + new_x_range
        y_new_min = y_mouse - (y_mouse - ax_scatter.get_ylim()[0]) * (new_y_range / y_range_old)
        y_new_max = y_new_min + new_y_range
        ax_scatter.set_xlim(x_new_min, x_new_max)
        ax_scatter.set_ylim(y_new_min, y_new_max)
        plt.draw()


    def on_click(event):
        global highlighted_point 
        if event.inaxes != ax_scatter or event.button != 3 and event.button !=1: 
            return
        x, y = event.xdata, event.ydata

        ratio = ax_scatter.get_data_ratio()
    
        if event.button == 3:
            closest_row = find_closest_point(x, y, data[data[:,3]==True],ratio)
        elif event.button == 1:
            closest_row = find_closest_point(x, y, data[data[:,3]==False],ratio)


        clear_highlight() 
        highlighted_point = ax_scatter.scatter(closest_row[0], closest_row[1], color='red',marker="x", zorder=10,s=100,label="Visualized solution")
        plt.legend()

        plotGeo(shape_file,outer_file,ids=closest_row[2],ax=ax_geo,reload=True)

        fig.canvas.draw()


    fig.canvas.mpl_connect('scroll_event', on_scroll)
    fig.canvas.mpl_connect('button_press_event', on_click)


def plotBoth(solution_file,shape_file,outer_file):
    fig, (ax_geo,ax_scatter) = plt.subplots(1, 2, figsize=(10, 5))

    ax_scatter.set_title('Pareto frontier')
    plotInteractive(fig, ax_scatter, ax_geo, solution_file, shape_file,outer_file)

    ax_geo.set_title('Geodata')
    plotGeo(shape_file,outer_file,ax=ax_geo)
    
    plt.tight_layout()
    plt.show()

def plotBothHelper(datasetName):
    plotBoth(f"{datasetName}/solutions_labeled_{datasetName}.csv",f"{datasetName}/shape/{datasetName}.shp",f"{datasetName}/outer.txt")



if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    plotBothHelper("osterloh")

