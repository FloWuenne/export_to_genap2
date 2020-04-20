## How to run tool
# Rscript alevin_to_seurat.R --input $alevin_matrix_rds  --output $seurat_object

# Set up R error handling to go to stderr
options(show.error.messages=F, error=function(){cat(geterrmessage(),file=stderr());q("no",1,F)})

# Avoid crashing Galaxy with an UTF8 error on German LC settings
loc <- Sys.setlocale("LC_MESSAGES", "en_US.UTF-8")


suppressPackageStartupMessages({
  library("getopt")
  library("Seurat")
})

# Import required libraries
options(stringAsfactors = FALSE, useFancyQuotes = FALSE)

# Take in trailing command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Get options using the spec as defined by the enclosed list
# Read the options from the default: commandArgs(TRUE)
option_specification = matrix(c(
  'input', 'i1', 2, 'character',
  'output', 'o', 2, 'character'
), byrow=TRUE, ncol=4)

# Parse options
options = getopt(option_specification)

# Print options to stderr
# Useful for debugging
#cat("\n input file: ",options$input)
#cat("\n output file: ",options$output)

## Read in alevin sparse Matrix as RDS file
dge_matrix <- readRDS(options$input)

## Create Seurat object
seurat_object <- CreateSeuratObject(dge_matrix)

# Output kmer counts
saveRDS(seurat_object, file = options$output)

cat("\n Successfully created Seurat object! \n")
