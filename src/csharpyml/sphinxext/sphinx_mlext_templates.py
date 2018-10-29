"""
Template for documentation.
"""

mddocs_index_template_docs = """
ML.net implementation details
=============================

The following pages were generated from content released in
`machinelearning/docs/docs <https://github.com/dotnet/machinelearning/tree/master/docs/code>`_

.. toctree::
    :maxdepth: 1
{% for doc in docs %}
    {{doc}}{% endfor %}
"""

mddocs_index_template_releases = """
ML.net releases details
=======================

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

.. _l-{{title.replace("(", "").replace(")", "").replace(" ", "-").lower()}}:

{{title}}
{{"=" * len(title)}}

.. only:: not md

    {% if MicrosoftML %}
    The documentation is generated based on the sources available at
    :epkg:`dotnet/machinelearning` and released under :epkg:`MIT License`.
    {% endif %}
    {% if ScikitML %}
    The documentation is generated based on the sources available at
    :epkg:`xadupre/machinelearningext` and released under :epkg:`MIT License`.
    {% endif %}

.. only:: md

    **Type:** {{kind}}
    **Aliases:** *{{aliases}}*
    **Namespace:** {{namespace}}
    **Assembly:** {{assembly}}

.. only:: not md

    **Type:** {{kind}}
    **Aliases:** *{{aliases}}*
    **Namespace:** {{namespace}}
    **Assembly:** {{assembly}}
    {{linkdocs}}

**Description**

{{summary}}{{docadd}}

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
