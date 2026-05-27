===================
Import Step: Events
===================

Adds an **Events + Registrations** import step for the ``import_core`` framework.

This module registers a step with code ``event`` and implements
the corresponding runner ``generic.import.runner.event``.

The step:

* Creates or reuses events
* Creates or reuses event registrations
* Links registrations to the imported event
* Optionally links registrations to a partner created or found by a previous contact step


Configuration
=============

1. Install:

   * ``import_core``
   * ``event``
   * this module

2. Go to:

   ``Imports → Templates``

3. Add the step:

   * **Events + Registrations**

4. Create field mappings for models:

   * ``event.event``
   * ``event.registration``

5. Mark one or more fields as **Is search field** if you want to
   search for existing events or registrations before creating new ones.


Usage
=====

Event import
------------

* Map CSV columns to ``event.event`` fields.
* If search fields are defined and a matching event is found,
  that event is reused.
* If no match is found, a new event is created.

Registration import
-------------------

* Map CSV columns to ``event.registration`` fields.
* The registration is automatically linked to the event from the same row using ``event_id``.
* If a previous import step has stored a partner in state, the registration is automatically linked to it using ``partner_id``.
* If search fields are defined and a matching registration is found,
  that registration is reused.
* If no match is found, a new registration is created.


Known issues / Roadmap
======================

- No automatic update of existing events or registrations.
- No advanced normalization or validation beyond basic empty-value cleanup.
- Registration partner linking depends on a previous step storing ``partner`` in import state.


Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
    :alt: Oy Tawasta OS Technologies Ltd.
    :target: http://tawasta.fi/