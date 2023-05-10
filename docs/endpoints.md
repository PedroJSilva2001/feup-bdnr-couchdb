# Endpoints

## Patient
- `GET` **/patient/\<ssn\>/**
    - returns the record of a given patient (minus its aggregates); error, otherwise

- `PUT` **/patient/\<ssn\>/**
    - creates a patient record if it doesn't exist or updates if it exists
    - body:
        - new patient record in json

- `DELETE` **/patient/\<ssn\>/**
    - deletes a patient record if it exists; error, otherwise


- `GET` **/patient/\<ssn\>/<aggregation>/**
    - returns the aggregated records (encounters, claims,...) of a given patient; error, otherwise

## Provider
- `GET` **/provider/**
    - returns all provider records based on a set of filters
    - query parameters:
        - gender:
        - speciality
        - city
        - state

- `GET` **/provider/\<id\>/**
    - returns the provider record with the corresponding id
    - error, otherwise 

- `PUT` **/provider/\<id\>/**
    - creates a provider record if it doesn't exist or updates if it exists
    - body:
        - new provider record in json

- `DELETE` **/provider/\<id\>/**
    - deletes a provider record if it exists; error, otherwise

- `GET` **/provider/\<id\>/encounters/**
    - returns the encounter records (the participated encounters) of the provider with that ID; error, otherwise
    - query parameters:
        - patient: patient participant ID
        - payer: payer ID
        - class: encounter class
        - code: encounter code
        - start: encounter start date in ISO format
        - end: encounter end date in ISO format