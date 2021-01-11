# generated by appcreator

from django.db import models
from django.urls import reverse
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point


from vocabs.models import SkosConcept

from browsing.browsing_utils import model_to_dict

from gn_places.config import GN_HTML_URL


def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


models.Field.set_extra = set_extra


class GeoNamesPlace(models.Model):
    """ A Geonames Place Instance """
    legacy_id = models.CharField(
        max_length=300, blank=True,
        verbose_name="Legacy ID"
        )
    gn_id = models.IntegerField(
        blank=True, null=True,
        verbose_name="GeoNames ID",
        help_text="GeoNames ID",
    ).set_extra(
        is_public=True,
        data_lookup="geonameid",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="GeoNames ID: <value>",
    )
    gn_name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Name",
        help_text="Name",
    ).set_extra(
        is_public=True,
        data_lookup="name",
        arche_prop="hasTitle",
    )
    gn_lat = models.FloatField(
        blank=True, null=True,
        verbose_name="latitude",
        help_text="Latitude",
    ).set_extra(
        is_public=True,
        data_lookup="latitude",
    )
    gn_long = models.FloatField(
        blank=True, null=True,
        verbose_name="longitude",
        help_text="Longitude",
    ).set_extra(
        is_public=True,
        data_lookup="longitude",
    )
    gn_point = PointField(
        blank=True, null=True,
        verbose_name="centroid",
        help_text="Centroid of the place",
    ).set_extra(
        is_public=True,
        arche_prop="hasWkt",
    )
    gn_feature_class = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Feature Class",
        help_text="Feature Class",
    ).set_extra(
        is_public=True,
        data_lookup="feature class",
    )
    gn_feature_code = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Feature Code",
        help_text="Feature Code",
    ).set_extra(
        is_public=True,
        data_lookup="feature code",
    )
    gn_feature = models.ForeignKey(
        SkosConcept,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Feature Code as SKOS",
        help_text="The Place's Feature Code as SKOS"
    ).set_extra(
        is_public=True
    )
    gn_country_code = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Country Code",
        help_text="Country Code",
    ).set_extra(
        is_public=True,
        data_lookup="country code",
    )
    gn_cc2 = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Alternate Country Codes",
        help_text="Alternate Country Codes",
    ).set_extra(
        is_public=True,
        data_lookup="cc2",
    )
    gn_population = models.IntegerField(
        blank=True, null=True,
        verbose_name="Population",
        help_text="Population",
    ).set_extra(
        is_public=True,
        data_lookup="population",
    )
    gn_elevation = models.IntegerField(
        blank=True, null=True,
        verbose_name="Elevation (m)",
        help_text="Elevation (m)",
    ).set_extra(
        is_public=True,
        data_lookup="elevation",
    )
    gn_modification_date = models.DateField(
        blank=True, null=True,
        verbose_name="Modifcation Date",
        help_text="Modification Date",
    ).set_extra(
        is_public=True,
        data_lookup="modification date",
    )
    orig_data_csv = models.TextField(
        blank=True,
        null=True,
        verbose_name="The original data"
        ).set_extra(
            is_public=True
        )

    class Meta:

        ordering = [
            'gn_name',
        ]
        verbose_name = "GeoNamesPlace"

    def __str__(self):
        if self.gn_name:
            return "{}".format(self.gn_name)
        else:
            return "{}".format(self.legacy_id)

    def save(self, *args, **kwargs):
        if self.gn_lat:
            point = Point(self.gn_long, self.gn_lat, srid=4326)
            self.gn_point = point

        if not self.gn_feature:
            if self.gn_feature_class and self.gn_feature_code:
                ft = ".".join((
                    self.gn_feature_class, self.gn_feature_code)
                )
                try:
                    self.gn_feature = SkosConcept.objects.get(notation=ft)
                except Exception as e:
                    print(e)
        super(GeoNamesPlace, self).save(*args, **kwargs)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse(
            'gn_places:geonamesplace_browse'
        )

    @classmethod
    def get_source_table(self):
        return "AL"

    @classmethod
    def get_natural_primary_key(self):
        return "gn_id"

    @classmethod
    def get_createview_url(self):
        return reverse(
            'gn_places:geonamesplace_create'
        )

    def get_geonames_url(self):
        return f"{GN_HTML_URL}{self.gn_id}"

    def get_geonames_rdf(self):
        return f"{GN_HTML_URL}{self.gn_id}/about.rdf"

    def get_absolute_url(self):
        return reverse(
            'gn_places:geonamesplace_detail', kwargs={'pk': self.id}
        )

    def get_delete_url(self):
        return reverse(
            'gn_places:geonamesplace_delete', kwargs={'pk': self.id}
        )

    def get_edit_url(self):
        return reverse(
            'gn_places:geonamesplace_edit', kwargs={'pk': self.id}
        )

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'gn_places:geonamesplace_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'gn_places:geonamesplace_detail',
                kwargs={'pk': prev.first().id}
            )
        return False
