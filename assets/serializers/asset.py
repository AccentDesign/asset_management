from rest_framework import serializers

from assets.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            'id',
            'name',
            'description',
            'asset_type',
            'contact',
            'parent',
            'is_root_node',
            'is_child_node',
            'is_leaf_node',
            'level'
        )
