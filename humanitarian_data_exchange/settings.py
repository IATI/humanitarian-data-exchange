import os

CKAN_URL = os.getenv("CKAN_URL", "https://data.humdata.org/")

CKAN_TAG_IDS = [
    "2bfc754f-deee-4e10-a85c-61ad8b8983f3",
    "a0fbb23a-6aad-4ccc-8062-e9ef9f20e5d2",
    "ec53893c-6dba-4656-978b-4a32289ea2eb",
]

CKAN_CAVEATS = 'Information originates from multiple IATI reporting organisations, and has not been centrally vetted or audited for accuracy or consistency.  \r\n\r\nIncludes only those activities from the [IATI Registry](https://iatiregistry.org/) that are included in [D-Portal](http://www.d-portal.org) and have the status "Implementing".\r\n\r\nThe total number of activities may include duplicates, if (for example) a donor and an implementing partner both report the same activity under different IATI identifiers.\r\n\r\nStart and end dates of activities within the dataset will differ.'

CKAN_TITLE_START = "Current IATI aid activities in "

CKAN_RESOURCE_V1_DESCRIPTION_START = "Currently-active IATI activities in "
CKAN_RESOURCE_V1_DESCRIPTION_END = ", in 3W/4W style with HXL hashtags. This dataset has one row for each unique activity/sector/location, so the same IATI activity may occupy multiple rows: use the #activity+id column to count unique activities."

DATASETS_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "datasets"
)
