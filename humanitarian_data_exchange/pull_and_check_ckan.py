import json
import os.path

import requests
import settings
import yaml


def pull_and_check_ckan():
    # Setup
    r = requests.get(
        settings.CKAN_URL
        + "/api/3/action/package_search?fq=organization:iati&rows=1000"
    )
    r.raise_for_status()
    data = r.json()
    problems = []
    # Loop
    for ckan_dataset in data.get("result").get("results"):
        # Handy Print Debugging
        # print("------------------------------------------------")
        # print(json.dumps(ckan_dataset, indent=2))
        # Check data
        if ckan_dataset.get("caveats") != settings.CKAN_CAVEATS:
            problems.append(
                "Resource " + ckan_dataset.get("name") + " has the wrong caveat"
            )
        tag_ids = [x.get("id") for x in ckan_dataset["tags"]]
        for tag_id in settings.CKAN_TAG_IDS:
            if tag_id not in tag_ids:
                problems.append(
                    "Resource "
                    + ckan_dataset.get("name")
                    + " does not have the expected tag "
                    + tag_id
                )
        # Make out data
        out_data = {
            "id": ckan_dataset.get("id"),
            "title": ckan_dataset.get("title"),
            "resources": [],
            "tags": [],
        }
        if out_data["title"].startswith(settings.CKAN_TITLE_START):
            out_data["title"] = out_data["title"][len(settings.CKAN_TITLE_START) :]
        else:
            problems.append(
                "Resource "
                + ckan_dataset.get("name")
                + " starts with a different title"
            )
        for ckan_resource in ckan_dataset.get("resources"):
            out_resource = {
                "description": ckan_resource.get("description"),
                "url": ckan_resource.get("url"),
            }
            out_data["resources"].append(out_resource)
        for ckan_tag in ckan_dataset.get("tags"):
            if ckan_tag.get("id") not in settings.CKAN_TAG_IDS:
                out_tag = {"id": ckan_tag.get("id"), "name": ckan_tag.get("name")}
                out_data["tags"].append(out_tag)
        ckan_dataset_solr_additions = json.loads(
            ckan_dataset.get("solr_additions", "{}")
        )
        # Check data (after processing has been done)
        if ckan_dataset_solr_additions.get("countries") != [out_data["title"]]:
            problems.append(
                "Resource "
                + ckan_dataset.get("name")
                + " has a different solr_additions/countries! "
                + str(ckan_dataset_solr_additions.get("countries"))
            )
        # Write out data
        with open(
            os.path.join(
                settings.DATASETS_DIRECTORY, ckan_dataset.get("name") + ".yaml"
            ),
            "w",
        ) as fp:
            yaml.dump(out_data, fp, indent=4, sort_keys=True)
    # return
    return problems


if __name__ == "__main__":
    problems = pull_and_check_ckan()
    if problems:
        print("PROBLEMS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for problem in problems:
            print(problem)
