import json
import os
import sys
import numpy as np
import pandas as pd
from time import time
from datetime import datetime
from copy import deepcopy

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

def get_patient_json_documents(datasets, claim_jsons, claim_transition_jsons, encounter_jsons):
    patients = datasets["patients"]
    allergies = datasets["allergies"]
    careplans = datasets["careplans"]
    conditions = datasets["conditions"]
    devices = datasets["devices"]
    imaging_studies = datasets["imaging_studies"]
    immunizations = datasets["immunizations"]
    medications = datasets["medications"]
    observations = datasets["observations"]
    procedures = datasets["procedures"]
    supplies = datasets["supplies"]

    patients_json = json.loads(patients.to_json(orient="records"))

    grouped_allergies = merge_datasets_1_n(patients, allergies, "patient_id", "allergy_patient")
    grouped_careplans = merge_datasets_1_n(patients, careplans, "patient_id", "careplan_patient")
    grouped_conditions = merge_datasets_1_n(patients, conditions, "patient_id", "condition_patient")
    grouped_devices = merge_datasets_1_n(patients, devices, "patient_id", "device_patient")
    grouped_imaging_studies = merge_datasets_1_n(patients, imaging_studies, "patient_id", "imaging_study_patient")
    grouped_immunizations = merge_datasets_1_n(patients, immunizations, "patient_id", "immunization_patient")
    grouped_medications = merge_datasets_1_n(patients, medications, "patient_id", "medication_patient")
    grouped_observations = merge_datasets_1_n(patients, observations, "patient_id", "observation_patient")
    grouped_procedures = merge_datasets_1_n(patients, procedures, "patient_id", "procedure_patient")
    grouped_supplies = merge_datasets_1_n(patients, supplies, "patient_id", "supply_patient")

    grouped_payer_transition_jsons = group_jsons(claim_transition_jsons, "patient")
    grouped_claim_jsons = group_jsons(claim_jsons, "patient")
    grouped_encounter_jsons = group_jsons(encounter_jsons, "patient")

    for patient_json in patients_json:
        patient_json["doc_type"] = "patient"
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

        patient_json["payer_transitions"] = grouped_payer_transition_jsons[patient_json["patient_id"]]
        patient_json["claims"] = grouped_claim_jsons[patient_json["patient_id"]]
        patient_json["encounters"] = grouped_encounter_jsons[patient_json["patient_id"]]

        strip_keys(patient_json, dataset_prefix("patients"))

        for prop in ["allergies", "careplans", "conditions", "devices",
                     "imaging_studies", "immunizations", "medications", 
                     "observations","procedures", "supplies", "encounters", 
                     "payer_transitions", "claims"]:
            patient_json[prop] = patient_json.pop(prop)
    
    return patients_json

def get_encounter_json_documents(datasets, claim_jsons):
    patients = datasets["patients"]
    organizations = datasets["organizations"]
    providers = datasets["providers"]
    payers = datasets["payers"]
    allergies = datasets["allergies"]
    careplans = datasets["careplans"]
    conditions = datasets["conditions"]
    devices = datasets["devices"]
    encounters = datasets["encounters"]
    imaging_studies = datasets["imaging_studies"]
    immunizations = datasets["immunizations"]
    medications = datasets["medications"]
    observations = datasets["observations"]
    procedures = datasets["procedures"]
    supplies = datasets["supplies"]

    merged = merge_datasets_1_1(encounters, patients, "encounter_patient", "patient_id")
    merged = merge_datasets_1_1(merged, providers, "encounter_provider", "provider_id")
    merged = merge_datasets_1_1(merged, organizations, "encounter_organization", "organization_id")
    merged = merge_datasets_1_1(merged, payers, "encounter_payer", "payer_id")

    encounters_json = json.loads(merged.to_json(orient="records"))

    grouped_allergies = merge_datasets_1_n(encounters, allergies, "encounter_id", "allergy_encounter")
    grouped_careplans = merge_datasets_1_n(encounters, careplans, "encounter_id", "careplan_encounter")
    grouped_conditions = merge_datasets_1_n(encounters, conditions, "encounter_id", "condition_encounter")
    grouped_devices = merge_datasets_1_n(encounters, devices, "encounter_id", "device_encounter")
    grouped_imaging_studies = merge_datasets_1_n(encounters, imaging_studies, "encounter_id", "imaging_study_encounter")
    grouped_immunizations = merge_datasets_1_n(encounters, immunizations, "encounter_id", "immunization_encounter")
    grouped_medications = merge_datasets_1_n(encounters, medications, "encounter_id", "medication_encounter")
    grouped_observations = merge_datasets_1_n(encounters, observations, "encounter_id", "observation_encounter")
    grouped_procedures = merge_datasets_1_n(encounters, procedures, "encounter_id", "procedure_encounter")
    grouped_supplies = merge_datasets_1_n(encounters, supplies, "encounter_id", "supply_encounter")

    grouped_claim_jsons = group_jsons(claim_jsons, "appointment")

    for encounter_json in encounters_json:
        encounter_json["doc_type"] = "encounter"
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

        encounter_json["claims"] = grouped_claim_jsons[encounter_json["encounter_id"]]

        strip_keys(encounter_json, dataset_prefix("encounters"))

        for prop in ["patient", "organization", "provider", "payer",
                     "allergies", "careplans", "conditions", "devices",
                     "imaging_studies", "immunizations", "medications", 
                     "observations","procedures", "supplies", 
                     "claims"]:
            encounter_json[prop] = encounter_json.pop(prop)
    
    return encounters_json

def get_simple_encounter_json_documents(datasets):
    encounters = datasets["encounters"]
    organizations = datasets["organizations"]
    providers = datasets["providers"]

    merged = merge_datasets_1_1(encounters, providers, "encounter_provider", "provider_id")
    merged = merge_datasets_1_1(merged, organizations, "encounter_organization", "organization_id")

    encounters_json = json.loads(merged.to_json(orient="records"))

    for encounter_json in encounters_json:
        aggregate_single(encounter_json, "encounter_organization", "organization_id", "organization_")
        aggregate_single(encounter_json, "encounter_provider", "provider_id","provider_")

        strip_keys(encounter_json, dataset_prefix("encounters"))

        del encounter_json["provider"]["address"]
        del encounter_json["provider"]["city"]
        del encounter_json["provider"]["state"]
        del encounter_json["provider"]["zip"]
        del encounter_json["provider"]["lat"]
        del encounter_json["provider"]["lon"]

        for prop in ["provider", "organization"]:
            encounter_json[prop] = encounter_json.pop(prop)
    
    return encounters_json

def get_provider_json_documents(datasets):
    providers = datasets["providers"]
    organizations = datasets["organizations"]

    merged = merge_datasets_1_1(providers, organizations, "provider_organization", "organization_id")

    provider_jsons = json.loads(merged.to_json(orient="records"))

    for provider_json in provider_jsons:
        provider_json["doc_type"] = "provider"

        aggregate_single(provider_json, "provider_organization", "organization_id", "organization_")

        strip_keys(provider_json, dataset_prefix("providers"))

        provider_json["organization"] = provider_json.pop("organization")

    return provider_jsons

def get_claim_json_documents(datasets):
    claims = datasets["claims"]
    claims_transactions = datasets["claims_transactions"]
    payers = datasets["payers"]
    providers = datasets["providers"]

    merged = merge_datasets_1_1(claims, payers, "claim_primary_patient_insurance", "payer_id", "primary_")
    merged = merge_datasets_1_1(merged, payers, "claim_secondary_patient_insurance", "payer_id", "secondary_")
    merged = merge_datasets_1_1(merged, providers, "claim_provider", "provider_id")
    merged = merge_datasets_1_1(merged, providers, "claim_referring_provider", "provider_id", "referring_")
    merged = merge_datasets_1_1(merged, providers, "claim_supervising_provider", "provider_id", "supervising_")

    grouped_claim_transactions = merge_datasets_1_n(claims, claims_transactions, "claim_id", "claims_transaction_claim")

    claims_json = json.loads(merged.to_json(orient="records"))

    for claim_json in claims_json:
        aggregate_single(claim_json, "claim_primary_patient_insurance", "primary_payer_id", "primary_payer_")
        aggregate_single(claim_json, "claim_secondary_patient_insurance", "secondary_payer_id", "secondary_payer_")
        aggregate_single(claim_json, "claim_provider", "provider_id", "provider_")
        aggregate_single(claim_json, "claim_referring_provider", "referring_provider_id", "referring_provider_")
        aggregate_single(claim_json, "claim_supervising_provider", "supervising_provider_id", "supervising_provider_")

        aggregate_multiple(claim_json, "claims_transactions", grouped_claim_transactions, "claim_id", "claims_transaction_claim", "claim")
        aggregate_properties(claim_json, "claim_diagnoses", ["claim_diagnosis1", "claim_diagnosis2", "claim_diagnosis3", "claim_diagnosis4",
                              "claim_diagnosis5", "claim_diagnosis6", "claim_diagnosis7", "claim_diagnosis8"])
        
        for claim_transaction_json in claim_json["claims_transactions"]:
            aggregate_properties(claim_transaction_json, "diagnoses_ref", ["diagnosis_ref1", "diagnosis_ref2", "diagnosis_ref3", "diagnosis_ref4"])
        
        strip_keys(claim_json, dataset_prefix("claims"))

        claim_json["claim_transactions"] = claim_json.pop("claims_transactions")

        for prop in ["primary_patient_insurance", "secondary_patient_insurance",
                     "provider", "referring_provider", "supervising_provider",
                     "claim_transactions"]:
            claim_json[prop] = claim_json.pop(prop)

    return claims_json

def get_payer_transition_json_documents(datasets):
    payer_transitions = datasets["payer_transitions"]
    payers = datasets["payers"]
  
    merged = merge_datasets_1_1(payer_transitions, payers, "payer_transition_primary_payer", "payer_id", "primary_")
    merged = merge_datasets_1_1(merged, payers, "payer_transition_secondary_payer", "payer_id", "secondary_")
    payer_transitions_json = json.loads(merged.to_json(orient="records"))

    for payer_transition_json in payer_transitions_json:
        aggregate_single(payer_transition_json, "payer_transition_primary_payer", "primary_payer_id", "primary_payer_")
        aggregate_single(payer_transition_json, "payer_transition_secondary_payer", "secondary_payer_id", "secondary_payer_")

        strip_keys(payer_transition_json, dataset_prefix("payer_transitions"))

    return payer_transitions_json

def export_output(output_path, patient_documents, encounter_documents, provider_documents):
    timestamp = time()
    timestamp_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    if not os.path.exists(output_path):
        os.mkdir(output_path)       

    batches_path = os.path.normpath(timestamp_str + "_" + patient_documents[0]["state"])
    batches_filepath = os.path.join(output_path, batches_path)
    new_batches_file_filepath = os.path.join(output_path, "batches.txt")

    batches_patients_filepath = os.path.join(batches_filepath, "patients")
    batches_encounters_filepath = os.path.join(batches_filepath, "encounters")
    batches_providers_filepath = os.path.join(batches_filepath, "providers")
    
    os.makedirs(batches_patients_filepath)
    os.makedirs(batches_encounters_filepath)
    os.makedirs(batches_providers_filepath)

    for patient in patient_documents:
        patient_filepath = os.path.join(batches_patients_filepath, patient["id"]+ ".json")
        with open(patient_filepath, 'w') as f:
            f.write(json.dumps(patient, indent=2))

    for encounter in encounter_documents:
        encounter_filepath = os.path.join(batches_encounters_filepath, encounter["id"]+ ".json")
        with open(encounter_filepath, 'w') as f:
            f.write(json.dumps(encounter, indent=2))

    for provider in provider_documents:
        provider_filepath = os.path.join(batches_providers_filepath, provider["id"] + ".json")
        with open(provider_filepath, 'w') as f:
            f.write(json.dumps(provider, indent=2))


    #if not os.path.exists(new_batches_file_filepath):
    with open(new_batches_file_filepath, "a") as f:
        f.write(timestamp_str + " " + patient_documents[0]["state"] + "\n")

def drop_and_rename_columns(datasets):
    # Remove unneeded columns

    #datasets["claims"].drop(["PATIENTID"], axis=1, inplace=True)

    datasets["claims_transactions"].drop(["PLACEOFSERVICE", "APPOINTMENTID", "PATIENTID", 
                                          "PROVIDERID","SUPERVISINGPROVIDERID",
                                          "PATIENTINSURANCEID", "LINENOTE", # insurance id incorrect and linenot unused
                                          "MODIFIER1", "MODIFIER2"], axis=1, inplace=True) # Modifiers unused

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
        #"LINENOTE": "LINE_NOTE",
        #"PATIENTINSURANCEID": "PATIENT_INSURANCE",
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
        "PAYER": "PRIMARY_PAYER",
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
    datasets["payer_transitions"]["payer_transition_secondary_payer"].replace(to_replace=np.nan, value=None, inplace=True)

    for dataset_name in dataset_names:
        dataset = datasets[dataset_name]
        prefix = dataset_prefix(dataset_name)
        for column in dataset.columns:
            if column == prefix + "reason_code":
                dataset[column] = dataset[column].fillna(-1)
                dataset[column] = dataset[column].astype(int)

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
    aggregated_json = { key: json.pop(key) for key in list(json.keys()) if key.startswith(prefix) }

    if aggregated_json[aggregated_json_key_id] == None:
        json[aggregate_key] = None
    else:
        strip_keys(aggregated_json, prefix, suffix)
        json[aggregate_key] = aggregated_json

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

def aggregate_properties(json, aggregate_key, keys):
    json[aggregate_key] = []
    for key in keys:
        value = json.pop(key)
        if value != None:
            json[aggregate_key].append(value)

def group_jsons(jsons, merged_json_key_id):
    grouped_jsons = {}

    for json in jsons:
        id = json[merged_json_key_id]
        json_copy = deepcopy(json)
        del json_copy[merged_json_key_id]
        if id in grouped_jsons:
            grouped_jsons[id].append(json_copy)
        else:
            grouped_jsons[id] = [json_copy]
    return grouped_jsons


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

    payer_transition_jsons = get_payer_transition_json_documents(datasets)
    claim_jsons = get_claim_json_documents(datasets)
    encounter_jsons = get_encounter_json_documents(datasets, claim_jsons)
    encounter_simple_jsons = get_simple_encounter_json_documents(datasets)

    patient_jsons = get_patient_json_documents(datasets, claim_jsons, payer_transition_jsons, encounter_simple_jsons)
    provider_jsons = get_provider_json_documents(datasets)

    export_output(output_path, patient_jsons, encounter_jsons, provider_jsons)
