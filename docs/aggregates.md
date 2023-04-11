# Aggregate

## Patient
This aggregate represents a given Patient's Medical Record.
```json
{
  "id": "569991d5-9e70-c072-d73d-dddaa4a8b8d7",
  "birthdate": "1964-04-05",
  "deathdate": null,
  "ssn": "999-77-3348",
  "drivers": "S99929752", // optional field
  "passport": "X58771668X", // optional field
  "prefix": "Mr.", // optional field
  "firstname": "Marco Antonio",
  "lastname": "Blanco",
  // "suffix": not present (no suffix)
  // "maidenname": not present (only for females)
  "marital_status": "S", // optional
  "race": "asian",
  "ethnicity": "hispanic",
  "gender": "M",
  "birthplace": "Mexico City  Mexico City  MX",
  "address": "617 Flatley Vista Suite 72",
  "city": "Inglewood",
  "state": "CA",
  "county": "Los Angeles County",
  "fips": 6037, // optional
  "zip": 90302,
  "lat": 33.914933842146,
  "lon": -118.36223201007287,
  "healthcare_expenses": 72047.54, // TODO remove?
  "healthcare_coverage": 171647.76, // TODO remove?
  "income": 92065,

  "allergies": [
    {
      "id": "00afb333-c814-abfe-9b25-0dff1973c3d1", // generated
      "encounter": "00afb4d8-c814-abfe-9b25-0dff1973c3d1",
      "start": "1998-07-15", 
      // "stop": null, // optional
      "code": 264287008, 
      "system": "SNOMED-CT",
      "description": "Unknown,Animal dander (substance)",
      "type": "allergy",
      "category": "environment",
      "reactions": [
        {
          "reaction": 878820003,
          "description": "Rhinoconjunctivitis (disorder)",
          "severity": "MODERATE",  
        },
        {
          "reaction": 247472004,
          "description": "Wheal (finding)",
          "severity": "MILD",  
        }
      ]
    },
    ...
  ],
 
  "careplans": [
    {
      "id": "607c1da7-dc13-312d-1565-63555beae1f6",
      "encounter": "307357ee-6e42-47fc-56e9-d690c878f93f",
      "start": "1976-06-18",
      "stop": "1976-07-04", // optional 
      "code": 225358003,
      "description": "Wound care",
      "reason_code": "370247008", // optional
      "reason_description": "Facial laceration", // optional
    },
    ...
  ],

  "conditions": [
    {
      "id":, // generated
      "encounter": "f9f039eb-ace6-92cb-15f0-64412c562e17",
      "start": "1971-08-03",
      "stop": "1971-08-12", // optional
      "code": 444814009,
      "description": "Viral sinusitis (disorder)",
    },
    ...
  ],

  "devices": [
    {
      "id":, // generated
      "encounter": "956d0fbf-d3a8-7b98-521a-a967fb07fbbb",
      "start": "1995-06-18T05:52:50Z",
      //"stop": null, // optional
      "code": 337414009,
      "description": "Blood glucose meter (physical object)",
      "udi": "(01)84233720445157(11)950528(17)200611(10)9104133687(21)33168",
    },
    ...
  ],

  "imaging_studies": [
    {
      "id": "db156ca2-1983-b1fb-1fb6-c7f6447b4e01",//*
      "encounter": "7dc353a1-3926-eba2-0b8e-5194467d0f6d",
      "date": "2003-02-20T06:55:09Z",
      "series_uid": "1.2.840.99999999.1.66637228.1045724109442",
      "bodysite_code": 40983000,
      "bodysite_description": "Structure of upper extremity between shoulder and elbow (body structure)",
      "modality_code": "DX",
      "modality_description": "Digital Radiography",
      "instance_uid": "1.2.840.99999999.1.1.74599082.1045724109442",
      "sop_code": "1.2.840.10008.5.1.4.1.1.1.1",
      "sop_description": "Digital X-Ray Image Storage",
      "procedure_code": 1225002,
    },
    ...
  ],

  "immunizations": [
    {
      "id":, // generated
      "encounter": "6e461fb6-36ce-8e2a-713b-36851d1d2130",
      "date": "1964-07-12T05:52:50Z",
      "code": 10,
      "description": "IPV",
      "base_cost": 136.00, // generated with common costs
    },
    ...
  ],

  "medications": [
    {
      "id": , // generated
      "encounter": "98b0eb99-7789-f6bf-f106-e9ccae9a2db2",
      "payer": "734afbd6-4794-363b-9bc0-6a3981533ed5", //TODO document or id
      "start": "1976-12-19T17:52:50Z",
      "stop": "1976-12-29T17:52:50Z", // optional
      "code": 562251,
      "description": "Amoxicillin 250 MG / Clavulanate 125 MG Oral Tablet",
      "base_cost": 437.91,
      "payer_coverage": 407.91,
      "dispenses": 1,
      "total_cost": 437.91,
      "reason_code": 444814009, //optional
      "reason_description": "Viral sinusitis (disorder)", // optional
    },
    ...
  ],

  "observations": [
    {
      "id":, // generated
      "encounter": "353320db-11d1-32ba-d720-1f969d5434cb", // optional
      "date": "2016-09-25T05:52:50Z",
      "category": "survey", // optional
      "code": "X9999-1",
      "description": "Operative Status Value",
      "value": "urgent",
      "units": "{score}", // optional
      "type": "text",
    },
    ...
  ],

  "procedures": [
    {
      "id": , // generated
      "encounter": "07da161f-cf62-44db-40bd-ec92e8901735",
      "start": "2016-10-05T03:42:35Z",
      "stop": "2016-10-05T04:56:20Z", 
      "code": 415070008,
      "description": "Percutaneous coronary intervention (procedure)",
      "base_cost": 26592.19,
      "reason_code": 274531002, // optional
      "reason_description": "Abnormal findings diagnostic imaging heart+coronary circulat (finding)", // optional
    },
    ...
  ],

  "encounters": [
    {
      "id":,
      "organization": ,
      "provider":,
    },
    ...
  ]
}
```

## Provider
```json
{
  "id":,
  "name":,
  "gender":,
  "address":,
  "city":,
  "state":,
  "county":,
  "zip": ,
  "lat": ,
  "lon": ,
  "organization" : [
    {
      "id": ,
    }
  ]
}
```

<!-- - personal data
- organization -->


## Encounter

```json
{
  "organization" : [
    {
      "id": ,
    }
  ],
  "provider" : [
    {
      "id": ,
    }
  ],
  "patient": [
    {
      "id": "569991d5-9e70-c072-d73d-dddaa4a8b8d7",
      "birthdate": "1964-04-05",
      "deathdate": null,
      "ssn": "999-77-3348",
      "drivers": "S99929752", // optional field
      "passport": "X58771668X", // optional field
      "prefix": "Mr.", // optional field
      "firstname": "Marco Antonio",
      "lastname": "Blanco",
      // "suffix": not present (no suffix)
      // "maidenname": not present (only for females)
      "marital_status": "S", // optional
      "race": "asian",
      "ethnicity": "hispanic",
      "gender": "M",
      "birthplace": "Mexico City  Mexico City  MX",
      "address": "617 Flatley Vista Suite 72",
      "city": "Inglewood",
      "state": "CA",
      "county": "Los Angeles County",
      "fips": 6037, // optional
      "zip": 90302,
      "lat": 33.914933842146,
      "lon": -118.36223201007287,
      "healthcare_expenses": 72047.54, // TODO remove?
      "healthcare_coverage": 171647.76, // TODO remove?
      "income": 92065,
    }
  ]
}
```
<!-- - organization (maybe key?)
- provider (maybe key?)
- info patient -->





