# How to run

- First generate the datasets with the [Synthea ETL pipeline](./synthea/)
- Then move the contents of the pipeline's output to a "datasets" path in the ["server" path](./server/)
- To test download this compressed folder content and move its content to a "datasets" path in the ["server" path](./server/)
- run `make build_dev` to build the project for development or `make build_prod` to build for production
- run `make run_dev` to run the project for development or `make run_prod` to run for production
- run 'npm run dev' on '/app' to run the frontend app
- app will be running on localhost:8080

### Some values that can be used for testing

#### Test users:

- Patient:
  - ssn: 999-11-1522
- Provider:
  - pid: 0b3ea153-64a1-392c-b528-7bb3425a6447

#### Test Stats:

- Allergies:

  - code: 3718001 (required)
  - state: California
  - city: Burbank

- Payer Coverage:

  - code: 6525002 (required)
  - payer id: df166300-5a78-3502-a46a-832842197811 (required)

- Patient Evolution:
  - code: 10509002 (required)
  - start date: 1965-02-06
  - end date: 1965-02-22
