=====
Usage
=====

To use GeoName Places in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'gn_places.apps.GnPlacesConfig',
        ...
    )

Add GeoName Places's URL patterns:

.. code-block:: python

    from gn_places import urls as gn_places_urls


    urlpatterns = [
        ...
        url(r'^', include(gn_places_urls)),
        ...
    ]
