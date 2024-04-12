import Levenshtein
from collections import defaultdict


def check_group(org_data, model_json_data):
    try:
        group_name = model_json_data["under_group"]
        if org_data:
            if group_name in [org_values["name"] for org_values in org_data]:
                return True
            else:
                distances = defaultdict(
                    list
                )  # Store distances and words with the same distance
                for org_values in org_data:
                    org_value = org_values["name"]
                    distance = Levenshtein.distance(group_name, org_value)
                    distances[distance].append(org_value)
                sorted_distances = sorted(distances.items())
                top_3 = []
                count = 0
                for _, i in sorted_distances:
                    for txt in i:
                        if count < 3:
                            top_3.append(txt)
                            count += 1
                        else:
                            break
                return top_3
        else:
            return "This Orgnization Id doesn't exists."
    except Exception as e:
        raise ValueError("under_group not defined or could not be parsed") from e
    except:
        raise


def check_ledger_name(ledger_data, ledger_name):
    try:
        if ledger_name in [
            ledger_values["ledger_name"] for ledger_values in ledger_data
        ]:
            return False
        else:
            return True
    except Exception as e:
        raise ValueError("ledger_name not defined or could not be parsed") from e
    except:
        raise



