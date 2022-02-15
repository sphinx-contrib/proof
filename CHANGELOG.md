* sphinxcontrib-proof 1.4.0 (2022-02-15)

    * Python support
      * Drop python3.5 support.
      * Add python3.9 and python3.10 support.
    * Modernize setup files.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 1.3.0 (2020-04-28)

    * Minor setup.py improvements.
    * Update deprecated APIs.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 1.2.0 (2020-01-16)

    * Python support

        * Drop python3.6 support.
        * Add python3.8 support.

    * Bug fixes and Features

        * Theorem titles are now correctly parsed. Closes #9.
        * Configuration option `proof_html_title_template` has been split into `proof_html_title_template_visit` and `proof_html_title_template_depart`.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 1.1.1 (2018-12-07)

    * Config value `proof_theorem_types` is used *after* config values have been inited. Closes !7.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 1.1.0 (2018-10-17)

    * Internationalisation: Custom theorem types can be set in configuration file (thanks Dominic Charrier). Closes #2.
    * Custom theorem types can be added in the configuration files.
    * Theorems can be labelled, referenced, numbered (and several related new configuration options). Closes #3.
    * More options for the LaTeX build.
    * Add python 3.7 support.
    * Internally, rename `name` to `label`, and `content` to `name`.
    * Add `singlehtml` builder. Closes #5.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 1.0.1 (2017-01-01)

    * Fix wheel.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 1.0.0 (2017-12-30)

    * Drop python2 support.
    * Minor internal improvements.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 0.1.1 (2017-02-19)

    * Add python3.6 support.
    * Fix minor bugs introduced by sphinx1.5.
    * Minor test improvements.

    -- Louis Paternault <spalax@gresille.org>

* sphinxcontrib-proof 0.1.0 (2015-09-26)

    * First published version: works for both LaTeX and HTML builders

    -- Louis Paternault <spalax@gresille.org>
