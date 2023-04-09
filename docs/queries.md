# Queries

## Allergies/Intolerances
- What are the (10) most common Allergens that patients are allergic to, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

    ```js
    /* Query the 10 all-time most common Allergens nationally */

    // map function
    function(doc) => {
        if (doc.documentType === "AllergyIntolerance" && doc.type === "allergy") {
            emit([doc.code, doc.patient.state, doc.patient.city], {
                description: doc.description,
                category: doc.category,
                count: 1
            });
        }
    }

    // reduce function
    function(keys, values, rereduce) {
        if (rereduce) {
            return values;
        } else {
            return values.reduce((a, b) => {
                return { 
                    description: a.description, 
                    category: a.category, 
                    count: a.count + b.count
                };
            });
        }
    }

    // Couchdb views don't support sorting by value in queries, only by key, so we can
    // at the application level retrieve all results by querying the view and select the top 10:
        GET /db/_design/design_doc/_view/view_name/?group=true&descending=true
    // or we can save the view's results in the database and use a mango query (which supports sorting by a given attribute):
        {
          "selector": {
            "documentType": "AllergyIntolerance",
            "type": "allergy"
          },
          "fields": [
            "code", 
            "description", 
            "category"
          ],
          "group": true,
          "limit": 10,
          "sort": [
            {"count": "desc"}
          ]
        }
    ```
- How many people are allergic to a given Allergy, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?
- What is the incidence , and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?
- What are the most common reactions of a given Allergy?
- What is the average severity of a given Allergy
- What is the prevalence of allergies among children under the age of 5?
- How does the prevalence of allergies differ by age, gender, and race/ethnicity?
- What is the average age of onset for different types of allergies, such as food allergies and seasonal allergies?
- How often do patients with a known allergy experience an allergic reaction, and what are the most common symptoms?
- What is the most common course of treatment for patients with severe allergies, such as anaphylaxis?
- How often do patients receive allergy testing, and how accurate are these tests in diagnosing specific allergies?
- What is the most common type of allergy medication prescribed, and how effective is it in managing allergy symptoms?
- What is the average cost of care for patients with allergies, including medication, allergy testing, and allergy shots?
- How does the incidence of asthma and other respiratory conditions vary among patients with allergies compared to those without allergies?

## Careplans

## Claims

## Claims Transactions

## Conditions
- What are the 10 most prevalent Medical Conditions, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?
- What is the prevalence of a Medical Condition among adults over a given age in a certain State/City?

## Devices
- What are the (10) most used Medical Devices, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?
- What is the average use of Medical Devices per Patient, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

## Encounter
- Find a given Medical Encounter
- Find Medical Encounters
    - in a given Health Organization / per Health Organization?
    - in a given city / state / nationally
    - in a given year / by year / all-time?

## Imaging Studies

## Immunizations
- What are the (10) most administered Immunizations, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

## Medications
- What are the (10) most administered Medications, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

## Observations

## Organizations


## Patients
- Find Allergies/Intolerances
- Find Careplans
- Find Medical Conditions
- Find Medical Devices
- Find Medical Encounters
- Find Imaging Studies
- Find Immunizations
- Find Medications
- Find Medical Observations
- Find Medical Procedures

## Payer Transitions

## Payers

## Procedures
- Find a given Medical Procedure
- Find Medical Procedures done by a given Patient
    - in a given Health Organization / per Health Organization?
    - in a given city / state / nationally
    - in a given year / by year / all-time?
- What are the (10) most common Medical Procedures, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?
- How many people have done a given Medical Procedure, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?
- Calculate how much money is spent on average in Medical Procedures per Patient, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

## Providers
- Find a given Health Provider
- List Health Providers
    - in a given Health Organization / per Health Organization?
    - in a given city / state / nationally
- How many Encounters has a given Health Provider conducted
    - in a given year / by year.
- How are Health Providers geographically distributed (Health Organization/Living place's city and state)?.
- How are Health Providers distributed by Speciality?
- How are Health Providers demographically distributed?

## Supplies
- What are the (10) most used Medical Supplies, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

- What is the average use of a Medical Supply per Patient, and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

- What is the average use of a Medical Supply per/in a given Medical Encounter Class (i.e wellness, urgent care..), and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

- What are the most used Medical Supplies per/in a given Medical Encounter Class (i.e wellness, urgent care..), and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

- What is the average use of a Medical Supply per/in a given Medical Encounter Type(i.e wellness, urgent care..), and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

- What are the most used Medical Supplies per/in a given Medical Encounter Type (i.e wellness, urgent care..), and how does this vary by factors such as geographic region, year/month and demographics (sex, race and age)?

### Notes
1 Encounter can have:
    - * Careplans
    - * Conditions
    - * observations
    - * Procedures
    - 1 provider
    - * Supplies

1 Observation can have or not an associated Encounter