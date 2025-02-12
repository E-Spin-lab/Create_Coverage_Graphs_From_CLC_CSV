# 
library(ggplot2)
options(max.print = 1000000)        # Maxes out at 1,000 need to increase
#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..
# Set these Variables
PathOfFiles <- "C:\\PATH\\TO\\CLC\\CSV\\FILES\\"
Image_Width <- 13
Image_Height <- 4
#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..#..
FileNameArray = list.files(path = PathOfFiles, pattern="*.csv", full.names = TRUE)
breaks <- 10^(-10:10)
minor_breaks <- rep(1:9, 21)*(10^rep(-10:10, each=9))

for(FileFullName in FileNameArray){
    # Explanation: (strsplit)split file name and path @ \\ (tail)grab the file name from the last indexed item in list, (strsplit) remove .csv
    Title = strsplit(tail(strsplit(FileFullName[1],"\\\\")[[1]],1),".csv")[[1]]
    Table <- read.table(file = FileFullName, header = TRUE, sep=",", dec=".")
    ggplot(Table, aes(x=Reference.position, y=Coverage, color=Mapping)) +
            geom_line(linewidth =0.5) +
            labs(title = Title, x ="Genome Position", y = "Coverage") +
            scale_color_manual(values = "#6433ff") +
            scale_y_log10(breaks = breaks, minor_breaks = minor_breaks) +
            theme(
                plot.title = element_text(hjust = 0.5, size=14, face ='bold'),
                axis.title.x = element_text (size=10, face ='bold'),
                axis.title.y = element_text (size=10, face = 'bold'),
                text=element_text(family="mono", colour="black"),
                panel.background = element_blank(),
                panel.grid.major.y = element_line(linewidth = 0.5, linetype = "solid", colour = "grey"),
                panel.grid.minor.y = element_line(linewidth = 0.25, linetype = "solid", colour = "grey"),
                axis.line = element_line(linewidth = 0.5, linetype = "solid", colour = "black"),
                legend.position="none"
            )
    # Save Image
    ImageOutPut <- paste(PathOfFiles, Title, ".png", sep = "")
    ggsave(ImageOutPut, width = Image_Width, height = Image_Height, units = "in")
}
