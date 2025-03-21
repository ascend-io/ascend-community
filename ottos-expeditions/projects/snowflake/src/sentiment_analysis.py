"""
Application to generate sentiment analysis
"""
from typing import Any

import jinja2
import yaml
from pydantic import BaseModel

from ascend.application.application import Application, ApplicationBuildContext, application
from ascend.common.jinja_util import pass_config, pass_ref
from ascend.models.component.component import Component
from ascend.resources import ComponentBuilder

class Category(BaseModel):
  name: str
  percent: int
  # Parameters relevant for particular sentiment analysis

class Config(BaseModel):
  input_name: str
  categories: list[Category]


@application(name="sentiment_analysis")
class SentimentAnalysis(Application):
  model_class: type[BaseModel] = Config

  def components(self, config: dict[str, Any], context: ApplicationBuildContext) -> list[Component | ComponentBuilder]:
    categories: list[Category] = config["categories"]
    assert isinstance(categories, list), f"Expected categories to be of type 'list[Category]', got '{type(categories)}'"
    env = jinja2.Environment()
    components = []
    for category in categories:
      tmpl = env.from_string(template_sql.replace("REPLACE_WITH_INPUT_NAME", config["input_name"]))
      tmpl.globals["ref"] = pass_ref
      tmpl.globals["pass_config"] = pass_config
      flow_name, compound_component_name = context.flow_build_context.flow_name, context.compound_component_name
      component = Component(**yaml.safe_load(tmpl.render(category=category, input_name=config["input_name"], flow_name=flow_name, compound_component_name=compound_component_name).strip()))
      components.append(component)
    return components

template_sql = """
component:
  name: {{ compound_component_name }}_{{ category.name }}
  transform:
    strategy:
      partitioned:
        enable_substitution_by_partition_name: false
        output_type: table
    inputs:
    - flow: {{ flow_name }}
      name: {{ input_name }}
      partition_spec: full_reduction
    sql: |-
      SELECT *
      FROM {{ ref("REPLACE_WITH_INPUT_NAME") }}
      TABLESAMPLE({{ category.percent }} PERCENT)
"""
