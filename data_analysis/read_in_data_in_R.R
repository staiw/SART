
### Read in SART data in R

#install.packages("dplyr") # Comment out this line to install dplyr before first use
library(dplyr)

# Set the working directory to the folder containing the data
setwd("../data")

# Define the task name (must be the beginning of the file names containing the data)
task_name <- 'sart'

# Get names of the data files
files <- list.files(pattern=paste0("^", task_name, ".*\\.csv$"))

# Read and combine all csv files into one dataframe
data <- lapply(files, read.csv) %>%
  bind_rows()
