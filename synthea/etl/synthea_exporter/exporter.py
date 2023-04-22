import json
import sys
import numpy as np
import pandas as pd

dataset_names = [
    "allergies",
    "careplans",
    "claims_transactions",
    "claims",
    "conditions",
    "devices",
    "encounters",
    "imaging_studies",
    "immunizations",
    "medications",
    "observations",
    "organizations",
    "patients",
    "payer_transitions",
    "payers",
    "procedures",
    "providers",
    "supplies"
]

def read_datasets(datasets_path):
    datasets = {}

    for dataset_name in dataset_names:
        try:
            dataset = pd.read_csv(datasets_path + "/csv/" + dataset_name + ".csv")
            datasets[dataset_name] = dataset
        except Exception:
            print("Couldn't load dataset " + dataset_name)
            return None
    
    return datasets

def get_patient_json_documents(datasets):
    patients = datasets["patients"]
    allergies = datasets["allergies"]
    careplans = datasets["careplans"]
    claims = datasets["claims"]
    conditions = datasets["conditions"]
    devices = datasets["devices"]
    encounters = datasets["encounters"]
    imaging_studies = datasets["imaging_studies"]
    immunizations = datasets["immunizations"]
    medications = datasets["medications"]
    observations = datasets["observations"]
    payer_transitions = datasets["payer_transitions"]
    procedures = datasets["procedures"]
    supplies = datasets["supplies"]

    patients_json = json.loads(patients.to_json(orient="records"))

    grouped_allergies = merge_datasets_1_n(patients, allergies, "patient_id", "allergy_patient")
    grouped_careplans = merge_datasets_1_n(patients, careplans, "patient_id", "careplan_patient")
#grouped_claims = merge_datasets_1_n(patients, claims, "patient_id", "careplan_patient")
    grouped_conditions = merge_datasets_1_n(patients, conditions, "patient_id", "condition_patient")
    grouped_devices = merge_datasets_1_n(patients, devices, "patient_id", "device_patient")
    grouped_imaging_studies = merge_datasets_1_n(patients, imaging_studies, "patient_id", "imaging_study_patient")
    grouped_immunizations = merge_datasets_1_n(patients, immunizations, "patient_id", "immunization_patient")
    grouped_medications = merge_datasets_1_n(patients, medications, "patient_id", "medication_patient")
    grouped_observations = merge_datasets_1_n(patients, observations, "patient_id", "observation_patient")
# payer transitions
    grouped_procedures = merge_datasets_1_n(patients, procedures, "patient_id", "procedure_patient")
    grouped_supplies = merge_datasets_1_n(patients, supplies, "patient_id", "supply_patient")

    for patient_json in patients_json:
        aggregate_multiple(patient_json, "allergies", grouped_allergies, "patient_id", "allergy_patient", "patient")
        aggregate_multiple(patient_json, "careplans", grouped_careplans, "patient_id", "careplan_patient", "patient")
        aggregate_multiple(patient_json, "conditions", grouped_conditions, "patient_id", "condition_patient", "patient")
        aggregate_multiple(patient_json, "devices", grouped_devices, "patient_id", "device_patient", "patient")
        aggregate_multiple(patient_json, "imaging_studies", grouped_imaging_studies, "patient_id", "imaging_study_patient", "patient")
        aggregate_multiple(patient_json, "immunizations", grouped_immunizations, "patient_id", "immunization_patient", "patient")
        aggregate_multiple(patient_json, "medications", grouped_medications, "patient_id", "medication_patient", "patient")
        aggregate_multiple(patient_json, "observations", grouped_observations, "patient_id", "observation_patient", "patient")
        aggregate_multiple(patient_json, "procedures", grouped_procedures, "patient_id", "procedure_patient", "patient")
        aggregate_multiple(patient_json, "supplies", grouped_supplies, "patient_id", "supply_patient", "patient")

        strip_keys(patient_json, dataset_prefix("patients"))
    
    return patients_json

def get_encounter_json_documents(datasets):
    patients = datasets["patients"]
    organizations = datasets["organizations"]
    providers = datasets["providers"]
    payers = datasets["payers"]
    allergies = datasets["allergies"]
    careplans = datasets["careplans"]
    claims = datasets["claims"]
    conditions = datasets["conditions"]
    devices = datasets["devices"]
    encounters = datasets["encounters"]
    imaging_studies = datasets["imaging_studies"]
    immunizations = datasets["immunizations"]
    medications = datasets["medications"]
    observations = datasets["observations"]
    payer_transitions = datasets["payer_transitions"]
    procedures = datasets["procedures"]
    supplies = datasets["supplies"]

    merged = merge_datasets_1_1(encounters, patients, "encounter_patient", "patient_id")
    merged = merge_datasets_1_1(merged, providers, "encounter_provider", "provider_id")
    merged = merge_datasets_1_1(merged, organizations, "encounter_organization", "organization_id")
    merged = merge_datasets_1_1(merged, payers, "encounter_payer", "payer_id")

    encounters_json = json.loads(merged.to_json(orient="records"))

    grouped_allergies = merge_datasets_1_n(encounters, allergies, "encounter_id", "allergy_encounter")
    grouped_careplans = merge_datasets_1_n(encounters, careplans, "encounter_id", "careplan_encounter")
#grouped_claims = merge_datasets_1_n(encounters, claims, "encounter_id", "careplan_encounter")
    grouped_conditions = merge_datasets_1_n(encounters, conditions, "encounter_id", "condition_encounter")
    grouped_devices = merge_datasets_1_n(encounters, devices, "encounter_id", "device_encounter")
    grouped_imaging_studies = merge_datasets_1_n(encounters, imaging_studies, "encounter_id", "imaging_study_encounter")
    grouped_immunizations = merge_datasets_1_n(encounters, immunizations, "encounter_id", "immunization_encounter")
    grouped_medications = merge_datasets_1_n(encounters, medications, "encounter_id", "medication_encounter")
    grouped_observations = merge_datasets_1_n(encounters, observations, "encounter_id", "observation_encounter")
# payer transitions
    grouped_procedures = merge_datasets_1_n(encounters, procedures, "encounter_id", "procedure_encounter")
    grouped_supplies = merge_datasets_1_n(encounters, supplies, "encounter_id", "supply_encounter")

    for encounter_json in encounters_json:
        aggregate_single(encounter_json, "encounter_patient", "patient_id", "patient_")
        aggregate_single(encounter_json, "encounter_organization", "organization_id", "organization_")
        aggregate_single(encounter_json, "encounter_provider", "provider_id","provider_")
        aggregate_single(encounter_json, "encounter_payer", "payer_id", "payer_")

        aggregate_multiple(encounter_json, "allergies", grouped_allergies, "encounter_id", "allergy_encounter", "encounter")
        aggregate_multiple(encounter_json, "careplans", grouped_careplans, "encounter_id", "careplan_encounter", "encounter")
        aggregate_multiple(encounter_json, "conditions", grouped_conditions, "encounter_id", "condition_encounter", "encounter")
        aggregate_multiple(encounter_json, "devices", grouped_devices, "encounter_id", "device_encounter", "encounter")
        aggregate_multiple(encounter_json, "imaging_studies", grouped_imaging_studies, "encounter_id", "imaging_study_encounter", "encounter")
        aggregate_multiple(encounter_json, "immunizations", grouped_immunizations, "encounter_id", "immunization_encounter", "encounter")
        aggregate_multiple(encounter_json, "medications", grouped_medications, "encounter_id", "medication_encounter", "encounter")
        aggregate_multiple(encounter_json, "observations", grouped_observations, "encounter_id", "observation_encounter", "encounter")
        aggregate_multiple(encounter_json, "procedures", grouped_procedures, "encounter_id", "procedure_encounter", "encounter")
        aggregate_multiple(encounter_json, "supplies", grouped_supplies, "encounter_id", "supply_encounter", "encounter")

        strip_keys(encounter_json, dataset_prefix("encounters"))
    
    return encounters_json

def get_provider_json_documents(datasets):
    providers = datasets["providers"]
    organizations = datasets["organizations"]

    merged = merge_datasets_1_1(providers, organizations, "provider_organization", "organization_id")

    providers_json = json.loads(merged.to_json(orient="records"))

    for provider_json in providers_json:
        aggregate_single(provider_json, "provider_organization", "organization_")

        strip_keys(provider_json, dataset_prefix("providers"))


    return json.dumps(providers_json, indent=2)

def get_claims_json_documents(datasets):
    claims = datasets["claims"]
    claims_transactions = datasets["claims_transactions"]
    patients = datasets["patients"]
    payers = datasets["payers"]
    providers = datasets["providers"]
    organizations = datasets["organizations"]
    encounters = datasets["encounters"]

    merged = merge_datasets_1_1(claims, patients, "claim_patient", "patient_id")
    merged = merge_datasets_1_1(merged, encounters, "claim_appointment", "encounter_id")
    merged = merge_datasets_1_1(merged, payers, "claim_primary_patient_insurance", "payer_id", "primary_")
    merged = merge_datasets_1_1(merged, payers, "claim_secondary_patient_insurance", "payer_id", "secondary_")
    merged = merge_datasets_1_1(merged, providers, "claim_provider", "provider_id")
    merged = merge_datasets_1_1(merged, providers, "claim_referring_provider", "provider_id", "referring_")
    merged = merge_datasets_1_1(merged, providers, "claim_supervising_provider", "provider_id", "supervising_")

    grouped_claim_transactions = merge_datasets_1_n(claims, claims_transactions, "claim_id", "claims_transaction_claim")

    claims_json = json.loads(merged.to_json(orient="records"))

    for claim_json in claims_json:
        aggregate_single(claim_json, "claim_patient", "patient_id", "patient_")
        aggregate_single(claim_json, "claim_appointment", "encounter_id", "encounter_")
        aggregate_single(claim_json, "claim_primary_patient_insurance", "primary_payer_id", "primary_payer_")
        aggregate_single(claim_json, "claim_secondary_patient_insurance", "secondary_payer_id", "secondary_payer_")
        aggregate_single(claim_json, "claim_provider", "provider_id", "provider_")
        aggregate_single(claim_json, "claim_referring_provider", "referring_provider_id", "referring_provider_")
        aggregate_single(claim_json, "claim_supervising_provider", "supervising_provider_id", "supervising_provider_")

        aggregate_multiple(claim_json, "claims_transactions", grouped_claim_transactions, "claim_id", "claims_transaction_claim", "claim")

        strip_keys(claim_json, dataset_prefix("claims"))

    return claims_json
    
def export_output(output_path, patients_dataset, encounters_dataset, providers_dataset):
    pass

def drop_and_rename_columns(datasets):
    # Remove unneeded columns

    datasets["claims_transactions"].drop(["PLACEOFSERVICE", "APPOINTMENTID", "PATIENTID", 
                                          "PROVIDERID","SUPERVISINGPROVIDERID"], axis=1, inplace=True)

    datasets["organizations"].drop(["REVENUE", "UTILIZATION"], axis=1, inplace=True)

    datasets["patients"].drop(["HEALTHCARE_EXPENSES", "HEALTHCARE_COVERAGE", "INCOME"], axis=1, inplace=True)

    datasets["payers"].drop([
        "AMOUNT_COVERED", "AMOUNT_UNCOVERED",
        "REVENUE",
        "COVERED_ENCOUNTERS", "UNCOVERED_ENCOUNTERS",
        "COVERED_MEDICATIONS", "UNCOVERED_MEDICATIONS",
        "COVERED_PROCEDURES", "UNCOVERED_PROCEDURES",
        "COVERED_IMMUNIZATIONS", "UNCOVERED_IMMUNIZATIONS",
        "UNIQUE_CUSTOMERS",
        "QOLS_AVG",
        "MEMBER_MONTHS"
    ], axis=1, inplace=True)

    datasets["providers"].drop(["ENCOUNTERS", "PROCEDURES"], axis=1, inplace=True)
  
    # Separate by underscores

    datasets["careplans"].rename(columns={
        "REASONCODE": "REASON_CODE",
        "REASONDESCRIPTION": "REASON_DESCRIPTION",
    }, inplace=True)

    datasets["claims"].rename(columns={
        "PATIENTID": "PATIENT",
        "PROVIDERID": "PROVIDER",
        "PRIMARYPATIENTINSURANCEID": "PRIMARY_PATIENT_INSURANCE",
        "SECONDARYPATIENTINSURANCEID": "SECONDARY_PATIENT_INSURANCE",
        "DEPARTMENTID": "DEPARTMENT_ID",
        "PATIENTDEPARTMENTID": "PATIENT_DEPARTMENT_ID",
        "REFERRINGPROVIDERID": "REFERRING_PROVIDER",
        "APPOINTMENTID": "APPOINTMENT",
        "CURRENTILLNESSDATE": "CURRENT_ILLNESS_DATE",
        "SERVICEDATE": "SERVICE_DATE",
        "SUPERVISINGPROVIDERID": "SUPERVISING_PROVIDER",
        "LASTBILLEDDATE1": "LAST_BILLED_DATE_1",
        "LASTBILLEDDATE2": "LAST_BILLED_DATE_2",
        "LASTBILLEDDATEP": "LAST_BILLED_DATE_P",
        "HEALTHCARECLAIMTYPEID1": "HEALTHCARE_CLAIM_TYPE_ID1",
        "HEALTHCARECLAIMTYPEID2": "HEALTHCARE_CLAIM_TYPE_ID2",
    }, inplace=True)

    datasets["claims_transactions"].rename(columns={
        "CLAIMID": "CLAIM",
        "CHARGEID": "CHARGE",
        "FROMDATE": "FROM_DATE",
        "TODATE": "TO_DATE",
        "PROCEDURECODE": "PROCEDURE_CODE",
        "DIAGNOSISREF1": "DIAGNOSIS_REF1",
        "DIAGNOSISREF2": "DIAGNOSIS_REF2",
        "DIAGNOSISREF3": "DIAGNOSIS_REF3",
        "DIAGNOSISREF4": "DIAGNOSIS_REF4",
        "DEPARTMENTID": "DEPARTMENT_ID",
        "UNITAMOUNT": "UNIT_AMOUNT",
        "TRANSFEROUTID": "TRANSFER_OUT_ID",
        "TRANSFERTYPE": "TRANSFER_TYPE",
        "LINENOTE": "LINE_NOTE",
        "PATIENTINSURANCEID": "PATIENT_INSURANCE",
        "FEESCHEDULEID": "FEE_SCHEDULE_ID",
    }, inplace=True)

    datasets["encounters"].rename(columns={
        "ENCOUNTERCLASS": "ENCOUNTER_CLASS",
        "REASONCODE": "REASON_CODE",
        "REASONDESCRIPTION": "REASON_DESCRIPTION",
    }, inplace=True)

    datasets["medications"].rename(columns={
        "TOTALCOST": "TOTAL_COST",
        "REASONCODE": "REASON_CODE",
        "REASONDESCRIPTION": "REASON_DESCRIPTION",
    }, inplace=True)

    datasets["payer_transitions"].rename(columns={
        "MEMBERID": "MEMBER_ID",
    }, inplace=True)

    datasets["procedures"].rename(columns={
        "REASONCODE": "REASON_CODE",
        "REASONDESCRIPTION": "REASON_DESCRIPTION",
    }, inplace=True)

    # Lowercase and prefix the columns

    for dataset_name in dataset_names:
        dataset = datasets[dataset_name]
        dataset.columns = map(str.lower, dataset.columns)
        dataset.columns = map(lambda col: dataset_prefix(dataset_name) +  col, dataset.columns)
    
    datasets["claims"]["claim_secondary_patient_insurance"].replace(to_replace=0, value=None, inplace=True)
    datasets["claims"]["claim_referring_provider"].replace(to_replace=np.nan, value=None, inplace=True)

def dataset_prefix(dataset_name):
    return (dataset_name[:-3] + "y" if dataset_name.endswith("ies") else dataset_name[:-1]) + "_"

def drop_prefix(jsons, prefix):
    for json in jsons:
        keys = list(json.keys())
        for key in keys:
            key_no_prefix = key.replace(prefix, "", 1)
            json[key_no_prefix] = json.pop(key)

def strip_keys(json, prefix, suffix=None):
    keys = list(json.keys())
    for key in keys:
        if not key.startswith(prefix):
            continue
        if not (suffix is None) and not key.endswith(suffix):
            continue
        value = json.pop(key)
    
        if suffix != None:
            stripped_key = str(key.replace(suffix, "", 1))
        else:
            stripped_key = str(key) 
        stripped_key = stripped_key.replace(prefix, "", 1)
        json[stripped_key] = value

def drop_property(jsons, property):
    for json in jsons:
        del json[property]

def aggregate_single(json, aggregate_key, aggregated_json_key_id, prefix, suffix=None):
    json[aggregate_key] = {}
    keys = list(json.keys())

    for key in keys:
        if not key.startswith(prefix):
            continue

        if suffix != None and (not key.endswith(suffix)):
            continue

        if key == aggregated_json_key_id and json[aggregated_json_key_id] == None:
            json[aggregate_key] = None
            return

        value = json.pop(key)
        if suffix != None:
            stripped_key = str(key.replace(suffix, "", 1))
        else:
            stripped_key = str(key)

        stripped_key = stripped_key.replace(prefix, "", 1)
        json[aggregate_key][stripped_key] = value

    strip_keys(json[aggregate_key], prefix, suffix)

def merge_datasets_1_1(dataset1, dataset2, left_on, right_on, prefix=None):
    if prefix != None:
        dataset2.columns = map(lambda col: prefix + str(col), dataset2.columns)

    merged = pd.merge(dataset1, dataset2, how="left", left_on=left_on, right_on=(prefix +right_on) if prefix != None else right_on)

    if prefix != None:
        dataset2.columns = map(lambda col: col.replace(prefix, "", 1), dataset2.columns)

    return merged

def merge_datasets_1_n(dataset1, dataset2, left_on, right_on):
    merged = pd.merge(dataset1, dataset2, how="outer", left_on=left_on, right_on=right_on)

    grouped_jsons = json.loads(merged.groupby(left_on).apply(
        lambda x: x[dataset2.columns].to_dict(orient="records")
    ).to_json())

    return grouped_jsons

def drop_na(jsons, key_id):
    return [json for json in jsons if json[key_id] != None]

def aggregate_multiple(json, aggregate_key, grouped_jsons, json_id, aggregated_jsons_key_id, dropped_property):
    aggregated_jsons = drop_na(grouped_jsons[json[json_id]], aggregated_jsons_key_id)
    drop_prefix(aggregated_jsons, dataset_prefix(aggregate_key))
    drop_property(aggregated_jsons, dropped_property)
    json[aggregate_key] = aggregated_jsons

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("wrong number of parameters\n")
        print("usage: exporter <datasets_path> <output_path>")
    
    datasets_path = sys.argv[1]
            
    output_path = sys.argv[2]

    datasets = read_datasets(datasets_path)

    if datasets == None:
        print("Couldn't load datasets")
    
    drop_and_rename_columns(datasets)
    #get_claims_json_documents(datasets)
    print(json.dumps(get_claims_json_documents(datasets)[0], indent=2))
    #print(get_provider_json_documents(datasets))
    #print(json.dumps(get_encounter_json_documents(datasets)[0], indent=2))
    #print(json.dumps(get_patient_json_documents(datasets), indent=2))