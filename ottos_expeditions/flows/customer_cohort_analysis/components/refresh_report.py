from ascend.resources import component, ref, test


@component(
  dependencies=[ref("customer_cohort_analysis_transform")]
)
# Function to refresh dataset
def refresh_dataset(customer_cohort_analysis_transform, context):
    pass
