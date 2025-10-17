"""
Python code for an Ascend Application that generates a compound component.
"""

from typing import Optional

import yaml
from ascend.application.application import (
    Application,
    ApplicationBuildContext,
    application,
)
from ascend.models.component.component import Component
from ascend.resources import ComponentBuilder
from pydantic import BaseModel


class Category(BaseModel):
    """Parameters relevant for particular NPS analysis"""

    name: str
    threshold: int


class AnalysisConfig(BaseModel):
    """Configuration for NPS analysis"""

    input_name: str
    random_func: Optional[str] = None
    categories: list[Category]


@application(name="nps_analysis")
class NPSAnalysis(Application[AnalysisConfig]):
    config_model: type[AnalysisConfig] = AnalysisConfig

    def components(
        self, config: AnalysisConfig, context: ApplicationBuildContext
    ) -> list[Component | ComponentBuilder]:
        components = []
        for category in config.categories:
            component_yaml = component_template.format(
                compound_component_name=context.compound_component_name,
                category_name=category.name,
                flow_name=context.flow_build_context.flow_name,
                input_name=config.input_name,
                random_func=config.random_func
                if config.random_func is not None
                else "RAND()",
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
      FROM {{{{ ref("{input_name}") }}}} WHERE {random_func} < ({category_threshold} / 100)
"""
