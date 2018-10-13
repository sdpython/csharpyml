"""
@file
@brief Templates for documentation.
"""

mddocs_index_template = """
ML.net implementation details
=============================

`MLnet on <https://github.com/dotnet/machinelearning>`_

.. toctree::
    :maxdepth: 1
{% for doc in docs %}
    {{doc}}{% endfor %}

*Release notes*

.. toctree::
    :maxdepth: 1
{% for doc in releases %}
    releases/{{doc}}{% endfor %}
"""

index_template = """
List of Machine Learning Components
===================================

.. toctree::
    :maxdepth: 1
{% for vk in sorted_kinds %}
    {{vk[1]}}{% endfor %}
"""

kind_template = """

{{title}}
{{"=" * len(title)}}

.. toctree::
    :maxdepth: 1
{% for fname in fnames %}
    {{fname}}{% endfor %}
"""

component_template = """

.. _l-{{title.replace(" ", "-").lower()}}:

{{title}}
{{"=" * len(title)}}

**Type:** {{kind}}
**Aliases:** *{{aliases}}*
**Namespace:** {{namespace}}
**Assembly:** {{assembly}}
{{linkdocs}}

**Description**

{{summary}}

{% if sorted_params %}
**Parameters**

.. list-table::
    :widths: 5 5 5 20
    :header-rows: 1

    * - Name
      - Short name
      - Default
      - Description{% for kv in sorted_params %}
    * - {{kv["Name"]}}
      - {{kv["ShortName"]}}
      - {{kv["Default"]}}
      - {{kv["Description"]}}{% endfor %}
{% endif %}
"""
