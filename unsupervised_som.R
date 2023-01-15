library(kohonen)
library(fastDummies)
# R script takes csv of ripps as input and constructs a som per method
# then assigns a som node to each datum for later use.

method <- '#MIRNY'

# unsupervised som
g <- somgrid(xdim = 4, ydim = 4, topo = "hexagonal")
# define the color, nais
coolBlueHotRed <- function(n, alpha = 1) {rainbow(n, end=4/6, alpha=alpha)[n:1]}

# define dataset
ripp_only <- raw_data[raw_data$RIPP == 1,]
unsupervised_aacon_som <- ripp_only[ripp_only$METHOD==method,]

som_model <- som(scale(unsupervised_aacon_som[,0:10]), 
                 grid= g, 
                 rlen=500, 
                 alpha=c(0.05,0.01))

plot(som_model, type = 'changes')
plot(som_model, type = 'count', palette.name = coolBlueHotRed)
plot(som_model, type= 'codes', palette.name = coolBlueHotRed)
# write node membership to df
unsupervised_aacon_som['RIPP'] <- som_model$unit.classif
print(unsupervised_aacon_som)

write.csv(unsupervised_aacon_som,"/home/work/Desktop/WUR/ch2_precursor_conservation/R_SOM/som_nodes.csv", row.names = FALSE)