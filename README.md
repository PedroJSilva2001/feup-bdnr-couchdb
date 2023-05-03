# How to run
- First generate the datasets with the [Synthea ETL pipeline](./synthea/)
- Then move the contents of the pipeline's output to a "datasets" path in the ["server" path](./server/)
- run `make build_dev` to build the project for development or `make build_prod` to build for production
- run `make run_dev` to run the project for development or `make run_prod` to run for production
