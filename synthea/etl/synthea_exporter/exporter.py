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
    pass

def get_encounter_json_documents(datasets):
    encounters = datasets["encounters"]
    patients = datasets["patients"]
    organizations = datasets["organizations"]
    providers = datasets["providers"]
    payers = datasets["payers"]

    merged = pd.merge(encounters, patients, how="left", left_on="encounter_patient", right_on="patient_id")
    merged = pd.merge(merged, organizations, how="left", left_on="encounter_organization", right_on="organization_id")
    merged = pd.merge(merged, providers, how="left", left_on="encounter_provider", right_on="provider_id")
    merged = pd.merge(merged, payers, how="left", left_on="encounter_payer", right_on="payer_id")


def get_provider_json_documents(datasets):
    providers = datasets["providers"]
    organizations = datasets["organizations"]

    merged = pd.merge(providers, organizations, how="left", left_on="provider_organization", right_on="organization_id")

    providers_json = json.loads(merged.to_json(orient="records"))

    for record in providers_json:
        record["provider_organization"] = {
            "id": record.pop("organization_id"),
            "name": record.pop("organization_name"),
            "address": record.pop("organization_address"),
            "city": record.pop("organization_city"),
            "state": record.pop("organization_state"),
            "zip": record.pop("organization_zip"),
            "lat": record.pop("organization_lat"),
            "lon": record.pop("organization_lon"),
            "phone": record.pop("organization_phone")
        }

    return json.dumps(providers_json, indent=2)

def get_claims_json_documents(datasets):
    claims = datasets["claims"]
    claims_transactions = datasets["claims_transactions"]
    patients = datasets["patients"]
    payers = datasets["payers"]
    providers = datasets["providers"]
    organizations = datasets["organizations"]
    encounters = datasets["encounters"]

    merged = pd.merge(claims, claims_transactions, how="outer", left_on="claim_id", right_on="claims_transaction_claim")

    grouped_claim_transactions = json.loads(merged.groupby("claim_id").apply(
        lambda x: x[claims_transactions.columns].to_dict(orient="records")
    ).to_json())

    merged = merge_datasets_1_1(claims, patients, "claim_patient", "patient_id")
    merged = merge_datasets_1_1(merged, encounters, "claim_appointment", "encounter_id")
    merged = merge_datasets_1_1(merged, payers, "claim_primary_patient_insurance", "payer_id", "primary_")
    merged = merge_datasets_1_1(merged, payers, "claim_secondary_patient_insurance", "payer_id", "secondary_")
    merged = merge_datasets_1_1(merged, providers, "claim_provider", "provider_id")
    merged = merge_datasets_1_1(merged, providers, "claim_referring_provider", "provider_id", "referring_")
    merged = merge_datasets_1_1(merged, providers, "claim_supervising_provider", "provider_id", "supervising_")

    claims_json = json.loads(merged.to_json(orient="records"))

    for claim_json in claims_json:
        claim_transactions_json = grouped_claim_transactions[claim_json["claim_id"]]
        drop_prefix(claim_transactions_json, dataset_prefix("claims_transactions"))
        drop_property(claim_transactions_json, "claim")
        claim_json["claim_transactions"] = claim_transactions_json

        aggregate(claim_json, "claim_patient", "patient_")
        aggregate(claim_json, "claim_appointment", "encounter_")
        aggregate(claim_json, "claim_primary_patient_insurance", "primary_payer_")
        aggregate(claim_json, "claim_secondary_patient_insurance", "secondary_payer_")
        aggregate(claim_json, "claim_provider", "provider_")
        aggregate(claim_json, "claim_referring_provider", "referring_provider_")
        aggregate(claim_json, "claim_supervising_provider", "supervising_provider_")

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

def aggregate(json, aggregate_key, prefix, suffix=None):
    json[aggregate_key] = {}
    keys = list(json.keys())

    for key in keys:
        if not key.startswith(prefix):
            continue

        if suffix != None and (not key.endswith(suffix)):
            continue

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
    #print(get_encounter_json_documents(datasets))
    #print(get_claims_json_documents(datasets))