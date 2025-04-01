import yaml

from typing import Any
from pydantic import BaseModel

from ascend.resources import ComponentBuilder
from ascend.application.application import (
    Application,
    ApplicationBuildContext,
    application,
)
from ascend.models.component.component import Component


class Category(BaseModel):
    """Parameters relevant for particular NPS analysis"""

    name: str
    threshold: int


class AnalysisConfig(BaseModel):
    """Configuration for NPS analysis"""

    input_name: str
    categories: list[Category]


@application(name="nps_analysis")
class NPSAnalysis(Application):
    model_class: type[BaseModel] = AnalysisConfig

    def components(
        self, config: dict[str, Any], context: ApplicationBuildContext
    ) -> list[Component | ComponentBuilder]:
        validated = AnalysisConfig.model_validate(config)
        components = []
        for category in validated.categories:
            component_yaml = component_template.format(
                compound_component_name=context.compound_component_name,
                category_name=category.name,
                flow_name=context.flow_build_context.flow_name,
                input_name=validated.input_name,
                category_threshold=category.threshold,
            )
            component = Component(**yaml.safe_load(component_yaml.strip()))
            components.append(component)
        return components


component_template = """
component:
  name: {compound_component_name}_{category_name}
  transform:
    strategy:
      partitioned:
        enable_substitution_by_partition_name: false
        output_type: table
    inputs:
    - flow: {flow_name}
      name: {input_name}
      partition_spec: full_reduction
    sql: |-
      SELECT *
      FROM {{{{ ref("{input_name}") }}}} WHERE rand() < ({category_threshold} / 100)
"""
