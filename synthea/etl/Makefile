JAVA = java

PYTHON = python3

# Path where the Synthea jar is
GENERATOR_JAR = ../synthea-with-dependencies.jar

# Path where the Synthea Config is
GENERATOR_CONFIG_PATH = ../synthea.properties

# Number of patients to generate
GENERATOR_BATCH_SIZE = 30

# Location
GENERATOR_LOCATION = California

# Synthea generator arguments
GENERATOR_ARGS = $(GENERATOR_LOCATION) -c $(GENERATOR_CONFIG_PATH) -p $(GENERATOR_BATCH_SIZE)

# Dataset path
DATASETS_PATH = ./datasets/

# Output path
OUTPUT_PATH = ./output/

all: generate_data process_data 

generate_data: 
			$(JAVA) -jar $(GENERATOR_JAR) $(GENERATOR_ARGS)

process_data:
			$(PYTHON) ./synthea_exporter/exporter.py $(DATASETS_PATH) $(OUTPUT_PATH)
