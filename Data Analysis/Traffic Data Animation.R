library(readr)
library(dplyr)
library(ggplot2)
library(ggmap)
library(gganimate)
library(gifski)
dfTraffic = read_csv("./Traffic Dept Forecasts.csv", col_names = TRUE)
#map
myLocation = 'Qatar'
map = get_map(location = myLocation, zoom = 8)
custom_reds <- c("LOW" = "#FFB6C1",   # Light Pink
                 "MODERATE" = "#FF4500", # Orange-Red
                 "HIGH" = "#8B0000")   # Dark Red
map_with_data = ggmap(map) + geom_point(data=dfTraffic, aes(x=Longitude, y=Latitude, size = Accident_Count, color = Level)) + scale_color_manual(values=custom_reds) 
map_with_animation <- map_with_data +
  shadow_mark() + transition_time(dfTraffic$Year) +
  ggtitle( 'Year: {frame_time}',
           subtitle = 'Frame {frame} of {nframes}')
num_years = max(dfTraffic$Year) - min(dfTraffic$Year) + 1
animate(map_with_animation, nframes = num_years, fps = 2)
anim_save("./Traffic_Data_Animation_with_Forecast.gif")
